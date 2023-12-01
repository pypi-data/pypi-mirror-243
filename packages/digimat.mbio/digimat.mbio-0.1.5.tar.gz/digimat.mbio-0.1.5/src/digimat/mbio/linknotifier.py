#!/bin/python

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .mbio import MBIO

import time
import datetime
import socket

from digimat.lp import PacketManager, LP

from .task import MBIOTask
from .xmlconfig import XMLConfig

from .valuenotifier import MBIOValueNotifier


kLP_ST=20
kLP_MBIO=0xA2

kMBIO_PING=0
kMBIO_PONG=1


class MBIOLinkPacketManager(PacketManager):
    def __init__(self, link: MBIOLink):
        super().__init__()
        self._link=link

    @property
    def link(self):
        return self._link

    @property
    def logger(self):
        return self._link.logger

    def dispose(self):
        self.link.disconnect()
        super().dispose()

    def write(self, data):
        return self.link.write(data)

    def manager(self):
        data=self.link.read()
        if data:
            self.receive(data)

    def lp(self, lptype=kLP_MBIO):
        return LP(lptype, self)

    # def upReadItems(self, lp, index, count=1):
        # up=lp.up(kEBU_READITEMS)
        # up.writeWord(index)
        # up.writeWord(count)
        # up.store()
        # self.logger.debug("upReadItems(%d, %d)" % (index, count))
        # return up

    # def upBrowseItems(self, lp, pid):
        # up=lp.up(kEBU_BROWSEITEMS)
        # up.writeWord(pid)
        # up.store()
        # self.logger.debug("upBrowseItems(%d)" % (pid))
        # return up

    # def upWriteItem(self, lp, index, value, unit, signalChange=False):
        # up=lp.up(kEBU_WRITEITEM)
        # up.writeWord(self.lid)
        # up.writeWord(index)
        # up.writeFloat(value)
        # up.writeByte(unit)
        # up.writeBool(signalChange)
        # up.store()
        # self.logger.debug("upWriteItem(%d) %.1f (dV=%d)" % (index, value, signalChange))
        # return up

    # def upSubscribe(self, lp, index, dv):
        # up=lp.up(kEBU_SUBSCRIBE)
        # up.writeWord(index)
        # up.writeFloat(dv)
        # up.store()
        # self.logger.debug("upSubscribe(%d, dv=%.1f)" % (index, dv))
        # return up


class MBIOLink(object):
    def __init__(self, mbio: MBIO, host, port=5000):
        self._mbio=mbio
        self._host=host
        self._port=port
        self._socket=None
        self._connected=False
        self._timeoutInhibit=3.0
        self._timeoutActivity=0
        self._packetManager=MBIOLinkPacketManager(self)
        self.registerHandlers()
        self.onInit()

    def onInit(self):
        pass

    @property
    def logger(self):
        return self._mbio.logger

    @property
    def packetManager(self):
        return self._packetManager

    def manager(self):
        if time.time()>=self._timeoutActivity:
            self.ping()
        self.packetManager.manager()

    def resetActivityTimeout(self):
        self._timeoutActivity=time.time()+10

    def connect(self):
        try:
            if not self._connected:
                if time.time()>=self._timeoutInhibit:
                    self.logger.info('Opening link %s:%d' % (self._host, self._port))
                    self._socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self._socket.settimeout(3)
                    address=(self._host, self._port)
                    self._socket.connect(address)
                    self._socket.settimeout(0)
                    self._connected=True
                    self._timeoutInhibit=time.time()+5
                    self.logger.info("Link connected to %s:%d" % (self._host, self._port))
                    self.resetActivityTimeout()
                    self.onConnect()
                    self._mbio.renotifyValues()
        except:
            self.logger.error("Unable to connect link to %s:%d" % (self._host, self._port))
            self._timeoutInhibit=time.time()+5

    def onConnect(self):
        self.DEBUG("Welcome!")

    def isConnected(self):
        return self._connected

    def disconnect(self):
        try:
            self._socket.close()
        except:
            pass

        if self._connected:
            self.logger.warning("Link disconnected from %s:%d" % (self._host, self._port))
            self._connected=False

    def write(self, data):
        try:
            self.connect()
            self._socket.send(data)
            self.resetActivityTimeout()
        except:
            self.disconnect()

    def read(self):
        try:
            self.connect()
            data = self._socket.recv(4096)
            if not data:
                self.disconnect()
                return

            self.resetActivityTimeout()
            return data
        except:
            pass

    def registerHandlers(self):
        self.packetManager.addHandler(kLP_MBIO, kMBIO_PONG, self.onPong)
        # self.packetManager.addHandler(kLP_MBIO, kEBU_READITEM_RESPONSE, self.onReadItemResponse)
        # self.packetManager.addHandler(kLP_MBIO, kEBU_BROWSEITEM_RESPONSE, self.onBrowseItemResponse)

    def ping(self):
        # FIXME:
        self.DEBUG("PING!")
        return
        lp=self.packetManager.lp()
        up=lp.up(kMBIO_PING)
        up.store()
        lp.send()

    def onPong(self, up):
        pass

    def DEBUG(self, data):
        self.write(data.encode())
        self.write('\n'.encode())

    # def onReadItemResponse(self, up):
        # pid=up.readWord()
        # index=up.readWord()
        # value=up.readFloat()
        # unit=up.readByte()
        # item=self._items.get(index)
        # if item:
            # item.value=value
            # item.unit=unit


class MBIOTaskLinkNotifier(MBIOTask):
    def onInit(self):
        self._link=None
        self._notifier=MBIOValueNotifier(self.getMBIO())

    def onLoad(self, xml: XMLConfig):
        mbio=self.getMBIO()

        host=xml.get('host')
        port=xml.getInt('port', 5000)

        if host:
            self._link=MBIOLink(mbio, host, port)

    def poweron(self):
        self._link.connect()
        return True

    def poweroff(self):
        self._link.disconnect()
        return True

    def run(self):
        self._link.manager()
        if self._link.isConnected():
            count=32
            while count>0:
                value=self._notifier.get(2.0)
                if value is None:
                    break
                count-=1
                self.logger.debug('NOTIFYUPDATE %s' % value)
                # TODO:
                now=datetime.datetime.now()
                self._link.DEBUG("MBIO->CPU: %s %s" % (now, str(value)))
            return 0.1
        else:
            return 2.0

    def isError(self):
        if super().isError():
            return True
        if not self._link.isConnected():
            return True
        return False


if __name__ == "__main__":
    pass

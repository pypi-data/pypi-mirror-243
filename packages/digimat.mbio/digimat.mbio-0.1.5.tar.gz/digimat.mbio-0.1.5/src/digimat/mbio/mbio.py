#!/bin/python

#      _ _       _                 _               _     _
#   __| (_) __ _(_)_ __ ___   __ _| |_   _ __ ___ | |__ (_) ___
#  / _` | |/ _` | | '_ ` _ \ / _` | __| | '_ ` _ \| '_ \| |/ _ \
# | (_| | | (_| | | | | | | | (_| | |_ _| | | | | | |_) | | (_) |
#  \__,_|_|\__, |_|_| |_| |_|\__,_|\__(_)_| |_| |_|_.__/|_|\___/
#          |___/                     The Digimat MBIO Processor


from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .values import MBIOValue

import pkg_resources

# import time
import logging
import logging.handlers
import xml.etree.ElementTree as ET
import signal

from prettytable import PrettyTable

from .gateway import MBIOGateway, MBIOGateways
from .task import MBIOTasks
from .xmlconfig import XMLConfig
from .valuenotifier import MBIOValueNotifier
from .linknotifier import MBIOTaskLinkNotifier

# TODO:
# -- MBIO MULTISTATE value (read, writable)
# -- r_112_1_mbio_GWDEV_VALUE (r_112_1_mbio_1.4_8 --> r_112_1_mbio_1<<8|4_8)
# --> gérer gateway.address et value.address (device.address deja ok)
# -- r_112_1_mbio_plc_1ai0


class MBIO(object):
    """MBIO processor base object"""
    def __init__(self, config='config.xml', logServer='localhost', logLevel=logging.DEBUG, ):
        logger=logging.getLogger("MBIO")
        logger.setLevel(logLevel)
        socketHandler = logging.handlers.SocketHandler(logServer, logging.handlers.DEFAULT_TCP_LOGGING_PORT)
        logger.addHandler(socketHandler)
        self._logger=logger

        self._gateways=MBIOGateways(logger)
        self._tasks=MBIOTasks(logger)
        self._valuesByKey: dict[str, MBIOValue]={}
        self._valueNotifiers=[]

        self.logger.info('Using MBIO v%s' % self.version)

        self._xmlConfig=None
        self.load(config)

        self.registerSignals()

    def registerSignals(self):
        def sigHALT(signum, frame):
            self.stop()
            exit(0)

        def sigIGNORE(signum, frame):
            pass

        signal.signal(signal.SIGINT, sigHALT)
        signal.signal(signal.SIGHUP, sigHALT)
        signal.signal(signal.SIGTERM, sigHALT)
        signal.signal(signal.SIGUSR1, sigIGNORE)
        signal.signal(signal.SIGUSR2, sigIGNORE)

    @property
    def logger(self):
        return self._logger

    def getVersion(self):
        """Return the version of the module"""
        try:
            distribution=pkg_resources.get_distribution('digimat.mbio')
            return distribution.parsed_version
        except:
            pass

    @property
    def version(self):
        """Version of the module"""
        return self.getVersion()

    def loadDevices(self, gateway, xml: XMLConfig):
        try:
            devices=xml.children('device')
            if devices:
                for d in devices:
                    if not d.getBool('enable', True):
                        continue

                    vendor=d.get('vendor')
                    model=d.get('model')
                    address=d.getInt('address')
                    try:
                        if gateway.device(address):
                            self.logger.error('Duplicate DEVICE declaration GW%s[%d]' % (gateway.key, address))
                            continue

                        gateway.declareDeviceFromName(vendor, model, address, xml=d)

                    except:
                        self.logger.exception('x')
                        self.logger.error('Error declaring DEVICE GW:%s (%s)' % (gateway.key, d.tostring()))

            item=xml.child('discover')
            if item:
                start=item.getInt('start', 1)
                end=item.getInt('end', 32)
                maxerrors=item.getInt('maxerrors', 3)
                gateway.discover(start, end, maxerrors)
        except:
            self.logger.exception('loadDevices(GW:%s)' % gateway.key)

    def loadGateways(self, xml: XMLConfig):
        try:
            gateways=xml.children('gateway')
            if gateways:
                for g in gateways:
                    if not g.getBool('enable', True):
                        continue

                    name=g.get('name')
                    host=g.get('host')
                    if name and host:
                        if self.gateway(host):
                            self.logger.error('Duplicate GATEWAY declaration %s:%s' % (name, host))
                            continue

                        gateway=self.declareGateway(name=name, host=host, port=g.get('port', 502), xml=g)
                        if gateway:
                            self.loadDevices(gateway, g)
                            continue

                    self.logger.error('Error declaring GATEWAY (%s)' % (g.tostring()))
        except:
            self.logger.exception('loadGateways')

    def load(self, fpath):
        try:
            root=ET.parse(fpath).getroot()

            # Make tree lowercase
            data=ET.tostring(root).lower()
            root=ET.fromstring(data)

            config=XMLConfig(root)
            self.loadGateways(config)

            items=config.children('notifier')
            for item in items:
                MBIOTaskLinkNotifier(self, item.get('name'), item)

            from .tasktest import MBIOTaskPulsar
            for item in config.children('pulsar'):
                MBIOTaskPulsar(self, item.get('name'), xml=item)
        except:
            self.logger.exception('xml')

    @property
    def tasks(self) -> MBIOTasks:
        """Registered tasks"""
        return self._tasks

    @property
    def gateways(self) -> MBIOGateways:
        """Registered gateways"""
        return self._gateways

    def gateway(self, gid):
        """Return the task given by it's id (key, name)"""
        return self._gateways.item(gid)

    def declareGateway(self, name, host, port=502, timeout=3, retries=3, xml: XMLConfig = None):
        gateway=self.gateway(host)
        if gateway:
            return gateway
        if name is None:
            name='%d' % len(self._gateways)
        gateway=MBIOGateway(self, name, host=host, port=port, timeout=timeout, retries=retries, xml=xml)
        self._gateways.add(gateway)
        return gateway

    def task(self, tid):
        return self._tasks.item(tid)

    def declareTask(self, task):
        self._tasks.add(task)

    def dump(self):
        t=PrettyTable()
        t.field_names=['Type', 'Key', 'State', 'Error']
        t.align='l'
        for gateway in self._gateways:
            state='CLOSED'
            if gateway.isOpen():
                state='OPEN'
            address='%s:%s' % (gateway.key, gateway.host)
            t.add_row([gateway.__class__.__name__, address, state, gateway.isError()])
        for task in self._tasks:
            t.add_row([task.__class__.__name__, task.key, task.statestr(), task.isError()])
        print(t)

    def tree(self, key=None, values=False):
        from treelib import Tree

        tree=Tree()
        tree.create_node('%s' % str(self), "root")
        tree.create_node('Gateways', 'gateways', parent='root')
        tree.create_node('Tasks', 'tasks', parent='root')

        for gateway in self._gateways:
            label=str(gateway)
            tree.create_node(label, gateway.key, parent='gateways')
            for device in gateway.devices:
                label=str(device)
                tree.create_node(label, device.key, parent=gateway.key)
                for value in device.values:
                    if not value.match(key):
                        continue
                    label=str(value)
                    tree.create_node(label, value.key, parent=device.key)

        for item in self._tasks:
            tree.create_node(str(item), item.key, parent='tasks')

        if values or key:
            tree.create_node('Values', 'values', parent='root')
            for item in self._valuesByKey.values():
                if not item.match(key):
                    continue
                tree.create_node(str(item), 'REF-'+item.key, parent='values')

        print(str(tree))

    def stop(self):
        """Stop the MBIO processor. Shoud be called before exiting to shutdown tasks"""
        self._tasks.stop()
        self._tasks.waitForThreadTermination()
        self._gateways.stop()
        self._gateways.waitForThreadTermination()

    def reset(self):
        """Reset (restart) all tasks and gateways"""
        self._tasks.reset()
        self._gateways.reset()

    def resetHalted(self):
        """Reset (restart) all tasks and gateways that are halted"""
        self._tasks.resetHalted()
        self._gateways.resetHalted()

    def halt(self):
        """Halt (pause) all tasks and gateways. A restart is done with reset()"""
        self._tasks.halt()
        self._gateways.halt()

    def discover(self):
        """Start a device discover on all gateways"""
        self._gateways.discover()

    def __getitem__(self, key):
        """Return the task, gateway or value given by it's key"""
        item=self.gateway(key)
        if item:
            return item
        item=self.task(key)
        if item:
            return item
        return self.value(key)

    def __del__(self):
        self.stop()

    def __repr__(self):
        return '%s(%d gateways, %d tasks, %d values, %d notifiers)' % (self.__class__.__name__,
            len(self._gateways),
            len(self._tasks),
            len(self._valuesByKey),
            len(self._valueNotifiers))

    def registerValue(self, value):
        """Any MBIOValue added to a MBIOValues collection will call this function to register itself to the MBIO"""
        # assert(isinstance(value, MBIOValue))
        self._valuesByKey[value.key]=value

    def value(self, key):
        """Return the MBIOValue given by it's key"""
        try:
            return self._valuesByKey[key]
        except:
            pass

    def registerValueNotifier(self, notifier: MBIOValueNotifier):
        """Register a MBIOValueNotifier (receive every value notification update)"""
        assert(isinstance(notifier, MBIOValueNotifier))
        self._valueNotifiers.append(notifier)

    def signalValueUpdateNotify(self, value):
        """MBIOValue update notification that will be sent to every registered notifier"""
        if self._valueNotifiers:
            for notifier in self._valueNotifiers:
                notifier.put(value)

    def renotifyValues(self):
        """Trigger an update notify for every registered MBIOValue"""
        if self._valuesByKey:
            for value in self._valuesByKey.values():
                value.notify(force=True)

    def on(self):
        """Send an ON to every registerred MBIOValue. Just another debug tool"""
        for gateway in self.gateways:
            gateway.on()

    def off(self):
        """Send an ON to every registerred MBIOValue. Just another debug tool"""
        for gateway in self.gateways:
            gateway.off()

    def toggle(self):
        """Send a TOGGLE to every registerred MBIOValue. Just another debug tool"""
        for gateway in self.gateways:
            gateway.toggle()


if __name__=='__main__':
    pass

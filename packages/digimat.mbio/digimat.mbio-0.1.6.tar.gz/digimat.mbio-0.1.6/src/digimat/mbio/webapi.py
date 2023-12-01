#!/bin/python

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .mbio import MBIO


from .task import MBIOTask
from .xmlconfig import XMLConfig
from .valuenotifier import MBIOValueNotifier


from bottle import route, run


class MBIOTaskWebApi(MBIOTask):
    def onInit(self):
        self._notifier=MBIOValueNotifier(self.getMBIO())

    def onLoad(self, xml: XMLConfig):
        self._port=xml.getInt('port', 9080)

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def run(self):
        run(host='localhost', port=self._port)
        return 2.0

    def isError(self):
        return False

    @route('/test')
    def test(self):
        return "HELLO"


if __name__ == "__main__":
    pass

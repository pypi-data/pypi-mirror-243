#!/bin/python

from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .mbio import MBIO

# import time
import time

from prettytable import PrettyTable
from digimat.units import Units

from .items import Items


from .config import MBIOConfig


# READ PRINCIPLE (values refresh)
# manager->refresh() retrieve I/O state and call value.updateValue(state)
# will set value._value (value.value)
# and call value.notify() if needed (queue values updates notifications in MBIO for dispatching)

# WRITE PRINCIPLE (value change orders)
# value=state or value.set(state)
# will set value._toReachValue (value.toreachValue) and call value.signalSync()
# manager->sync() checks value.isPendingSync(), update I/O and call value.clearSync()
# Note: a write don't update the value.value, which will be updated by the refresh process.
# If the value isn't auto refreshed, use value.clearSyncAndUpdateValue() instead of .clearSync()
# In the manager->sync() a device->signalRefresh() is automatically called after a manager->sync() to
# speedup the value refresh


class MBIOValue(object):
    def __init__(self, parent: MBIOValues, name, unit=None, default=None, resolution=0.1, writable=False):
        assert(isinstance(parent, MBIOValues))
        self._parent=parent
        if not name:
            name='%d' % parent.count()
        self._name=name
        self._key=parent.computeValueKeyFromName(name)
        self._writable=writable
        self._enable=True
        if type(unit)==str:
            unit=parent.units.getByName(unit)
        self._unit=unit
        self._error=False
        self._manual=None
        self._override=False
        self._stamp=0
        self._min=None
        self._max=None
        self._default=self.normalizeValue(default)
        self._value=self._default
        self._flags=None
        self._config=MBIOConfig()
        self._resolution=resolution
        self._lastValueNotified=None
        self.onInit()
        self.updateFlags()
        self._parent.add(self)

    def checkNotify(self):
        try:
            if type(self._value) is bool or self._lastValueNotified is None:
                return True
            if self._resolution is not None:
                if abs(self._value-self._lastValueNotified)>=self._resolution:
                    return True
                return False
        except:
            pass
        return True

    def notify(self, force=False):
        if force or self.checkNotify():
            self.parent.getMBIO().signalValueUpdateNotify(self)
            self._lastValueNotified=self.value

    @property
    def config(self) -> MBIOConfig:
        return self._config

    @property
    def parent(self) -> MBIOValues:
        return self._parent

    @property
    def logger(self):
        return self._parent.logger

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    def onInit(self):
        pass

    def setRange(self, min, max):
        self._min=min
        self._max=max

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        self._resolution = value

    def normalizeValue(self, value):
        if self._min is not None:
            value=max(self._min, value)
        if self._max is not None:
            value=min(self._max, value)
        return value

    def isWritable(self):
        if self._writable:
            return True
        return False

    def isError(self):
        return self._error

    def isManual(self):
        if self._manual is not None:
            return True
        return False

    def signalSync(self, value=None):
        pass

    def manual(self, value=None):
        if value is None:
            value=self.value
        if value is not None:
            value=self.normalizeValue(value)
            if value!=self._manual:
                self._manual=value
                self.updateFlags()
            if self.isWritable():
                self.signalSync(self._manual)
            else:
                self.updateValue(self._manual)
                self._stamp=time.time()

    def auto(self):
        if self._manual is not None:
            self._manual=None
            self.updateFlags()

    @property
    def override(self):
        return self._override

    def setOverride(self, state=True):
        state=bool(state)
        if state!=self._override:
            self._override=state
            self.updateFlags()

    def setError(self, state=True):
        state=bool(state)
        if state!=self._error:
            self._error=state
            self.updateFlags()

    def isEnabled(self):
        return self._enable

    def enable(self, state=True):
        state=bool(state)
        if state!=self._enable:
            self._enable=state
            self.updateFlags()

    def disable(self):
        self.enable(False)

    def age(self):
        return time.time()-self._stamp

    def isTimeout(self, delay):
        if self.age()>=delay:
            return True
        return False

    @property
    def value(self):
        if self.isError() and self._default is not None:
            return self._default
        return self._value

    @property
    def flags(self):
        return self._flags

    def isFlag(self, flag):
        try:
            if flag.upper() in self._flags:
                return True
        except:
            pass
        return False

    def updateFlags(self):
        flags=''
        if self.override:
            flags+='*'
        if self.isError():
            flags+='E'
        if self.isManual():
            flags+='M'
        if not self.isEnabled():
            flags+='X'

        if flags!=self._flags:
            self._flags=flags
            # Force notify
            self.notify(True)
            return True
        return False

    def updateValue(self, value, unit=None):
        if self.isManual():
            if not self.isWritable():
                value=self._manual
        else:
            self._stamp=time.time()
        value=self.normalizeValue(value)
        notify=self._lastValueNotified is None
        if unit is not None and self._unit!=unit:
            self._unit=unit
            notify=True
        if value!=self._value:
            self._value=value
            notify=True
        if notify:
            self.notify()

    def isValid(self):
        if self.isEnabled() and self._value is None:
            return False
        return True

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        if type(value)==str:
            value=self.parent.units.getByName(value)
        if self._unit!=value:
            self._unit=value
            self.notify()

    def unitstr(self):
        return self.parent.units.str(self.unit)

    def __repr__(self):
        if self.updateFlags():
            # should not be called
            self.logger.warning('%s --> updateFlags TRUE', self.key)
        if self._flags:
            return '%s(%s=%s%s, flags=[%s], %ds)' % (self.__class__.__name__, self.key,
                str(self.value), self.unitstr(), self._flags, self.age())
        return '%s(%s=%s%s, %ds)' % (self.__class__.__name__, self.key, str(self.value), self.unitstr(), self.age())

    def match(self, key):
        try:
            if key is None:
                return True
            if key.lower() in self._key:
                return True
        except:
            pass
        return False


# FIXME: duplicated code MBIOValueWritable - MBIOValueDigitalWritable
class MBIOValueWritable(MBIOValue):
    def __init__(self, parent: MBIOValues, name, unit=None, default=None, resolution=0.1):
        super().__init__(parent, name, unit, default, writable=True, resolution=resolution)
        self._toReachValue=None
        self._pendingSync=False

    @MBIOValue.value.setter
    def value(self, value):
        if value is not None:
            if self.isEnabled():
                if self.isManual():
                    value=self._manual
                value=self.normalizeValue(value)
                resolution=self._resolution
                if resolution is not None and resolution>0:
                    if abs(value-self.value)>=resolution:
                        self.signalSync(value)
                    else:
                        self.signalSync(value)

    def set(self, value):
        self.value=value

    def signalSync(self, value=None):
        if value is not None:
            self._toReachValue=value
        self._pendingSync=True
        self.parent.signalSync()

    def isPendingSync(self, reset=False):
        if self._pendingSync and self._toReachValue is not None:
            if reset:
                self.clearSync()
            return True
        return False

    @property
    def toReachValue(self):
        return self._toReachValue

    def clearSync(self):
        self._pendingSync=False

    def clearSyncAndUpdateValue(self):
        self.clearSync()
        if self.toReachValue is not None:
            self.updateValue(self.toReachValue)
            self._stamp=time.time()


class MBIOValueDigital(MBIOValue):
    def __init__(self, parent: MBIOValues, name, default=None, writable=False):
        super().__init__(parent, name, 15, default, writable=writable)

    def normalizeValue(self, value):
        if type(value) is bool:
            return value
        if type(value) is int:
            return bool(value)
        if value is None:
            return False
        self.logger.error('Unable to normalize value')
        return bool(value)

    def isOn(self):
        if self.value:
            return True
        return False

    def isOff(self):
        return not self.isOn()


class MBIOValueDigitalWritable(MBIOValueDigital):
    def __init__(self, parent: MBIOValues, name, default=None):
        super().__init__(parent, name, default, writable=True)
        self._toReachValue=None
        self._pendingSync=False

    @MBIOValueDigital.value.setter
    def value(self, value):
        if value is not None:
            if self.isEnabled():
                if self.isManual():
                    value=self._manual
                value=self.normalizeValue(value)
                if value!=self.value:
                    self.signalSync(value)

    def set(self, value):
        self.value=value

    def signalSync(self, value=None):
        if value is not None:
            self._toReachValue=value
        self._pendingSync=True
        self.parent.signalSync()

    def isPendingSync(self):
        if self._pendingSync and self._toReachValue is not None:
            return True
        return False

    @property
    def toReachValue(self):
        return self._toReachValue

    def clearSync(self):
        self._pendingSync=False

    def clearSyncAndUpdateValue(self):
        self.clearSync()
        if self.toReachValue is not None:
            self.updateValue(self.toReachValue)
            self._stamp=time.time()

    def toggle(self):
        self.value=not self.value

    def on(self):
        self.value=True

    def off(self):
        self.value=False


class MBIOValues(Items):
    def __init__(self, parent, prefix, logger):
        super().__init__(logger)
        self._parent=parent
        self._prefix=prefix
        self._items: list[MBIOValue]=[]
        self._itemByKey={}
        self._itemByName={}
        self._units=Units()
        self._hasWritableValue=False

    @property
    def parent(self):
        return self._parent

    @property
    def units(self):
        return self._units

    def computeValueKeyFromName(self, name):
        if self._prefix:
            return '%s_%s' % (self._prefix, name)
        return name

    def getByKeyComputedFromName(self, name):
        return self.getByKey(self.computeValueKeyFromName(name))

    def getMBIO(self) -> MBIO:
        return self._parent.getMBIO()

    def item(self, key):
        item=super().item(key)
        if item:
            return item

        item=self.getByKey(key)
        if item:
            return item

        item=self.getByName(key)
        if item:
            return item

        try:
            return self[key]
        except:
            pass

    def hasWritableValue(self):
        if self._hasWritableValue:
            return True
        return False

    def add(self, value: MBIOValue) -> MBIOValue:
        if isinstance(value, MBIOValue):
            super().add(value)
            self._itemByKey[value.key]=value
            self._itemByName[value.name]=value
            if value._writable:
                self._hasWritableValue=True
            try:
                self.getMBIO().registerValue(value)
            except:
                pass

    def getByKey(self, key):
        try:
            return self._itemByKey[key]
        except:
            pass

    def getByName(self, key):
        try:
            return self._itemByName[key]
        except:
            pass

    def __radd__(self, other):
        self.add(other)

    def signalSync(self):
        try:
            self._parent.signalSync()
        except:
            pass


if __name__ == "__main__":
    pass

#####################################################################
#
# SharedResource  A place to hang resources that should be unique
#                 instead of per-thread, and protect them with locking
#                 My thanks go to Dieter Maurer whose code forms the
#                 bulk of this module.
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################
__version__='$Revision: 929 $'[11:-2]


"""Shared Resource.

'Shared Resource' is a module that manages resources shared by all threads. 
Such resources can be controlled much more easily. A shared resource provides
locking capabilities (via Python's RLock) and performs automatic locking for 
function calls. Access to non-functions is not protected.

A shared resource is identified by an id. The application
is responsible that id s are unique.
"""

from threading import _RLock, Lock

_ResourceMap = {}
_ResourceLock = Lock()

def getResource(id, factory, factoryArgs=()):
    """returns a resource for *id*.

    If such a resource does not yet exist, one is created
    by calling *factory* with *factoryArgs*.
    Note, that *factory* and *factoryArgs* should only
    depend on *id* and not any other context, as no
    object is created, when a resource for *id* already
    exists.
    """
    _ResourceLock.acquire()

    try:
        try:
            return _ResourceMap[id]
        except KeyError:
            _ResourceMap[id] = _SharedResource(factory(*factoryArgs))
            return _ResourceMap[id]
    finally: 
        _ResourceLock.release()

def setResource(id, resource):
    """ Forcibly set the resource """
    _ResourceLock.acquire()

    try:
        _ResourceMap[id] = _SharedResource(resource)
    finally:
        _ResourceLock.release()


class _SharedResource(_RLock):
    # for __setattr__
    _myAttributes = { '_target' : None
      	            # _RLock instance variables
      	            , '_RLock__block' : None
      	            , '_RLock__count' : None
      	            , '_RLock__owner' : None
      	            # Verbose instance variables
      	            , '_Verbose__verbose' : None
      	            }
    _myAttributes.update(_RLock.__dict__)
    _isMyAttribute = _myAttributes.has_key
    _target = None

    def __init__(self, target):
        self._target = target
        _RLock.__init__(self)

    def __getattr__(self, key):
        a = getattr(self._target, key)
        if callable(a): 
            a = _SharedCallable(self,a)

        return a

    def __setattr__(self, key, value):
        if self._isMyAttribute(key): 
            self.__dict__[key] = value
        else:
            setattr(self._target, key, value)

    def _type(self):
        return type(self._target)

    # def __delattr__(self,key,value): # do not implement for the time being

    def __len__(self): return len(self._target)
    def __getitem__(self, key): return self._target[key]
    def __setitem__(self, key, value): self._target[key] = value
    def __delitem__(self, key): del self._target[key]


class _SharedCallable:
    def __init__(self, lock, callable):
        self._lock = lock
        self._callable = callable

    def __call__(self, *args, **kw):
        self._lock.acquire()
        try: 
            return self._callable(*args, **kw)
        finally: 
            self._lock.release()



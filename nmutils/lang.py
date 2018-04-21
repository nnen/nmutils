# nmutils.lang


import pprint
import logging


LOGGER = logging.getLogger(__name__)


def safe_repr(value):
    try:
        return pprint.saferepr(value)
    except:
        return "<repr-error>"


def args_repr(*args, **kwargs):
    parts = [safe_repr(arg) for arg in args]
    parts.extend("{}={}".format(k, safe_repr(v)) for k, v in kwargs.items())
    return ", ".join(parts)


def obj_repr(obj, *args, **kwargs):
    typ = type(obj)
    return "{}({})".format(
        typ.__name__,
        args_repr(*args, **kwargs)
    )


class Proxy:
    __slots__ = ["_target", ]

    def __init__(self, target=None):
        self._target = target

    def __str__(self):
        return str(self._target)

    def __repr__(self):
        return "Proxy({!r})".format(self._target)

    def __getitem__(self, item):
        return self._target[item]

    def __setitem__(self, key, value):
        self._target[key] = value

    def __getattr__(self, item):
        if item.startswith("_"):
            return getattr(self, item)
        return getattr(self._target, item)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            setattr(self._target, key, value)


def add_callback(callbacks: list, callback):
    if callbacks is None:
        callbacks = []
    callbacks.append(callback)
    return callbacks


def remove_callback(callbacks: list, callback):
    if callbacks is not None:
        callbacks.remove(callback)


def invoke_callbacks(callbacks: list, *args, **kwargs):
    if callbacks is None:
        return
    for callback in callbacks:
        try:
            callback(*args, **kwargs)
        except:
            LOGGER.exception("Exception occured in a callback '%r'.", callback)


class Callbacks:
    def __init__(self):
        self._callbacks = None

    def __call__(self, *args, **kwargs):
        self.invoke(*args, **kwargs)

    def __len__(self):
        if self._callbacks is None:
            return 0
        return len(self._callbacks)

    def add(self, callback):
        self._callbacks = add_callback(self._callbacks, callback)

    def remove(self, callback):
        remove_callback(self._callbacks, callback)

    def invoke(self, *args, **kwargs):
        invoke_callbacks(self._callbacks, *args, **kwargs)


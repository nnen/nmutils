# nmutils.lang


import pprint


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


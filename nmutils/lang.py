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


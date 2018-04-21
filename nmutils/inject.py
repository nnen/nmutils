# nmutils.inject


import importlib
import logging


LOGGER = logging.getLogger(__name__)


from .lang import obj_repr


class DependencyManager:
    def __init__(self):
        self._entries = {}

    def reset(self):
        self._entries.clear()

    def get_entry(self, name):
        entry = self._entries.get(name, None)
        if entry is None:
            entry = DependencyEntry(name)
            self._entries[name] = entry
        return entry

    def get_proxy(self, name):
        entry = self.get_entry(name)
        return entry.proxy

    def add_provider(self, name, provider):
        entry = self.get_entry(name)
        entry.add_provider(provider)
        return provider

    def provide(self, name, value, *args, **kwargs):
        if isinstance(value, str):
            provider = NameLookupProvider(value, args, kwargs)
        else:
            provider = ValueProvider(value)

        return self.add_provider(name, provider)


class DependencyEntry:
    def __init__(self, name):
        self.name = name
        self._providers = []
        self._value = None
        self._all_values = None
        self._proxy = None

        self.add_provider(NameLookupProvider(self.name))

    def add_provider(self, provider):
        self._providers.append(provider)

    @property
    def proxy(self):
        if self._proxy is None:
            self._proxy = DependencyProxy(self)
        return self._proxy

    @property
    def value(self):
        try:
            if self._value is None:
                LOGGER.info("Looking up value for dependency '%s'...", self.name)
                for provider in reversed(self._providers):
                    value = provider.get_value(self)
                    if value is not None:
                        self._value = value
                        LOGGER.info("Value for dependency '%s' found using provider '%s': %s",
                                    self.name, provider.description, repr(value))
                        break
            return self._value
        except:
            LOGGER.exception("Failed to get dependency value for '%s'.", self.name)
            return None

    @property
    def all_values(self):
        if self._all_values is None:
            try:
                self._all_values = [p.get_value(self) for p in self._providers]
            except:
                LOGGER.exception("Failed to get all dependency values for '%s'.", self.name)
                self._all_values = []
        return self._all_values


class DependencyProxy:
    def __init__(self, entry: DependencyEntry):
        self._entry = entry
        self._value = None

    def _get_value(self):
        if self._value is None:
            self._value = self._entry.value
        return self._value

    def __getattr__(self, item):
        return getattr(self._get_value(), item)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            setattr(self._get_value(), key, value)


class Provider:
    def __init__(self):
        self._value = None

    @property
    def description(self):
        return repr(self)

    def set_value(self, value):
        self._value = value

    def get_value(self, entry):
        if self._value is None:
            self._value = self._get_value_inner(entry)
        return self._value

    def _get_value_inner(self, entry):
        return None


class FunctionProvider(Provider):
    def __init__(self, function, func_args=None, func_kwargs=None):
        super().__init__()
        self.function = function
        self.func_args = func_args or []
        self.func_kwargs = func_kwargs or {}

    def __repr__(self):
        if len(self.func_args) == 0 and len(self.func_kwargs) == 0:
            return obj_repr(self, self.function)
        return obj_repr(self, self.function, self.func_args, self.func_kwargs)

    def _get_value_inner(self, entry):
        if self.function is None:
            return None

        try:
            return self.function(*self.func_args, **self.func_kwargs)
        except:
            LOGGER.exception("Exception occured in %s provider while looking up dependency '%s'.",
                             self.description, entry.name)
            return None


class NameLookupProvider(FunctionProvider):
    def __init__(self, name, ctor_args=None, ctor_kwargs=None):
        super().__init__(None, ctor_args, ctor_kwargs)
        self.name = name

    def __repr__(self):
        if len(self.func_args) == 0 and len(self.func_kwargs) == 0:
            return obj_repr(self, self.name)
        return obj_repr(self, self.name, self.func_args, self.func_kwargs)

    def get_class(self, entry):
        name_parts = self.name.split(".")

        if len(name_parts) == 0:
            return None

        if len(name_parts) == 1:
            return globals().get(name_parts[0], None)

        class_name = name_parts[-1]
        module_name = ".".join(name_parts[:-1])

        try:
            module = importlib.import_module(module_name)
            return getattr(module, class_name, None)
        except:
            LOGGER.exception("Error occured while importing modules for dependency '%s'.", entry.name)
            return None

    def _get_value_inner(self, entry):
        self.function = self.get_class(entry)
        return super()._get_value_inner(entry)


class ValueProvider(Provider):
    def __init__(self, value):
        super().__init__()
        self.set_value(value)


def provide(name, value, *args, **kwargs):
    return MANAGER.provide(name, value, *args, **kwargs)


def provider(name, *args, **kwargs):
    def decorator_fun(value):
        provider = FunctionProvider(value, args, kwargs)
        MANAGER.add_provider(name, provider)
        return value
    return decorator_fun


def dependency(name):
    return MANAGER.get_entry(name)


def proxy(name):
    return MANAGER.get_proxy(name)


MANAGER = DependencyManager()


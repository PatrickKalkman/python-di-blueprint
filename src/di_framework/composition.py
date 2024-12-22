from contextlib import contextmanager
from enum import Enum
from functools import wraps
import inspect
from typing import Any, Callable, Dict, Generic, Optional, Type, TypeVar
from uuid import uuid4


class Lifetime(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"


class Scope:
    def __init__(self):
        self.id = str(uuid4())
        self.instances: Dict[Type, Any] = {}


T = TypeVar('T')


class Interceptor(Generic[T]):
    def __init__(self, instance: T):
        self._instance = instance
        self._before_callbacks: list[Callable] = []
        self._after_callbacks: list[Callable] = []

    def before(self, callback: Callable):
        self._before_callbacks.append(callback)
        return self

    def after(self, callback: Callable):
        self._after_callbacks.append(callback)
        return self

    def __getattr__(self, name):
        attr = getattr(self._instance, name)
        if callable(attr):
            @wraps(attr)
            def wrapped(*args, **kwargs):
                # Execute before callbacks
                for callback in self._before_callbacks:
                    callback(self._instance, name, args, kwargs)

                # Call the original method
                result = attr(*args, **kwargs)

                # Execute after callbacks
                for callback in self._after_callbacks:
                    callback(self._instance, name, result, args, kwargs)

                return result
            return wrapped
        return attr


class SimpleContainer:
    def __init__(self):
        self._registry: Dict[Type, tuple[Type, Lifetime]] = {}
        self._singletons: Dict[Type, Any] = {}
        self._current_scope: Optional[Scope] = None
        self._interceptors: Dict[Type, list[Callable[[Any], Any]]] = {}

    @contextmanager
    def create_scope(self):
        previous_scope = self._current_scope
        self._current_scope = Scope()
        try:
            yield self._current_scope
        finally:
            self._current_scope = previous_scope

    def register(self, cls: Type, lifetime: Lifetime = Lifetime.TRANSIENT):
        self._registry[cls] = (cls, lifetime)

    def register_interceptor(self, cls: Type, interceptor_factory: Callable[[Any], Any]):
        if cls not in self._interceptors:
            self._interceptors[cls] = []
        self._interceptors[cls].append(interceptor_factory)

    def resolve(self, cls: Type) -> Any:
        if cls not in self._registry:
            raise ValueError(f"{cls} is not registered in the container.")

        registered_cls, lifetime = self._registry[cls]

        if lifetime == Lifetime.SINGLETON:
            if cls not in self._singletons:
                self._singletons[cls] = self._create_instance(registered_cls)
            return self._singletons[cls]

        if lifetime == Lifetime.SCOPED:
            if not self._current_scope:
                raise ValueError("Cannot resolve scoped dependency outside of a scope")

            if cls not in self._current_scope.instances:
                self._current_scope.instances[cls] = self._create_instance(registered_cls)
            return self._current_scope.instances[cls]

        return self._create_instance(registered_cls)

    def _create_instance(self, cls: Type) -> Any:
        # Create the instance with dependencies
        constructor_params = inspect.signature(cls.__init__).parameters.values()
        dependencies = [
            self.resolve(param.annotation)
            for param in constructor_params
            if param.annotation is not inspect.Parameter.empty
        ]
        instance = cls(*dependencies)

        if cls in self._interceptors:
            for factory in self._interceptors[cls]:
                instance = factory(instance)

        return instance

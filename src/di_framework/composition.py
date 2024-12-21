from enum import Enum
import inspect
from typing import Any, Dict, Type


class Lifetime(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"


class SimpleContainer:
    def __init__(self):
        self._registry: Dict[Type, tuple[Type, Lifetime]] = {}
        self._singletons: Dict[Type, Any] = {}

    def register(self, cls: Type, lifetime: Lifetime = Lifetime.TRANSIENT):
        self._registry[cls] = (cls, lifetime)

    def resolve(self, cls: Type) -> Any:
        if cls not in self._registry:
            raise ValueError(f"{cls} is not registered in the container.")

        registered_cls, lifetime = self._registry[cls]

        if lifetime == Lifetime.SINGLETON:
            if cls not in self._singletons:
                self._singletons[cls] = self._create_instance(registered_cls)
            return self._singletons[cls]

        return self._create_instance(registered_cls)

    def _create_instance(self, cls: Type) -> Any:
        constructor_params = inspect.signature(cls.__init__).parameters.values()
        dependencies = [
            self.resolve(param.annotation)
            for param in constructor_params
            if param.annotation is not inspect.Parameter.empty
        ]
        return cls(*dependencies)

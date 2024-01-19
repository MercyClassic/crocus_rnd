from abc import ABC
from typing import Dict, Type


class DependencyContainer:
    def __init__(self):
        self.__deps: Dict[Type[ABC], Type] = {}

    def bind(self, interface: Type[ABC], implementation: Type) -> None:
        self.__deps[interface] = implementation

    def bind_multiple(self, bindings: Dict[Type[ABC], Type]) -> None:
        for interface, implementation in bindings.items():
            self.bind(interface, implementation)

    def override(self, interface: Type[ABC], implementation: Type) -> None:
        self.bind(interface, implementation)

    def get(self, interface: Type[ABC]) -> Type:
        return self.__deps[interface]

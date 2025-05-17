from __future__ import annotations

import dataclasses
import functools
from enum import Enum, auto


@dataclasses.dataclass
class Dependency:
    concrete: type
    dependency_type: DependencyLifeTime


class DependencyLifeTime(Enum):
    Transient = 1
    Scoped = auto()
    Singleton = auto()


class NotSubclassException(Exception):
    def __init__(self, concrete, abstract):
        raise Exception(
            f"{concrete=}".split("=", maxsplit=2)[1]
            + " is not a subclass of "
            + f"{abstract=}".split("=", maxsplit=2)[1]
        )


class Inject:  # noqa
    __injection_with_types: dict[type, Dependency] = {}

    def __init__(self, cls: type):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        @functools.wraps(self.cls)
        def func(*_, **__):
            obj = self.cls()

            Inject.set_params(obj)

            return obj

        return func()

    @staticmethod
    def check_is_subclass(concrete: type | Inject, abstract: type) -> None:
        if isinstance(concrete, Inject) and not issubclass(concrete.cls, abstract):
            raise NotSubclassException(concrete.cls, abstract)

        if not isinstance(concrete, Inject) and not issubclass(concrete, abstract):
            raise NotSubclassException(concrete, abstract)

    @staticmethod
    def set_params(obj):
        for parameter_name, parameter_type in obj.__annotations__.items():
            parameter = Inject.__injection_with_types.get(parameter_type)
            if parameter:
                setattr(obj, parameter_name, parameter.concrete())

    @staticmethod
    def add_transient(abstract: type, concrete: type | Inject | None = None) -> None:
        Inject.__add_dependency(abstract, concrete, DependencyLifeTime.Transient)

    @staticmethod
    def add_scoped(abstract: type, concrete: type | Inject | None = None) -> None:
        Inject.__add_dependency(abstract, concrete, DependencyLifeTime.Scoped)

    @staticmethod
    def add_singleton(abstract: type, concrete: type | Inject | None = None) -> None:
        Inject.__add_dependency(abstract, concrete, DependencyLifeTime.Singleton)

    @staticmethod
    def __add_dependency(
            abstract: type,
            concrete: type | Inject | None = None,
            dependency_type: DependencyLifeTime | None = None
    ) -> None:
        if concrete is None:
            concrete = abstract

        Inject.check_is_subclass(concrete, abstract)

        Inject.__injection_with_types[abstract] = Dependency(concrete, dependency_type)


class InjectClass(type, Inject):
    def __new__(cls, cls_name, bases, cls_dict):
        obj = super().__new__(cls, cls_name, bases, cls_dict)

        Inject.set_params(obj)

        return obj

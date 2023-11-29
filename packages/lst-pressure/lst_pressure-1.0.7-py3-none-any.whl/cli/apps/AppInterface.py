from abc import ABC, abstractmethod
from typing import Self


class AppInterface(ABC):
    @property
    @staticmethod
    def id():
        pass

    @property
    @staticmethod
    def usage():
        pass

    @property
    @staticmethod
    def description():
        pass

    def __init__(self, parser_sub) -> None:
        self.parser_sub = parser_sub
        self.build()

    @abstractmethod
    def build(self) -> Self:
        pass

    @abstractmethod
    def parse(self) -> Self:
        pass

    @abstractmethod
    def exe(self) -> Self:
        pass

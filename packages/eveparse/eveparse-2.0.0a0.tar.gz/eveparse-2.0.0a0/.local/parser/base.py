from abc import ABC, abstractmethod


class EveParser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls, string: str) -> tuple[str, int]:
        """Extract a valid type name and quantity or raise an Exception"""

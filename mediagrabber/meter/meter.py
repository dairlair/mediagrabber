from abc import ABC, abstractmethod

class MeterInterface(ABC):
    @abstractmethod
    def save(self, content: bytes, name: str) -> str:
        raise NotImplementedError

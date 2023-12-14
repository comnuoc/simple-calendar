from abc import ABC, abstractmethod


class SettingRepository(ABC):
    @abstractmethod
    def get(self, key: str, default: str = "") -> str:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def getMultiple(self, keys: list[str]) -> dict[str, str]:
        raise NotImplementedError

    @abstractmethod
    def setMultiple(self, values:dict[str, str]) -> None:
        raise NotImplementedError

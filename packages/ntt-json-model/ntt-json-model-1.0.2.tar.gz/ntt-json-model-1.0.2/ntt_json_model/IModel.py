from abc import *
from ntt_signal import Signal


class IModel(ABC):
    @abstractmethod
    def _AppendModelData(self, strAttributeName: str, bIsModel: bool = False) -> None:
        pass

    @abstractmethod
    def ToDict(self) -> dict:
        pass

    @abstractmethod
    def FromDict(self, dictData: dict) -> None:
        pass

    @abstractmethod
    def Attach(self, signal: Signal) -> None:
        pass

    @abstractmethod
    def ToFile(self, strFileName: str) -> None:
        pass

    @abstractmethod
    def FromFile(self, strFileName: str) -> None:
        pass
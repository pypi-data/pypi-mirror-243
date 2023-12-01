from typing import *
from abc import *
from ntt_signal import Signal
from ..IModel import IModel


class Property(Signal, ABC):
    def __init__(self, model:IModel, strAttributeName: str, 
                    datatype: type = None, 
                    bIsModel: bool = False) -> None:
        super().__init__(datatype)
        self.Attach(model)
        setattr(model, strAttributeName, self)
        model._AppendModelData(strAttributeName, bIsModel=bIsModel)

    @abstractmethod
    def GetValue(self) -> Any:
        pass

    @abstractmethod
    def SetValue(self, newValue: object, bNotify: bool = True) -> None:
        pass
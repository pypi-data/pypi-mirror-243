from typing import Any
from ntt_signal import Signal

from ..IModel import IModel
from .Property import Property


class ModelProperty(Property):
    def __init__(self, model: IModel, mData: IModel, strAttributeName: str) -> None:
        super().__init__(model, strAttributeName)

        self._mData = mData
        self._mData.Attach(self)

    def GetValue(self) -> IModel:
        return self._mData
    
    def SetValue(self, mNewData: IModel, bNotify: bool = True) -> None:
        pass
from typing import Any
from ntt_signal import Signal
from typing import *
from ..IModel import IModel 
from .Property import Property
from ntt_observable_list import ObservableList


class ListProperty(Property):
    def __init__(self, model: IModel, lstData: List[Any], strAttributeName: str) -> None:
        super().__init__(model, strAttributeName, list)

        self._lstData = ObservableList(lstData)
        self._lstData.Attach(self)

    def GetValue(self) -> IModel:
        return self._lstData

    def SetValue(self, lstData: List[Any], bNotify: bool = True) -> None:
        self._lstData = ObservableList(lstData)
        self._lstData.Attach(self)
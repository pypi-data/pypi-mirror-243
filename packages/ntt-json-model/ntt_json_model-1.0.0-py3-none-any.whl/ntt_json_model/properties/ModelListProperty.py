from typing import *
from typing import Any
from ..IModel import IModel
from .Property import Property
from ntt_observable_list import ObservableList


class ModelListProperty(Property):
    def __init__(self, model: IModel, mModels: List[IModel], strAttributeName: str) -> None:
        super().__init__(model, strAttributeName, None, bIsModel=True)

        self._mModels = ObservableList(mModels)
        self._mModels.Attach(self)

    def GetValue(self) -> ObservableList:
        return self._mModels
    
    def SetValue(self, mNewModels: ObservableList[IModel], bNotify: bool = True) -> None:
        self._mModels = mNewModels
        self._mModels.Attach(self)
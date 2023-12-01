from typing import Any
from ntt_json_model.IModel import IModel
from .Property import *


class BoolProperty(Property):
    def __init__(self, model: IModel, bDefaultValue: bool, 
                        strAttributeName: str, 
                        bIsModel: bool = False) -> None:
        super().__init__(model, strAttributeName, bool, bIsModel)

        self._bValue = bDefaultValue

    def GetValue(self) -> Any:
        return self._bValue

    def SetValue(self, newValue: object, bNotify: bool = True) -> None:
        if self._bValue != newValue:
            self._bValue = newValue

            if bNotify:
                self.Emit(self._bValue)
from typing import Any
from ntt_signal import Signal
from .Property import Property


class StrProperty(Property):
    def __init__(self, model: Signal, strValue: str, strAttributeName: str) -> None:
        super().__init__(model, strAttributeName, str)

        self._strValue = strValue

    def GetValue(self) -> Any:
        return self._strValue

    def SetValue(self, strValue: str, bNotify: bool = True) -> None:
        if self._strValue != strValue:
            self._strValue = strValue
            if bNotify:
                self.Emit(self._strValue)
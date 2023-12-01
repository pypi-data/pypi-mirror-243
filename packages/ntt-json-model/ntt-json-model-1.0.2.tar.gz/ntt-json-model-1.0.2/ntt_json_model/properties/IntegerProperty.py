from typing import Any
from ntt_signal import Signal
from .Property import Property


class IntegerProperty(Property):
    def __init__(self, model: Signal, nValue: int, strAttributeName: str) -> None:
        super().__init__(model, strAttributeName, int)
        self._nValue = nValue

    def GetValue(self) -> Any:
        return self._nValue
    
    def SetValue(self, nNewValue:int, bNotify: bool = True) -> None:
        if nNewValue != self._nValue:
            self._nValue = nNewValue
            if bNotify:
                self.Emit(self._nValue)
from typing import Any
from ntt_signal import Signal
from .Property import Property


class FloatProperty(Property):
    def __init__(self, model: Signal, fValue: float, strAttributeName: str) -> None:
        super().__init__(model, strAttributeName, float)

        self._fValue = fValue

    def GetValue(self) -> Any:
        return self._fValue

    def SetValue(self, fNewValue: float, bNotify: bool = True) -> None:
        if isinstance(fNewValue, float) or isinstance(fNewValue, int):
            if fNewValue != self._fValue:
                self._fValue = float(fNewValue)
                if bNotify:
                    self.Emit(self._fValue)
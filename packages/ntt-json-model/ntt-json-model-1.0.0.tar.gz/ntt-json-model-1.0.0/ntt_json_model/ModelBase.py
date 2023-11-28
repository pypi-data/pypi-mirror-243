from typing import *
import json
from ntt_signal import Signal
from .Exception import *
from .properties import *
from .IModel import IModel


class ModelBase(Signal, IModel):
    mSubModels: dict = {}

    def __init__(self) -> None:
        super().__init__()
        self._strDataAttributeNames: List[str] = []
        self._strModelDataAttributeNames: List[str] = []

    def _AppendModelData(self, strAttributeName: str, bIsModel: bool = False) -> None:
        if bIsModel:
            self._strModelDataAttributeNames.append(strAttributeName)
        else:
            self._strDataAttributeNames.append(strAttributeName)

    def ToDict(self) -> dict:
        dictData: dict = {}

        for strAttributeName in self._strDataAttributeNames:
            attribute: Property = getattr(self, strAttributeName)
            if isinstance(attribute, FloatProperty) \
                    or isinstance(attribute, IntegerProperty) \
                    or isinstance(attribute, ListProperty) \
                    or isinstance(attribute, StrProperty):
                dictData[strAttributeName] = attribute.GetValue()
            elif isinstance(attribute, ModelProperty):
                dictData[strAttributeName] = attribute.GetValue().ToDict()

        for strAttributeName in self._strModelDataAttributeNames:
            dictData[strAttributeName] = []
            mModels: List[IModel] = getattr(self, strAttributeName).GetValue()
            for mModel in mModels:
                dictData[strAttributeName].append(mModel.ToDict())


        dictData["__class__"] = self.__class__.__name__

        return dictData

    def FromDict(self, dictData: dict, bEmit: bool = True) -> None:
        if "__class__" not in dictData:
            raise InputDictError("Input dict has no __class__ key")
        elif dictData["__class__"] != self.__class__.__name__:
            raise TargetClassError(f"Expect {self.__class__.__name__} but received {dictData['__class__']}")
        else:
            for strAttributeName in self._strDataAttributeNames:
                if strAttributeName in dictData:
                    if not isinstance(dictData[strAttributeName], dict):
                        getattr(self,strAttributeName).SetValue(dictData[strAttributeName], False)
                    else:
                        getattr(self, strAttributeName).GetValue().FromDict(dictData[strAttributeName], False)

            for strAttributeName in self._strModelDataAttributeNames:
                if strAttributeName in dictData:
                    attribute: ModelListProperty = getattr(self, strAttributeName)
                    mModels = ObservableList([])
                    for dictObjectData in dictData[strAttributeName]:
                        obj: IModel = self.mSubModels[dictObjectData["__class__"]]()
                        obj.FromDict(dictObjectData, bEmit=False)

                        mModels.append(obj)

                    attribute.SetValue(mModels, False)

            if bEmit:
                self.Emit()

    def ToFile(self, strFileName: str) -> None:
        with open(strFileName, "w") as file:
            json.dump(self.ToDict(), file, indent=4)

    def FromFile(self, strFileName: str) -> None:
        with open(strFileName, "r") as file:
            self.FromDict(json.load(file))
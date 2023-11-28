import unittest
import json
from unittest.mock import *
from ntt_json_model import *
from .TestClass import *


class ModelListPropertyTest(unittest.TestCase):
    model = None

    def setUp(self) -> None:
        self.model = TestModelListClass()

    def test_WhenChangeThePropertyOfTheModelAttribute_ThenTheModelIsEmitted(self):
        testCallback = Mock()

        self.model.Connect(testCallback)

        self.model.Models.extend([3, 4, 5])

        testCallback.assert_called_once()

    def test_WhenExportDataOfModelListPropertyToDict_ThenGetRightValue(self):
        self.model.Score = 4.3
        self.model.Models.extend([
            TestModelClass(nScore=4, nValue=3, fTemp=3.2, strName="ThaoNguyenThe"),
            TestModelClass(nScore=5, nValue=3, fTemp=3.2, strName="ThaoNguyenThe", lstScores=[3, 2]),
        ])

        dictData: dict = self.model.ToDict()

        self.assertDictEqual(
            dictData,
            {
                "__class__": "TestModelListClass",
                "_fScore": 4.3,
                "_mModels": [
                    {
                        "__class__": "TestModelClass",
                        "_nScore": 4,
                        "_mTestModel": {
                            "__class__": "TestModel",
                            "_nValue": 3,
                            "_fTemp": 3.2,
                            "_strName": "ThaoNguyenThe",
                            "_lstScores": []
                        }
                    },
                    {
                        "__class__": "TestModelClass",
                        "_nScore": 5,
                        "_mTestModel": {
                            "__class__": "TestModel",
                            "_nValue": 3,
                            "_fTemp": 3.2,
                            "_strName": "ThaoNguyenThe",
                            "_lstScores": [3, 2]
                        }
                    }
                ]
            }
        )

    def test_WhenLoadDataForModelListFromDict_ThenGetRightvalue(self):
        dictData = {
            "__class__": "TestModelListClass",
            "_fScore": 4.3,
            "_mModels": [
                {
                    "__class__": "TestModelClass",
                    "_nScore": 4,
                    "_mTestModel": {
                        "__class__": "TestModel",
                        "_nValue": 3,
                        "_fTemp": 3.2,
                        "_strName": "ThaoNguyenThe",
                        "_lstScores": []
                    }
                },
                {
                    "__class__": "TestModelClass",
                    "_nScore": 5,
                    "_mTestModel": {
                        "__class__": "TestModel",
                        "_nValue": 3,
                        "_fTemp": 3.2,
                        "_strName": "ThaoNguyenThe",
                        "_lstScores": [3, 2]
                    }
                }
            ]
        }
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.FromDict(dictData)

        self.assertEqual(self.model.Score, 4.3)
        self.assertEqual(len(self.model.Models), 2)
        self.assertEqual(self.model.Models[0].Score, 4)
        self.assertEqual(self.model.Models[1].Score, 5)
        self.assertEqual(self.model.Models[0].TestModel.Name, "ThaoNguyenThe")
        self.assertEqual(self.model.Models[1].TestModel.Name, "ThaoNguyenThe")
        self.assertListEqual(self.model.Models[0].TestModel.Scores, [])
        self.assertListEqual(self.model.Models[1].TestModel.Scores, [3, 2])

        testCallback.assert_called_once()

    def test_WhenLoadDataForModelListFromDictAndChangeList_TheModelIsEmitted(self):
        dictData = {
            "__class__": "TestModelListClass",
            "_fScore": 4.3,
            "_mModels": [
                {
                    "__class__": "TestModelClass",
                    "_nScore": 4,
                    "_mTestModel": {
                        "__class__": "TestModel",
                        "_nValue": 3,
                        "_fTemp": 3.2,
                        "_strName": "ThaoNguyenThe",
                        "_lstScores": []
                    }
                },
                {
                    "__class__": "TestModelClass",
                    "_nScore": 5,
                    "_mTestModel": {
                        "__class__": "TestModel",
                        "_nValue": 3,
                        "_fTemp": 3.2,
                        "_strName": "ThaoNguyenThe",
                        "_lstScores": [3, 2]
                    }
                }
            ]
        }
        testCallback = Mock()
        self.model.FromDict(dictData)
        self.model.Connect(testCallback)

        self.model.Models.append(TestModel())

        testCallback.assert_called_once()
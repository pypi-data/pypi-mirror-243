import unittest
from unittest.mock import Mock
from ntt_json_model import *
from .TestClass import *


class ModelPropertyTest(unittest.TestCase):
    model = None
    def setUp(self) -> None:
        self.model = TestModelClass() 

    def test_WhenChangeThePropertyOfTheModelAttribute_ThenTheModelIsEmitted(self):
        testCallback = Mock()

        self.model.Connect(testCallback)

        self.model.TestModel.Name = "ThaoNguyenThe"

        testCallback.assert_called_once()

    def test_WhenExportDataOfModelPropertyToDict_ThenGetRightValue(self):
        self.model.Score = 4
        self.model.TestModel.Name = "ThaoNguyenThe"
        self.model.TestModel.Temp = 3.2
        self.model.TestModel.Scores.extend([3, 2])

        dictData: dict = self.model.ToDict()

        self.assertDictEqual(
            dictData,
            {
                "__class__": "TestModelClass",
                "_nScore": 4,
                "_mTestModel": {
                    "__class__": "TestModel",
                    "_nValue": 3,
                    "_fTemp": 3.2,
                    "_strName": "ThaoNguyenThe",
                    "_lstScores": [3, 2]
                }
            }
        )

    def test_WhenLoadDataModelPropertyFromDict_ThenGetRightValueAndTheModelIsEmittedOnce(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        dictData = {
            "__class__": "TestModelClass",
            "_nScore": 4,
            "_mTestModel": {
                "__class__": "TestModel",
                "_nValue": 3,
                "_fTemp": 3.2,
                "_strName": "ThaoNguyenThe",
                "_lstScores": [3, 2]
            }
        }

        self.model.FromDict(dictData)

        self.assertEqual(self.model.Score, 4)
        self.assertEqual(self.model.TestModel.Name, "ThaoNguyenThe")
        self.assertEqual(self.model.TestModel.Value, 3)
        self.assertEqual(self.model.TestModel.Temp, 3.2)
        self.assertEqual(self.model.TestModel.Scores, [3, 2])
        testCallback.assert_called_once()
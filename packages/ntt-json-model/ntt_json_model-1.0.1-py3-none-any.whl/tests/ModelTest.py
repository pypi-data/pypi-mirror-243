import unittest
from typing import *
from unittest.mock import Mock
from .TestClass import *
from ntt_json_model import *


class ModelTest(unittest.TestCase):
    model = None

    def setUp(self) -> None:
        self.model = TestModel()

    def test_GivenModelWithData_WhenThatDataHasChanged_ThenTheModelIsEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Value = 5

        testCallback.assert_called_once()

    def test_GivenModelWithData_WhenThatStrDataHasChanged_ThenTheModelIsEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Temp = 5.3

        testCallback.assert_called_once()

    def test_WhenChangeFloatPropertyWithUnchangedData_ThenNoEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Temp = 3.1
        
        testCallback.assert_not_called()

    def test_WhenChangeFloatPropertyWithInt_ThenModelIsEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Temp = 5

        testCallback.assert_called_once()

    def test_WhenChangeDataWithoutChangingValueActually_ThenNoEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Value = 3

        testCallback.assert_not_called()

    def test_WhenChangeStrPropertyWithInt_ThenModelIsEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Name = "Test"

        testCallback.assert_called_once()

    def test_WhenChangeStrDataWithoutChangingValueActually_ThenNoEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Name = "Hello"

        testCallback.assert_not_called()

    def test_WhenChangeListPropertyWithInt_ThenModelIsEmitted(self):
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.Scores.append(4)

        testCallback.assert_called_once()

    def test_GivenModel_WhenExtractToDict_ThenDataConvertedToDict(self):
        self.model.Name = "Testing"
        self.model.Value = 3
        self.model.Temp = 45
        self.model.Scores.append(4)

        dictData = self.model.ToDict()

        self.assertDictEqual(
            dictData,
            {
                "__class__": "TestModel",
                "_nValue": 3,
                "_fTemp": 45.0,
                "_strName": "Testing",
                "_lstScores": [4]
            }
        )

    def test_GivenModel_WhenLoadDataFromDict_ModelIsEmittedOnce(self):
        dictData = {
            "__class__": "TestModel",
            "_nValue": 3,
            "_fTemp": 45.0,
            "_strName": "Testing",
            "_lstScores": [4],
        }
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.FromDict(dictData)

        self.assertEqual(self.model.Name, "Testing")
        self.assertEqual(self.model.Temp, 45.0)
        self.assertEqual(self.model.Value, 3)
        self.assertListEqual(self.model.Scores, [4])
        testCallback.assert_called_once()

    def test_GivenModelWhichIsLoadedFromDict_WhenChangeTheProperty_ThenModelIsEmitted(self):
        dictData = {
            "__class__": "TestModel",
            "_nValue": 3,
            "_fTemp": 45.0,
            "_strName": "Testing",
            "_lstScores": [4],
        }
        testCallback = Mock()
        self.model.Connect(testCallback)

        self.model.FromDict(dictData)

        self.model.Value = 2
        self.model.Scores.clear()

        self.assertEqual(
            testCallback.call_count,
            3,
            "The Callback should be called 3 times",
        )

    def test_WhenLoadModelFromNonEnoughDataDict_ThenNoErrors(self):
        dictData = {
            "__class__": "TestModel",
            "_nValue": 3,
            "_strName": "Testing",
            "_lstScores": [4],
        }

        self.model.FromDict(dictData)

        self.assertEqual(self.model.Temp, 3.1)

    def test_WhenLoadModelFromNonClassKey_ThenRaiseError(self):
        dictData = {
            "_nValue": 3,
            "_strName": "Testing",
            "_fTemp": 4.1,
            "_lstScores": [4],
        }

        with self.assertRaises(InputDictError) as context:
            self.model.FromDict(dictData)
            
        self.assertEqual(str(context.exception), "Input dict has no __class__ key")

    def test_WhenLoadModelFromWrongClassValue_ThenRaiseError(self):
        dictData = {
            "__class__": "TestingModel",
            "_nValue": 3,
            "_fTemp": 45.0,
            "_strName": "Testing",
            "_lstScores": [4],
        }

        with self.assertRaises(TargetClassError) as context:
            self.model.FromDict(dictData)

        self.assertEqual(str(context.exception), "Expect TestModel but received TestingModel")
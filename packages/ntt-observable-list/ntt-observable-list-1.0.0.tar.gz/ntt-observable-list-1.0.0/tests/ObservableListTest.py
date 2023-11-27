import unittest
from unittest.mock import Mock
from ntt_observable_list import *
from ntt_signal import Signal


class SubSignal(Signal):
    def __init__(self, nValue: int) -> None:
        super().__init__(int)
        
        self._nValue = nValue

    @property
    def Value(self) -> int:
        return self._nValue

    @Value.setter
    def Value(self, nNewValue: int) -> None:
        self._nValue = nNewValue
        self.Emit(self._nValue)


class ObservableListTest(unittest.TestCase):
    def test_WhenAppended_ThenTheObservableListIsEmitted(self):
        lst = ObservableList([1, 2, 3])
        testCallback = Mock()
        lst.Connect(testCallback)

        lst.append(5)

        self.assertListEqual(
            lst, 
            [1, 2, 3, 5]
        )
        testCallback.assert_called_once_with([1, 2, 3, 5])

    def test_WhenPopped_ThenTheObservableListIsEmitted(self):
        lst = ObservableList([1, 2, 3])
        testCallback = Mock()
        lst.Connect(testCallback)

        lst.pop()

        self.assertListEqual(
            lst, 
            [1, 2]
        )
        testCallback.assert_called_once_with([1, 2])

    def test_WhenChangeItemInsideTheObservableList_ThenTheListIsEmitted(self):
        lst = ObservableList([1, 2, 3])
        testCallback = Mock()
        lst.Connect(testCallback)

        lst[2] = 4

        self.assertEqual(
            lst,
            [1, 2, 4]
        )
        testCallback.assert_called_once_with([1, 2, 4])

    def test_GivenTheListContainAListOfSignalSubclasses_WhenSignalElemnentIsEmitted_ThenTheListIsEmitted(self):
        lst = ObservableList([SubSignal(1), SubSignal(2), SubSignal(3)])
        testCallback = Mock()
        lst.Connect(testCallback)

        lst[0].Value = 4

        testCallback.assert_called_once()
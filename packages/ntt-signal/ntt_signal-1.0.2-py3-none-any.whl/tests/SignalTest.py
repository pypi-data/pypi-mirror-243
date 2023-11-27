import unittest
from unittest.mock import Mock
from ntt_signal import *


class SignalTest(unittest.TestCase):
    def test_GivenSignalWithACallbackIsAssigned_WhenTheSignalIsEmitted_ThenTheCallbackIsCalled(self):
        signal = Signal()
        testCallback = Mock()
        signal.Connect(testCallback)

        signal.Emit()

        testCallback.assert_called_once()

    def test_Given2Callbacks_WhenDeletedOneAndSignalIsEmitted_ThenItIsNotCalled(self):
        signal = Signal()
        firstTestCallback = Mock()
        secondTestCallback = Mock()
        signal.Connect(firstTestCallback)
        signal.Connect(secondTestCallback)
        signal.Disconnect(firstTestCallback)

        signal.Emit()

        firstTestCallback.assert_not_called()
        secondTestCallback.assert_called_once()
        
    def test_GivenSignalWithSpecialType_WhenEmitThatSignal_ThenPassThatTypeData(self):
        signal = Signal(int)
        testCallback = Mock()
        signal.Connect(testCallback)

        signal.Emit(3)

        testCallback.assert_called_once_with(3)

    def test_GivenSignalWithSpecialType_WhenEmitThatSignalWithWrongType_ThenRaiseError(self):
        signal = Signal(int)
        testCallback = Mock()
        signal.Connect(testCallback)

        with self.assertRaises(SignalTypeError) as context:
            signal.Emit("hello")

        self.assertEqual(str(context.exception), "Emit expects int but received str")
    
    def test_GivenSignalWithoutType_WhenIsEmittedWithData_ThenRaiseError(self):
        signal = Signal()
        testCallback = Mock()
        signal.Connect(testCallback)

        with self.assertRaises(SignalTypeError) as context:
            signal.Emit("hello")

        self.assertEqual(str(context.exception), "Emit expects no argument but received str")

    def test_Given2SignalsWhichIsAttached_WhenTheChildSignalIsEmitted_ThenTheParentSignalIsAlsoEmitted(self):
        signal = Signal()
        child_signal = Signal()
        testCallback = Mock()
        child_signal.Attach(signal)
        signal.Connect(testCallback)

        child_signal.Emit()

        testCallback.assert_called_once()

    def test_WhenAttachSignalWithNonSignalObject_ThenRaiseAttachError(self):
        signal = Signal()

        with self.assertRaises(AttachTypeError) as context:
            signal.Attach(3)

        self.assertEqual(str(context.exception), "Attach method expects Signal object but received int")

    def test_WhenAttachSignal_WhenTheParentIsEmitted_ThenTheChildIsNot(self):
        signal = Signal()
        child_signal = Signal()
        testCallback = Mock()
        child_signal.Attach(signal)
        child_signal.Connect(testCallback)

        signal.Emit()

        testCallback.assert_not_called()
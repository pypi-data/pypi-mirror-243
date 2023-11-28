import unittest
from unittest.mock import Mock
from ntt_signal import *


class SignalTest(unittest.TestCase):
    signal = None
    int_signal = None
    str_signal = None

    child_signal = None
    child_int_signal = None
    child_str_signal = None

    def setUp(self) -> None:
        self.signal = Signal()
        self.int_signal = Signal(int)
        self.str_signal = Signal(str)

        self.child_signal = Signal()
        self.child_int_signal = Signal(int)
        self.child_str_signal = Signal(str)

    def test_GivenSignalWithACallbackIsAssigned_WhenTheSignalIsEmitted_ThenTheCallbackIsCalled(self):
        testCallback = Mock()
        self.signal.Connect(testCallback)

        self.signal.Emit()

        testCallback.assert_called_once()

    def test_Given2Callbacks_WhenDeletedOneAndSignalIsEmitted_ThenItIsNotCalled(self):
        firstCallback = Mock()
        secondCallback = Mock()
        self.signal.Connect(firstCallback)
        self.signal.Connect(secondCallback)
        self.signal.Disconnect(firstCallback)

        self.signal.Emit()

        firstCallback.assert_not_called()
        secondCallback.assert_called_once()
        
    def test_GivenSignalWithSpecialType_WhenEmitThatSignal_ThenPassThatTypeData(self):
        testCallback = Mock()
        self.int_signal.Connect(testCallback)

        self.int_signal.Emit(3)

        testCallback.assert_called_once_with(3)

    def test_GivenSignalWithSpecialType_WhenEmitThatSignalWithWrongType_ThenRaiseError(self):
        testCallback = Mock()
        self.int_signal.Connect(testCallback)

        with self.assertRaises(SignalTypeError) as context:
            self.int_signal.Emit("hello")

        self.assertEqual(str(context.exception), "Emit expects int but received str")
    
    def test_GivenSignalWithoutType_WhenIsEmittedWithData_ThenRaiseError(self):
        testCallback = Mock()
        self.signal.Connect(testCallback)

        with self.assertRaises(SignalTypeError) as context:
            self.signal.Emit("hello")

        self.assertEqual(str(context.exception), "Emit expects no argument but received str")

    def test_Given2SignalsWhichIsAttached_WhenTheChildSignalIsEmitted_ThenTheParentSignalIsAlsoEmitted(self):
        testCallback = Mock()
        self.child_signal.Attach(self.signal)
        self.signal.Connect(testCallback)

        self.child_signal.Emit()

        testCallback.assert_called_once()

    def test_WhenAttachSignalWithNonSignalObject_ThenRaiseAttachError(self):
        with self.assertRaises(AttachTypeError) as context:
            self.signal.Attach(3)

        self.assertEqual(str(context.exception), "Attach method expects Signal object but received int")

    def test_WhenAttachSignal_WhenTheParentIsEmitted_ThenTheChildIsNot(self):
        testCallback = Mock()
        self.child_signal.Attach(self.signal)
        self.child_signal.Connect(testCallback)

        self.signal.Emit()

        testCallback.assert_not_called()

    def test_GivenSignalAndChildSignalWithTheParentHasNotType_WhenTheChildIsEmitted_ThenTheParentIsEmited(self):
        testCallback = Mock()
        self.child_str_signal.Attach(self.signal)
        self.signal.Connect(testCallback)

        self.child_str_signal.Emit("Hello World")

        testCallback.assert_called_once()

    def test_GivenParentSignalHasTypeButTheAttachSignalDoesNo_WhenAttachSignal_ThenRaisesError(self):
        with self.assertRaises(AttachTypeError) as context:
            self.child_signal.Attach(self.str_signal)

        self.assertEqual(str(context.exception), "Attach signal which require str, but does not have")

    def test_GivenParentSignalAndAttachedSignalHasSameType_WhenChildSignalIsEmitted_ThenParentIsEmitted(self):
        testCallback = Mock()

        self.int_signal.Connect(testCallback)
        self.child_int_signal.Attach(self.int_signal)

        self.child_int_signal.Emit(3)

        testCallback.assert_called_once_with(3)
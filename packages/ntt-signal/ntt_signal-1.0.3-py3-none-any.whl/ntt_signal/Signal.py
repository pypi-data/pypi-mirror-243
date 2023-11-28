from typing import *
from .Exceptions import *


class Signal:
    def __init__(self, datatype: type = None) -> None:
        self._datatype = datatype
        self._callbacks: List[callable] = []
        self._signals: list = []
        self._maps: list = []

    @property
    def Datatype(self) -> type:
        return self._datatype

    def Connect(self, callback: callable) -> None:
        self._callbacks.append(callback)

    def Disconnect(self, callback: callable) -> None:
        self._callbacks.remove(callback)

    def Attach(self, signal) -> None:
        if not isinstance(signal, Signal):
            raise AttachTypeError(f"Attach method expects Signal object but received {type(signal).__name__}")
        elif signal.Datatype is not None and signal.Datatype != self._datatype:
            raise AttachTypeError(f"Attach signal which require {signal.Datatype.__name__}, but does not have")
        self._signals.append(signal)

    def Emit(self, data: object = None) -> None:
        if data is not None and self._datatype is None:
            raise SignalTypeError(
                f"Emit expects no argument but received {type(data).__name__}"
            )
        if data is not None:
            if not isinstance(data,self._datatype):
                strDatatypeName = self._datatype.__name__
                raise SignalTypeError(
                    f"Emit expects {strDatatypeName} but received {type(data).__name__}"
                )

        for callback in self._callbacks:
            if self._datatype == None:
                callback()
            else:
                callback(data)

        for signal in self._signals:
            if signal.Datatype is not None:
                signal.Emit(data)
            else:
                signal.Emit()
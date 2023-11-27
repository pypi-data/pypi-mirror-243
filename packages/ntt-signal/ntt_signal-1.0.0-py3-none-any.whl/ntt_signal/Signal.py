from typing import *
from .Exceptions import *


class Signal:
    def __init__(self, datatype: type = None) -> None:
        self._datatype = datatype
        self._callbacks: List[callable] = []

    def Connect(self, callback: callable) -> None:
        print(callback)
        self._callbacks.append(callback)

    def Disconnect(self, callback: callable) -> None:
        self._callbacks.remove(callback)

    def Emit(self, data: object = None) -> None:
        if data is not None:
            if not isinstance(data,self._datatype):
                strDatatypeName = self._datatype.__name__
                raise WrongSignalTypeError(
                    f"Signal({strDatatypeName}) Emit() expects {strDatatypeName} but received {type(data).__name__}"
                )

        for callback in self._callbacks:
            if self._datatype == None:
                callback()
            else:
                callback(data)

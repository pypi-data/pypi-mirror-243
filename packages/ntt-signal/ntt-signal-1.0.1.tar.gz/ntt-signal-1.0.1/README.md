# ntt-signal
Signal library by threezinedine

## Example
```python
def Callback() -> None:
    print("Signal is emitted")

signal = Signal()
signal.Connect(Callback)

signal.Emit()
```

## Example with type
```python
def Callback(nValue: int) -> None:
    print(f"Signal is emitted with value {nValue}")

signal = Signal(int)
signal.Connect(Callback)

signal.Emit(3)
```
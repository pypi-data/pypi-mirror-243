class SignalTypeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AttachTypeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
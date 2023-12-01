class InputDictError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class TargetClassError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
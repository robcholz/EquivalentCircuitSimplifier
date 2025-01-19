import uuid


class Pin:
    def __init__(self, display_name: str = 'Anonymous'):
        self._display_name: str = display_name
        self._id: str = display_name + "_" + str(uuid.uuid4())

    def get_display_name(self) -> str:
        return self._display_name

    def set_pin_id(self, new_id: str) -> None:
        self._id = new_id

    def get_pin_id(self) -> str:
        return self._id

    def is_connected_to(self, other: "Pin") -> bool:
        return self._id is other._id

    def __eq__(self, other) -> bool:
        if not isinstance(other, Pin):
            return False
        return self._id is other._id and self._display_name is other._display_name

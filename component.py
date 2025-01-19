from abc import abstractmethod
from typing import List, Optional

from pin import Pin
from unit import Unit


class Wire:
    def __init__(self, left_id: str, right_id: str):
        self._left = Pin()
        self._right = Pin()
        self._left.set_pin_id(left_id)
        self._right.set_pin_id(right_id)

    def left(self) -> Pin:
        return self._left

    def right(self) -> Pin:
        return self._right


class Component(Unit):
    def __init__(self, display_name: str, unit_symbol: [str, None], unit_in_language: str, pins: List[Pin]):
        super().__init__(unit_symbol, unit_in_language)
        self._pins: List[Pin] = pins
        self._display_name: str = display_name
        self._data: any = ()

    def set_data(self, data: any) -> None:
        self._data = data

    def pins(self) -> List[Pin]:
        return self._pins

    def display_name(self) -> str:
        return self._display_name

    def data(self) -> any:
        return self._data

    def is_parallel_to(self, other: "Component") -> bool:
        other_pins = other.pins()
        if len(other_pins) is not len(self._pins):
            return False

        # check for the parallel connections
        connected_count: int = 0
        for other_pin in other_pins:
            for this_pin in self._pins:
                if other_pin.is_connected_to(this_pin):
                    connected_count += 1
        if connected_count is len(self._pins):
            return True

    def is_series_to(self, other: "Component") -> bool:
        other_pins = other.pins()
        if len(other_pins) is not len(self._pins):
            return False
        connected_count: int = 0
        for other_pin in other_pins:
            for this_pin in self._pins:
                if other_pin.is_connected_to(this_pin):
                    if connected_count == 2:
                        # more than one connection between two components
                        return False
                    connected_count += 1
        return True

    def __str__(self):
        return "[{} {} {}-{}]".format(self.display_name(),
                                      self.get_simplified_value_with_unit(self.data()),
                                      self._pins[0].get_pin_id(),
                                      self._pins[1].get_pin_id()
                                      )

    @abstractmethod
    def on_parallel(self, other: "Component") -> Optional["Component"]:
        """
            The operation when two components are in parallel
        """
        pass

    @abstractmethod
    def on_series(self, other: "Component") -> Optional["Component"]:
        """
            The operation to do when two components are in series
        """
        pass

from typing import Optional, List

from component import Component
from pin import Pin


def to_id_pins(pins: List[Pin]) -> List[str]:
    result = []
    for p in pins:
        result.append(p.get_pin_id())
    return result


def calculate_2_pins(self: "Component", other: "Component") -> (str, str):
    set_left = set(to_id_pins(self.pins()))
    set_right = set(to_id_pins(other.pins()))
    eq_pins = list((set_left | set_right) - (set_left & set_right))
    left_eq = eq_pins[0]
    right_eq = eq_pins[1]
    return left_eq, right_eq


class Resistor(Component):
    def __init__(self, left_id: str, right_id: str, resistance: float):
        left = Pin(display_name='R_A')
        right = Pin(display_name='R_B')
        left.set_pin_id(left_id)
        right.set_pin_id(right_id)
        super().__init__("Resistor", 'Ω', 'Resistance', [left, right])
        super().set_data(resistance)

    def on_parallel(self, other: "Component") -> Optional["Component"]:
        if isinstance(other, Resistor) is False:
            return None
        return Resistor(self.pins()[0].get_pin_id(), self.pins()[1].get_pin_id(),
                        1 / (1 / super().data() + 1 / other.data()))

    def on_series(self, other: "Component") -> Optional["Component"]:
        if isinstance(other, Resistor) is False:
            return None
        left_eq, right_eq = calculate_2_pins(self, other)
        return Resistor(left_eq, right_eq, super().data() + other.data())

    def get_unit_value_by_power(self, power: int, value: float) -> str:
        if 0 <= power <= 2:
            return str(value)
        if 3 <= power <= 6:
            return 'k' + str(value / 1000)
        return 'm' + str(value / 1000000)


class Capacitor(Component):
    def __init__(self, left_id: str, right_id: str, capacitance: float):
        left = Pin(display_name='C_A')
        right = Pin(display_name='C_B')
        left.set_pin_id(left_id)
        right.set_pin_id(right_id)
        super().__init__("Capacitor", None, 'Capacitance', [left, right])
        super().set_data(capacitance)

    def on_parallel(self, other: "Component") -> Optional["Component"]:
        if isinstance(other, Capacitor) is False:
            return None
        left_eq, right_eq = calculate_2_pins(self, other)
        return Capacitor(left_eq, right_eq, super().data() + other.data())

    def on_series(self, other: "Component") -> Optional["Component"]:
        if isinstance(other, Capacitor) is False:
            return None
        left_eq, right_eq = calculate_2_pins(self, other)
        return Capacitor(left_eq, right_eq, 1 / (1 / super().data() + 1 / other.data()))

    def get_unit_value_by_power(self, power: int, value: float) -> str:
        if -2 <= power:
            return str(value) + ' F'
        elif -6 <= power <= -3:
            return f'{value / 1000:.3f} mF'
        elif -9 <= power <= -7:
            return f'{value / 1000000:.3f} μF'
        elif -12 <= power <= -10:
            return f'{value / 1000000000:.3f} nF'
        else:
            return f'{value / 1000000000000:.3f} pF'

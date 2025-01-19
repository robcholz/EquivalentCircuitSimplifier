import math
from abc import abstractmethod


class Unit:
    def __init__(self, unit_symbol: [str, None], unit_in_language: str):
        self._unit_symbol: [str, None] = unit_symbol
        self._unit_in_language: str = unit_in_language

    def get_standard_value_with_unit(self, value: float) -> str:
        return "{}{}".format(value, self._unit_symbol)

    def get_simplified_value_with_unit(self, value: float) -> str:
        num = 0.0
        if value != 0:
            num = float(self.get_unit_value_by_power(math.floor(math.log10(value)), value))
        if num.is_integer():
            return "{}{}".format(
                int(num),
                self._unit_symbol
            )
        return "{}{}".format(
            round(num, 3),
            self._unit_symbol
        )

    @abstractmethod
    def get_unit_value_by_power(self, power: int, value: float) -> str:
        pass

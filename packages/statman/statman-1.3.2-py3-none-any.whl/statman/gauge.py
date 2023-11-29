from .metric import Metric


class Gauge(Metric):
    _value = None

    def __init__(self, name=None, value: float = 0):
        super().__init__(name=name)
        self.value = value

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value: float) -> float:
        if value is None:
            value = 0
        self._value = value

    def increment(self, amount: int = 1) -> float:
        if amount is None:
            amount = 1
        self._value += amount

    def decrement(self, amount: int = 1) -> float:
        if amount is None:
            amount = 1
        self._value -= amount

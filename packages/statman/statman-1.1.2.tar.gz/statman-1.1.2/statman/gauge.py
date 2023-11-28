class Gauge():
    _name = None
    _value = None

    def __init__(self, name=None, value: float = 0):
        self._name = name
        self.value = value

    def __str__(self):
        name = self.name
        if not name:
            name = '(Gauge)'
        return f'[{name} => value={self.value}]'

    def print(self):
        self.report(output_stdout=True)

    def report(self, output_stdout: bool = False):
        output = str(self)
        if output_stdout:
            print(output)
        return output

    @property
    def name(self) -> str:
        return self._name

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

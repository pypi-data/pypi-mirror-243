class Metric():
    _name = None

    def __init__(self, name=None):
        self._name = name

    def __str__(self):
        name = self.name
        if not name:
            name = '(Metric)'
        value = self.read()
        buffer = f'[{name} => {value}]'
        return buffer

    @property
    def name(self) -> str:
        return self._name

    def read(self, precision: int = None) -> float:
        value = self.value
        if not precision is None:
            value = round(value, precision)
        return value

    @property
    def value(self) -> float:
        pass

    def print(self):
        self.report(output_stdout=True)

    def report(self, output_stdout: bool = False):
        output = str(self)
        if output_stdout:
            print(output)
        return output

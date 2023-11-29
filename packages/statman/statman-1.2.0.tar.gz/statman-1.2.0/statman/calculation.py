class Calculation():
    _name = None
    _function = None

    def __init__(self, name=None, function=None):
        self._name = name
        self._function = function

    def __str__(self):
        name = self.name
        if not name:
            name = '(Calculation)'
        value = self.read(precision=0)
        buffer = f'[{name} => {value}'
        return buffer

    def print(self):
        self.report(output_stdout=True)

    @property
    def name(self) -> str:
        return self._name

    def report(self, output_stdout: bool = False):
        output = str(self)
        if output_stdout:
            print(output)
        return output

    def read(self, precision: int = None) -> float:
        try:
            result = self._function()
        except Exception as e:
            print(f'failed to execute calculation [{self.name}][{e}]')
            return None

        if precision:
            result = round(result, precision)
        return result

    @property
    def value(self) -> float:
        return self.read()

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, function):
        self._function = function

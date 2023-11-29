from .metric import Metric


class Calculation(Metric):
    _function = None

    def __init__(self, name=None, function=None):
        super().__init__(name=name)
        self._function = function

    @property
    def value(self) -> float:
        try:
            f = self.calculation_function
            result = f()
            return result
        except Exception as e:
            print(f'failed to execute calculation [{self.name}][{e}]')
            return None

    @property
    def calculation_function(self):
        return self._function

    @calculation_function.setter
    def calculation_function(self, function):
        self._function = function

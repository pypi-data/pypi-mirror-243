from .calculation import Calculation


class Rate(Calculation):
    _numerator_metric_name = None
    _denominator_metric_name = None

    def __init__(self, name=None, numerator_metric_name=None, denominator_metric_name=None):
        super().__init__(name=name, function=lambda: self._numerator_value / self._denominator_value)
        self._numerator_metric_name = numerator_metric_name
        self._denominator_metric_name = denominator_metric_name

    def __str__(self):
        name = self.name
        if not name:
            name = '(Rate)'
        value = self.read(precision=2)
        numerator = round(self._numerator_value, 2)
        denominator = round(self._denominator_value, 2)
        buffer = f'[{name} => {numerator}/{denominator} = {value}]'
        return buffer

    @property
    def _numerator_value(self):
        from statman import Statman  #pylint: disable=import-outside-toplevel
        return Statman.get(self._numerator_metric_name).value

    @property
    def _denominator_value(self):
        from statman import Statman  #pylint: disable=import-outside-toplevel
        return Statman.get(self._denominator_metric_name).value

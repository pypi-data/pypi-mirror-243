import datetime
import statistics
from functools import reduce


class History():
    _data = []

    def __init__(self):
        self._data = []

    def __str__(self):
        pass

    def append(self, dt: datetime = None, value: float = None) -> str:
        event = self.create_event(dt=dt, value=value)
        self._data.append(event)

    def create_event(self, dt, value):
        return Event(dt, value)

    def count(self):
        return len(self._data)

    def events(self):
        return self._data

    def values(self):
        return [event.value for event in self.events()]

    def max_value(self, precision=0):
        if self.count() == 0:
            return None
        result = reduce(lambda x, y: x if x > y else y, self.values())
        return round(result, precision)

    def min_value(self, precision=0):
        if self.count() == 0:
            return None
        result = reduce(lambda x, y: x if x < y else y, self.values())
        return round(result, precision)

    def tota(self, precision=0):
        if self.count() == 0:
            return None
        result = self.sum_value()
        return round(result, precision)

    def sum_value(self, precision=0):
        if self.count() == 0:
            return None
        result = reduce(lambda x, y: x + y, self.values())
        return round(result, precision)

    def average_value(self, precision=0):
        if self.count() == 0:
            return None
        result = statistics.fmean(self.values())
        return round(result, precision)

    def median_value(self, precision=0):
        if self.count() == 0:
            return None
        result = statistics.median(self.values())
        return round(result, precision)

    def mode_value(self, precision=0):
        if self.count() == 0:
            return None
        result = statistics.mode(self.values())
        return round(result, precision)

    def print(self):
        print(self.report())

    def report(self):
        part_delimiter = '; '
        parts = []
        parts.append(self.report_part(label='count', value=self.count(), unit=None))
        parts.append(self.report_part(label='avg', value=self.average_value(precision=3), unit='s'))
        parts.append(self.report_part(label='min', value=self.min_value(precision=3), unit='s'))
        parts.append(self.report_part(label='max', value=self.max_value(precision=3), unit='s'))
        buffer = f'[{ part_delimiter.join(parts) }]'
        return buffer

    def report_part(self, label: str, value: float, unit: str):
        buffer = f'{label}='
        buffer += str(value)
        if value and unit:
            buffer += unit
        return buffer


class Event():
    _dt = None
    _value = None

    def __init__(self, dt, value):
        if not dt:
            dt = datetime.datetime.now()
        elif isinstance(dt, str):
            dt = datetime.datetime.strptime(dt, '%m/%d/%Y %H:%M:%S')
        self._dt = dt
        self._value = value

    @property
    def dt(self):
        return self._dt

    @property
    def value(self):
        return self._value

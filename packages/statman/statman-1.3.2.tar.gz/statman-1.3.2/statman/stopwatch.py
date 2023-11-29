import time
from .metric import Metric
from statman.history import History


class Stopwatch(Metric):
    _start_time = None
    _stop_time = None
    _initial_delta = None
    _read_units = 'ms'
    _history = None

    def __init__(self, name=None, autostart=False, initial_delta=None, enable_history=False):
        super().__init__(name=name)
        self.reset()
        self._initial_delta = initial_delta
        if enable_history:
            self._history = History()
        if autostart:
            self.start()

    def __str__(self):
        state = None
        name = self.name
        if not name:
            name = '(Stopwatch)'
        elapsed = self.read(precision=0, units=self._read_units)
        buffer = f'[{name} => state={state}'

        buffer += f'; elapsed={elapsed}'
        if elapsed:
            buffer += self._read_units

        if self.history:
            buffer += ' ' + self.history.report()
        return buffer

    def start(self):
        self.reset()
        self._start_time = self._now()

    def stop(self, units: str = 's', precision: int = None) -> float:
        self._stop_time = self._now()

        if self.history:
            self.history.append(value=self.value)

        return self.read(units=units, precision=precision)

    def reset(self):
        self._start_time = None
        self._stop_time = None

    def restart(self):
        self.reset()
        self.start()

    def read(self, units: str = 's', precision: int = None) -> float:
        delta = None
        if self._start_time:
            stop_time = None
            if self._stop_time:
                stop_time = self._stop_time
            else:
                stop_time = self._now()
            delta = stop_time - self._start_time

            if self._initial_delta:
                delta += self._initial_delta

            if not units is None:
                if units == 's':
                    # no conversion, already in seconds
                    pass
                elif units == 'ms':
                    delta = delta * 1000
                elif units == 'm':
                    delta = delta / 60
                else:
                    raise Exception(f'Invalid units {units}')

            if not precision is None:
                delta = round(delta, precision)
        return delta

    @property
    def history(self) -> History:
        return self._history

    @property
    def value(self) -> float:
        value = None
        if self._stop_time:
            value = self.read()
        else:
            value = None
        return value

    def _now(self):
        return time.perf_counter()

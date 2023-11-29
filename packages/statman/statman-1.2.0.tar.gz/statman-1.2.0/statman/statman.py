from .stopwatch import Stopwatch
from .gauge import Gauge
from .calculation import Calculation

_registry = {}


class Statman():

    def __init__(self):
        pass

    @staticmethod
    def reset():
        '''Clears all metrics from the registry.'''
        _registry.clear()

    @staticmethod
    def count():
        '''Returns a count of the registered metrics.'''
        return len(_registry.keys())

    @staticmethod
    def stopwatch(name: str = None, autostart: bool = False, initial_delta: float = None, enable_history=False) -> Stopwatch:
        ''' Returns a stopwatch instance.  If there is a registered stopwatch with this name, return it.  If there is no registered stopwatch with this name, create a new instance, register it, and return it. '''
        sw = Statman.get(name)

        if not sw:
            sw = Stopwatch(name=name, autostart=autostart, initial_delta=initial_delta, enable_history=enable_history)

        if not name is None:
            Statman.register(name, sw)

        return sw

    @staticmethod
    def gauge(name=None, value: float = 0) -> Gauge:
        ''' Returns a stopwatch instance.  If there is a registered stopwatch with this name, return it.  If there is no registered stopwatch with this name, create a new instance, register it, and return it. '''
        g = Statman.get(name)

        if not g:
            g = Gauge(name=name, value=value)

        if not name is None:
            Statman.register(name, g)

        return g

    @staticmethod
    def calculation(name=None, function=None) -> Calculation:
        ''' Returns a numeric calculation instance.  If there is a registered calculation with this name, return it.  If there is no registered calculation with this name, create a new instance, register it, and return it. '''
        c = Statman.get(name)

        if not c:
            c = Calculation(name=name, function=function)

        if not name is None:
            Statman.register(name, c)

        return c

    @staticmethod
    def register(name, metric):
        '''Manually register a new metric.'''
        _registry[name] = metric

    @staticmethod
    def get(name):
        metric = None
        if name:
            metric = _registry.get(name)
        return metric

    @staticmethod
    def report(output_stdout: bool = False, log_method=None):
        output = []
        report_header = 'statman metric report:'
        line_delimiter = '\n'
        prefix = '- '

        output.append(report_header)
        for metric in _registry:
            output.append(prefix + _registry.get(metric).report(output_stdout=False))

        for line in output:
            if output_stdout:
                print(line)

            if log_method:
                log_method(line)

        return line_delimiter.join(output)

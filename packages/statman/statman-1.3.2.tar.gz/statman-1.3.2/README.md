# statman

[![Python package](https://github.com/jasonray/statman-stopwatch.py/actions/workflows/python-package.yml/badge.svg)](https://github.com/jasonray/statman-stopwatch.py/actions/workflows/python-package.yml)
[![PyPI version](https://badge.fury.io/py/statman.svg)](https://badge.fury.io/py/statman)
[![Known Vulnerabilities](https://snyk.io/test/github/jasonray/statman.py/badge.svg)](https://snyk.io/test/github/jasonray/statman.py)

# Overview

Statman is a collection of metric collectors to embed within your python application.  It includes a registry to easily access your metrics.

`Statman` => registry  
`Metric` => set of classes that can perform metric collection  
`Stopwatch` => a metric class responsible for tracking time delta  
`Gauge` => a metric class responsible for providing a single value  
`Calculation` => a metric class responsible for performing calculations  
`Rate` => a specialized calculation metric which calculates x/y rate

# Install it!

Statman is availble from [pypi](https://pypi.org/project/statman/).

It can be manually installed by:
```
pip install statman
```

or by adding the following to your `requirements.txt`:
```
statman=*
```

# Use it

## Statman (Registry)

`Statman` offers a registery to make it easily to globally access metrics.  Perhaps you will create and register a stopwatch in the depths of your codebase to measure the time to write to a database, and then want to access that result in some other part of your application.

### Register
* `register(name, metric)` => manually register a new metric

### Get
* `get(name)` => get a metric by name

### Count
* `count()` => returns a count of the registered metrics.

### Reset
* `reset()` => clears all metrics from the registry.

### Specialized register / get
* `stopwatch(name)` => returns a stopwatch instance.  If there is a registered stopwatch with this name, return it.  If there is no registered stopwatch with this name, create a new instance, register it, and return it.

## Stopwatch

`Stopwatch` is for timing operations within your system.  Suppose that you are trying to track down where the system is slow.  Put a stopwatch around certain critical areas, time those operations, and compare.

### Constructor
* `Stopwatch(name=None, autostart=False, initial_delta=None)` => create an instance of a stopwatch.
  * If `autostart` set to true, the stopwatch will automatically start
  * If `initial_delta` is set to a value, and `read` of the stopwatch is incremented by this amount.  This can be helpful if you adding timings together.
  * `name` is used for to string / reporting for identification of this metric.  Defaults to blank
  * If `enable_history` is set to true, when a timing is collected (`stop` invoked), an event is collected.  This can be accessed by the `history` property to examing statistics on this stopwatch
 
### Start
* `start()` => starts the stopwatch, let the timing begin!

### Read
* `read(units, precision)` => reads the stopwatch to determine how much time has elapsed.  Returns the time elapsed in seconds.
  * The elapsed time will be returned based upon the `units` ('m' minutes, 's' seconds, 'ms', milliseconds).  Defaults to seconds.
  * If precision is provided, `read()` will round to the number of decimals places based on precision.
  * Note: `read` does NOT stop the stopwatch - if the stopwatch is runnning, it will continues to run.
* `time(units, precision)` => alias for `read()`

### Stop
* `stop(units, precision)` => stops the stopwatch, and returns the time elapsed in seconds
  * See read for the role of `units` and `precision`

### Reset
* `reset()` => restores the stopwatch back to init state and clears start and stop times

### Restart
* `restart()` => `reset`s the stopwatch, then `start`s it

### History
* `history` => if `enable_history` set during stopwatch construction, the `history` property returns an instance of a history object, which can be used for examing statistics

## Gauge

A gauge is an instantaneous measurement of a value.  Suppose that you are interested in counting the number of messages that have been processed.  A gauge can be used to count events and produce a value.

### Constructor
* `Gauge(name=None, value: float = 0)` => create an instance of a gauge
  * If `value` is provided, this will be used as the initial value of the gauge

### Value
* `value()` => get / set the current value of the gauge

### Increment / Decrement
* `increment(amount: int = 1)` => adds to the current value
* `decrement(amount: int = 1)` => subtracts from the current value

## Calculation

### Constructor
* `Calculation(name=None, function=None)` => creates a new instance of a calculation metric

#### Function
* `function` => set the function used the calculation.
  * The function is to be a parameterless function that returns a numeric value.  
  * The function can internally reference other items, such as other Statman metrics or access to other resources.  
  * The function can be a named or lambda function.

#### Value / Read
* `read(precision: int = None)` => execute the function, and returns the value rounded based on specified precision
* `value(self)` => execute the function, and returns the value

## Rate

### Constructor
* `Rate(name=None, numerator_metric_name=None, denominator_metric_name=None)` => creates a new instance of a rate metric
  * The `Rate` metric extends teh `Calculation` metric, where the function is numerator/denominator
  * The `numerator_metric_name` and `denominator_metric_name` refer to other metrics within the Statman registry

## Examples

### Maually Register Metric
``` python
from statman import Statman
Statman.register('expensive-operation-timing',Stopwatch())

stopwatch = Statman.get('expensive-operation-timing')
```

### Stopwatch via Statman Registry
``` python
from statman import Statman

Statman.stopwatch('stopwatch-name').start()
# do some expensive operation that you want to measure
Statman.stopwatch('stopwatch-name').read()

print(f'event took {Statman.stopwatch('stopwatch-name').read(precision=1)}s to execute')  # event took 1.0s to execute
```

### Stopwatch: Direct Usage (no registry)
``` python
from statman import Stopwatch
sw = Stopwatch()
sw.start()

# do some expensive operation that you want to measure

delta = sw.stop()
print(f'event took {sw.read(precision=1)}s to execute')  # event took 1.0s to execute
```

### Stopwatch: History
``` python
from statman import Stopwatch
number_of_events = 1000000

sw = Stopwatch(enable_history=True)
for i in range(0, number_of_events):
    sw.start()
    # do some expensive operation that you want to measure
    sw.stop()

print('number of measurements:', sw.history.count())
print('min:', sw.history.min_value())
print('max:', sw.history.max_value())
print('ave:', sw.history.average_value())
print('mode:', sw.history.mode_value())
```

### Gauge using increment via Statman Registry
``` python
from statman import Statman
Statman.gauge('number-of-messages-processed')

# in area where something interesting occurs, update gauge
# update can occur using .increment() or .value=
Statman.gauge('number-of-messages_processed').increment()

print('number-of-messages_processed:', Statman.gauge('number-of-messages_processed').value)
```

### Calculation via Statman Registry
``` python
from statman import Statman

Statman.calculation('messages-per-second').function = lambda: (Statman.gauge('messages-processed').value / Statman.stopwatch('sw').value)
Statman.stopwatch('time-to-process-batch').start()

# code to process batch, incrementing each time message is handles
Statman.gauge('messages-processed').increment()

Statman.stopwatch('sw').stop()

print(Statman.calculation('messages-per-second').value)
```

### Rate via Statman Registry
``` python
from statman import Statman

Statman.stopwatch('sw').start()
time.sleep(0.5)
Statman.stopwatch('sw').stop()

Statman.gauge('messages_processed').value = 100

Statman.rate(name='messages_per_second', numerator_metric_name='messages_processed', denominator_metric_name='sw')
print(Statman.rate('messages_per_second').value)
```

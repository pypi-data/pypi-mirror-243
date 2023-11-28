#### Anodot metric monitor

## Usage
- `pip install anodot-monitor`
- export ANODOT_ROLE="your_role"
- export ANODOT_TOKEN="your_token"
- export STACK="your_stack"

## Example
```python
from anodot import AnodotMetric
c = "component_name"
w = "what"
un = "hits"
uc = "test_user"

counter1 = metrics_adapter.create_counter(c, "counter_x", un, uc, a="1")
counter1.inc(3)

counter2 = metrics_adapter.create_counter(c, "counter_y", un, uc, a="2")
counter2.inc(4)

timer = metrics_adapter.create_timer(c, "timer_x", un, uc, a="3")
with timer.time():
    time.sleep(10)

meter = metrics_adapter.create_meter(c, "meter_x", un, uc, a="4")
meter.mark()

gauge = metrics_adapter.create_gauge(c, "gauge_x", un, uc, a="5")
gauge.set_value(2)

histogram = metrics_adapter.create_histogram(c, "histogram_x", un, uc, a="6")
histogram.add(5)

logtime = 0

while logtime < 1200:
    time.sleep(5)
    logtime += 5
    counter1.inc()
    counter2.inc()
    with timer.time():
        time.sleep(10)
    meter.mark()

    gauge.set_value(logtime)
    histogram.add(5)
```

Reports to monitoring environment.


### Publishing to pypi:
```shell
python setup.py sdist bdist_wheel
twine upload dist/*
```

from anodot_monitor.metric_registry import AnodotMetricsRegistry
from anodot_monitor.settings import settings
from anodot_monitor.anodot_reporter import AnodotReporter
from datetime import datetime
import time
from anodot_monitor.metric_name import MetricName
from pyformance.meters import Meter, Counter, Histogram, Timer, Gauge
import socket


class MetricsAdapter:
    def __init__(self, dc="na", customer="na", role="undefined-services", clock=None, include_server_property: bool = True):
        self._stack = settings['stack']
        self._dc = dc
        self._az = settings['aws.ses.region']
        self._role = role
        self._include_server_property = include_server_property
        self._server = socket.gethostname()
        self._customer = customer
        self._registry = AnodotMetricsRegistry()
        self.clock = clock or time
        monitoring_url = settings.get('anodot.monitoring.url')
        if monitoring_url:
            url = f"{settings['anodot.monitoring.url']}metrics"
            token = settings['anodot.monitoring.token']
            self._reporter = AnodotReporter(url=url, token=token, registry=self._registry, clock=self.clock)
        else:
            from pyformance.reporters.reporter import Reporter
            self._reporter = Reporter()
        self._reporter.start()

    def create_counter(self, component=None, what=None, unit=None, user_id=None, **properties) -> Counter:
        return self.__create_element(setter=self._registry.get_counter,
                                     component=component,
                                     what=what,
                                     unit=unit,
                                     user_id=user_id,
                                     properties=properties)

    def create_histogram(self, component=None, what=None, unit=None, user_id=None, **properties) -> Histogram:
        return self.__create_element(setter=self._registry.get_histogram,
                                     component=component,
                                     what=what,
                                     unit=unit,
                                     user_id=user_id,
                                     properties=properties)

    def create_meter(self, component=None, what=None, unit=None, user_id=None, **properties) -> Meter:
        return self.__create_element(setter=self._registry.get_meter,
                                     component=component,
                                     what=what,
                                     unit=unit,
                                     user_id=user_id,
                                     properties=properties)

    def create_gauge(self, component=None, what=None, unit=None, user_id=None, **properties) -> Gauge:
        return self.__create_element(setter=self._registry.get_gauge,
                                     component=component,
                                     what=what,
                                     unit=unit,
                                     user_id=user_id,
                                     properties=properties)

    def create_timer(self, component=None, what=None, unit=None, user_id=None, **properties) -> Timer:
        return self.__create_element(setter=self._registry.get_timer,
                                     component=component,
                                     what=what,
                                     unit=unit,
                                     user_id=user_id,
                                     properties=properties)
    
    def submit_sample(self, component=None, what=None, value:float=0, timestamp:int = None,  unit=None, user_id=None, flush:bool = True, **properties):
        timestamp = timestamp or int(round(self.clock.time()))
        metric_name = self.__get_metric_name(component=component,
                                             what=what,
                                             unit=unit,
                                             user_id=user_id,
                                             properties=properties)
        
        self._reporter.submit(name=metric_name, value=value, timestamp=timestamp, flush=flush, properties=properties)

    
    def __create_element(self, setter, component, what, unit, user_id, properties=None):
        metric_name = self.__get_metric_name(component=component,
                                             what=what,
                                             unit=unit,
                                             user_id=user_id,
                                             properties=properties)
        return setter(metric_name)

    def __get_metric_name(self, component, what, unit, user_id, properties=None):
        builder = MetricName.builder(what)\
            .with_property("stack", self._stack)\
            .with_property("dc", self._dc)\
            .with_property("az", self._az)\
            .with_property("role", self._role)\
            .with_property("component", component)\
            .with_property("unit", unit)\
            .with_property("user_id", user_id)\
            .with_property("customer", self._customer)\

        if self._include_server_property:
            builder.with_property("server", self._server)

        if properties:
            for key, value in properties.items():
                builder.with_property(key, value)

        return builder.build()


metrics_adapter = MetricsAdapter(settings["role"])

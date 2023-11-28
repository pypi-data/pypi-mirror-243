import logging
from pyformance.reporters.reporter import Reporter
import requests

logger = logging.getLogger(__name__)


class AnodotReporter(Reporter):
    def __init__(self, registry=None, reporting_interval=50, url: str = None, token: str = None, clock=None):
        super(AnodotReporter, self).__init__(
            registry=registry, reporting_interval=reporting_interval, clock=clock)
        self._url = url
        self._token = token

    @staticmethod
    def __create_metric(timestamp, value, properties, name):
        target_type = f".target_type={properties['target_type']}" if 'target_type' in properties else ''
        interval = f".interval={properties['interval']}" if 'interval' in properties else ''
        unit = f".unit={properties['unit']}" if 'unit' in properties else ''
        return {
            "properties": properties,
            "timestamp": timestamp,
            "value": value,
            "name": f"{name}{target_type}{interval}{unit}"
        }
    
    def submit(self, name, value, timestamp, flush:bool, properties):
        metric = self.__create_metric(timestamp=timestamp, value=value, properties=properties, name=name.as_string())
        metrics=[metric]
        if flush:
            rollup = 'shortRollup'
            flushInterval = 60
            end_of_bucket_timestamp = timestamp + (flushInterval - timestamp % flushInterval) % flushInterval
            flush_metric = self.__create_metric(timestamp=end_of_bucket_timestamp, value=value, properties=properties, name=name.as_string())
            flush_metric['rollup'] = rollup
            flush_metric['flush'] = True
            del flush_metric['value']
            metrics.append(flush_metric)
        
        self.__submit(metrics=metrics, timestamp=timestamp)
    
    def __submit(self, metrics,  timestamp=None):
        args = {'headers':
                {'cache-control': "no-cache", 'andt-auditlog': '{"admin":true}', 'Content-type': 'application/json'},
                'params': {'token': self._token},
                'json': metrics,
                }
        if metrics:
            try:
                response = requests.request(method='POST', url=self._url, **args)
                response.raise_for_status()
                if "errors" in response.json() and response.json()["errors"]:
                    raise Exception(response.json()["errors"])
            except Exception as e:
                logger.exception('failed to post metrics {}'.format(e))

    def report_now(self, registry=None, timestamp=None):
        metrics = self._dump_metrics(registry or self.registry, timestamp)
        self.__submit(timestamp=timestamp, metrics=metrics)
    
    def _dump_metrics(self, registry, timestamp=None):
        timestamp = timestamp or int(round(self.clock.time()))

        metrics = self._collect_metrics(registry.get_counters(), timestamp)
        metrics += self._collect_metrics(registry.get_gauges(), timestamp)
        metrics += self._collect_metrics(registry.get_timers(), timestamp)
        metrics += self._collect_metrics(registry.get_meters(), timestamp)
        metrics += self._collect_metrics(registry.get_histograms(), timestamp)

        return metrics

    def _collect_metrics(self, metrics, timestamp=None):
        result = []
        for metric in metrics:
            metric_name = self.registry.get_metric_name(metric['metric_key'])
            # add all properties from metric name
            for key, value in metric_name.properties():
                metric['properties'].setdefault(key,  value)

            result.append(self.__create_metric(timestamp=timestamp,
                                               value=metric['value'],
                                               properties=metric['properties'],
                                               name=metric_name.as_string())
                          )
        return result
    

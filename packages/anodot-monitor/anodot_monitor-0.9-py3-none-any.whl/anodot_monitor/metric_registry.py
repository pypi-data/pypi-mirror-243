from pyformance import MetricsRegistry


class AnodotMetricsRegistry(MetricsRegistry):
    def __init__(self):
        super(AnodotMetricsRegistry, self).__init__()
        self._metric_names = {}

    def get_timer(self, metric_name):
        key = self.__set_metric_name(metric_name)
        return self.timer(key)

    def get_counter(self, metric_name):
        key = self.__set_metric_name(metric_name)
        return self.counter(key)

    def get_meter(self, metric_name):
        key = self.__set_metric_name(metric_name)
        return self.meter(key)

    def get_histogram(self, metric_name):
        key = self.__set_metric_name(metric_name)
        return self.histogram(key)

    def get_gauge(self, metric_name):
        key = self.__set_metric_name(metric_name)
        return self.gauge(key)

    def __set_metric_name(self, metric_name):
        metric_key = metric_name.as_string()
        if metric_key not in self._metric_names:
            self._metric_names[metric_key] = metric_name

        return metric_key

    def get_metric_name(self, key):
        if not self._metric_names:
            return None
        else:
            return self._metric_names[key]

    def get_counters(self):
        result = []
        for metric_key in self._counters.keys():
            result.append({
                'metric_key': metric_key,
                'target_type': 'gauge',
                'value': self._counters[metric_key].get_count(),
                'properties': {
                    'target_type': 'counter'
                }
            })
        return result

    def get_gauges(self):
        result = []
        for metric_key in self._gauges.keys():
            result.append({
                'metric_key': metric_key,
                'target_type': 'gauge',
                'value': self._gauges[metric_key].get_value(),
                'properties': {
                    'target_type': 'gauge'
                }
            })
        return result

    def get_histograms(self):
        result = []
        for metric_key in self._histograms.keys():
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_count(),
                'properties': {'target_type': 'counter'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_max(),
                'properties': {'target_type': 'gauge', 'stat': 'max'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_mean(),
                'properties': {'target_type': 'gauge', 'stat': 'mean'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_min(),
                'properties': {'target_type': 'gauge', 'stat': 'min'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_stddev(),
                'properties': {'target_type': 'gauge', 'stat': 'std'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_snapshot().get_median(),
                'properties': {'target_type': 'gauge', 'stat': 'p50'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_snapshot().get_75th_percentile(),
                'properties': {'target_type': 'gauge', 'stat': 'p75'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_snapshot().get_95th_percentile(),
                'properties': {'target_type': 'gauge', 'stat': 'p95'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_snapshot().get_percentile(0.98),
                'properties': {'target_type': 'gauge', 'stat': 'p98'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_snapshot().get_99th_percentile(),
                'properties': {'target_type': 'gauge', 'stat': 'p99'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._histograms[metric_key].get_snapshot().get_999th_percentile(),
                'properties': {'target_type': 'gauge', 'stat': 'p999'}})
        return result

    def get_meters(self):
        result = []
        for metric_key in self._meters.keys():
            metric_name = self.get_metric_name(metric_key)

            if 'unit' not in metric_name.properties():
                unit = 'hits_per_S'
            else:
                unit = metric_name.properties()['unit'] + '_per_S'

            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._meters[metric_key].get_count(),
                'properties': {'target_type': 'counter'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'rate',
                'value': self._meters[metric_key].get_count(),
                'properties': {'target_type': 'rate', 'interval': 'last_1m', 'unit': unit}})
            result.append({
                'metric_key': metric_key, 'target_type': 'rate',
                'value': self._meters[metric_key].get_five_minute_rate(),
                'properties': {'target_type': 'rate', 'interval': 'last_5m', 'unit': unit}})
            result.append({
                'metric_key': metric_key, 'target_type': 'rate',
                'value': self._meters[metric_key].get_fifteen_minute_rate(),
                'properties': {'target_type': 'rate', 'interval': 'last_15m', 'unit': unit}})
            result.append({
                'metric_key': metric_key, 'target_type': 'rate',
                'value': self._meters[metric_key].get_mean_rate(),
                'properties': {'target_type': 'rate', 'interval': 'mean', 'unit': unit}})
        return result

    def get_timers(self):
        result = []
        for metric_key in self._timers.keys():
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_max(),
                'properties': {'target_type': 'rate', 'stat': 'max', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_mean(),
                'properties': {'target_type': 'rate', 'stat': 'mean', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_min(),
                'properties': {'target_type': 'rate', 'stat': 'min', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_stddev(),
                'properties': {'target_type': 'rate', 'stat': 'std', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_snapshot().get_median(),
                'properties': {'target_type': 'rate', 'stat': 'p50', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_snapshot().get_75th_percentile(),
                'properties': {'target_type': 'rate', 'stat': 'p75', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_snapshot().get_95th_percentile(),
                'properties': {'target_type': 'rate', 'stat': 'p95', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_snapshot().get_percentile(0.98),
                'properties': {'target_type': 'rate', 'stat': 'p98', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_snapshot().get_99th_percentile(),
                'properties': {'target_type': 'rate', 'stat': 'p99', 'unit': 'm'}})
            result.append({
                'metric_key': metric_key, 'target_type': 'gauge',
                'value': self._timers[metric_key].get_snapshot().get_999th_percentile(),
                'properties': {'target_type': 'rate', 'stat': 'p999', 'unit': 'm'}})

        return result

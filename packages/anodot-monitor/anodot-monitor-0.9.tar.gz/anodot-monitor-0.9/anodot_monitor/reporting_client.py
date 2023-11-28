import logging
import requests
import more_itertools
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ReportingClient:
    monitoring_url: str
    token: str
    max_samples_per_query: int = 1000

    def send_metrics(self, metrics):
        for chunk in more_itertools.chunked(metrics, self.max_samples_per_query):
            rsp = requests.post(url=self.monitoring_url,
                                params={"token": self.token, "protocol": "anodot20"},
                                json=chunk)
            rsp.raise_for_status()


from anodot_monitor.settings import settings

metrics_reporting_client = ReportingClient(
    monitoring_url=settings['anodotd.monitoring.url'] + 'metrics',
    token=settings['anodotd.monitoring.token'],
)

import socket
from anodot_monitor.settings import settings

BASE_PROPERTIES = dict(
    dc="na",
    az=settings['aws.ses.region'],
    server=socket.gethostname(),
    role="na",
    stack=settings['stack'],
)


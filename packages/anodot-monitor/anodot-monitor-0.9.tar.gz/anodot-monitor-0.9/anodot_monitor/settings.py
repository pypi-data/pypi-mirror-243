import os

settings = {
    "stack": os.getenv("STACK", "dev"),
    "anodot.monitoring.url": os.getenv("ANODOT_URL", "https://app-monitoring.anodot.com/api/v1/"),
    "anodot.monitoring.token": os.getenv("ANODOT_TOKEN"),
    "aws.ses.region": os.getenv("SES_REGION", "us-east-1"),
    "role": os.getenv("ANODOT_ROLE"),
}

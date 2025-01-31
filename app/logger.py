import logging
from datetime import datetime, timezone

from pythonjsonlogger.json import JsonFormatter

from app.config import settings

logger = logging.getLogger()

logHandler = logging.StreamHandler()


class CustomJsonFomatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get("timestamp"):
            now = datetime.now(timezone.utc).strftime("%H:%M")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname
        return


formatter = CustomJsonFomatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)

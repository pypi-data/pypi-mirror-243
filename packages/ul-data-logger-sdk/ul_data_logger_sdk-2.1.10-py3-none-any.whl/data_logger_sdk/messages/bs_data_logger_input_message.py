from enum import Enum
from typing import Optional, Any, Dict
from unipipeline.message.uni_message import UniMessage


class BsLogType(Enum):
    device_data = "device_data"
    heartbit = "heartbit"


class BsDataLoggerInputV0Message(UniMessage):
    latitude: float
    longitude: float
    soft: Optional[str]
    station_id: int
    time: float
    log_type: Optional[BsLogType]
    init_message: Optional[Dict[str, Any]]

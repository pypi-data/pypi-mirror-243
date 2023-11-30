from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict, Union

from unipipeline.message.uni_message import UniMessage


class UniversalApiType(Enum):
    USPD = 'USPD'
    GENERAL_API = 'GENERAL_API'


class UniversalApiDataLoggerInputV0Message(UniMessage):
    name: str
    type: UniversalApiType
    geo_latitude: float
    geo_longitude: float
    soft: Optional[str]
    note: Optional[str]
    ipv4: Optional[str]
    current_dt: datetime
    uptime_s: int
    raw_message: Union[str, Dict[str, Any]]

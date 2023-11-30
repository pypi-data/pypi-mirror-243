from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel
from unipipeline.message.uni_message import UniMessage


class DataNbfi(BaseModel):
    mac: int
    f_ask: bool
    iterator: int
    multi: bool
    system: bool
    payload: str


class DataUnbp(BaseModel):
    mac: int
    ack: bool
    iterator: int
    payload: str


class DataUnbp2(BaseModel):
    mac: int
    payload: str


class SdrInfo(BaseModel):
    freq: int
    freq_channel: int
    sdr: int
    baud_rate: int
    rssi: int
    snr: int


class DevicePackageNetworkTypeEnum(Enum):
    downlink = 'downlink'
    uplink = 'uplink'


class DevicePackageProtocolTypeEnum(Enum):
    nbfi = 'nbfi'
    unbp = 'unbp'
    unbp2 = 'unbp2'


class DevicePackage(BaseModel):
    footprint: Optional[str] = None
    dt: datetime
    raw: str
    type: DevicePackageNetworkTypeEnum
    protocol: DevicePackageProtocolTypeEnum
    data_nbfi: Optional[DataNbfi]
    data_unbp: Optional[DataUnbp]
    data_unbp2: Optional[DataUnbp2]
    sdr_info: Optional[SdrInfo]


class BaseStationEnvironmentInfo(BaseModel):
    dt: datetime
    spectrum: List[float]
    sdr: int
    freq_carrier: float
    freq_delta: float


class BaseStationInfoGeo(BaseModel):
    dt: datetime
    longitude: float
    latitude: float
    actual: bool


class BaseStationInfo(BaseModel):
    geo: BaseStationInfoGeo
    uptime_s: int


class BaseStationAdditionalInfo(BaseModel):
    id: int  # SERIAL NUMBER
    version: Optional[str]


class BaseStationLogsTypeEnum(Enum):
    emerg = 'emerg'
    alert = 'alert'
    critical = 'critical'
    error = 'error'
    warning = 'warning'
    notice = 'notice'
    debug = 'debug'
    info = 'info'


class BaseStationLogs(BaseModel):
    type: BaseStationLogsTypeEnum
    mdl: Optional[str]
    dt: datetime
    text: str


class HttpNeroBsPacketV0Message(UniMessage):
    data: List[DevicePackage]
    base_station_environment_info: Optional[List[BaseStationEnvironmentInfo]]
    base_station_info: BaseStationInfo
    base_station_additional_info: BaseStationAdditionalInfo
    base_station_logs: Optional[List[BaseStationLogs]]

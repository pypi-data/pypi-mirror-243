from pydantic import BaseModel
from typing import Optional, List
from .region_alarm_model import RegionAlarmModel


class RegionAlarmsHistory(BaseModel):
    regionId: Optional[str]
    regionName: Optional[str]
    alarms: Optional[List[RegionAlarmModel]]

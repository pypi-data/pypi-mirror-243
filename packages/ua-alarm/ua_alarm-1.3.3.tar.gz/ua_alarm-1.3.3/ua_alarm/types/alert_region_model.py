from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .alert import Alert
from ..enums import v2RegionType


class AlertRegionModel(BaseModel):
    regionId: Optional[str]
    regionType: v2RegionType
    regionName: Optional[str]
    regionEngName: Optional[str]
    lastUpdate: datetime
    activeAlerts: Optional[List[Alert]]

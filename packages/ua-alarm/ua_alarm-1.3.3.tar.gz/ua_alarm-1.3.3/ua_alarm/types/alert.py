from pydantic import BaseModel
from datetime import datetime
from ..enums import AlertType, v2RegionType


class Alert(BaseModel):
    regionId: str
    regionType: v2RegionType
    type: AlertType
    lastUpdate: datetime

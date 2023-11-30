from pydantic import BaseModel
from typing import Optional, List, Union
from ..enums import v2RegionType


class RegionChildModel(BaseModel):
    regionId: str
    regionName: str
    regionType: v2RegionType


class RegionViewModel(BaseModel):
    regionId: Optional[str]
    regionName: Optional[str]
    regionType: v2RegionType
    regionChildIds: Optional[List[Union["RegionViewModel", RegionChildModel]]]

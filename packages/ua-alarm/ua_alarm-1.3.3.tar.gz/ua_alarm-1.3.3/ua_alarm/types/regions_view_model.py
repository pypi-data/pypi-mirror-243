from pydantic import BaseModel
from typing import Optional, List
from .region_view_model import RegionViewModel


class RegionsViewModel(BaseModel):
    states: Optional[List[RegionViewModel]]

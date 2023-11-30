from pydantic import BaseModel
from typing import Optional


class WebHook(BaseModel):
    webHookUrl: Optional[str]

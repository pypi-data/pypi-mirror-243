from pydantic import BaseModel


class AlertModification(BaseModel):
    lastActionIndex: int

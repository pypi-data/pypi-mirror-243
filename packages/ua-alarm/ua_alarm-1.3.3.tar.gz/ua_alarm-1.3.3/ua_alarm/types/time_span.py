from pydantic import BaseModel


class TimeSpan(BaseModel):
    ticks: int
    days: int
    hours: int
    milliseconds: int
    minutes: int
    seconds: int
    totalDays: float
    totalHours: float
    totalMilliseconds: float
    totalMinutes: float
    totalSeconds: float

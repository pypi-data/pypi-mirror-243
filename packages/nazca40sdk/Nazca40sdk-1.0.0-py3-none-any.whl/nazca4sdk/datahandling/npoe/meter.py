from pydantic import BaseModel


class Meter(BaseModel):
    connectionId: str
    meterDeviceId: str
    id: str
    systemName: str
    name: str
    active: bool

from typing import List

from pydantic import BaseModel


class BootProfileMeter(BaseModel):
    id: str
    systemName: str


class BootProfile(BaseModel):
    id: str
    name: str
    startTime: str
    recorded: bool
    isActive: bool
    meters: List[BootProfileMeter]


class BootProfiles(BaseModel):
    __root__: List[BootProfile]

    def boot_profiles(self):
        return self.__root__

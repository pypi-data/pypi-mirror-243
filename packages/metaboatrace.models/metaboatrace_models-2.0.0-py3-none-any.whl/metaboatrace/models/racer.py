from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, StrictInt

from .region import Branch, Prefecture


class Gender(Enum):
    MALE = 1
    FEMALE = 2


class RacerRank(Enum):
    A1 = 1
    A2 = 2
    B1 = 3
    B2 = 4

    @classmethod
    def from_string(cls, s: str) -> "RacerRank":
        return cls.__members__[s]


class Racer(BaseModel):
    registration_number: StrictInt
    last_name: str
    first_name: str = ""
    gender: Optional[Gender] = None
    term: Optional[StrictInt] = None
    birth_date: Optional[date] = None
    height: Optional[StrictInt] = None
    born_prefecture: Optional[Prefecture] = None
    branch: Optional[Branch] = None
    current_rating: Optional[RacerRank] = None


class RacerCondition(BaseModel):
    recorded_on: date
    racer_registration_number: StrictInt
    weight: float
    adjust: float

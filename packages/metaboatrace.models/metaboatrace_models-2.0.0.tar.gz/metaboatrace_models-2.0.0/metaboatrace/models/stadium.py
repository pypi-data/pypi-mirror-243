from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, StrictInt


class StadiumTelCode(Enum):
    KIRYU = 1
    TODA = 2
    EDOGAWA = 3
    HEIWAJIMA = 4
    TAMAGAWA = 5
    HAMANAKO = 6
    GAMAGORI = 7
    TOKONAME = 8
    TSU = 9
    MIKUNI = 10
    BIWAKO = 11
    SUMINOE = 12
    AMAGASAKI = 13
    NARUTO = 14
    MARUGAME = 15
    KOJIMA = 16
    MIYAJIMA = 17
    TOKUYAMA = 18
    SHIMONOSEKI = 19
    WAKAMATSU = 20
    ASHIYA = 21
    FUKUOKA = 22
    KARATSU = 23
    OMURA = 24


class SeriesGrade(Enum):
    SG = 1
    G1 = 2
    G2 = 3
    G3 = 4
    NO_GRADE = 5

    @classmethod
    def from_string(cls, s: str) -> "SeriesGrade":
        return cls.__members__[s]


class SeriesKind(Enum):
    UNCATEGORIZED = 1
    ALL_LADIES = 2
    VENUS = 3
    ROOKIE = 4
    SENIOR = 5
    DOUBLE_WINNER = 6
    TOURNAMENT = 7


class Event(BaseModel):
    stadium_tel_code: StadiumTelCode
    starts_on: date
    days: StrictInt = Field(..., ge=3, le=7)
    grade: SeriesGrade
    kind: SeriesKind
    title: str


class MotorRenewal(BaseModel):
    stadium_tel_code: StadiumTelCode
    date: date

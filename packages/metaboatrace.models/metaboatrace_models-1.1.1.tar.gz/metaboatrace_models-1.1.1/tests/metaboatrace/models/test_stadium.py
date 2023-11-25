from datetime import date

import pytest
from pydantic import ValidationError

from metaboatrace.models.stadium import Event, SeriesGrade, SeriesKind, StadiumTelCode


@pytest.mark.parametrize(
    "stadium_tel_code,starts_on,days,grade,kind,title,expected",
    [
        (
            StadiumTelCode.KIRYU,
            date.today(),
            5,
            SeriesGrade.SG,
            SeriesKind.ALL_LADIES,
            "Test Event",
            True,
        ),  # valid case
        (
            StadiumTelCode.KIRYU,
            date.today(),
            2,
            SeriesGrade.SG,
            SeriesKind.ALL_LADIES,
            "Test Event",
            False,
        ),  # invalid days
        (
            StadiumTelCode.KIRYU,
            date.today(),
            8,
            SeriesGrade.SG,
            SeriesKind.ALL_LADIES,
            "Test Event",
            False,
        ),  # invalid days
    ],
)
def test_event(stadium_tel_code, starts_on, days, grade, kind, title, expected):  # type: ignore
    data = {
        "stadium_tel_code": stadium_tel_code,
        "starts_on": starts_on,
        "days": days,
        "grade": grade,
        "kind": kind,
        "title": title,
    }
    if expected:
        Event(**data)
    else:
        with pytest.raises(ValidationError):
            Event(**data)

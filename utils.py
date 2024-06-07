from datetime import datetime


def get_date(year=None, month=None, day=None, date=None):

    if any((year is not None, month is not None, day is not None, date is not None)):

        if year is not None:
            assert isinstance(year, int)
            assert month is not None
            assert day is not None
            assert date is None

        if month is not None:
            assert isinstance(month, int)
            assert year is not None
            assert day is not None
            assert date is None

        if day is not None:
            assert isinstance(day, int)
            assert year is not None
            assert month is not None
            assert date is None

        if date is not None:
            assert isinstance(date, datetime)
            assert year is None
            assert month is None
            assert day is None

        _date = date if date is not None else datetime(year, month, day)
    else:
        _date = None

    return _date


def day_suffix(day):
    assert isinstance(day, int)
    assert 1 <= day <= 31

    return {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 20, 'th')


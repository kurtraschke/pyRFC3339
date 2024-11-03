import re
from datetime import datetime, timedelta, timezone

from pyrfc3339.utils import format_timezone


def parse(timestamp, utc=False, produce_naive=False):
    """
    Parse an :RFC:`3339`-formatted timestamp and return a
    :class:`datetime.datetime`.

    If the timestamp is presented in UTC, then the `tzinfo` parameter of the
    returned `datetime` will be set to :attr:`datetime.timezone.utc`.

    >>> parse('2009-01-01T10:01:02Z')
    datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=datetime.timezone.utc)

    Otherwise, a :class:`datetime.timezone` instance is created with the appropriate offset, and
    the `tzinfo` parameter of the returned `datetime` is set to that value.

    >>> parse('2009-01-01T14:01:02-04:00')
    datetime.datetime(2009, 1, 1, 14, 1, 2, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000), '<UTC-04:00>'))

    However, if `parse()`  is called with `utc=True`, then the returned
    `datetime` will be normalized to UTC (and its tzinfo parameter set to
    `datetime.timezone.utc`), regardless of the input timezone.

    >>> parse('2009-01-01T06:01:02-04:00', utc=True)
    datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=datetime.timezone.utc)

    The input is strictly required to conform to :RFC:`3339`, and appropriate
    exceptions are thrown for invalid input.

    >>> parse('2009-01-01T06:01:02')
    Traceback (most recent call last):
    ...
    ValueError: timestamp does not conform to RFC 3339

    >>> parse('2009-01-01T25:01:02Z')
    Traceback (most recent call last):
    ...
    ValueError: hour must be in 0..23

    """

    parse_re = re.compile(
        r"""^(?:(?:(?P<date_fullyear>[0-9]{4})\-(?P<date_month>[0-9]{2})\-(?P<date_mday>[0-9]{2}))T(?:(?:(?P<time_hour>[0-9]{2})\:(?P<time_minute>[0-9]{2})\:(?P<time_second>[0-9]{2})(?P<time_secfrac>(?:\.[0-9]{1,}))?)(?P<time_offset>(?:Z|(?P<time_numoffset>(?P<time_houroffset>(?:\+|\-)[0-9]{2})\:(?P<time_minuteoffset>[0-9]{2}))))))$""",
        re.I | re.X,
    )

    match = parse_re.match(timestamp)

    if match is not None:
        if match.group("time_offset") in ["Z", "z", "+00:00", "-00:00"]:
            if produce_naive is True:
                tzinfo = None
            else:
                tzinfo = timezone.utc
        else:
            if produce_naive is True:
                raise ValueError(
                    "cannot produce a naive datetime from a local timestamp"
                )
            else:
                tz_hours = int(match.group("time_houroffset"))
                tz_minutes = int(match.group("time_minuteoffset"))
                if tz_hours < 0:
                    tz_minutes *= -1
                td = timedelta(hours=tz_hours, minutes=tz_minutes)
                tzinfo = timezone(td, f"<UTC{format_timezone(td.total_seconds())}>")

        secfrac = match.group("time_secfrac")
        if secfrac is None:
            microsecond = 0
        else:
            microsecond = int(round(float(secfrac) * 1000000))

        dt_out = datetime(
            year=int(match.group("date_fullyear")),
            month=int(match.group("date_month")),
            day=int(match.group("date_mday")),
            hour=int(match.group("time_hour")),
            minute=int(match.group("time_minute")),
            second=int(match.group("time_second")),
            microsecond=microsecond,
            tzinfo=tzinfo,
        )

        if utc:
            dt_out = dt_out.astimezone(timezone.utc)

        return dt_out
    else:
        raise ValueError("timestamp does not conform to RFC 3339")

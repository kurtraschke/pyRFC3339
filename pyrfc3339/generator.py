import datetime

from pyrfc3339.utils import format_timezone


def generate(dt, utc=True, accept_naive=False, microseconds=False):
    """
    Generate an :RFC:`3339`-formatted timestamp from a
    :class:`datetime.datetime`.

    >>> from datetime import datetime, timezone
    >>> from zoneinfo import ZoneInfo
    >>> generate(datetime(2009,1,1,12,59,59,0,timezone.utc))
    '2009-01-01T12:59:59Z'

    The timestamp will use UTC unless `utc=False` is specified, in which case
    it will use the timezone from the :class:`datetime.datetime`'s
    :attr:`tzinfo` parameter.

    >>> eastern = ZoneInfo('US/Eastern')
    >>> dt = datetime(2009,1,1,12,59,59, tzinfo=eastern)
    >>> generate(dt)
    '2009-01-01T17:59:59Z'
    >>> generate(dt, utc=False)
    '2009-01-01T12:59:59-05:00'

    Unless `accept_naive=True` is specified, the `datetime` must not be naive.

    >>> generate(datetime(2009,1,1,12,59,59,0))
    Traceback (most recent call last):
    ...
    ValueError: naive datetime and accept_naive is False

    >>> generate(datetime(2009,1,1,12,59,59,0), accept_naive=True)
    '2009-01-01T12:59:59Z'

    If `accept_naive=True` is specified, the `datetime` is assumed to be UTC.
    Attempting to generate a local timestamp from a naive datetime will result
    in an error.

    >>> generate(datetime(2009,1,1,12,59,59,0), accept_naive=True, utc=False)
    Traceback (most recent call last):
    ...
    ValueError: cannot generate a local timestamp from a naive datetime

    """

    if dt.tzinfo is None:
        if accept_naive is True:
            if utc is True:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            else:
                raise ValueError("cannot generate a local timestamp from " +
                                 "a naive datetime")
        else:
            raise ValueError("naive datetime and accept_naive is False")

    if utc is True:
        dt = dt.astimezone(datetime.timezone.utc)

    timestamp = dt.strftime('%Y-%m-%dT%H:%M:%S')
    if microseconds is True:
        timestamp += dt.strftime('.%f')
    if dt.tzinfo is datetime.timezone.utc:
        timestamp += 'Z'
    else:
        timestamp += format_timezone(dt.tzinfo.utcoffset(dt).total_seconds())

    return timestamp

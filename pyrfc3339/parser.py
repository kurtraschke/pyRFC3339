from datetime import UTC, datetime


def parse(timestamp: str, utc: bool = False, produce_naive: bool = False) -> datetime:
    """
    Parse an :RFC:`3339`-formatted timestamp and return a :class:`datetime.datetime`.

    If the timestamp is presented in UTC, then the :attr:`~datetime.datetime.tzinfo` attribute of the
    returned `datetime` will be set to :attr:`datetime.timezone.utc`.

    >>> parse('2009-01-01T10:01:02Z')
    datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=datetime.timezone.utc)

    Otherwise, a :class:`datetime.timezone` instance is created with the appropriate offset, and
    the :attr:`~datetime.datetime.tzinfo` attribute of the returned :class:`~datetime.datetime` is set to that value.

    >>> parse('2009-01-01T14:01:02-04:00')
    datetime.datetime(2009, 1, 1, 14, 1, 2, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))

    However, if :meth:`parse()`  is called with :python:`utc=True`, then the returned
    :class:`~datetime.datetime` will be normalized to UTC (and its :attr:`~datetime.datetime.tzinfo` attribute set to
    :attr:`~datetime.timezone.utc`), regardless of the input timezone.

    >>> parse('2009-01-01T06:01:02-04:00', utc=True)
    datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=datetime.timezone.utc)

    If :meth:`parse()` is called with :python:`produce_naive=True`, then the returned
    :class:`~datetime.datetime` will be naive (and its :attr:`~datetime.datetime.tzinfo` attribute set to
    :python:`None`). This is not permitted for input timestamps which have a non-zero timezone offset, unless those
    are normalized to UTC with the use of :python:`utc=True`.
    The use of naive datetimes, is, as a matter of course, not recommended.

    >>> parse('2009-01-01T06:01:02Z', produce_naive=True)
    datetime.datetime(2009, 1, 1, 6, 1, 2)

    >>> parse('2009-01-01T06:01:02+00:00', produce_naive=True)
    datetime.datetime(2009, 1, 1, 6, 1, 2)

    >>> parse('2009-01-01T06:01:02-00:00', produce_naive=True)
    datetime.datetime(2009, 1, 1, 6, 1, 2)

    >>> parse('2009-01-01T06:01:02-04:00', produce_naive=True) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: cannot produce a naive datetime from a local timestamp

    >>> parse('2009-01-01T06:01:02-04:00', utc=True, produce_naive=True)
    datetime.datetime(2009, 1, 1, 10, 1, 2)

    As parsing is delegated to :meth:`datetime.datetime.fromisoformat()`, certain
    timestamps which do not strictly adhere to :RFC:`3339` are nonetheless accepted.

    >>> parse('2009-01-01T06:01:02')
    datetime.datetime(2009, 1, 1, 6, 1, 2)

    Exceptions will, however, be thrown for blatantly invalid input:

    >>> parse('2009-01-01T25:01:02Z') # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    ValueError: hour must be in 0..23

    :param str timestamp: the :RFC:`3339` timestamp to be parsed
    :param bool utc: :const:`True` to normalize the timestamp to UTC; :const:`False` otherwise. Defaults to :const:`False`.
    :param bool produce_naive: :const:`True` if the produced :class:`~datetime.datetime` instance should
                               not have a timezone attached (that is, be 'naive'); :const:`False` otherwise.
                               Defaults to :const:`False`. Not permitted for input timestamps which have
                               a non-zero timezone offset.
    :return: the parsed timestamp
    :rtype: datetime.datetime

    """

    # Python only recognizes the 'Z' suffix, not 'z'. (python/cpython#80010)
    if timestamp.endswith("z"):
        timestamp = timestamp[:-1] + "Z"

    dt_out = datetime.fromisoformat(timestamp)

    if utc:
        dt_out = dt_out.astimezone(UTC)

    if produce_naive:
        if dt_out.tzinfo == UTC:
            dt_out = dt_out.replace(tzinfo=None)
        else:
            raise ValueError("cannot produce a naive datetime from a local timestamp")

    return dt_out

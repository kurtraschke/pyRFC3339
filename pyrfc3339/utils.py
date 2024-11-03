def format_timezone(utcoffset):
    """
    Return a string representing the timezone offset.
    Remaining seconds are rounded to the nearest minute.

    >>> format_timezone(3600)
    '+01:00'
    >>> format_timezone(5400)
    '+01:30'
    >>> format_timezone(-28800)
    '-08:00'

    """

    hours, seconds = divmod(abs(utcoffset), 3600)
    minutes = round(float(seconds) / 60)

    if utcoffset >= 0:
        sign = "+"
    else:
        sign = "-"
    return "{0}{1:02d}:{2:02d}".format(sign, int(hours), int(minutes))

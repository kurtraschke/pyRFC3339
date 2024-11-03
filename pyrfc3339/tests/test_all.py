"""
Test suite for pyRFC3339.

"""

import unittest
import zoneinfo
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from pyrfc3339 import generate, parse


class TestCore(unittest.TestCase):
    """
    This test suite contains tests to address cases not tested in the doctests,
    as well as additional tests for end-to-end verification.

    """

    def test_zero_offset(self):
        """
        Both +00:00 and -00:00 are equivalent to the offset 'Z' (UTC).

        """
        timestamp = "2009-01-01T10:02:03+00:00"
        dt = parse(timestamp)
        self.assertEqual(dt.tzinfo, timezone.utc)

        timestamp = "2009-01-01T10:02:03-00:00"
        dt = parse(timestamp)
        self.assertEqual(dt.tzinfo, timezone.utc)

    def test_parse_microseconds(self):
        """
        Test parsing timestamps with microseconds.

        """
        timestamp = "2009-01-01T10:02:03.25Z"
        dt = parse(timestamp)
        self.assertEqual(dt.microsecond, 250000)

    def test_generate_microseconds(self):
        """
        Test generating timestamps with microseconds.

        """
        dt = datetime(2009, 1, 1, 10, 2, 3, 500000, tzinfo=timezone.utc)
        timestamp = generate(dt, microseconds=True)
        self.assertEqual(timestamp, "2009-01-01T10:02:03.500000Z")

    def test_mixed_case(self):
        """
        Timestamps may use either 'T' or 't' and either 'Z' or 'z'
        according to :RFC:`3339`.

        """
        dt1 = parse("2009-01-01t10:01:02z")
        dt2 = datetime(2009, 1, 1, 10, 1, 2, tzinfo=timezone.utc)

        self.assertEqual(dt1, dt2)

    def test_parse_naive_utc(self):
        """
        Test parsing a UTC timestamp to a naive datetime.

        """
        dt1 = parse("2009-01-01T10:01:02Z", produce_naive=True)
        self.assertEqual(dt1.tzinfo, None)

    def test_parse_naive_local(self):
        """
        Test that parsing a local timestamp to a naive datetime fails.

        """
        with self.assertRaises(ValueError):
            parse("2009-01-01T10:01:02-04:00", produce_naive=True)

    def test_generate_utc_parse_utc(self):
        """
        Generate a UTC timestamp and parse it into a UTC datetime.

        """
        dt1 = datetime.now(timezone.utc)

        dt2 = parse(generate(dt1, microseconds=True))
        self.assertEqual(dt1, dt2)

    def test_generate_local_parse_local(self):
        """
        Generate a local timestamp and parse it into a local datetime.

        """
        eastern = ZoneInfo("US/Eastern")
        dt1 = datetime.now(eastern)
        dt2 = parse(generate(dt1, utc=False, microseconds=True), utc=False)
        self.assertEqual(dt1, dt2)

    def test_generate_local_parse_utc(self):
        """
        Generate a local timestamp and parse it into a UTC datetime.

        """
        eastern = ZoneInfo("US/Eastern")
        dt1 = datetime.now(eastern)
        dt2 = parse(generate(dt1, utc=False, microseconds=True))
        self.assertEqual(dt1, dt2)

    @unittest.skip("fails due to python/cpython#120713")
    def test_three_digit_year(self):
        dt = datetime(999, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(generate(dt), "0999-01-01T00:00:00Z")


class TestExhaustiveRoundtrip(unittest.TestCase):
    """
    This test suite exhaustively tests parsing and generation by generating
    a local RFC 3339 timestamp for every timezone supported by `zoneinfo`,
    and parsing that timestamp into a local datetime and a UTC datetime.
    """

    def test_local_roundtrip(self):
        """
        Generates a local datetime using the given timezone,
        produces a local timestamp from the datetime, parses the timestamp
        to a local datetime, and verifies that the two datetimes are equal.

        """
        for tz_name in zoneinfo.available_timezones():
            with self.subTest(tz=tz_name):
                tzinfo = ZoneInfo(tz_name)
                dt1 = datetime.now(tzinfo)
                timestamp = generate(dt1, utc=False, microseconds=True)
                dt2 = parse(timestamp, utc=False)
                self.assertEqual(dt1, dt2)

    def test_utc_roundtrip(self):
        """
        Generates a local datetime using the given timezone,
        produces a local timestamp from the datetime, parses the timestamp
        to a UTC datetime, and verifies that the two datetimes are equal.

        """
        for tz_name in zoneinfo.available_timezones():
            with self.subTest(tz=tz_name):
                tzinfo = ZoneInfo(tz_name)
                dt1 = datetime.now(tzinfo)
                timestamp = generate(dt1, utc=False, microseconds=True)
                dt2 = parse(timestamp)
                self.assertEqual(dt1, dt2)

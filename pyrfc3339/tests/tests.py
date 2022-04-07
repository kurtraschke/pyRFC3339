'''
Test suite for pyRFC3339.

'''

from datetime import datetime
from copy import deepcopy

from pyrfc3339 import generate, parse
from pyrfc3339.utils import timezone
import unittest
import pytest
import pytz

class TestCore(unittest.TestCase):
    '''
    This test suite contains tests to address cases not tested in the doctests,
    as well as additional tests for end-to-end verification.

    '''
    def test_timezone_rounding(self):
        '''
        Test rounding of timezone values to the nearest second.

        '''
        if not timezone(5429) == '+01:30':
            raise AssertionError("%r != %r" % (timezone(5429), '+01:30'))

        if not timezone(5431) == '+01:31':
            raise AssertionError("%r != %r" % (timezone(5431), '+01:31'))

    def test_zero_offset(self):
        '''
        Both +00:00 and -00:00 are equivalent to the offset 'Z' (UTC).

        '''
        timestamp = '2009-01-01T10:02:03+00:00'
        dt = parse(timestamp)
        if not dt.tzinfo == pytz.utc:
            raise AssertionError("%r != %r" % (dt.tzinfo, pytz.utc))

        timestamp = '2009-01-01T10:02:03-00:00'
        dt = parse(timestamp)
        if not dt.tzinfo == pytz.utc:
            raise AssertionError("%r != %r" % (dt.tzinfo, pytz.utc))

    def test_deepcopy(self):
        '''
        Tests that deepcopy works and doesn't crash

        '''
        timestamp = '2009-01-01T10:02:03+02:00'
        dt = parse(timestamp)
        deepcopy(dt)

    def test_parse_microseconds(self):
        '''
        Test parsing timestamps with microseconds.

        '''
        timestamp = '2009-01-01T10:02:03.25Z'
        dt = parse(timestamp)
        if not dt.microsecond == 250000:
            raise AssertionError("%r != %r" % (dt.microsecond, 250000))

    def test_generate_microseconds(self):
        '''
        Test generating timestamps with microseconds.

        '''
        dt = datetime(2009, 1, 1, 10, 2, 3, 500000, pytz.utc)
        timestamp = generate(dt, microseconds=True)
        if not timestamp == '2009-01-01T10:02:03.500000Z':
            raise AssertionError("%r != %r" % (timestamp, '2009-01-01T10:02:03.500000Z'))

    def test_mixed_case(self):
        '''
        Timestamps may use either 'T' or 't' and either 'Z' or 'z'
        according to :RFC:`3339`.

        '''
        dt1 = parse('2009-01-01t10:01:02z')
        dt2 = datetime(2009, 1, 1, 10, 1, 2, tzinfo=pytz.utc)

        if not dt1 == dt2:
            raise AssertionError("%r != %r" % (dt1, dt2))

    def test_parse_naive_utc(self):
        '''
        Test parsing a UTC timestamp to a naive datetime.

        '''
        dt1 = parse('2009-01-01T10:01:02Z', produce_naive=True)
        if not dt1.tzinfo == None:
            raise AssertionError("%r != %r" % (dt1.tzinfo, None))

    def test_parse_naive_local(self):
        '''
        Test that parsing a local timestamp to a naive datetime fails.

        '''
        with self.assertRaises(ValueError) as context:
            parse('2009-01-01T10:01:02-04:00', produce_naive=True)


    def test_generate_utc_parse_utc(self):
        '''
        Generate a UTC timestamp and parse it into a UTC datetime.

        '''
        dt1 = datetime.utcnow()
        dt1 = dt1.replace(tzinfo=pytz.utc)

        dt2 = parse(generate(dt1, microseconds=True))
        if not dt1 == dt2:
            raise AssertionError("%r != %r" % (dt1, dt2))

    def test_generate_local_parse_local(self):
        '''
        Generate a local timestamp and parse it into a local datetime.

        '''
        eastern = pytz.timezone('US/Eastern')
        dt1 = eastern.localize(datetime.utcnow())
        dt2 = parse(generate(dt1, utc=False, microseconds=True), utc=False)
        if not dt1 == dt2:
            raise AssertionError("%r != %r" % (dt1, dt2))

    def test_generate_local_parse_utc(self):
        '''
        Generate a local timestamp and parse it into a UTC datetime.

        '''
        eastern = pytz.timezone('US/Eastern')
        dt1 = eastern.localize(datetime.utcnow())
        dt2 = parse(generate(dt1, utc=False, microseconds=True))
        if not dt1 == dt2:
            raise AssertionError("%r != %r" % (dt1, dt2))


@pytest.mark.parametrize('tz_name', pytz.all_timezones)
class TestExhaustiveRoundtrip:
    '''
    This test suite exhaustively tests parsing and generation by generating
    a local RFC 3339 timestamp for every timezone supported by pytz,
    and parsing that timestamp into a local datetime and a UTC datetime.
    '''

    slow = True

    def test_local_roundtrip(self, tz_name):
        '''
        Generates a local datetime using the given timezone,
        produces a local timestamp from the datetime, parses the timestamp
        to a local datetime, and verifies that the two datetimes are equal.

        '''
        if not tz_name == 'leapseconds':
            tzinfo = pytz.timezone(tz_name)
            dt1 = tzinfo.localize(datetime.utcnow())
            timestamp = generate(dt1, utc=False, microseconds=True)
            dt2 = parse(timestamp, utc=False)
            if not dt1 == dt2:
                raise AssertionError("%r != %r" % (dt1, dt2))

    def test_utc_roundtrip(self, tz_name):
        '''
        Generates a local datetime using the given timezone,
        produces a local timestamp from the datetime, parses the timestamp
        to a UTC datetime, and verifies that the two datetimes are equal.

        '''
        if not tz_name == 'leapseconds':
            tzinfo = pytz.timezone(tz_name)
            dt1 = tzinfo.localize(datetime.utcnow())
            timestamp = generate(dt1, utc=False, microseconds=True)
            dt2 = parse(timestamp)
            if not dt1 == dt2:
                raise AssertionError("%r != %r" % (dt1, dt2))

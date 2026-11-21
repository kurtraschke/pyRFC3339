.. image:: https://github.com/kurtraschke/pyRFC3339/actions/workflows/python.yml/badge.svg
    :target: https://github.com/kurtraschke/pyRFC3339/actions/workflows/python.yml
    :alt: Build Status

.. image:: https://readthedocs.org/projects/pyrfc3339/badge/?version=latest
    :target: https://pyrfc3339.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Description
===========

pyRFC3339 parses and generates :RFC:`3339`-compliant timestamps using `Python <https://www.python.org/>`_ `datetime.datetime <https://docs.python.org/3/library/datetime.html#datetime-objects>`_ objects.

>>> from pyrfc3339 import generate, parse
>>> from datetime import UTC, datetime
>>> generate(datetime.now(UTC)) #doctest:+ELLIPSIS
'...T...Z'
>>> parse('2009-01-01T10:01:02Z')
datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=datetime.timezone.utc)
>>> parse('2009-01-01T14:01:02-04:00')
datetime.datetime(2009, 1, 1, 14, 1, 2, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=72000)))

Status
======

The first lines of code for what would become pyRFC3339 were written in 2009, as part of a larger project which would itself never see the light of day. At the time, the most expedient approach to parsing RFC 3339 timestamps seemed to be to use a regular expression derived from the ABNF grammar contained in the RFC. In retrospect, this seems absurd. Seventeen years later, the Python standard library is now well-suited to the task.

To be blunt: **you do not need pyRFC3339 on any modern version of Python** [#f1]_. This library is now merely a thin wrapper around the `datetime.datetime.fromisoformat() <https://docs.python.org/3/library/datetime.html#datetime.datetime.fromisoformat>`_ and `datetime.datetime.isoformat() <https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat>`_. You can call these functions yourself and eliminate a dependency from your dependency tree.

It is completely true that once upon a time, handling of `ISO 8601 <https://www.iso.org/iso-8601-date-and-time-format.html>`_ (and, by extension, RFC 3339) timestamps was a notable blindspot in Python's "batteries-included" standard library. But this is no longer the case. There is now built-in support for the `IANA time zone database <https://www.iana.org/time-zones>`_ as well as all of the relevant parts of ISO 8601.

Installation
============

To install the latest version from `PyPI <https://pypi.org/>`_:

``$ pip install pyRFC3339``

To install the latest development version:

``$ pip install https://github.com/kurtraschke/pyRFC3339/tarball/main#egg=pyRFC3339-dev``

Tests as well as enforcement of code style, formatting, and type safety are run with `tox <https://tox.wiki/>`_:

``$ tox``

To build the documentation with Sphinx:

``$ tox -e docs``

The documentation is also available online at:

https://pyrfc3339.readthedocs.io/

.. rubric:: Footnotes

.. [#f1] for clarity, any Python version supported as of November 2026, or any version greater than or equal to 3.11
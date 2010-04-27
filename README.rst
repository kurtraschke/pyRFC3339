Description
===========

pyRFC3339 produces and generates :RFC:`3339`-compliant timestamps from Python `datetime.datetime` objects.

>>> from pyrfc3339 import generate, parse
>>> from datetime import datetime
>>> import pytz
>>> generate(datetime.utcnow().replace(tzinfo=pytz.utc)) #doctest:+ELLIPSIS
'...T...Z'
>>> parse('2009-01-01T10:01:02Z')
datetime.datetime(2009, 1, 1, 10, 1, 2, tzinfo=<UTC>)
>>> parse('2009-01-01T14:01:02-04:00')
datetime.datetime(2009, 1, 1, 14, 1, 2, tzinfo=<UTC-04:00>)

Installation
============

In the future (once a formal release has been made and uploaded to PyPI),
install pyRFC3339 as follows:

``$ easy_install pyRFC3339``

Until then, either clone the repository listed below, or download a snapshot
from the URL given:

* git://github.com/kurtraschke/pyRFC3339.git
* http://github.com/kurtraschke/pyRFC3339/tarball/master#egg=pyRFC3339-dev

Then install as follows:

#. ``$ python setup.py build``
#. ``$ python setup.py nosetests``
#. ``$ python setup.py install``

To build the documentation with Sphinx:

#. ``$ easy_install Sphinx``
#. ``$ python setup.py build_sphinx``

The latest development version can also be installed with:

``$ easy_install http://github.com/kurtraschke/pyRFC3339/tarball/master#egg=pyRFC3339-dev``
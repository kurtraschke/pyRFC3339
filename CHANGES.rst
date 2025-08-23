Changelog
=========

2.1.0 (2025-08-23)
------------------

(The Git branch used for development was renamed from ``master`` to ``main``)

- Greatly simplify timestamp parsing and generation code, leveraging improvements in native Python
  capabilities in the past decade-and-a-half. See :commit:`53c2d15` for further details.
- Simplify GitHub Actions workflow. Add `zizmor <http://zizmor.sh/>`_ to audit workflows.
- Modernize packaging and documentation configuration.

2.0.1 (2024-11-03)
------------------

- Fix GitHub Actions badge in README.rst.

2.0 (2024-11-03)
----------------

(not released to PyPI)

- Migrate tests from ``nose`` to ``unittest`` and ``pytest`` (:issue:`16`)
- Replace :mod:`pytz` dependency with :attr:`datetime.timezone.utc` and :mod:`zoneinfo` (:issue:`15`)
- Reformat codebase with ``black`` and ``isort``
- Configure GitHub Actions; remove Travis CI configuration file

1.1 (2018-06-10)
----------------

- Drop support for EOL Python releases, add (explicit) support for Python 3.5 and 3.6 (:issue:`7,10,11,12`)
- Add :meth:`.utils.FixedOffset.__deepcopy__()` method, to prevent crash on deepcopy (:issue:`8`)

1.0 (2015-11-09)
----------------

- First formally-tagged release
- Fix :func:`.utils.timedelta_seconds()` to use :meth:`datetime.timedelta.total_seconds()` when the native method is available (:issue:`6`)
- Documentation and packaging cleanup (:issue:`4,5`)

0.2 (2014-02-09)
----------------

- Python 3 compatibility (:issue:`2`)

0.1 (2011-01-26)
----------------

- Initial release

from distutils.version import LooseVersion
from setuptools import setup, __version__ as setuptools_version

with open("README.rst", "r") as readme:
    long_description = readme.read()


setuptools_known_environment_markers = (LooseVersion(setuptools_version) >= LooseVersion('36.2'))
if setuptools_known_environment_markers:
    install_requires = ['pytz ; python_version < "3.2"']
else:
    install_requires = ['pytz']


setup(
    name = "pyRFC3339",
    version = "1.1",
    author = "Kurt Raschke",
    author_email = "kurt@kurtraschke.com",
    url = "https://github.com/kurtraschke/pyRFC3339",
    description = "Generate and parse RFC 3339 timestamps",
    long_description = long_description,
    keywords = "rfc 3339 timestamp",
    license = "MIT",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet"
        ],

    packages = ['pyrfc3339'],

    install_requires = install_requires,
    test_suite = 'nose.collector',
    tests_require = ['nose', 'coverage', 'pytz']
)

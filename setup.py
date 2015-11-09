from setuptools import setup

with open("README.rst", "r") as readme:
    long_description = readme.read()

setup(
    name = "pyRFC3339",
    version = "1.0",
    author = "Kurt Raschke",
    author_email = "kurt@kurtraschke.com",
    url = "https://github.com/kurtraschke/pyRFC3339",
    description = "Generate and parse RFC 3339 timestamps",
    long_description = open("README.rst").read(),
    keywords = "rfc 3339 timestamp",
    license = "MIT",
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Topic :: Internet"
        ],

    packages = ['pyrfc3339'],

    install_requires = ['pytz'],
    test_suite = 'nose.collector',
    tests_require = ['nose']
)

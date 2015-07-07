#!/usr/bin/env python
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name="metaconfig",
    version="0.1",
    url="https://github.com/khwilson/metaconfig",
    author="Kevin Wilson",
    author_email="khwilson@gmail.com",
    license="Apache 2.0",
    packages=find_packages(),
    cmdclass={"test": PyTest},
    install_requires=open('requirements.txt').read(),
    tests_require=open('requirements.testing.txt').read(),
    description="An example of using metaclasses to load configuration files",
    long_description="\n" + open("README.md").read(),
)

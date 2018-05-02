#!/usr/bin/env python3

import locale
import platform
import sys
from subprocess import call

import setuptools.command.build_py
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

try:
    lc = locale.getlocale()
    pf = platform.system()
    if pf != 'Windows' and lc == (None, None):
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except (ValueError, UnicodeError):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

VERSION = '0.7.0'

# Workaround missing 'docs' command
__all__ = ['call']


class PyTestCommand(TestCommand):
    """
    From https://pytest.org/latest/goodpractices.html
    """
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open('test-requirements.txt') as requirements:
    test_required = requirements.read().splitlines()

with open('README.rst') as readme:
    long_description = readme.read()

extras_require = None
data_files = None

if __name__ == '__main__':
    setup(
        name='coala_utils',
        version=VERSION,
        description='A collection of coala utilities',
        author='Adrian Zatreanu',
        author_email='adrianzatreanu1@gmail.com',
        maintainer='Adrian Zatreanu, Alexandros Dimos, Lasse Schuirmann',
        url='https://gitlab.com/coala/coala-utils',
        package_data={'coala_utils': ["VERSION"]},
        packages=find_packages(exclude=["build.*", "tests", "tests.*"]),
        install_requires=required,
        tests_require=test_required,
        long_description=long_description,
        keywords=['coala', 'utils', 'bears', 'decorators'],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',

            'Intended Audience :: Science/Research',
            'Intended Audience :: Developers',

            'License :: OSI Approved :: MIT License',

            'Operating System :: OS Independent',

            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3 :: Only',
        ],
        cmdclass={
            'test': PyTestCommand,
        },
    )

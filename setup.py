#!/usr/bin/env python3

import locale
import os
import platform
import sys

import setuptools.command.build_py
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

try:
    lc = locale.getlocale()
    pf = platform.system()
    if pf != 'Windows' and lc == (None, None):
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except (ValueError, UnicodeError, locale.Error):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

VERSION = '0.7.0'
DEPENDENCY_LINKS = []

SETUP_COMMANDS = {}

# Workaround missing 'docs' command
__all__ = ['call']


def set_python_path(path):
    if 'PYTHONPATH' in os.environ:
        user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
        user_paths.insert(0, path)
        os.environ['PYTHONPATH'] = os.pathsep.join(user_paths)
    else:
        os.environ['PYTHONPATH'] = path


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


SETUP_COMMANDS['test'] = PyTestCommand


__dir__ = os.path.dirname(__file__)


def read_requirements(filename):
    """
    Parse a requirements file.

    Accepts vcs+ links, and places the URL into
    `DEPENDENCY_LINKS`.

    :return: list of str for each package
    """
    data = []
    filename = os.path.join(__dir__, filename)
    with open(filename) as requirements:
        required = requirements.read().splitlines()
        for line in required:
            if not line or line.startswith('#'):
                continue

            if '+' in line[:4]:
                repo_link, egg_name = line.split('#egg=')
                if not egg_name:
                    raise ValueError('Unknown requirement: {0}'
                                     .format(line))

                DEPENDENCY_LINKS.append(repo_link)

                line = egg_name.replace('-', '==')

            data.append(line)

    return data


required = read_requirements('requirements.txt')

test_required = read_requirements('test-requirements.txt')

filename = os.path.join(__dir__, 'README.rst')
with open(filename) as readme:
    long_description = readme.read()

extras_require = None
EXTRAS_REQUIRE = {}
data_files = None

if extras_require:
    EXTRAS_REQUIRE = extras_require
SETUP_COMMANDS.update({
})

if __name__ == '__main__':
    setup(
        name='coala_utils',
        version=VERSION,
        description='A collection of coala utilities',
        author='Adrian Zatreanu',
        author_email='adrianzatreanu1@gmail.com',
        maintainer='Adrian Zatreanu, Alexandros Dimos, Lasse Schuirmann',
        url='https://gitlab.com/coala/coala-utils',
        package_data={'coala_utils': ['VERSION']},
        packages=find_packages(exclude=['build.*', 'tests', 'tests.*']),
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

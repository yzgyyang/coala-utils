from coala_utils import VERSION
from coala_utils import get_version
from distutils.core import setup
from setuptools import find_packages


with open("README.rst") as readme:
    long_description = readme.read()

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open('test-requirements.txt') as requirements:
    test_required = requirements.read().splitlines()

setup(
    name='coala_utils',
    version=VERSION,
    description='A collection of coala utilities.',
    author='Adrian Zatreanu',
    author_email='adrianzatreanu1@gmail.com',
    maintainers={'Adrian Zatreanu', 'Alexandros Dimos', 'Lasse Schuirmann'},
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
)

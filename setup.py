from coala_decorators import VERSION
from coala_decorators import get_version
from distutils.core import setup

setup(
  name='coala_decorators',
  packages=['coala_decorators'],
  version=VERSION,
  description='A collection of useful decorators.',
  author='Adrian Zatreanu',
  author_email='adrian.zatreanu@eestec.ro',
  url='https://github.com/coala-analyzer/coala-decorators',
  package_data={'coala_decorators': ["VERSION"]},
  keywords=['coala', 'decorators', 'bears'],
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
              'Programming Language :: Python :: 3 :: Only'],
)

import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


version = '0.1'


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = 'test'
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='fowler.switchboard',
    version=version,
    description='',
    long_description='''''',
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords='',
    author='Dmitrijs Milajevs, Christopher Potts',
    author_email='dimazest@gmail.com',
    url='',
    license='Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['fowler'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'cython>=0.13',
        'nltk',
        'opster',
        'pandas',
        'python-dateutil',
        'pyyaml',
        'scikit-learn',
        'scipy',
        'setuptools',
        'tables',
    ],
    entry_points={
        'console_scripts': [
            'sw = fowler.switchboard.main:dispatch',
        ],
    },
    tests_require=['pytest>=2.4.2'],
    cmdclass={'test': PyTest},
)

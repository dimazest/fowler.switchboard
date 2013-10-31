from setuptools import setup, find_packages


version = '0.1'


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
        'nltk',
        'opster',
        'python-dateutil',
        'scikit-learn',
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'sw = fowler.switchboard.main:dispatch',
        ],
    },
)

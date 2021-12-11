from os import path

from setuptools import setup

from sqlparser import __version__ as version

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name='sqlparser',
    version=version,
    description='Sql Query Parser',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/antrikshmisri/SQL-Query-Parser',
    author='Antriksh Misri',
    author_email='antrikshmisri@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords=['sql', 'parser', 'query', 'parser'],
    include_package_data=True,
    packages=['sqlparser'],
)

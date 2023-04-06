from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f"\n{f.read()}"

VERSION = '1.0.0b6'
DESCRIPTION = 'A Python library for generating snowflakes.'
LONG_DESCRIPTION = 'A Python library for generating Discord, Twitter, Instagram and custom snowflakes.'

# Setup
setup(
    name='snowflake-util',
    version=VERSION,
    author="TheMultii",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    project_urls = {
    'Repository': 'https://github.com/TheMultii/snowflake-util',
    },
    install_requires=[],
    keywords=['python', 'snowflake', 'generator', 'custom', 'library', 'id generator', 'uid'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

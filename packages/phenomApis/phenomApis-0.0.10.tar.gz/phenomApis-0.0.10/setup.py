from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.10'
DESCRIPTION = 'phenomApis'
LONG_DESCRIPTION = 'A package to access phenom apis'

# Setting up
setup(
    name="phenomApis",
    version=VERSION,
    author="phenom",
    author_email="8297991468h@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['PyJWT==2.8.0', 'certifi==2023.11.17', 'urllib3==2.1.0', 'six==1.16.0'],
    keywords=['resumeparser', 'exsearch'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
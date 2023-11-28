# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md") as f:
    README = f.read()


VERSION = "0.0.1"


setup(
    name="bi-sc-client",
    version=VERSION,
    author="Coopdevs, Som Connexio",
    author_email="info@coopdevs.org",
    maintainer="Daniel Palomar",
    url="https://git.coopdevs.org/coopdevs/som-connexio/bi/bi-sc-client",
    description="Python wrapper for BI SomConnexió API",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests", "docs")),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests == 2.28.1",
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Operating System :: POSIX :: Linux",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)

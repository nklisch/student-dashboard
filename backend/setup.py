from setuptools import find_packages, setup
from package import Package

setup(
    author="Nathan Klisch",
    author_email="nklisch@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    cmdclass={"package": Package},
)

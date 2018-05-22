from setuptools import setup, find_packages
setup(
    name="coalescence",
    version="0.1",
    author="Guillaume Loetscher",
    author_email="sterfield@gmail.com",
    description="Merge several data source with ease !",
    url="https://github.com/sterfield/coalescence",
    packages=find_packages(),
    tests_require=['pytest'],
    setup_requires=['pytest-runner'],
)
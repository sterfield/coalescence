from setuptools import setup, find_packages
setup(
    name="coalescence",
    version="0.1",
    packages=find_packages(),
    test_require=['pytest', 'pytest-mock'],
    setup_requires=['pytest-runner'],
)
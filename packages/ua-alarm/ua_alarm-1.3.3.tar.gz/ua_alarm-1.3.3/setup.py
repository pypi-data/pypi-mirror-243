from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="ua_alarm",
    author="user-sspmynxdvb",
    version="1.3.3",
    description="Implements api.ua_alarm.com API that returns info about Ukraine air raid alarms.",
    license="GNUv3",
    url="https://github.com/user-sspmynxdvb/ua_alarm",
    packages=find_packages(),
    install_requires=["aiohttp>=3.9.0", "pydantic>=2.5.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)

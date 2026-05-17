from setuptools import setup, find_packages

BUILD = [
    "delta-spark",
    "pyspark",
    "pyspark[sql]",
]

TEST = [
    "pytest>=8.4.1,<9.0",
    "pytest-cov>=5.0.0,<6.0",
    "pylint>=3.0.2,<4.0",
    "flake8>=6.1.0,<7.0",
]

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="synapse_sdk",
    version="0.1.0",
    description="Synapse SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Fanni Jako",
    author_email="fannijako@gmail.com",

    url="https://github.com/fannijako/synapse_sdk",

    packages=find_packages(),
    include_package_data=True,

    install_requires=BUILD,

    extras_require={
        "test": TEST,
        "build": BUILD,
    },

    python_requires=">=3.10",
)

from setuptools import setup, find_packages

print(find_packages())

setup(
    name="dtac-tools",
    version="0.8.12",
    packages=find_packages(),
    install_requires=[
        "cryptography>=3.4.8",
        "grpcio>=1.59.2",
        "protobuf>=4.25.0",
        "pydantic>=1.10.0",
        "setuptools>=59.6.0",
    ]
)
from setuptools import setup, find_packages

print(find_packages())

setup(
    name="dtac-tools",
    version="0.8.7",
    packages=find_packages(),
    install_requires=[
        "cryptography>=3.4.8",
        "grpcio>=1.59.2",
        "protobuf>=4.25.0",
        "pydantic>=2.4.2",
        "setuptools>=59.6.0",
        "debugpy>=1.5.1",
    ]
)
from setuptools import setup, find_packages

setup(
    name="genebe",
    version="0.0.4",
    packages=find_packages(),
    install_requires=["mmh3", "tinynetrc", "pandas", "requests"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

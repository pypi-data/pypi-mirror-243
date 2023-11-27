import setuptools

__version__ = '1.1.0'


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="PyYep",
    version=__version__,
    author="Daniel Montalvão Bomfim",
    author_email="daniellsmv@hotmail.com",
    description="A simple schema builder for value parsing and validation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["PyYep"],
    python_requires=">=3.10",
    url="https://github.com/danielmbomfim/PyYep",
    project_urls={
        "Bug Tracker": "https://github.com/danielmbomfim/PyYep/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="simple_config_handler",
    version="0.0.3",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A simple config handler for python",
    author="Justin Rose",
    author_email="rosejustin601@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
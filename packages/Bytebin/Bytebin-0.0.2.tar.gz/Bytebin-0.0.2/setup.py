from setuptools import setup, find_packages
import os

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


VERSION = "0.0.2"
DESCRIPTION = "Bytebin API Wrapper"


setup(
    name="Bytebin",
    author="alexraskin",
    description=DESCRIPTION,
    version=VERSION,
    url="https://github.com/alexraskin/bytebin.py",
    author_email="<root@alexraskin.com",
    license="MIT License",
    keywords=["module", "Bytebin", "library", "package", "python"],
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    install_requires=["requests"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

from setuptools import setup
from setuptools import find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="decisionlab",
    version="0.1.1",
    packages=find_packages(),
    author="decisionLab",
    author_email="jsanchezcastillejos@gmail.com",
    description="A Python package for accessing decision data from JustDecision.com",
    long_description=long_description,  # Add the long_description field
    long_description_content_type="text/markdown",  # Specify the format of the long_description content
    url="https://github.com/TuDecides/decisionlab",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)

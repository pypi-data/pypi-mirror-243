from setuptools import setup
from setuptools import find_packages

with open("Readme.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='fiqus',
    version="2023.11.3",
    author="STEAM Team",
    author_email="steam-team@cern.ch",
    description="Source code for STEAM FiQuS tool",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.cern.ch/steam/fiqus",
    keywords={'STEAM', 'FiQuS', 'CERN'},
    install_requires=required,
    python_requires='>=3.8',
    package_data={'': ['CCT_template.pro', 'Multipole_template.pro', 'Pancake3D_template.pro']},
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8"],

)

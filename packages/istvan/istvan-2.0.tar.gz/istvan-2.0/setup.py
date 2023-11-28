from setuptools import setup, find_packages
import os
from pathlib import Path
os.path.dirname(os.path.abspath('__file__'))
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="istvan",
    version="2.0",
    author="Istvan",
    author_email="pista1125@gmail.com",
    description="A description of your package",
    license="MIT",
    url="https://github.com/pista1125/pityu",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages()
)
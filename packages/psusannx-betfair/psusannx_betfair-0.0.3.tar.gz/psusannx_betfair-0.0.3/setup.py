from setuptools import setup, find_packages
from pathlib import Path

# Get the current directory of the setup.py file (as this is where the README.md will be too)
current_dir = Path(__file__).parent
long_description = (current_dir / "README.md").read_text()

# Set up the package metadata
setup(
    name="psusannx_betfair",
    author="Jamie O'Brien",
    description="A package with functions for getting Betfair Exchange odds on upcoming Premier League matches.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.0.3",
    packages=find_packages(include=["psusannx_betfair", "psusannx_betfair.*"]),
    install_requires=[
        "numpy", 
        "pandas", 
        "requests"
    ],
    project_urls={
        "Source Code": "https://github.com/jamieob63/psusannx_betfair.git",
        "Bug Tracker": "https://github.com/jamieob63/psusannx_betfair.git/issues",
    }
)
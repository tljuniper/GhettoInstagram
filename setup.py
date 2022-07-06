from setuptools import setup, find_packages

setup(
    name="vinstagram",
    version="1.0",
    author="",
    url="",
    description="Vinstagram - vintage instagram",
    packages=find_packages(),
    entry_points={"console_scripts": ["vinstagram = src.app:run"]},
    extras_require={"dev": ["mypy", "black"]},
)

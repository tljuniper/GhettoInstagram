from setuptools import setup, find_packages

setup(
    name="ghetto_instagram",
    version="1.0",
    author="",
    url="",
    description="Ghetto Instagram",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "run = src.app:run",
        ]
    },
    extras_require={"dev": ["mypy", "black"]},
)

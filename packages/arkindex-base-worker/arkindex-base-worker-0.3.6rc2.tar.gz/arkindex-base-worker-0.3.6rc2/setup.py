#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup


def requirements(path: Path):
    assert path.exists(), f"Missing requirements {path}"
    with path.open() as f:
        return list(map(str.strip, f.read().splitlines()))


setup(
    version=Path("VERSION").read_text().strip(),
    install_requires=requirements(Path("requirements.txt")),
    extras_require={"docs": requirements(Path("docs-requirements.txt"))},
    packages=find_packages(),
)

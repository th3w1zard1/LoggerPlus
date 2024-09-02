from __future__ import annotations

from setuptools import setup

setup(
    name="LoggerPlus",
    version="0.1.0",
    description="A wrapper around the Python logging module that provides a more flexible and powerful logging solution.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Benjamin Auquite",
    author_email="halomastar@gmail.com",
    url="https://github.com/th3w1zard1/LoggerPlus",
    packages=["loggerplus", "utility"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "color": ["colorama"],
    },
    project_urls={
        "Homepage": "https://github.com/th3w1zard1/LoggerPlus",
        "Documentation": "https://github.com/th3w1zard1/LoggerPlus/blob/master/README.md",
        "Repository": "https://github.com/th3w1zard1/LoggerPlus.git",
        "Issues": "https://github.com/th3w1zard1/LoggerPlus/issues",
        # "Changelog": "https://github.com/th3w1zard1/LoggerPlus/blob/master/CHANGELOG.md",
    },
    license_files=("LICENSE",),
)

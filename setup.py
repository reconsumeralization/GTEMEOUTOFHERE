"""
COSURVIVAL: Connected Intelligence Network
Setup script for package installation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="cosurvival",
    version="0.1.0",
    description="Connected Intelligence Network - Transforming activity data into ethical collaboration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="COSURVIVAL Contributors",
    author_email="",  # Add contact email
    url="https://github.com/yourusername/cosurvival",  # Update with actual repo URL
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.3.3",
            "black>=23.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "cosurvival=pipeline:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)


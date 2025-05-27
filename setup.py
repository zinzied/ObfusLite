"""
Setup script for PyObfuscator - Custom Python Code Obfuscation Library
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pyobfuscator",
    version="1.0.0",
    author="Custom Obfuscation Library",
    author_email="zinzied@gmail.com",
    description="Advanced Python code obfuscation library with novel encoding techniques",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/zinzied/pyobfuscator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "gui": ["PyQt6>=6.4.0"],
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0"],
    },
    entry_points={
        "console_scripts": [
            "pyobfuscator=pyobfuscator.cli:main",
            "pyobfuscator-gui=pyobfuscator.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "pyobfuscator": ["templates/*.py"],
    },
    keywords="obfuscation, code protection, encryption, security, python",
    project_urls={
        "Bug Reports": "https://github.com/zinzied/pyobfuscator/issues",
        "Source": "https://github.com/zinzied/pyobfuscator",
        "Documentation": "https://github.com/zinzied/pyobfuscator/blob/main/README.md",
    },
)

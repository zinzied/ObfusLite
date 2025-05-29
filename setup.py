"""
Setup script for ObfusLite - Advanced Python Code Obfuscation Library
"""

from setuptools import setup, find_packages

# Read the README file
def read_readme():
    try:
        with open("README.md", "r", encoding="utf-8") as fh:
            return fh.read()
    except FileNotFoundError:
        return "ObfusLite - Advanced Python Code Obfuscation Library"

# Read requirements
def read_requirements():
    try:
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return []

setup(
    name="obfuslite",
    version="1.1.0",
    author="Zied Boughdir",
    author_email="zinzied@gmail.com",
    description="Advanced Python code obfuscation library with enhanced GUI and multi-file support",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/zinzied/obfuslite",
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
        "full": ["PyQt6>=6.4.0", "numpy>=1.21.0", "scipy>=1.9.0"],
    },
    entry_points={
        "console_scripts": [
            "obfuslite=obfuslite.cli:main",
            "obfuslite-gui=obfuslite.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "obfuslite": ["templates/*.py"],
    },
    keywords="obfuscation, code protection, encryption, security, python, gui, batch processing",
    project_urls={
        "Bug Reports": "https://github.com/zinzied/obfuslite/issues",
        "Source": "https://github.com/zinzied/obfuslite",
        "Documentation": "https://github.com/zinzied/obfuslite/blob/main/README.md",
        "GUI Features": "https://github.com/zinzied/obfuslite/blob/main/GUI_FEATURES.md",
    },
)

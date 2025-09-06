#!/usr/bin/env python3
"""
Setup script for Lane Detection Application
Created by Sunil Sharma ❤️
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="lane-detection-app",
    version="1.0.0",
    author="Sunil Sharma",
    author_email="sunil.sharma@example.com",
    description="Advanced Lane Detection Application with Real-time Processing",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunbyte16/lane-detection-app",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "lane-detection=run_app:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.png", "*.jpg", "*.mp4", "*.md"],
    },
    keywords="computer-vision, lane-detection, opencv, machine-learning, autonomous-vehicles, image-processing",
    project_urls={
        "Bug Reports": "https://github.com/sunbyte16/lane-detection-app/issues",
        "Source": "https://github.com/sunbyte16/lane-detection-app",
        "Documentation": "https://github.com/sunbyte16/lane-detection-app#readme",
        "Portfolio": "https://lively-dodol-cc397c.netlify.app",
        "LinkedIn": "https://www.linkedin.com/in/sunil-kumar-bb88bb31a/",
    },
)

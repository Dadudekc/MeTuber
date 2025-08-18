#!/usr/bin/env python3
"""
Setup script for MeTuber webcam filter application.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "MeTuber - Advanced Webcam Filter Application"

# Read requirements
def read_requirements(filename):
    requirements_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="metuber",
    version="2.0.0",
    description="Advanced webcam filter application with real-time effects",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="MeTuber Team",
    author_email="",
    url="https://github.com/yourusername/metuber",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Video",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements('requirements-core.txt'),
    extras_require={
        'full': read_requirements('requirements.txt'),
        'dev': [
            'pytest>=8.0.0',
            'pytest-cov>=4.1.0',
            'pytest-qt>=4.2.0',
            'black>=23.7.0',
            'flake8>=6.1.0',
            'mypy>=1.5.1',
        ],
        'audio': [
            'pyaudio>=0.2.11',
            'whisper>=1.1.10',
            'speech-recognition>=3.10.0',
        ],
        'advanced': [
            'av>=10.0.0',
            'pillow>=10.0.0',
            'scikit-image>=0.22.0',
            'scikit-learn>=1.4.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'metuber=webcam_filter_pyqt5:main',
            'metuber-check-deps=check_dependencies:main',
        ],
    },
    include_package_data=True,
    package_data={
        'styles': ['*.py'],
        'gui_components': ['*.py'],
    },
    keywords="webcam, filter, effects, video, real-time, opencv, pyqt5",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/metuber/issues",
        "Source": "https://github.com/yourusername/metuber",
        "Documentation": "https://github.com/yourusername/metuber/wiki",
    },
)



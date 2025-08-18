# MeTuber Dependency Management Guide

This document explains how to manage dependencies for the MeTuber webcam filter application.

## Overview

MeTuber uses a tiered dependency system:
- **Core Dependencies**: Required for basic functionality
- **Optional Dependencies**: Enable advanced features
- **Development Dependencies**: For development and testing

## Quick Start

### 1. Install Core Dependencies (Minimal)
```bash
pip install -r requirements-core.txt
```

### 2. Install All Dependencies (Full Features)
```bash
pip install -r requirements.txt
```

### 3. Install with Extras
```bash
# Development dependencies
pip install -e .[dev]

# Audio features
pip install -e .[audio]

# Advanced features
pip install -e .[advanced]

# All extras
pip install -e .[full]
```

## Windows Installation

### PowerShell Script (Recommended)
```powershell
# Run as Administrator
.\install.ps1 -Core    # Minimal installation
.\install.ps1 -Full    # Full installation
.\install.ps1 -Dev     # Development installation
```

### Manual Installation
```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements-core.txt
```

## Dependency Checker

Run the dependency checker to verify your installation:
```bash
python check_dependencies.py
```

This will show:
- ✅ Available packages
- ❌ Missing core dependencies
- ⚠️ Missing optional dependencies
- System requirements status

## Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt5 | 5.15.9 | GUI framework |
| opencv-python | 4.8.0.76 | Computer vision |
| numpy | 1.24.3 | Numerical computing |
| pyvirtualcam | 0.12.1 | Virtual camera |

## Optional Dependencies

| Package | Version | Purpose | Feature |
|---------|---------|---------|---------|
| av | 10.0.0 | Advanced video processing | Advanced video I/O |
| pillow | 10.0.0 | Image processing | Image file support |
| scikit-image | 0.22.0 | Advanced image processing | Advanced effects |
| scikit-learn | 1.4.0 | Machine learning | AI optimization |
| pyaudio | 0.2.11 | Audio processing | Audio capture |
| whisper | 1.1.10 | Speech recognition | Audio captioning |
| speech-recognition | 3.10.0 | Speech recognition | Audio features |

## Feature Matrix

| Feature | Core Dependencies | Optional Dependencies |
|---------|------------------|----------------------|
| Basic Webcam | ✅ | - |
| Virtual Camera | ✅ | - |
| Real-time Effects | ✅ | - |
| Advanced Video I/O | ❌ | av |
| Image File Support | ❌ | pillow |
| Advanced Effects | ❌ | scikit-image |
| AI Optimization | ❌ | scikit-learn |
| Audio Captioning | ❌ | pyaudio, whisper |

## Troubleshooting

### Common Issues

#### 1. PyQt5 Installation Problems
```bash
# Windows
pip install PyQt5==5.15.9

# Linux
sudo apt-get install python3-pyqt5
```

#### 2. OpenCV Installation Problems
```bash
# If opencv-python fails
pip install opencv-python-headless
```

#### 3. Virtual Camera Issues
- Install OBS Studio for virtual camera support
- Ensure pyvirtualcam is properly installed
- Check system permissions

#### 4. Audio Dependencies (Windows)
```bash
# Install Visual C++ Build Tools first
pip install pyaudio
```

### Dependency Resolution

#### Missing Core Dependencies
```bash
# Check what's missing
python check_dependencies.py

# Install missing packages
pip install <package_name>
```

#### Version Conflicts
```bash
# Create fresh virtual environment
python -m venv fresh_venv
source fresh_venv/bin/activate  # Linux/Mac
.\fresh_venv\Scripts\Activate.ps1  # Windows

# Install with specific versions
pip install -r requirements-core.txt
```

## Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd metuber
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
```

### 3. Install Development Dependencies
```bash
pip install -e .[dev]
```

### 4. Run Tests
```bash
pytest
pytest --cov=.
```

## Continuous Integration

The project includes CI/CD configuration for dependency management:

- **Dependency Check**: Runs on every commit
- **Version Pinning**: Ensures reproducible builds
- **Platform Testing**: Tests on multiple platforms
- **Dependency Updates**: Automated security updates

## Best Practices

### 1. Always Use Virtual Environments
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows
```

### 2. Pin Versions
- Use exact versions in production
- Use version ranges in development
- Update dependencies regularly

### 3. Test Dependencies
```bash
# Run dependency checker
python check_dependencies.py

# Run application tests
python -m pytest
```

### 4. Document Changes
- Update requirements files when adding dependencies
- Document why dependencies are needed
- Include installation instructions

## Support

If you encounter dependency issues:

1. **Check the logs**: Look for specific error messages
2. **Run dependency checker**: `python check_dependencies.py`
3. **Check system requirements**: Ensure Python 3.8+ and proper system packages
4. **Create issue**: Include error logs and system information

## Links

- [Python Package Index](https://pypi.org/)
- [PyQt5 Documentation](https://doc.qt.io/qtforpython/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [OBS Studio](https://obsproject.com/) (for virtual camera)



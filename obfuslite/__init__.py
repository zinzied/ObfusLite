"""
ObfusLite - Advanced Python Code Obfuscation Library

A comprehensive Python code obfuscation library featuring novel encoding techniques
that go beyond traditional methods. Designed for protecting Python code before
compilation with PyInstaller.

Features:
- 6 Fast encoding techniques for optimal performance
- 7 Advanced encoding techniques for maximum security
- Multi-layer obfuscation support
- PyInstaller compatibility
- Command-line interface
- Enhanced GUI interface with multi-file support

Usage:
    from obfuslite import Obfuscator

    obfuscator = Obfuscator()
    result = obfuscator.obfuscate(code, technique='fast_xor', layers=2)
    standalone_code = obfuscator.create_standalone_file(result)

Command Line:
    obfuslite obfuscate input.py -o output.py -t fast_xor -l 2
    obfuslite-gui  # Launch enhanced GUI interface

GUI Features:
    - Multi-file batch processing
    - Project management
    - Code analysis and recommendations
    - Side-by-side comparison tools
    - Template system for configurations
"""

__version__ = "1.0.0"
__author__ = "Zied Boughdir"
__email__ = "zinzied@gmail.com"
__license__ = "MIT"

# Import main classes for easy access
from .core import Obfuscator
from .encoders import get_available_techniques, get_fast_techniques, get_advanced_techniques

# Define what gets imported with "from obfuslite import *"
__all__ = [
    'Obfuscator',
    'get_available_techniques',
    'get_fast_techniques',
    'get_advanced_techniques',
    '__version__',
]

# Performance modes
PERFORMANCE_MODES = {
    'fast': 'Ultra-fast processing with good security',
    'balanced': 'Balance of speed and security',
    'full': 'Maximum security with all techniques'
}

# Quick access functions
def quick_obfuscate(code: str, technique: str = 'fast_xor', layers: int = 2) -> str:
    """
    Quick obfuscation function for simple use cases

    Args:
        code: Python source code to obfuscate
        technique: Obfuscation technique to use (default: 'fast_xor')
        layers: Number of obfuscation layers (default: 2)

    Returns:
        Standalone Python code that can be executed directly
    """
    obfuscator = Obfuscator()
    result = obfuscator.obfuscate(code, technique=technique, layers=layers)
    return obfuscator.create_standalone_file(result)

def get_version_info():
    """Get detailed version information"""
    return {
        'version': __version__,
        'author': __author__,
        'license': __license__,
        'techniques': len(get_available_techniques()),
        'fast_techniques': len(get_fast_techniques()),
        'advanced_techniques': len(get_advanced_techniques())
    }

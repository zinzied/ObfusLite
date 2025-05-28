#!/usr/bin/env python3
"""
Enhanced GUI Demo for ObfusLite

This script demonstrates the new enhanced GUI features including:
- Multi-file batch processing
- Project management
- Code analysis
- Comparison tools
- Template system
"""

import sys
import os

# Add the parent directory to the path so we can import obfuslite
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    """Main function to launch the enhanced GUI"""
    try:
        from obfuslite.gui import main as gui_main
        print("🚀 Launching ObfusLite Enhanced GUI...")
        print("\n🎯 New Features:")
        print("✓ Batch Processing - Process multiple files at once")
        print("✓ Project Management - Save and load obfuscation projects")
        print("✓ Code Analysis - Analyze code complexity and get recommendations")
        print("✓ Comparison Tool - Compare original vs obfuscated code")
        print("✓ Template System - Save and reuse obfuscation configurations")
        print("✓ Export Options - Multiple export formats including ZIP")
        print("✓ Performance Monitoring - Track obfuscation metrics")
        print("\n🖥️  Starting GUI...")

        return gui_main()

    except ImportError as e:
        print(f"❌ Error: Failed to import ObfusLite GUI: {e}")
        print("Make sure PyQt6 is installed: pip install PyQt6")
        return 1
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

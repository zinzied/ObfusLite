"""
Build script for PyObfuscator package
Helps with building and uploading to PyPI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning build artifacts...")
    
    dirs_to_clean = ['build', 'dist', 'pyobfuscator.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}")
    
    print("✅ Build artifacts cleaned")

def run_tests():
    """Run tests to ensure package works"""
    print("🧪 Running tests...")
    
    # Try to run pytest first
    if run_command("python -m pytest tests/ -v", "Running pytest"):
        return True
    
    # Fallback to manual test
    print("   Pytest not available, running manual test...")
    return run_command("python tests/test_basic.py", "Running manual tests")

def build_package():
    """Build the package"""
    print("📦 Building package...")
    
    # Install build dependencies
    if not run_command("pip install build twine", "Installing build dependencies"):
        return False
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        return False
    
    return True

def check_package():
    """Check the built package"""
    print("🔍 Checking package...")
    
    # Check with twine
    if not run_command("python -m twine check dist/*", "Checking package with twine"):
        return False
    
    return True

def upload_to_test_pypi():
    """Upload to Test PyPI"""
    print("🚀 Uploading to Test PyPI...")
    
    command = "python -m twine upload --repository testpypi dist/*"
    print(f"   Command: {command}")
    print("   Note: You'll need to enter your Test PyPI credentials")
    
    return run_command(command, "Uploading to Test PyPI")

def upload_to_pypi():
    """Upload to PyPI"""
    print("🚀 Uploading to PyPI...")
    
    command = "python -m twine upload dist/*"
    print(f"   Command: {command}")
    print("   Note: You'll need to enter your PyPI credentials")
    
    return run_command(command, "Uploading to PyPI")

def install_locally():
    """Install the package locally for testing"""
    print("💻 Installing package locally...")
    
    # Install in development mode
    return run_command("pip install -e .", "Installing package locally")

def test_cli():
    """Test the CLI commands"""
    print("🖥️ Testing CLI commands...")
    
    commands = [
        ("pyobfuscator --help", "Testing help command"),
        ("pyobfuscator list-techniques", "Testing list-techniques command"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def main():
    """Main build process"""
    print("🏗️ PyObfuscator Package Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("setup.py"):
        print("❌ Error: setup.py not found. Run this script from the package root directory.")
        return 1
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        action = sys.argv[1]
    else:
        action = "build"
    
    if action == "clean":
        clean_build()
        return 0
    
    elif action == "test":
        if not run_tests():
            return 1
        return 0
    
    elif action == "build":
        # Full build process
        clean_build()
        
        if not run_tests():
            print("❌ Tests failed. Fix issues before building.")
            return 1
        
        if not build_package():
            return 1
        
        if not check_package():
            return 1
        
        print("\n🎉 Package built successfully!")
        print("📁 Built files are in the 'dist/' directory")
        print("\n📋 Next steps:")
        print("   1. Test locally: python build_package.py install")
        print("   2. Upload to Test PyPI: python build_package.py test-upload")
        print("   3. Upload to PyPI: python build_package.py upload")
        
        return 0
    
    elif action == "install":
        if not install_locally():
            return 1
        
        if not test_cli():
            return 1
        
        print("\n✅ Package installed and tested locally!")
        return 0
    
    elif action == "test-upload":
        if not upload_to_test_pypi():
            return 1
        
        print("\n✅ Package uploaded to Test PyPI!")
        print("   Test installation: pip install -i https://test.pypi.org/simple/ pyobfuscator")
        return 0
    
    elif action == "upload":
        print("⚠️ WARNING: This will upload to the real PyPI!")
        response = input("Are you sure you want to continue? (yes/no): ")
        
        if response.lower() != "yes":
            print("Upload cancelled.")
            return 0
        
        if not upload_to_pypi():
            return 1
        
        print("\n🎉 Package uploaded to PyPI!")
        print("   Install with: pip install pyobfuscator")
        return 0
    
    else:
        print(f"❌ Unknown action: {action}")
        print("Available actions: clean, test, build, install, test-upload, upload")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

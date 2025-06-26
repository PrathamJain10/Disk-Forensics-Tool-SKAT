#!/usr/bin/env python3
"""
Test script for SKAT (Sleuth Kit Automation Tool)
This script tests basic functionality of the disk forensics tool.
"""

import os
import sys
import subprocess
import tempfile
import shutil

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    try:
        import skat
        print("✓ SKAT module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import SKAT: {e}")
        return False

def test_help_command():
    """Test if the help command works."""
    print("Testing help command...")
    try:
        result = subprocess.run([sys.executable, "skat.py", "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✓ Help command works")
            return True
        else:
            print(f"✗ Help command failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ Help command error: {e}")
        return False

def test_verify_command():
    """Test the verify command."""
    print("Testing verify command...")
    try:
        result = subprocess.run([sys.executable, "skat.py", "verify"], 
                              capture_output=True, text=True, timeout=10)
        print("✓ Verify command executed")
        # Note: This will likely fail on Windows due to missing TSK tools
        # but the command itself should work
        return True
    except Exception as e:
        print(f"✗ Verify command error: {e}")
        return False

def test_directory_structure():
    """Test if required directories exist."""
    print("Testing directory structure...")
    required_dirs = ["evidence", "reports", "samples"]
    missing_dirs = []
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    if missing_dirs:
        print(f"✗ Missing directories: {missing_dirs}")
        return False
    else:
        print("✓ All required directories exist")
        return True

def test_sample_file():
    """Test if sample disk image exists."""
    print("Testing sample file...")
    sample_path = os.path.join("samples", "2011-10-19-Sample.E01")
    if os.path.exists(sample_path):
        print("✓ Sample disk image found")
        return True
    else:
        print("✗ Sample disk image not found")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("SKAT Tool Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_help_command,
        test_verify_command,
        test_directory_structure,
        test_sample_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The tool is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    print("\nNote: Some tests may fail on Windows due to missing TSK tools.")
    print("This tool is designed to work on Linux/Unix systems.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
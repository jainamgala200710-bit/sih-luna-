#!/usr/bin/env python
"""
Test script to verify the LunaAlign AI environment setup.
"""
import sys
import os

def test_imports():
    """Test that core packages can be imported."""
    try:
        import cv2
        import numpy as np
        import scipy
        print("[PASS] Core packages imported successfully")
        print(f"  OpenCV version: {cv2.__version__}")
        print(f"  NumPy version: {np.__version__}")
        print(f"  SciPy version: {scipy.__version__}")
        return True
    except ImportError as e:
        print(f"[FAIL] Failed to import packages: {e}")
        return False

def test_directory_structure():
    """Test that key directories exist."""
    required_dirs = [
        'data/raw',
        'data/processed',
        'data/synthetic',
        'data/pairs',
        'data/metadata',
        'data/splits',
        'src',
        'src/preprocessing',
        'src/matching',
        'src/evaluation',
        'notebooks',
        'tests',
        'docs'
    ]
    
    missing_dirs = []
    for dir_path in required_dirs:
        if not os.path.isdir(dir_path):
            missing_dirs.append(dir_path)
    
    if missing_dirs:
        print(f"[FAIL] Missing directories: {missing_dirs}")
        return False
    else:
        print("[PASS] Directory structure verified")
        return True

def test_python_command():
    """Test that we're using the correct Python executable."""
    print(f"[PASS] Python executable: {sys.executable}")
    print(f"[PASS] Python version: {sys.version}")
    return True

def main():
    """Run all tests."""
    print("LunaAlign AI Environment Setup Test")
    print("=" * 40)
    
    tests = [
        test_python_command,
        test_imports,
        test_directory_structure
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    if passed == total:
        print("[PASS] All tests passed! Environment is ready.")
        return 0
    else:
        print("[FAIL] Some tests failed. Please check the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

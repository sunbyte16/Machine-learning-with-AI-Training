#!/usr/bin/env python3
"""
Lane Detection Application Launcher
Created by Sunil

This script provides a simple way to run the integrated lane detection application.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'opencv-python',
        'Pillow',
        'numpy',
        'matplotlib',
        'moviepy',
        'tkinter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'opencv-python':
                import cv2
            elif package == 'Pillow':
                import PIL
            elif package == 'numpy':
                import numpy
            elif package == 'matplotlib':
                import matplotlib
            elif package == 'moviepy':
                import moviepy
            elif package == 'tkinter':
                import tkinter
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nTo install missing packages, run:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    print("=" * 50)
    print("Lane Detection Application")
    print("Created by Sunil")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install missing dependencies and try again.")
        return
    
    # Check if video file exists
    video_file = "test2.mp4"
    if not os.path.exists(video_file):
        print(f"\nWarning: {video_file} not found!")
        print("Please make sure you have a video file named 'test2.mp4' in the current directory.")
        print("You can use any MP4 video file and rename it to 'test2.mp4'")
        
        response = input("\nDo you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Run the integrated application
    try:
        print("\nStarting Lane Detection Application...")
        print("Features:")
        print("  - Real-time lane detection")
        print("  - Side-by-side video comparison")
        print("  - Save processed video")
        print("  - Interactive controls")
        print("\nPress Ctrl+C to stop the application")
        print("-" * 50)
        
        # Import and run the integrated app
        from integrated_app import main as run_app
        run_app()
        
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
    except Exception as e:
        print(f"\nError running application: {e}")
        print("Please check that all files are in the correct location.")

if __name__ == "__main__":
    main()

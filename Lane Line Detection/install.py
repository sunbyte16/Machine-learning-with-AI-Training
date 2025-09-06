#!/usr/bin/env python3
"""
Professional Installation Script for Lane Detection Application
Created by Sunil Sharma ❤️

This script provides a complete setup for the Lane Detection Application.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class Colors:
    """ANSI color codes for terminal output"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    """Print the application banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🚗 Lane Detection Application - Professional Setup 🚗    ║
║                                                              ║
║              Created with ❤️ by Sunil Sharma                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
"""
    print(banner)

def print_step(step_num, total_steps, message):
    """Print a formatted step message"""
    print(f"\n{Colors.BLUE}[{step_num}/{total_steps}]{Colors.END} {Colors.BOLD}{message}{Colors.END}")
    print("-" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print_step(1, 6, "🐍 Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"{Colors.RED}❌ Python 3.8+ is required. Current version: {version.major}.{version.minor}{Colors.END}")
        return False
    
    print(f"{Colors.GREEN}✅ Python {version.major}.{version.minor}.{version.micro} detected{Colors.END}")
    return True

def check_system_requirements():
    """Check system requirements"""
    print_step(2, 6, "💻 Checking System Requirements")
    
    system = platform.system()
    print(f"Operating System: {system}")
    
    if system == "Windows":
        print(f"{Colors.YELLOW}⚠️  Windows detected - some features may require additional setup{Colors.END}")
    elif system == "Darwin":
        print(f"{Colors.GREEN}✅ macOS detected - full compatibility{Colors.END}")
    elif system == "Linux":
        print(f"{Colors.GREEN}✅ Linux detected - full compatibility{Colors.END}")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print_step(3, 6, "📦 Installing Dependencies")
    
    try:
        # Upgrade pip
        print("Upgrading pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        
        # Install requirements
        print("Installing project dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print(f"{Colors.GREEN}✅ All dependencies installed successfully{Colors.END}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}❌ Error installing dependencies: {e}{Colors.END}")
        return False

def create_directories():
    """Create necessary directories"""
    print_step(4, 6, "📁 Creating Project Directories")
    
    directories = [
        "output",
        "test_videos",
        "logs",
        "temp"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"Created directory: {directory}")
    
    print(f"{Colors.GREEN}✅ Project directories created{Colors.END}")

def setup_environment():
    """Setup environment variables and configuration"""
    print_step(5, 6, "⚙️ Setting Up Environment")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        with open(env_file, "w") as f:
            f.write("# Lane Detection Application Environment Variables\n")
            f.write("DEBUG=False\n")
            f.write("LOG_LEVEL=INFO\n")
            f.write("VIDEO_FPS=30\n")
            f.write("DETECTION_THRESHOLD=0.5\n")
        print("Created .env file")
    
    print(f"{Colors.GREEN}✅ Environment configured{Colors.END}")

def test_installation():
    """Test the installation"""
    print_step(6, 6, "🧪 Testing Installation")
    
    try:
        # Test imports
        print("Testing imports...")
        import cv2
        import numpy as np
        import matplotlib.pyplot as plt
        from PIL import Image
        import tkinter as tk
        
        print(f"{Colors.GREEN}✅ All imports successful{Colors.END}")
        
        # Test OpenCV
        print("Testing OpenCV...")
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
        print(f"{Colors.GREEN}✅ OpenCV working correctly{Colors.END}")
        
        return True
        
    except ImportError as e:
        print(f"{Colors.RED}❌ Import error: {e}{Colors.END}")
        return False
    except Exception as e:
        print(f"{Colors.RED}❌ Test error: {e}{Colors.END}")
        return False

def print_success_message():
    """Print success message with next steps"""
    success_message = f"""
{Colors.GREEN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║                    🎉 Installation Complete! 🎉              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}

{Colors.CYAN}Next Steps:{Colors.END}
1. Place your video file as 'test2.mp4' in the project directory
2. Run the application: {Colors.BOLD}python run_app.py{Colors.END}
3. Or try the demo: {Colors.BOLD}python demo.py{Colors.END}

{Colors.CYAN}Available Commands:{Colors.END}
• {Colors.BOLD}python run_app.py{Colors.END}     - Run the main application
• {Colors.BOLD}python demo.py{Colors.END}       - Run with sample video
• {Colors.BOLD}python integrated_app.py{Colors.END} - Run directly

{Colors.CYAN}Documentation:{Colors.END}
• README.md - Complete documentation
• CONTRIBUTING.md - Contribution guidelines

{Colors.CYAN}Support:{Colors.END}
• GitHub: https://github.com/sunbyte16
• LinkedIn: https://www.linkedin.com/in/sunil-kumar-bb88bb31a/
• Portfolio: https://lively-dodol-cc397c.netlify.app

{Colors.MAGENTA}Thank you for using Lane Detection Application!{Colors.END}
{Colors.RED}Made with ❤️ by Sunil Sharma{Colors.END}
"""
    print(success_message)

def main():
    """Main installation function"""
    print_banner()
    
    # Check if we're in the right directory
    if not Path("requirements.txt").exists():
        print(f"{Colors.RED}❌ requirements.txt not found. Please run this script from the project root directory.{Colors.END}")
        return False
    
    steps = [
        check_python_version,
        check_system_requirements,
        install_dependencies,
        create_directories,
        setup_environment,
        test_installation
    ]
    
    for step in steps:
        if not step():
            print(f"\n{Colors.RED}❌ Installation failed at step: {step.__name__}{Colors.END}")
            return False
    
    print_success_message()
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Installation cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)

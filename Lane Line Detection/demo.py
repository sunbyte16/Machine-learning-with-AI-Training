#!/usr/bin/env python3
"""
Lane Detection Application Demo
Created by Sunil Sharma ❤️

This script demonstrates the lane detection capabilities with sample data.
"""

import cv2
import numpy as np
import os
from integrated_app import process_image

def create_sample_video():
    """Create a sample video for demonstration if test2.mp4 doesn't exist"""
    print("🎬 Creating sample video for demonstration...")
    
    # Create a simple road-like video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('test2.mp4', fourcc, 20.0, (640, 480))
    
    for i in range(200):  # 10 seconds at 20fps
        # Create a frame with road-like appearance
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Road surface (gray)
        cv2.rectangle(frame, (0, 300), (640, 480), (50, 50, 50), -1)
        
        # Lane lines (white)
        cv2.line(frame, (200, 300), (200 + i*2, 480), (255, 255, 255), 8)
        cv2.line(frame, (440, 300), (440 + i*2, 480), (255, 255, 255), 8)
        
        # Center line (yellow, dashed)
        if i % 10 < 5:
            cv2.line(frame, (320, 300), (320 + i, 480), (0, 255, 255), 6)
        
        # Add some noise for realism
        noise = np.random.randint(0, 50, (480, 640, 3), dtype=np.uint8)
        frame = cv2.add(frame, noise)
        
        out.write(frame)
    
    out.release()
    print("✅ Sample video created: test2.mp4")

def run_demo():
    """Run the lane detection demo"""
    print("🚗 Lane Detection Application Demo")
    print("=" * 50)
    print("Created by Sunil Sharma ❤️")
    print("=" * 50)
    
    # Check if video exists, create sample if not
    if not os.path.exists('test2.mp4'):
        create_sample_video()
    
    # Run the main application
    try:
        from integrated_app import main
        print("\n🎯 Starting Lane Detection Application...")
        print("Features:")
        print("  🔍 Real-time lane detection")
        print("  📊 Side-by-side video comparison")
        print("  💾 Save processed video")
        print("  🎛️ Interactive controls")
        print("\nPress Ctrl+C to stop the application")
        print("-" * 50)
        
        main()
        
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user. Thank you!")
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")
        print("Please check that all dependencies are installed.")

if __name__ == "__main__":
    run_demo()

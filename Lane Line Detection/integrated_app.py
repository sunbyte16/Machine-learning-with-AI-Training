import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from moviepy.editor import VideoFileClip
import math

# Global variables for lane detection
first_frame = 1
cache = None

def interested_region(img, vertices):
    if len(img.shape) > 2: 
        mask_color_ignore = (255,) * img.shape[2]
    else:
        mask_color_ignore = 255
        
    cv2.fillPoly(np.zeros_like(img), vertices, mask_color_ignore)
    return cv2.bitwise_and(img, np.zeros_like(img))

def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    lines_drawn(line_img, lines)
    return line_img

def lines_drawn(img, lines, color=[255, 0, 0], thickness=6):
    global cache
    global first_frame
    slope_l, slope_r = [], []
    lane_l, lane_r = [], []

    α = 0.2 
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            slope = (y2-y1)/(x2-x1)
            if slope > 0.4:
                slope_r.append(slope)
                lane_r.append(line)
            elif slope < -0.4:
                slope_l.append(slope)
                lane_l.append(line)
        img.shape[0] = min(y1, y2, img.shape[0])
    
    if((len(lane_l) == 0) or (len(lane_r) == 0)):
        print('no lane detected')
        return 1
        
    slope_mean_l = np.mean(slope_l, axis=0)
    slope_mean_r = np.mean(slope_r, axis=0)
    mean_l = np.mean(np.array(lane_l), axis=0)
    mean_r = np.mean(np.array(lane_r), axis=0)
    
    if ((slope_mean_r == 0) or (slope_mean_l == 0)):
        print('dividing by zero')
        return 1
    
    x1_l = int((img.shape[0] - mean_l[0][1] - (slope_mean_l * mean_l[0][0]))/slope_mean_l) 
    x2_l = int((img.shape[0] - mean_l[0][1] - (slope_mean_l * mean_l[0][0]))/slope_mean_l)   
    x1_r = int((img.shape[0] - mean_r[0][1] - (slope_mean_r * mean_r[0][0]))/slope_mean_r)
    x2_r = int((img.shape[0] - mean_r[0][1] - (slope_mean_r * mean_r[0][0]))/slope_mean_r)
    
    if x1_l > x1_r:
        x1_l = int((x1_l+x1_r)/2)
        x1_r = x1_l
        y1_l = int((slope_mean_l * x1_l ) + mean_l[0][1] - (slope_mean_l * mean_l[0][0]))
        y1_r = int((slope_mean_r * x1_r ) + mean_r[0][1] - (slope_mean_r * mean_r[0][0]))
        y2_l = int((slope_mean_l * x2_l ) + mean_l[0][1] - (slope_mean_l * mean_l[0][0]))
        y2_r = int((slope_mean_r * x2_r ) + mean_r[0][1] - (slope_mean_r * mean_r[0][0]))
    else:
        y1_l = img.shape[0]
        y2_l = img.shape[0]
        y1_r = img.shape[0]
        y2_r = img.shape[0]
      
    present_frame = np.array([x1_l, y1_l, x2_l, y2_l, x1_r, y1_r, x2_r, y2_r], dtype="float32")
    
    if first_frame == 1:
        next_frame = present_frame        
        first_frame = 0        
    else:
        prev_frame = cache
        next_frame = (1-α)*prev_frame + α*present_frame
             
    cv2.line(img, (int(next_frame[0]), int(next_frame[1])), (int(next_frame[2]), int(next_frame[3])), color, thickness)
    cv2.line(img, (int(next_frame[4]), int(next_frame[5])), (int(next_frame[6]), int(next_frame[7])), color, thickness)
    
    cache = next_frame

def weighted_img(img, initial_img, α=0.8, β=1., λ=0.):
    return cv2.addWeighted(initial_img, α, img, β, λ)

def process_image(image):
    global first_frame
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    lower_yellow = np.array([20, 100, 100], dtype="uint8")
    upper_yellow = np.array([30, 255, 255], dtype="uint8")

    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    mask_white = cv2.inRange(gray_image, 200, 255)
    mask_yw = cv2.bitwise_or(mask_white, mask_yellow)
    mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)

    gauss_gray = cv2.GaussianBlur(mask_yw_image, (5, 5), 0)
    canny_edges = cv2.Canny(gauss_gray, 50, 150)

    imshape = image.shape
    lower_left = [imshape[1]/9, imshape[0]]
    lower_right = [imshape[1]-imshape[1]/9, imshape[0]]
    top_left = [imshape[1]/2-imshape[1]/8, imshape[0]/2+imshape[0]/10]
    top_right = [imshape[1]/2+imshape[1]/8, imshape[0]/2+imshape[0]/10]
    vertices = [np.array([lower_left, top_left, top_right, lower_right], dtype=np.int32)]
    roi_image = interested_region(canny_edges, vertices)

    theta = np.pi/180
    line_image = hough_lines(roi_image, 4, theta, 30, 100, 180)
    result = weighted_img(line_image, image, α=0.8, β=1., λ=0.)
    return result

class LaneDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lane Detection - Sunil")
        self.root.geometry("1400x800+50+50")
        
        # Video capture objects
        self.cap_original = None
        self.cap_processed = None
        self.is_processing = False
        
        # Initialize GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Logo and title
        try:
            img = ImageTk.PhotoImage(Image.open(os.path.join(os.path.dirname(__file__), "logo.png")))
            heading = Label(self.root, image=img, text="Lane-Line Detection")
            heading.pack()
        except:
            heading = Label(self.root, text="Lane-Line Detection", font=('arial', 20, 'bold'))
            heading.pack()
        
        heading2 = Label(self.root, text="Lane-Line Detection by Sunil", pady=10, font=('arial', 30, 'bold'))
        heading2.configure(foreground='#364156')
        heading2.pack()
        
        # Control buttons frame
        control_frame = Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_btn = Button(control_frame, text="Start Processing", command=self.start_processing, 
                               bg='green', fg='white', font=('arial', 12, 'bold'))
        self.start_btn.pack(side=LEFT, padx=5)
        
        self.stop_btn = Button(control_frame, text="Stop Processing", command=self.stop_processing, 
                              bg='red', fg='white', font=('arial', 12, 'bold'))
        self.stop_btn.pack(side=LEFT, padx=5)
        
        self.save_btn = Button(control_frame, text="Save Processed Video", command=self.save_video, 
                              bg='blue', fg='white', font=('arial', 12, 'bold'))
        self.save_btn.pack(side=LEFT, padx=5)
        
        # Video display frame
        video_frame = Frame(self.root)
        video_frame.pack(pady=10)
        
        # Original video label
        original_label = Label(video_frame, text="Original Video", font=('arial', 14, 'bold'))
        original_label.pack(side=LEFT, padx=20)
        
        # Processed video label
        processed_label = Label(video_frame, text="Processed Video (Lane Detection)", font=('arial', 14, 'bold'))
        processed_label.pack(side=RIGHT, padx=20)
        
        # Video display labels
        self.lmain_original = Label(self.root, bg='black')
        self.lmain_processed = Label(self.root, bg='black')
        
        self.lmain_original.pack(side=LEFT, padx=10)
        self.lmain_processed.pack(side=RIGHT, padx=10)
        
        # Status label
        self.status_label = Label(self.root, text="Ready to start processing", 
                                 font=('arial', 12), fg='blue')
        self.status_label.pack(pady=10)
        
        # Exit button
        exit_button = Button(self.root, text='Quit', fg="red", command=self.quit_app, 
                           font=('arial', 12, 'bold'))
        exit_button.pack(side=BOTTOM, pady=10)
        
    def start_processing(self):
        """Start the video processing"""
        try:
            video_path = os.path.join(os.path.dirname(__file__), "test2.mp4")
            if not os.path.exists(video_path):
                self.status_label.config(text="Error: test2.mp4 not found!", fg='red')
                return
                
            self.cap_original = cv2.VideoCapture(video_path)
            self.cap_processed = cv2.VideoCapture(video_path)
            
            if not self.cap_original.isOpened() or not self.cap_processed.isOpened():
                self.status_label.config(text="Error: Cannot open video file!", fg='red')
                return
                
            self.is_processing = True
            self.status_label.config(text="Processing video...", fg='green')
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            
            # Start video display
            self.show_original_video()
            self.show_processed_video()
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg='red')
    
    def stop_processing(self):
        """Stop the video processing"""
        self.is_processing = False
        self.status_label.config(text="Processing stopped", fg='orange')
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        
        if self.cap_original:
            self.cap_original.release()
        if self.cap_processed:
            self.cap_processed.release()
    
    def show_original_video(self):
        """Display original video"""
        if not self.is_processing or not self.cap_original:
            return
            
        ret, frame = self.cap_original.read()
        if ret and frame is not None:
            frame = cv2.resize(frame, (600, 400))
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain_original.imgtk = imgtk
            self.lmain_original.configure(image=imgtk)
        
        if self.is_processing:
            self.root.after(30, self.show_original_video)
    
    def show_processed_video(self):
        """Display processed video with lane detection"""
        if not self.is_processing or not self.cap_processed:
            return
            
        ret, frame = self.cap_processed.read()
        if ret and frame is not None:
            # Process frame for lane detection
            processed_frame = process_image(frame)
            processed_frame = cv2.resize(processed_frame, (600, 400))
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            self.lmain_processed.imgtk = imgtk
            self.lmain_processed.configure(image=imgtk)
        
        if self.is_processing:
            self.root.after(30, self.show_processed_video)
    
    def save_video(self):
        """Save the processed video to file"""
        try:
            video_path = os.path.join(os.path.dirname(__file__), "test2.mp4")
            output_path = os.path.join(os.path.dirname(__file__), "output_lane_detection.mp4")
            
            self.status_label.config(text="Saving processed video...", fg='blue')
            self.root.update()
            
            # Process video and save
            clip = VideoFileClip(video_path)
            processed_clip = clip.fl_image(process_image)
            processed_clip.write_videofile(output_path, audio=False)
            
            self.status_label.config(text=f"Video saved as: {output_path}", fg='green')
            
        except Exception as e:
            self.status_label.config(text=f"Error saving video: {str(e)}", fg='red')
    
    def quit_app(self):
        """Quit the application"""
        self.stop_processing()
        self.root.quit()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = LaneDetectionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

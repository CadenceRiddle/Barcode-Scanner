import cv2
import tkinter as tk
from tkinter import Button
from PIL import Image, ImageTk

# Initialize Tkinter window
window = tk.Tk()
window.title("Camera Feed")
window.geometry("800x600")

# Create a label to display the video feed
video_label = tk.Label(window)
video_label.pack()

# Open the camera (usually camera index 0 is the default webcam)
cap = cv2.VideoCapture(0)

def update_frame():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret:
        # Convert the frame (OpenCV uses BGR, Tkinter expects RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Update the label with the new frame
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
    # Call this function again after 10 ms
    video_label.after(10, update_frame)

def close_camera():
    # Release the camera and close the window
    cap.release()
    window.quit()

# Add the "Exit" button
exit_button = Button(window, text="Exit", command=close_camera)
exit_button.pack()

# Start updating the frames
update_frame()

# Run the Tkinter event loop
window.mainloop()

# Make sure the camera is released if the window is closed
cap.release()
cv2.destroyAllWindows()

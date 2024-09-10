import cv2

# Function to detect shapes in a frame
def detect_shapes(frame):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply GaussianBlur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edge-detected frame
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        # Approximate the contour to a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Draw the contours
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)

        # Detect and label the shape based on the number of vertices
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            # Check if it's a square or rectangle
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = w / float(h)
            if 0.95 <= aspect_ratio <= 1.05:
                shape = "Square"
            else:
                shape = "Rectangle"
        elif len(approx) > 4:
            shape = "Circle"
        else:
            shape = "Unknown"
        
        # Find the center of the shape and label it
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0

        # Display the shape name on the frame
        cv2.putText(frame, shape, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame

# Access webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

# Continuously capture frames from the webcam
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to grab a frame.")
        break

    # Process the frame to detect shapes
    frame_with_shapes = detect_shapes(frame)
    
    # Display the processed frame
    cv2.imshow('Shape Detection in Live Video', frame_with_shapes)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

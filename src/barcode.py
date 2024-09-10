import cv2
from pyzbar import pyzbar

# Function to detect and decode barcodes
def detect_barcodes(frame):
    # Detect barcodes in the frame using pyzbar
    barcodes = pyzbar.decode(frame)

    for barcode in barcodes:
        # Extract the bounding box location of the barcode
        (x, y, w, h) = barcode.rect
        # Draw a rectangle around the barcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # The data is byte object, so decode it to string
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type

        # Draw the barcode data and type on the frame
        text = f"{barcode_data} ({barcode_type})"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return frame

# Access the webcam
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

    # Process the frame to detect barcodes
    frame_with_barcodes = detect_barcodes(frame)

    # Display the processed frame
    cv2.imshow('Barcode Detection in Live Video', frame_with_barcodes)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

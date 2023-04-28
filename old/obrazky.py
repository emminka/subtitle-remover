import cv2

# Load the video
video_path = r'C:\Users\Emma\Desktop\Bakalarka\web\na_masku.mp4'  # Replace with your video file path
cap = cv2.VideoCapture(video_path)

# Check if video file is opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Set the frame number to extract
frame_number = 10
# Read through the video frames until reaching the desired frame number
for i in range(frame_number):
    ret, frame = cap.read()

    # Check if end of video is reached before the desired frame number
    if not ret:
        print(f"Error: Frame {frame_number} is out of range.")
        cap.release()
        exit()

# Extract the desired frame
ret, frame = cap.read()

# Check if frame is read successfully
if not ret:
    print(f"Error: Could not extract frame {frame_number}.")
    cap.release()
    exit()

# Save the frame as an image
image_path = f'maska3.jpg'  # Replace with the desired image file path
cv2.imwrite(image_path, frame)

# Release the video file
cap.release()

print(f"Frame {frame_number} saved as {image_path}.")
import cv2

filepath =  r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\fr68.mp4'
count = 0

cap = cv2.VideoCapture(filepath)
# Loop through the frames of the video
while cap.isOpened():
    # Read the next frame
    ret, frame = cap.read()

    # Check if there was a problem reading the frame
    if not ret:
        break

    # Save the frame as an image file
    filename = 'hu{}.jpg'.format(count)
    cv2.imwrite(filename, frame)

    # Increment the counter
    count += 1

# Release the video file
cap.release()
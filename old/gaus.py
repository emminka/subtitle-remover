import cv2
import numpy as np

maska = cv2.imread(r'C:\Users\Emma\Desktop\Bakalarka\web\mamama2.jpg', 0)
framik = cv2.imread(r'C:\Users\Emma\Desktop\Bakalarka\web\hu39.jpg')

# Apply mask to the image
#masked_frame = cv2.bitwise_and(framik, framik, mask=maska)


def combine_images_with_mask(image1, image2, mask):
    """Function to combine two images using a mask."""
    # Convert the mask to a binary mask (0 or 255)
    #mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Resize the mask to match the input images
    #mask = cv2.resize(mask, (image1.shape[1], image1.shape[0]))

    mask = cv2.GaussianBlur(mask, (19,19), 0)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,10))
    dilatedMask = cv2.dilate(mask, kernel, iterations=3)

    mask3 = cv2.cvtColor(dilatedMask,cv2.COLOR_GRAY2RGB)
    normalized_mask3 = mask3.astype('float32') / 255.0

    #_, mask = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)

    # Create a white image of the same size as the input images
    combined_image = np.zeros_like(image1)
    combined_image.fill(255)

    # Use bitwise operations to combine the images based on the mask
    a = cv2.multiply(1 - normalized_mask3, image1.astype('float32')) / 255.0
    b = cv2.multiply(normalized_mask3, image2.astype('float32')) / 255.0

    return cv2.add(a,b)





# Apply Gaussian blur to the masked image
gausvka = cv2.GaussianBlur(framik, (151,151), 0)
#gausvka_masked = cv2.bitwise_and(gausvka, gausvka, mask=maska)

# Apply inpainting to the original image
no_subtitles_frame = cv2.inpaint(framik, maska, 3, cv2.INPAINT_NS)
no_subtitles_frame2 = cv2.inpaint(framik, maska, 3, cv2.INPAINT_TELEA)

vysledocek = combine_images_with_mask(framik,gausvka,maska)



# Resize the frames for display
width = 960  # Specify the desired width
height = 540  # Specify the desired height
smaller_frame1 = cv2.resize(no_subtitles_frame, (width, height))
smaller_frame4 = cv2.resize(no_subtitles_frame2, (width, height))
#smaller_frame2 = cv2.resize(gausvka_masked, (width, height))
smaller_frame3 = cv2.resize(gausvka, (width, height))
smaller_frame5 = cv2.resize(vysledocek, (width, height))

# Display the inpainted and blurred frames
cv2.imshow('InpaintingNS', smaller_frame1)
cv2.imshow('InpaintingTELEA', smaller_frame4)
#cv2.imshow('Gaussian Blur', smaller_frame2)
cv2.imshow('Pred Blur', smaller_frame3)
cv2.imshow('HOTOVCO', smaller_frame5)
cv2.waitKey(0)
cv2.destroyAllWindows()
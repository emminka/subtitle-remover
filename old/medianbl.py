import cv2
import numpy as np


maska = cv2.imread(r'C:\Users\Emma\Desktop\Bakalarka\web\mamama2.jpg', 0)
framik = cv2.imread(r'C:\Users\Emma\Desktop\Bakalarka\web\hu39.jpg')

# Apply mask to the image
#masked_frame = cv2.bitwise_and(framik, framik, mask=maska)


def combine_images_with_mask(image1,  mask):
    """Function to combine two images using a mask."""

    #mask = cv2.GaussianBlur(mask, (5,5), 0)

   # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
   # dilatedMask = cv2.dilate(mask, kernel, iterations=1)

    mask3 = cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    normalized_mask3 = mask3.astype('float32') / 255.0

    #_, mask = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)

    # Create a white image of the same size as the input images
    combined_image = np.zeros_like(image1)
    combined_image.fill(255)

    # Use bitwise operations to combine the images based on the mask
    a = np.multiply(1 - normalized_mask3, framik.astype('float32')) / 255.0
    b = np.multiply(normalized_mask3, medianbl.astype('float32')) / 255.0

    return np.add(a,b)

# Apply Gaussian blur to the masked image



#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#pokus = cv2.filter2D(framik, kernel, iterations=5)





#pokus = cv2.buildPyramid(framik,0)
#gausvka_masked = cv2.bitwise_and(gausvka, gausvka, mask=maska)

# Apply inpainting to the original image

#vysledocek = combine_images_with_mask(medianbl,maska)

#pokus = cv2.copyTo(bilaaa, maska)

pokus = cv2.bilateralFilter(framik,15,75,75)

#pokus = cv2.pyrMeanShiftFiltering(framik, 10, 20)


# Resize the frames for display
width = 960  # Specify the desired width
height = 540  # Specify the desired height

#smaller_frame2 = cv2.resize(vysledocek, (width, height))

smaller_frame6 = cv2.resize(pokus, (width, height))

# Display the inpainted and blurred frames
#cv2.imshow('Blur', smaller_frame1)
#cv2.imshow('InpaintingTELEA', smaller_frame4)
#cv2.imshow('vysledok', smaller_frame2)
cv2.imshow('pokus', smaller_frame6)
#cv2.imshow('gaus', smaller_frame5)
cv2.waitKey(0)
cv2.destroyAllWindows()
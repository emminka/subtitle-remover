
from __future__ import print_function
import cv2
import argparse


prva =  r'C:\Users\Emma\Desktop\Bakalarka\web\text12.png'
druha =  r'C:\Users\Emma\Desktop\Bakalarka\web\text11.png'
# Načtení prvního obrázku
img1 = cv2.imread(prva, 0)

# Načtení druhého obrázku
img2 = cv2.imread(druha, 0)

# Odečtení druhého obrázku od prvního
img_subtract = cv2.absdiff(img1, img2)

cv2.imshow('Subst', img_subtract)

ret, thresh = cv2.threshold(img_subtract,100, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
dilated = cv2.dilate(thresh, kernel, iterations=1)





# Zobrazení výsledného obrázku

cv2.imshow('Thresholded Image', thresh)

cv2.imshow('Dilated Image', dilated)

cv2.imwrite('maska_vysledok_dilat.jpg', dilated)
cv2.imwrite('maska_tresh.jpg', thresh)
cv2.imwrite('maska_rozdiel.jpg', img_subtract)

cv2.waitKey(0)
cv2.destroyAllWindows()

from __future__ import print_function
import cv2
import argparse


prva =  r'C:\Users\Emma\Desktop\Bakalarka\old\hormaska_nic.jpg'
druha =  r'C:\Users\Emma\Desktop\Bakalarka\old\hormaska_t.jpg'
# Načtení prvního obrázku
img1 = cv2.imread(prva,0)

# Načtení druhého obrázku
img2 = cv2.imread(druha, 0)

# Odečtení druhého obrázku od prvního
img_subtract = cv2.absdiff(img1, img2)

#cv2.imshow('Subst', img_subtract)

ret, thresh = cv2.threshold(img_subtract,100, 255, cv2.THRESH_BINARY)

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8,8))
dilated = cv2.dilate(thresh, kernel, iterations=2)





# Zobrazení výsledného obrázku

#cv2.imshow('fit_tresh192.jpg', dilated)
#cv2.imwrite('fit_ciernob.jpg', img1)

cv2.imwrite('2maska.jpg', dilated)

#cv2.imwrite('maska_vysledok_dilat.jpg', dilated)
#cv2.imwrite('maska_tresh.jpg', thresh)
#cv2.imwrite('maska_rozdiel.jpg', img_subtract)

cv2.waitKey(0)
cv2.destroyAllWindows()
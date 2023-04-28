import cv2

path_obrazok = r'C:\Users\Emma\Desktop\Bakalarka\web\fotky\fit.jpg' 
path_maska =  r'C:\Users\Emma\Desktop\Bakalarka\web\fotky\maska.jpg' 
# Načítanie obrázku
obrazok = cv2.imread(path_obrazok)

# Načítanie masky
maska = cv2.imread(path_maska, 0)  # Načítanie masky ako čiernobielej

# Aplikácia in-paintingu na obrázok s použitím masky
obrazok_inpaint = cv2.inpaint(obrazok, maska, 3, cv2.INPAINT_TELEA)
obrazok_inpaint = cv2.inpaint(obrazok, maska, 3, cv2.INPAINT_TELEA)
medianblur_frame = cv2.medianBlur(obrazok, 25)

cv2.imwrite('fit_median.jpg', medianblur_frame)
cv2.imshow('Obrázok s in-paintingom', medianblur_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
vidcap = cv2.VideoCapture( r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\titulky.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(r'C:\Users\Emma\Desktop\Bakalarka\web\FuseFormer\data\DAVIS\JPEGImages\pepa\%d.jpg' % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  count += 1
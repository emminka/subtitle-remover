import matplotlib.pyplot as plt

import keras_ocr
import os
import sys

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
sourceFile  = open('output.txt','w')
pipeline = keras_ocr.pipeline.Pipeline()

pathto1 = r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\text1.PNG'
pathto11 = r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\text1.PNG'
pathto111 = r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\text1.PNG'
pathto1111 = r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\text1.PNG'

pathto2 = r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\text2.PNG'
pathto22 = r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\text2.PNG'
pathto3 = r'C:\Users\Emma\Desktop\Bakalarka\videos\videa_bakalarka\no_text.PNG'


cesticky=[pathto1]
cesticky2=[pathto2, pathto22,pathto3]
cesticky3=[pathto3, pathto1]
print(cesticky)
# Get a set of three example images
images = [
    keras_ocr.tools.read(img) for img in cesticky
]

images2 = [
    keras_ocr.tools.read(img) for img in cesticky2
]

images3 = [
    keras_ocr.tools.read(img) for img in cesticky3
]

print(len(images))
print(len(images2))
# Each list of predictions in prediction_groups is a list of
# (word, box) tuples.
prediction_groups = pipeline.recognize(images)
#prediction_groups2 = pipeline.recognize(images2)
#prediction_groups3 = pipeline.recognize(images3)


# Plot the predictions
#fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
#for ax, image, predictions in zip(axs, images, prediction_groups):
   # keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

print("huhuh")
#print(prediction_groups, file = sourceFile)
#print(prediction_groups)

for x in range(len(images)):
    print("number",x)
    for text, box in prediction_groups[x]:
        print(text)

#plt.show()


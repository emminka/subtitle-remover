import matplotlib.pyplot as plt

import keras_ocr
import os

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.
pipeline = keras_ocr.pipeline.Pipeline()

# Get a set of three example images
images = [
    keras_ocr.tools.read(url) for url in [
        'https://upload.wikimedia.org/wikipedia/commons/b/b4/EUBanana-500x112.jpg',
        'https://scontent-prg1-1.cdninstagram.com/v/t51.2885-15/331661481_5794284590685613_2433262251339321851_n.jpg?stp=dst-jpg_e35&_nc_ht=scontent-prg1-1.cdninstagram.com&_nc_cat=101&_nc_ohc=wYtFtjxtHJEAX9W2rHi&edm=AAAAAAABAAAA&ccb=7-5&ig_cache_key=MzA0MTY2NDEwODM1Nzg5ODI0NA%3D%3D.2-ccb7-5&oh=00_AfC9OZMtL1LktCKQ3-eJqwRnWQbn7zKp6s_j1LhGPf8MRA&oe=63F6B161&_nc_sid=022a36'
    ]
]

# Each list of predictions in prediction_groups is a list of
# (word, box) tuples.
prediction_groups = pipeline.recognize(images)

# Plot the predictions
fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
for ax, image, predictions in zip(axs, images, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

plt.show()


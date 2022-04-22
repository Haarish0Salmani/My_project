import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf 

model = tf.keras.models.load_model("RHL.model")

data = tf.keras.datasets.mnist

(x_train,y_train),(x_test,y_test) = data.load_data()

x_train = tf.keras.utils.normalize(x_train,axis=1)
x_test = tf.keras.utils.normalize(x_test,axis=1)


loss, accuracy = model.evaluate(x_test,y_test)



image_num = 1
while os.path.isfile(f"C:/Users/Haarish salmani/.spyder-py3/autosave/digits/image{image_num}.png"):
    try:
        img = cv2.imread(f"C:/Users/Haarish salmani/.spyder-py3/autosave/digits/image{image_num}.png")[:,:,:0]
        img =np.invert(np.array([img]))
        prediction = model.predict(img)
        print(f"the image is probably {np.argmax(prediction)}")
        plt.imshow(img[0],cmap= plt.cm.binary)
        plt.show()
    except:
        print("Error!")
    finally:
        image_num += 1
        
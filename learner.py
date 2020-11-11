from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout

class learner:
    @staticmethod
    def build(width, height, depth, classes):
        model = Sequential() #initialize the model
        inputShape = (height, width, depth)

        #First Set conv => relu => pool layers
        model.add(Conv2D(32, (5, 5), padding="same", input_shape=inputShape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        #Second Set
        model.add(Conv2D(32, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        #First Set fc => relu layers
        model.add(Flatten())
        model.add(Dense(64))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        #Second Set
        model.add(Dense(64))
        model.add(Activation("relu"))
        model.add(Dropout(0.5))

        #softmax classifier
        model.add(Dense(classes))
        model.add(Activation("Softmax"))

        return model


# %%

import sys
import os
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization
from keras.layers import AveragePooling2D
from keras.losses import categorical_crossentropy
from keras.optimizers import Adam
from keras.regularizers import l2
from keras.utils import np_utils


# %%

# Reading the dataset and initializing the train and test sets

df = pd.read_csv('fer2013.csv')
X_train, train_y, X_test, test_y = [], [], [], []

# Building the train and test sets with appropriate column headers

for index, row in df.iterrows():
    val = row['pixels'].split(" ")
    try:
        if 'Training' in row['Usage']:
            X_train.append(np.array(val, 'float32'))
            train_y.append(row['emotion'])
        elif 'PublicTest' in row['Usage']:
            X_test.append(np.array(val, 'float32'))
            test_y.append(row['emotion'])
    except:
        print(f"error occured at index :{index} and row:{row}")


# %%

# Optimally defining the training parameters of the model

num_features = 64
num_labels = 7
batch_size = 64
epochs = 200
width, height = 48, 48

# Converting the train and test sets to compatible numpy array format

X_train = np.array(X_train, 'float32')
train_y = np.array(train_y, 'float32')
X_test = np.array(X_test, 'float32')
test_y = np.array(test_y, 'float32')

train_y = np_utils.to_categorical(train_y, num_classes=num_labels)
test_y = np_utils.to_categorical(test_y, num_classes=num_labels)


# %%

# Normalizing the training and test data between 0 and 1

X_train -= np.mean(X_train, axis=0)
X_train /= np.std(X_train, axis=0)

X_test -= np.mean(X_test, axis=0)
X_test /= np.std(X_test, axis=0)

# Reshaping the input sets to fit the input layer of the model

X_train = X_train.reshape(X_train.shape[0], 48, 48, 1)
X_test = X_test.reshape(X_test.shape[0], 48, 48, 1)


# %%

# Initializing the neural network

model = Sequential()

# Defining the input layer and first convolution layer

model.add(Conv2D(64, kernel_size=(3, 3), activation='relu',
                 input_shape=(X_train.shape[1:])))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))


# Max Pooling the first layer and adding dropout

model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))


# Adding the second convolution layer

model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Conv2D(64, (3, 3), activation='relu'))

# Max Pooling the second layer and adding dropout

model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
model.add(Dropout(0.5))

# Adding the third convolution layer

model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(Conv2D(128, (3, 3), activation='relu'))

# Max Pooling the third layer

model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# Flattening the convolution layer's output

model.add(Flatten())

# Adding two dense layers with appropriate dropout

model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.2))

# Defining the output layer

model.add(Dense(num_labels, activation='softmax'))


# %%

# Defining the appropriate loss and optimization function for the model

model.compile(loss=categorical_crossentropy,
              optimizer=Adam(),
              metrics=['accuracy'])


# %%

# Training the model on predefined parameters

model.fit(X_train, train_y,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(X_test, test_y),
          shuffle=True)


# In[8]:

# Pickling the architecture and weights of the trained model

model.save('Facial_Emotion_Detection_Model_Weights.hdf5')

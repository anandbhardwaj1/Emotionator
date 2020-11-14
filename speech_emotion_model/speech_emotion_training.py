
# In[1]:

import os
import glob
from glob import glob
from tqdm import tqdm
import pandas as pd
import numpy as np
import soundfile
import pickle
import librosa
import matplotlib.pyplot as plt
import noisereduce as nr
from scipy.io import wavfile
from scipy.fftpack import fft
from python_speech_features import mfcc, logfbank
from sklearn.utils.class_weight import compute_class_weight
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from scipy import signal
get_ipython().magic('matplotlib inline')

# In[2]:

# Listing the files of the working directory (Utility function)

os.listdir(path='.\speech-emotion-recognition-ravdess-data(1)')


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

# Getting the list of files and initializing the filename of the training set

dirName = './speech-emotion-recognition-ravdess-data(1)'
listOfFiles = getListOfFiles(dirName)

# In[3]:

# Bucketing feature into categorical variable


def envelope(y, rate, threshold):
    mask = []
    y = pd.Series(y).apply(np.abs)
    y_mean = y.rolling(window=int(rate/10),  min_periods=1, center=True).mean()
    for mean in y_mean:
        if mean > threshold:
            mask.append(True)
        else:
            mask.append(False)
    return mask

# In[4]:
# Defining FFT features


def calc_fft(y, rate):
    n = len(y)
    freq = np.fft.rfftfreq(n, d=1/rate)
    Y = abs(np.fft.rfft(y)/n)
    return(Y, freq)

# In[19]:

# Defining feature sets

signals = {}
fft = {}
fbank = {}
mfccs = {}

# Loading training data for feature extraction

for file in range(0, len(listOfFiles), 1):
    signal, rate = librosa.load(listOfFiles[file], sr=44100)
    mask = envelope(signal, rate, 0.0005)
    signals[file] = signal
    fft[file] = calc_fft(signal, rate)
    bank = logfbank(signal[:rate], rate, nfilt=26, nfft=1103).T
    fbank[file] = bank
    mel = mfcc(signal[:rate], rate, numcep=13, nfilt=26, nfft=1103).T
    mfccs[file] = mel


# In[20]:

# Reading the training dataset

dynamic_file_path = r'.\speech-emotion-recognition-ravdess-data(1)\\**\\*.wav'
for file in tqdm(glob.glob(dynamic_file_path)):
    file_name = os.path.basename(file)
    signal, rate = librosa.load(file, sr=16000)
    mask = envelope(signal, rate, 0.0005)
    wavfile.write(filename=r'.\clean_speech_2\\'+str(file_name),
                  rate=rate,
                  data=signal[mask])


# In[21]:

# Extracting the training features

def extract_feature(file_name, mfcc, chroma, mel):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        s_rate = sound_file.samplerate
        if chroma:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=s_rate,
                                                 n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft,
                                                         sr=s_rate).T, axis=0)
        result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(X,
                                                         sr=s_rate).T, axis=0)
        result = np.hstack((result, mel))
    return result


# In[22]:

# List of possible emotions

emotions = {
  '01': 'neutral',
  '02': 'calm',
  '03':  'happy',
  '04': 'sad',
  '05': 'angry',
  '06': 'fearful',
  '07': 'disgust',
  '08': 'surprised'
}

# List of emotions to be determined by the model

observed_emotions = ['calm', 'happy', 'sad', 'angry']


# In[23]:
# Load the data and extract features for each sound file

def load_data(test_s=0.33):
    x, y = [], []
    answer = 0
    for file in glob.glob(r'C:\Users\anand\Desktop\clean_speech_2\\*.wav'):
        file_name = os.path.basename(file)
        emotion = emotions[file_name.split("-")[2]]
        if emotion not in observed_emotions:
            answer += 1
            continue
        feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
        x.append(feature)
        y.append([emotion, file_name])
    return train_test_split(np.array(x), y, test_size=test_s, random_state=9)


# In[24]:

# Defining training and test sets

x_train, x_test, y_trai, y_tes = load_data(test_size=0.25)
print(np.shape(x_train), np.shape(x_test), np.shape(y_trai), np.shape(y_tes))
y_test_map = np.array(y_tes).T
y_test = y_test_map[0]
test_filename = y_test_map[1]
y_train_map = np.array(y_trai).T
y_train = y_train_map[0]
train_filename = y_train_map[1]

# In[25]:

# Printing the number of features extracted

print(f'Features extracted: {x_train.shape[1]}')

# In[26]:

# Initializing the Multi Layer Perceptron Classifier

model = MLPClassifier(alpha=0.01,
                      batch_size=256,
                      epsilon=1e-08,
                      hidden_layer_sizes=(300,),
                      learning_rate='adaptive',
                      max_iter=500)

# In[27]:

# Training the model

model.fit(x_train, y_train)

# In[28]:

# Pickling the trained model

Pkl_Filename = "Emotion_Voice_Detection_Model.pkl"

with open(Pkl_Filename, 'wb') as file:
    pickle.dump(model, file)

# In[29]:

# Loading the pickled model
with open(Pkl_Filename, 'rb') as file:
    Emotion_Voice_Detection_Model = pickle.load(file)

# In[30]:

# Predicting the user emotion

y_pred = Emotion_Voice_Detection_Model.predict(x_test)

# In[31]:

# Printing and saving the prediction

y_pred1 = pd.DataFrame(y_pred, columns=['predictions'])
y_pred1['file_names'] = test_filename
print(y_pred1)
y_pred1.to_csv('predictionfinal.csv')

# In[32]:

# Calculating the accuracy of our model
accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)

# Printing the accuracy
print("Accuracy: {:.2f}%".format(accuracy*100))

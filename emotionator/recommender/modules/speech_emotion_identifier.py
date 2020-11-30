# %%

import pickle
import soundfile
import librosa
import numpy as np

# %%

model_name = 'Emotion_Voice_Detection_Model.pkl'
Pkl_Filename = f'..\\..\\Emotionator\\speech_emotion_model\\{model_name}'

# Loading the pickled model
with open(Pkl_Filename, 'rb') as file:
    Emotion_Voice_Detection_Model = pickle.load(file)


# %%

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


# %%

# 0 : calm, 1 : angry(disgust), 2 : sad(fearful), 3 : happy
def predict_speech(filepath):
    file = filepath
    ans = []
    new_feature = extract_feature(file, mfcc=True, chroma=True, mel=True)
    ans.append(new_feature)
    ans = np.array(ans)

    probabs = Emotion_Voice_Detection_Model.predict_proba(ans)
    return probabs

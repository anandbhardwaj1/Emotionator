import os
import wave
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from werkzeug.utils import secure_filename
from .modules import emotion_identifier as e_id
from .modules import speech_emotion_identifier as se_id
from .modules import facial_emotion_identifier as fe_id
from .modules import rec_system


def home(request):

    # View function for rendering the homepage template

    return render(request, 'home.html')


def identifyEmotion(request):

    # Function to return final emotion from  emotion probability values

    emotionLevels = {
        'happy': float(request.POST.get('happy')),
        'sad': float(request.POST.get('sad')),
        'angry': float(request.POST.get('angry')),
        'calm': float(request.POST.get('calm')),
        }

    primaryEmotion = e_id.determinePrimary(emotionLevels)
    enhancedEmotion = e_id.determineEnhanced(emotionLevels, primaryEmotion)

    return JsonResponse({
                        'primaryEmotion': primaryEmotion,
                        'enhancedEmotion': enhancedEmotion
                        })


def recGenres(request):

    # Function to return content genres for the specified emotion

    primaryEmotion = request.POST['primary-emotion']
    enhancedEmotion = request.POST['enhanced-emotion']

    genres = rec_system.getGenres(primaryEmotion, enhancedEmotion)

    newsContent = rec_system.getNews(genres['newsGenres'])
    videoContent = rec_system.getVideos(genres['videoGenres'])
    musicContent = rec_system.getSongs(genres['musicGenres'])

    return JsonResponse({
        'videoGenres': genres['videoGenres'],
        'newsGenres': genres['newsGenres'],
        'musicGenres': genres['musicGenres'],
        'newsContent': newsContent,
        'videoContent': videoContent,
        'musicContent': musicContent
    })


def speechEmotion(request):

    # Function to return emotion probabilities for an uploaded audio file

    file_objs = request.FILES['audio-file']

    if(request.POST['source'] == 'upload'):
        handle_uploaded_file(request.FILES['audio-file'])
    else:
        handle_uploaded_file(request.FILES['audio-file'])

    filepath = "..\\..\\Emotionator\\media\\input-audio.wav"
    emotion = se_id.predict_speech(filepath)
    for state in emotion:
        state *= 100

    return JsonResponse({
        'happy': norm(emotion[0][3]),
        'sad': norm(emotion[0][2]),
        'angry': norm(emotion[0][1]),
        'calm': norm(emotion[0][0])
    })


def handle_uploaded_file(f):

    # Helper function for 'speechEmotion'
    # Function to write the uploaded audio file blob to server as a .wav file

    ext = os.path.splitext(f.name)[1]
    destination = open(f'../media/input-audio.wav', 'wb+')

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()


def norm(state):

    # Helper function for 'speechEmotion'
    # Function to normalize audio-emotion probabilities in the working range

    norm_state = 11 + ((state / 100) * 83)
    return norm_state


def facialEmotion(request):

    # Function to resturn emotion probabilities for recorded video stream

    final_emotions = fe_id.vidCapture()
    return JsonResponse({
        'happy': final_emotions[0] * 100,
        'sad': final_emotions[1] * 100,
        'angry': final_emotions[2] * 100,
        'calm': final_emotions[3] * 100
    })

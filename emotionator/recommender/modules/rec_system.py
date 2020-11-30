import requests
import webbrowser
import spotipy
import pandas as pd
import pprint
import matplotlib.pyplot as pd
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from io import BytesIO
from urllib.request import urlopen
from spotipy.oauth2 import SpotifyClientCredentials
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


def getGenres(primaryEmotion, enhancedEmotion):

    # Emotion to genre mapping dictionaries

    musicGenresKey = {
            'happy': ['hard-rock', 'pop', 'edm',
                      'latino', 'rock-n-roll', 'romance'],
            'sad': ['rock', 'romance', 'jazz', 'classical', 'blues', 'sad'],
            'angry': ['jazz', 'classical', 'reggae', 'trance'],
            'calm': ['hard-rock', 'trance', 'rock-n-roll', 'heavy-metal'],
            'energetic': ['heavy-metal', 'hard-rock', 'edm', 'death-metal'],
            'content': ['rock', 'trance', 'romance', 'happy'],
            'despair': ['jazz', 'rock', 'reggae', 'sad'],
            'gloomy': ['hard-rock', 'trance', 'sad', 'rainy-day']
            }

    videoCategoriesKey = {
            'happy': ['informative'],
            'sad': ['stand-up'],
            'angry': ['soothing'],
            'calm': ['motivational'],
            'energetic': ['informative', 'soothing'],
            'content': ['informative', 'motivational'],
            'despair': ['stand-up', 'soothing'],
            'gloomy': ['stand-up', 'motivational']
            }

    newsCategoriesKey = {
            'happy': ['self-help'],
            'sad': ['world'],
            'angry': ['laughs'],
            'calm': ['inspiring'],
            'energetic': ['self-help', 'laughs'],
            'content': ['self-help', 'inspiring'],
            'despair': ['world', 'laughs'],
            'gloomy': ['world', 'inspiring']
            }

    # Initializing and filling genre lists

    musicGenres = []
    videoCategories = []
    newsCategories = []

    if(enhancedEmotion == 'null'):
        videoCategories.append(videoCategoriesKey[primaryEmotion])
        newsCategories.append(newsCategoriesKey[primaryEmotion])
        musicGenres = musicGenresKey[primaryEmotion]

    else:
        videoCategories = videoCategoriesKey[enhancedEmotion]
        newsCategories = newsCategoriesKey[enhancedEmotion]
        musicGenres = musicGenresKey[enhancedEmotion]

    # Adding all genres to a single dictionary and returning it

    genreDict = {
        'videoGenres': videoCategories,
        'newsGenres': newsCategories,
        'musicGenres': musicGenres
    }

    return genreDict


def getNews(genreList):

    # Defining user agents and appending them to scraping request header

    mozilla_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    apple_agent = 'AppleWebKit/537.36 (KHTML, like Gecko)'
    chrome_agent = 'Chrome/58.0.3029.110 Safari/537.3'
    headers = {'User-Agent': f'{mozilla_agent} {apple_agent} {chrome_agent}'}

    # Fetching news content to a single dict using a Beautiful Soup scraper

    newsContent = {}

    for genre in genreList:
        newsGenre = genre
        newsLink = f"https://www.goodnewsnetwork.org/category/news/{newsGenre}"
        newsSource = requests.get(newsLink, headers=headers).text
        newsSoup = BeautifulSoup(newsSource, 'lxml')
        prettyNews = newsSoup.prettify()

        newsDivClass = 'td_module_3 td_module_wrap td-animation-stack'
        newsResultSet = newsSoup.findAll("div", {"class": f"{newsDivClass}"})

        newsHeadlines = []
        newsThumbs = []
        newsLinks = []

        for result in newsResultSet:
            newsHeadlines.append(result.h3.a.text)
            newsLinks.append(result.h3.a['href'])
            newsThumbs.append(result.div.div.a.img['src'])

        newsContent[genre] = [newsHeadlines, newsLinks, newsThumbs]

    return newsContent


def getVideos(genreList):

    # Defining API Keys aund auth variables for Youtube API

    DEVELOPER_KEY = "AIzaSyACMrUGO9o6eexlpwjt4O7U5crcMEQg-BQ"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    # Function to return a dictionary of videos for a single genre

    def youtube_search(q,
                       max_results=50,
                       order="relevance",
                       token=None,
                       location=None,
                       location_radius=None):

        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                        developerKey=DEVELOPER_KEY)

        search_response = youtube.search().list(
            q=q,
            type="video",
            pageToken=token,
            order=order,
            part="id, snippet",
            maxResults=max_results,
            location=location,
            locationRadius=location_radius
        ).execute()

        title = []
        channelId = []
        channelTitle = []
        videoId = []
        viewCount = []
        tags = []
        thumbnails = []

        for search_result in search_response.get("items", []):
            if (search_result["id"]["kind"] == "youtube#video"):
                title.append(search_result['snippet']['title'])

                videoId.append(search_result['id']['videoId'])

                response = youtube.videos().list(
                    part='statistics, snippet',
                    id=search_result['id']['videoId']).execute()

                resItems = response['items'][0]
                channelId.append(resItems['snippet']['channelId'])
                channelTitle.append(resItems['snippet']['channelTitle'])
                viewCount.append(resItems['statistics']['viewCount'])
                thumbnail_list = resItems['snippet']['thumbnails']
                thumbnails.append(thumbnail_list['default']['url'])

                if 'tags' in response['items'][0]['snippet'].keys():
                    tags.append(response['items'][0]['snippet']['tags'])
                else:
                    tags.append([])

        youtube_dict = {
            'tags': tags,
            'channelId': channelId,
            'channelTitle': channelTitle,
            'title': title,
            'videoId': videoId,
            'viewCount': viewCount,
            'thumbnails': thumbnails,
            }

        return youtube_dict

    # Initializing and filling a dictionary mapping genres and video content

    videoContent = {}

    for genre in genreList:
        videoContent[genre] = youtube_search(genre)

    return videoContent


def getSongs(genreList):

    # Defining API Keys aund auth variables for Spotify API

    cid = '4f916d0a2f8b4341aa10ed94776081dc'
    secret = 'e9267d6c7edc4aeeba9d459128da1124'
    client_credentials_manager = SpotifyClientCredentials(client_id=cid,
                                                          client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Fetching song content for different genres and mapping them to a dict

    songContent = {}

    for genre in genreList:

        cur_genres = []
        cur_genres.append(genre)

        artist_name = []
        track_name = []
        popularity = []
        track_url = []
        cover_art = []

        songs = sp.recommendations(seed_genres=cur_genres,
                                   limit=25,
                                   type='track')

        for t in enumerate(songs['tracks']):
            artist_name.append(t[1]['artists'][0]['name'])
            track_name.append(t[1]['name'])
            track_url.append(t[1]['external_urls'])
            popularity.append(t[1]['popularity'])
            cover_art.append(t[1]['album']['images'][0]['url'])

        songsDict = {
                'artist_name': artist_name,
                'track_name': track_name,
                'track_url': track_url,
                'popularity': popularity,
                'cover_art': cover_art
                }

        songContent[genre] = songsDict

    return songContent


#importing required libraries

import isodate
import datetime
from datetime import datetime
from googleapiclient.errors import HttpError
import pymongo
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import mysql.connector
import pymysql
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import json

global youtube

# used st.cache_data method to cache the data that are retrived from the fuctions. It helps improve performance

# function to cobvert date time from youtube API

@st.cache_data
def convert_datetime(published_at):
    datetime_obj = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
    return datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

# function to convert video duration from PT (Period of time) to clock duration

@st.cache_data
def format_duration(duration):
    duration_obj = isodate.parse_duration(duration)
    hours = duration_obj.total_seconds() // 3600
    minutes = (duration_obj.total_seconds() % 3600) // 60
    seconds = duration_obj.total_seconds() % 60
    formatted_duration = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return formatted_duration

# getting all details (Channel, Plalist, VIdeo) using API

@st.cache_data  
def get_ch_det(ch_ids,API):
    from googleapiclient.discovery import build
    youtube = build('youtube', 'v3', developerKey=API)
    
    all_data=[]

    response=youtube.channels().list(
             part='snippet,contentDetails,statistics,status',
             id=','.join(ch_ids)).execute()

    for channel in response['items']:
        ch_details = {'channel_id' : channel['id'] , 
                      'title' : channel['snippet']['title'],    
                      'channel_views': int(channel['statistics']['viewCount']),
                      'description' : channel['snippet']['description'], 
                      'subscriber_count' : int(channel['statistics']['subscriberCount']), 
                      'video_count' : int(channel['statistics']['videoCount']),
                      'status': channel['status']['privacyStatus'],
                      'playlist':channel["contentDetails"]["relatedPlaylists"]["uploads"]}
      
     
        response=youtube.playlistItems().list(
                    part='contentDetails',
                    playlistId=ch_details['playlist'],
                    maxResults=50).execute()
    
        vid = {}
        x = 1
        for videoid in response['items']:
            video_key = f'video_{x}'
            vid[video_key] = {'video_id' : videoid['contentDetails']['videoId']}
            x += 1

        #Retrieve video information from youtube API aith videoId as input and append in the vid dictionary
        for n in vid:
            video_response = youtube.videos().list(
                part='snippet,contentDetails,statistics',
                id=vid[n]['video_id']
            ).execute()
            if  len(video_response['items']) > 0:
                vid[n]['title'] = video_response['items'][0]['snippet']['title']
                vid[n]['description'] = video_response['items'][0]['snippet']['description']
                vid[n]['published_at'] = convert_datetime(video_response['items'][0]['snippet']['publishedAt'])
                vid[n]['view_count'] = int(video_response['items'][0]['statistics']['viewCount'])
                vid[n]['like_count'] = int(video_response['items'][0]['statistics'].get('likeCount','0'))
                vid[n]['favorite_count'] = int(video_response['items'][0]['statistics']['favoriteCount'])
                vid[n]['comment_count'] = int(video_response['items'][0]['statistics'].get('commentCount','0'))
                vid[n]['thumbnail_url'] = video_response['items'][0]['snippet']['thumbnails']['default']['url']
                vid[n]['duration'] = format_duration(video_response['items'][0]['contentDetails']['duration'])
                vid[n]['caption_status'] = video_response['items'][0]['contentDetails']['caption']
                vid[n]['Tags'] = video_response['items'][0]['snippet'].get('tags')
                vid[n]['video_id'] = video_response['items'][0]['id']
            else:
                vid[n]['title'] = "Video not available"
                vid[n]['description'] = ""
                vid[n]['published_at'] = ""
                vid[n]['view_count'] = int("0")
                vid[n]['like_count'] = int("0")
                vid[n]['favorite_count'] = int("0")
                vid[n]['comment_count'] = int("0")
                vid[n]['duration'] = ""
                vid[n]['caption_status'] = ""
        ch_details['videos']=vid
        all_data.append(ch_details)
    return all_data



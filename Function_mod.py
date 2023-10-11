
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

# function to get chaneel data using API
@st.cache_data
def get_ch_info(ch_id,API_KEY):
    from googleapiclient.discovery import build
    global youtube 
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    channel_response = youtube.channels().list(
        part='snippet,contentDetails,statistics,status',
        id=ch_id).execute()

    #store the desired channel data which are extracted from youtube into a dictionary
    ch_details = {}
    for channel in channel_response['items']:
        ch_details = {'channel_id' : channel['id'] , 
                      'title' : channel['snippet']['title'], 
                      'channel_views': int(channel['statistics']['viewCount']),
                      'description' : channel['snippet']['description'], 
                      'subscriber_count' : int(channel['statistics']['subscriberCount']), 
                      'video_count' : int(channel['statistics']['videoCount']),
                      'status': channel['status']['privacyStatus'],
                      'playlist':channel["contentDetails"]["relatedPlaylists"]["uploads"],}
        return(ch_details)

# function to get playlist details and video details

@st.cache_data
def get_vd_info(playlist,API_KEY):
    # Retrieve the playlistItems from the YouTube API
    videoid_response=youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist,
        maxResults=50
    ).execute()

    #Extract videoId from playlistItems and store it in a dictionary with dynamite key
    vids = {}
    x = 1
    for videoid in videoid_response['items']:
        video_key = 'video_' + str(x)
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
    return(vids)

# function to get playlist items info

@st.cache_data
def get_pl_info(ch_id,API_KEY):
    # Retrieve the PLaylist information from the YouTube API
    playlist_response = youtube.playlists().list(
                        part = "snippet,contentDetails",
                        channelId  = ch_id,
                        maxResults = 50).execute()

    #store the desired playlist data which are extracted from youtube into a dictionary with dynamite key
    pl_details = {}
    pl_no = 1
    #if len(playlist_response['items'])>0:
    for pl in playlist_response['items']:
        playlist_key = 'playlist_' + str(pl_no)
        pl_details[playlist_key] = {'playlist_id' : pl['id'], 'channel_id' : pl['snippet']['channelId'], 'title' : pl['snippet']['title']}
        pl_no += 1
    return(pl_details)

# getting video details

@st.cache_data
def get_vd_info(playlist_id,API_KEY):
    # Retrieve the playlistItems from the YouTube API
    videoid_response=youtube.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=50
    ).execute()

    #Extract videoId from playlistItems and store it in a dictionary with dynamite key
    vid = {}
    x = 1
    for videoid in videoid_response['items']:
        video_key = 'video_' + str(x)
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
            vid[n]['dislike_count'] = int(video_response['items'][0]['statistics'].get('dislikeCount','0'))
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
    return(vid)

#getting comment details
@st.cache_data
def get_comment_info(video_id,API_KEY):
    try:
        #Retrieve comments from a video from youtube API
        comment_response=youtube.commentThreads().list(
            part="snippet",
            videoId=video_id
        ).execute()

        #Extract the desired data from response and store in a dictionary with dynamtite key
        cmnts = {}
        cno = 1
        for comment in comment_response['items']:
            comment_key = 'comment_' + str(cno)
            cmnts[comment_key] = {'comment_id' : comment['id'], 
                                  'comment_text' : comment['snippet']['topLevelComment']['snippet']['textDisplay'], 
                                  'author_name' : comment['snippet']['topLevelComment']['snippet']['authorDisplayName'], 
                                  'published_at' : convert_datetime(comment['snippet']['topLevelComment']['snippet']['publishedAt'])}
            cno += 1
        return(cmnts)

    except HttpError:
        pass

# Combing all data as per the requirement
@st.cache_data
def alldata(ch_id,API_KEY):
    from googleapiclient.discovery import build
    global youtube 
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    channel_details = get_ch_info(ch_id,API_KEY)
    playlist_details = get_pl_info(ch_id,API_KEY)
    playlist=get_ch_info(ch_id,API_KEY)['playlist']
    if len(playlist_details)>0:
        for i in playlist_details:
            playlist_id = playlist_details[i]['playlist_id']

            video_details = get_vd_info(playlist_id,API_KEY)
            for j in video_details:
                video_id = video_details[j]['video_id']

                comments = get_comment_info(video_id,API_KEY)
                video_details[j]['comments'] = comments
            playlist_details[i]['videos'] = video_details
        channel_details['playlists'] = playlist_details
    else:
        video_details = get_vd_info(playlist,API_KEY)
        for i in video_details:
            video_id = video_details[i]['video_id']
            comments = get_comment_info(video_id,API_KEY)
            video_details[i]['comments'] = comments
            channel_details['videos']=video_details
    return(channel_details)

# function to push data from MongoDB to MySQL
@st.cache_data
def mdb_to_sql(ch_name):
    mycl = pymongo.MongoClient("mongodb://localhost:27017")
    mydb=mycl.Guvi_capstone
    mycol = mydb.Channel_Name
    data = mycol.find({'title': ch_name})
    ch_data = []
    playlists = []
    videos=[]
    comments = []
    for i in data:
        ch_det={
            'channel_id':i['channel_id'],
               'title':i['title'],
               'channel_views': i['channel_views'],
               'description':i['description'],
               'subscriber_count':i['status'],
               'status':i['video_count']
               }
        ch_data.append(ch_det)

        channel_playlists = i.get('playlists', {})
        for pl in channel_playlists.values():
            playlist_id = pl['playlist_id']
            playlist_data = {'playlist_id':playlist_id,
                             'channel_id':pl['channel_id'],
                             'playlist_title':pl['title']
                             }
            playlists.append(playlist_data)
            for video in pl['videos'].values():
                video['playlist_id'] = playlist_id
                videos.append({key: value for key, value in video.items() if key != 'comments' and key != 'Tags'})
                if video['comments'] is not None:
                    video_comments = video['comments'].values()
                    if video_comments:
                        for comment in video_comments:
                            comment['video_id'] = video['video_id']
                            comments.append(comment)

    channel_df = pd.DataFrame(ch_data)
    playlists_df = pd.DataFrame(playlists)
    videos_df = pd.DataFrame(videos)
    videos_df.drop_duplicates(subset = "video_id", keep = 'first', inplace = True)
    comments_df = pd.DataFrame(comments)
    comments_df.drop_duplicates(subset = "comment_id", keep = 'first', inplace = True)

    table1 = 'channel_details'
    table2 = 'playlist_details'
    table3 = 'video_details'
    table4 = 'comment_details'


    engine = create_engine('mysql+pymysql://root:Sansuganyas%4022@localhost:3306/guvi_capstone',pool_pre_ping=True)
    channel_df.to_sql(name=table1, con=engine, if_exists='append', index=False)
    playlists_df.to_sql(name=table2, con=engine, if_exists='append', index=False)
    videos_df.to_sql(name=table3, con=engine, if_exists='append', index=False)
    comments_df.to_sql(name=table4, con=engine, if_exists='append', index=False)

    st.success(f"🟢{ch_name} channel data migrated from MongoDB to MySQL 🥇")
    engine.dispose()

# Function to connnect MySQL and retrive data based on the query defined. Converting data to Data Frame.
@st.cache_data
def sdfmd(_query,*cols,):
    engine = create_engine('mysql+pymysql://root:Sansuganyas%4022@localhost:3306/guvi_capstone',pool_pre_ping=True)
    with engine.connect() as con:
        result = con.execute(_query)
        data=result.fetchall()
        df =pd.DataFrame(data,columns=cols)
    return df


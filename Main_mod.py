
#importing required libraries

import streamlit as st
import json
import pymongo
import pandas as pd
import pymysql
from sqlalchemy import text
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import mysql.connector
from isodate import parse_duration
import sqlite3
import os
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from streamlit_option_menu import option_menu
from google.auth.exceptions import DefaultCredentialsError
from googleapiclient.errors import HttpError


# defining images to display in streamlit app

image=Image.open("C:\\Users\\sansu\\OneDrive\\Pictures\\data-icon-26.jpg")
you_image=Image.open("C:\\Users\\sansu\\OneDrive\\Pictures\\Youtube.png")

#Streamlit page configuration
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    page_title="San's Data",
    page_icon=image)

#used columns to center image
col1, col2, col3 = st.columns([1,.5,1])

with col1:
	st.write("")

with col2:
	st.image(you_image, use_column_width=True)

with col3:	
	st.write("")

# Page title and break line
st.markdown("<h1 style='text-align: center; color: #45292D;'> YouTube Data Harvesting and Warehousing using SQL, MongoDB and Streamlit </h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 2px solid #805A59;'>", unsafe_allow_html=True)
	
# creating side bar and break line
with st.sidebar:
    st.sidebar.markdown("<h1 style='text-align: center; color: #45292D;font-size: 28px; font-family: Arial, sans-serif;'>Menu", unsafe_allow_html=True)
    st.sidebar.markdown("<hr style='border: 2px solid #805A59;'>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,options=['Home','Data Harvesting & Warehousing','Bulk data harvesting & Warehousing'],icons=['house','database-check','database-check'],styles={
        "container": {"padding": "0!important", "background-color": "#F9F8F9"},
        "icon": {"color": "#A0A2A0", "font-size": "25px"}, 
        "nav-link": {"font-size": "25px", "color": "#805A59","text-align": "left", "margin":"0px", "--hover-color": "#84706E"},
        "nav-link-selected": {"background-color": "#84706E","color": "white"},
    })
    st.sidebar.markdown("<hr style='border: 2px solid #805A59;'>", unsafe_allow_html=True)

# Defining actions if user selects Home from the side bar

if selected == 'Home':
    st.markdown("<h3 style='text-align: center; color: #45292D;'>Welcome to the YouTube Data Harvesting App!", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: left; color: 45292D;'>This app allows user:</h5>", unsafe_allow_html=True)
    st.markdown("<h7 style='text-align: left; color: black;'><ol> <li > To access and analyze data from multiple YouTube channels. </li> <li> To retrive YouTube channel details by using the YouTube channel ID (Channel name, subscribers, total video count, playlist ID, video ID, likes, dislikes, comments of each video)  </li> <li >To store the data in a MongoDB database as a data lake. </li><li >To collect data for up to 10 different YouTube channels and store them in the data lake by clicking a button. </li><li >To select a channel name and migrate its data from the data lake to a SQL database as tables.</li><li >To search and retrieve data from the SQL database using different search options, including joining tables to get channel details.</li></ol><h7>", unsafe_allow_html=True)

    # Defining actions if user selects 'Data Harvesting & Warehousing' from the side bar

if selected== 'Data Harvesting & Warehousing':
	#creating 3 tabs to separate different actions
	tab1,tab2,tab3 = st.tabs(["Harvesting & Warehousing Data", "Mongo DB to MySQL", "MySQL Queries"])

	with tab1:
		#creating 3 columns to separate different actions and used try method to handle error exceptions 
		col1,col2,col3 = st.columns(3)
		try:
			#creating input to get the API and channel id and button to perform the action
		    with col1:
		        API_KEY = st.text_input("Enter API Key:",help='💡YouTube Data API is a set of rules and protocols that allows different software applications to communicate with and access specific features or data from YouTubes platform. Click [here](https://developers.google.com/youtube/v3/getting-started) for more guides & references')
		        ch_id = st.text_input('Enter channel ID:',help='Hint: 💡Go to YouTube channel home pane, right click and hit view page source to find a channel_id. Click [here](https://mixedanalytics.com/blog/find-a-youtube-channel-id/) for guidance')
		        search=st.button('🔍 Search')    

		        # importing defined functions from the other module
		        from Function_mod import alldata
		      
		    with col2:
		    	# Running function to get data
		    	global channel_details
		    	# channel_details=alldata(ch_id,API_KEY)

		    	if search: 
		    		# Displaying data in Json fromat 
		    		channel_details=alldata(ch_id,API_KEY)
		    		st.json(channel_details, expanded=True)
		    	
			# Pushing data to Mongo DB
		    with col3:
		        mdb_load=st.button('Push data to MongoDB ➡️')
		        mycl = pymongo.MongoClient("mongodb://localhost:27017")

		        if mdb_load:
		        	channel_details=alldata(ch_id,API_KEY)
		        	mydb=mycl.Guvi_capstone
		        	mycol = mydb.Channel_Name
		        	try:
		        		mycol.insert_one(channel_details)
		        		st.snow()
		        		st.success('🟢 Channel details loaded to MongoDB')
		        	except Exception as e:
		        		st.error(f'❌ Error: {str(e)}')
		        	
		except HttpError as e:
		    st.write("Please check your API's quota. It must be expired") if 'quota' in str(e) else st.exception(e)

		except KeyError as e:
			pass
			st.warning('Please provide the API ID and channel ID.', icon='⚠️')
			st.info('If you need assistance, click on the question mark "②". It will display the instructions on hover.',icon='ℹ️')
		except DefaultCredentialsError:
			st.warning('Please provide the API ID and channel ID.', icon='⚠️')
			st.info('If you need assistance, click on the question mark "②". It will display the instructions on hover.',icon='ℹ️')	
		except KeyError:
			st.warning('Please provide the API ID and channel ID.', icon='⚠️')
			st.info('If you need assistance, click on the question mark "②". It will display the instructions on hover.',icon='ℹ️')	
		except NameError:
			pass


	with tab2:
		col1,col2=st.columns(2)
		with col1:

		# getting channel name from the Mongo DB to list a dropdown so we can move channel details to SQL

		    mydb=mycl.Guvi_capstone
		    mycol=mydb.Channel_Name
		    ch_name= mycol.find({},{"_id" : 0, "title" : 1})
		    names=set()
		    name = ("👇Select a channel name to migrate the data to MySQL👇")
		    for i in ch_name:
		        ch_ttitle = i['title']
		        names.add(ch_ttitle)
		      
		    name_selection = st.selectbox('Select a channel to move the channel data into MySQL',[name]+(list(names)),index=0)
		    mysql_load=st.button('Push into MySQL 🛫')
		    if mysql_load:
	    		from Function_mod import mdb_to_sql
	    		mdb_to_sql(name_selection)


	with col2:
		    if name_selection != name:
		    	query = {"title": name_selection}
		    	results = list(mycol.find(query,{"channel_id": 1, "title": 1, "channel_views": 1,"description":1,"subscriber_count":1,"video_count":1,"status":1,"playlist":1}))
		    	st.json(results, expanded=True)

	    

	# Defining questions based on the project details provided by Guvi
	with tab3:
	    Ques_0 = '👇 Select query to proceed further 👇'
	    Ques_1 = '1. What are the names of all the videos and their corresponding channels?'
	    Ques_2 = '2. Which channels have the most number of videos, and how many videos do they have?'
	    Ques_3 = "3. What are the top 10 most viewed videos and their respective channels?"
	    Ques_4 = "4. How many comments were made on each video, and what are their corresponding video names?"
	    Ques_5 = '5. Which videos have the highest number of likes, and what are their corresponding channel names?'
	    Ques_6 = '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?'
	    Ques_7 = '7. What is the total number of views for each channel, and what are their corresponding channel names?'
	    Ques_8 = '8. What are the names of all the channels that have published videos in the year 2022?'
	    Ques_9 = '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?'
	    Ques_10 ='10. Which videos have the highest number of comments, and what are their corresponding channel names?'

	    # Creating queries to interact with MySQL to get the data and mapping to the respective question
	    ques = st.selectbox('Lets find something..!🕵️‍♂️',(Ques_0,Ques_1,Ques_2,Ques_3,Ques_4,Ques_5,Ques_6,Ques_7,Ques_8,Ques_9,Ques_10))
	    go_find=st.button('🔍 Lets find out!')
	    

	    if go_find:
	    	#connecting to MySQL
	        engine = create_engine('mysql+pymysql://root:Sansuganyas%4022@localhost:3306/Guvi_capstone')
	        st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)
	        from Function_mod import sdfmd
        	
	        if ques==Ques_1:
	            query=text('SELECT ch.channel_id, ch.title as Channel_name, vd.title as video_title FROM channel_details as ch join playlist_details as pl on ch.channel_id = pl.channel_id join video_details as vd on pl.playlist_id = vd.playlist_id')
	            df = sdfmd(query,'Channel_Id','Channel_Name','video_Name')
	            # df['title'] = df['title'].str.replace(' ', '\n')
	            st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=True)
	            st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)
	            # snsplot(df,sns.barplot,'title','video_count','video_count by channel name','Channel Names','video_count')
	            # st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)



	        elif ques==Ques_2:
	            query=text("SELECT ch.channel_id, ch.title as Channel_name, Count(vd.video_id) as video_count FROM channel_details as ch join playlist_details as pl on ch.channel_id = pl.channel_id join video_details as vd on pl.playlist_id = vd.playlist_id group by ch.channel_id, ch.title order by video_count desc -- limit 1")
	            df=sdfmd(query,'channel_id','Channel_Name','video_count')
	            df_display = df.reset_index(drop=True) 
	            st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=True)
	            st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)


	            
	        elif ques==Ques_3:
	            query=text('SELECT ch.channel_id, ch.title as Channel_name, vd.title as video_title,vd.view_count FROM channel_details as ch join playlist_details as pl on ch.channel_id = pl.channel_id join video_details as vd on pl.playlist_id = vd.playlist_id order by view_count desc limit 10')
	            df=sdfmd(query,'channel_id','Channel_Name','video_title','view_count')
	            st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=True)
	            st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)


	        elif ques==Ques_4:
	            query=text('select vd.video_id, vd.title as Video_Title,count(cmt.comment_id) as Comment_Count from video_details as vd join comment_details as cmt on vd.video_id = cmt.video_id group by vd.video_id, vd.title order by comment_count Desc')
	            df=sdfmd(query,'video_id','Video_Title','Comment_Count')
	            st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=True)
	            st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)
	       
	        
	        elif ques==Ques_0:
	            st.warning('👆 Please select the query from the dropdown above and hit the button to provide the details. 👆', icon='⚠')
	            st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)

	        elif ques==Ques_5:
	            query = text("select ch.title as Channel_Name, vd.title as Video_Title,vd.like_count as Likes from channel_details as ch join playlist_details as pl on ch.channel_id = pl.channel_id join video_details as vd on pl.playlist_id = vd.playlist_id order by like_count desc limit 1 ")
	            df=sdfmd(query,'Channel_Name','Video_Title','Likes')
	            st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=True)
	            st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)

	        elif ques==Ques_6:
	        	query=text("select title as Video_Title, like_count as Likes, dislike_count as Dislikes from video_details where title != 'Video not available'")
	        	df=sdfmd(query,'Video_Title','Likes','Dislikes')
	        	st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=True)
	        	st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)
	        
	        elif ques==Ques_7:
	        	query=text("select title as Channel_Name,channel_views as Channel_Views from channel_details order by Channel_Views desc")
	        	df=sdfmd(query,'Channel_Name','Channel_Views')
	        	st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=False)
	        	st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)
	        
	        elif ques==Ques_8:
	        	query=text("select ch.title as Channel_Name,year(vd.published_at) as Published_Year from channel_details as ch join playlist_details as pl on ch.channel_id = pl.channel_id join video_details as vd on pl.playlist_id = vd.playlist_id WHERE YEAR(vd.published_at) = 2022 GROUP BY ch.title, YEAR(vd.published_at)")
	        	df=sdfmd(query,'Channel_Name','Published_Year')
	        	st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=False)
	        	st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)

	        elif ques==Ques_9:
	        	query=text("SELECT ch.title AS Channel_Name, round(AVG( CAST(SUBSTRING(duration, 1, 2) AS SIGNED) * 3600 + CAST(SUBSTRING(duration, 4, 2) AS SIGNED) * 60 + CAST(SUBSTRING(duration, 7, 2) AS SIGNED) ),2) AS Avg_Dur_Minutes FROM channel_details AS ch JOIN playlist_details AS pl ON ch.channel_id = pl.channel_id JOIN video_details AS vd ON pl.playlist_id = vd.playlist_id WHERE YEAR(vd.published_at) = 2022 GROUP BY ch.title, YEAR(vd.published_at)")
	        	df=sdfmd(query,'Channel_Name','Avg_Dur_Minutes')
	        	st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=False)
	        	st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)

	        elif ques==Ques_10:
	        	query=text("sELECT ch.title AS Channel_Name, video_comments.max_comments FROM channel_details AS ch JOIN playlist_details AS pl ON ch.channel_id = pl.channel_id JOIN video_details AS vd ON pl.playlist_id = vd.playlist_id JOIN(SELECT vd.video_id, COUNT(cmt.comment_id) AS max_comments FROM video_details AS vd JOIN comment_details AS cmt ON vd.video_id = cmt.video_id GROUP BY vd.video_id order by max_comments desc limit 1) AS video_comments ON vd.video_id = video_comments.video_id")
	        	df=sdfmd(query,'Channel_Name','video_comments')
	        	st.dataframe(df, width=None, height=None,hide_index=True,use_container_width=False	)
	        	st.markdown("<hr style='border: 1px solid #805A59;'>", unsafe_allow_html=True)


# Creating another side bar to get multiple channel details at once
if 	selected == 'Bulk data harvesting & Warehousing':
	#Defining columns and input
	col1,col2, col3 = st.columns(3)
	with col1:
		API = st.text_input("Enter API Key:",help='💡YouTube Data API is a set of rules and protocols that allows different software applications to communicate with and access specific features or data from YouTubes platform. Click [here](https://developers.google.com/youtube/v3/getting-started) for more guides & references')
		ch_ids = st.text_input('Enter channel IDs: (Separator is comma (,))',help='Hint: 💡Go to YouTube channel home pane, right click and hit view page source to find a channel_id. Click [here](https://mixedanalytics.com/blog/find-a-youtube-channel-id/) for guidance')
		search1=st.button('🔍 Push details to Mongo DB')
		ch_ids = ch_ids.split(',')


	with col2:
		# importing defined functions from another module 
		if search1:
			from Functuib_mod_bulk import get_ch_det
			channel_data = get_ch_det(ch_ids,API)
			st.json(channel_data, expanded=True)
			with col3:

				mycl = pymongo.MongoClient("mongodb://localhost:27017")
				mydb=mycl.Guvi_capstone
				mycol = mydb.bulk_run
				for i in channel_data:
					mycol.insert_one(i)
				st.success('🟢 Channel details loaded to MongoDB')
				st.snow()


			

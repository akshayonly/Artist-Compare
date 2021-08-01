"""
Title: Artist Compare
Author: Akshay Shirsath
Icons made by www.flaticon.com
"""
######################
# Libraries
######################

import streamlit as st
import base64
import json
from datetime import datetime
import sys
import io
from secrets import *

import urllib 
import requests
from PIL import Image
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

######################
# Custom Functions
######################

@st.cache
def Authorization(client_ID, client_Secret):
    
    # Authorization 
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    # Encode as Base64
    message = f"{client_ID}:{client_Secret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"

    r = requests.post(url, headers=headers, data=data)

    token = r.json()['access_token']
    
    return token

def GetArtistID(artist_name, token, country='IN'):

    search_url = f"https://api.spotify.com/v1/search"

    headers = {"Authorization": "Bearer " + token}

    query = {
        'q': artist_name,
        'type': 'artist',
        'market': country
            }

    request = requests.get(url=search_url, headers=headers, params=query)

    search_results = dict(request.json())

    artist_id = search_results['artists']['items'][0]['id']
    
    return artist_id


def TopTracks(artist_id, token, country='IN'):

    top_tracks_Url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"

    headers = {
        "Authorization": "Bearer " + token
    }

    country = {'market': country}

    request = requests.get(url=top_tracks_Url, headers=headers, params=country)

    top_tracks_results = dict(request.json())
    
    return top_tracks_results

def SingleTrackFeature(track_id, token):
    
    track_url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {
        "Authorization": "Bearer " + token
    }
    req = requests.get(url=track_url, headers=headers)
    
    track_info = dict(req.json(), indent=2)
    
    audio_features = [track_info.get(key) for key in track_info.keys()][0:11]
    
    return audio_features

def MultiTrackFeatures(results, token):
    
    top_tracks_features = list()

    for item in results['tracks']:

        audio_features = SingleTrackFeature(item['id'], token)

        audio_features.append(item['popularity'])

        top_tracks_features.append(audio_features) 
        
    top_tracks_features = MinMaxScaler().fit_transform(np.asarray(top_tracks_features))
    
    return top_tracks_features

def GetAnArtist(artist_id, token, country='US'):

    top_tracks_Url = f"https://api.spotify.com/v1/artists/{artist_id}"

    headers = {
        "Authorization": "Bearer " + token
    }

    country = {'market': country}

    request = requests.get(url=top_tracks_Url, headers=headers, params=country)

    Artist_results = dict(request.json())
    
    return Artist_results


######################
# Page Body
######################

# Logo
image = Image.open('Artist-Compare-Dark.png')
st.image(image, use_column_width=True)

st.markdown("""
- This web app compares any two music artists or bands based on their popular tracks. 
Whatever genres, languages they have sung, enter their names in the below boxes, and compare!
""")

expander_bar = st.beta_expander("Site Info")
expander_bar.markdown("""
* **version 1.5**
* **Python Libraries:** streamlit, json, urllib, requests, sklearn, plotly, pandas
* **Data source:** [Spotify API](https://developer.spotify.com/documentation/web-api/)
* **Author:** Akshay Shirsath   
""")                                              

# Artist 01
st.subheader('Compare')
default1 = "Ravi Shankar"
first_artist_name = st.text_input("Artist I", default1)

# Artist 02
st.subheader('And')
default2 = "Pink Floyd"
second_artist_name = st.text_input("Artist II", default2)

#######################################
# Selecting subset columns & parameters
#######################################

st.subheader('With Parameters')
features_numbers = st.select_slider('Slide To Select', options=[3, 5, 8])

primary = ['acousticness', 'danceability', 'energy']
secondary = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'popularity score']
tertiary = ['acousticness', 'danceability', 'energy', 'liveness', 'instrumentalness', 
            'popularity score', 'tempo', 'valence']

three = ("""
    * **Acousticness:** Describe acoustic music, i.e. 
    usage of musical instruments without electrical amplification.
    * **Danceability:** Describe danceable music.
    * **Energy:** Describes energetic tracks e.g., 
    Heavy Metal is energetic, whereas Classical Music has low energy.
    """)  

five = ("""
    * **Acousticness:** Describe acoustic music, i.e. 
    usage of musical instruments without electrical amplification.
    * **Danceability:** Describe danceable music.
    * **Energy:** Describes energetic tracks e.g., 
    Heavy Metal is energetic, whereas Classical Music has low energy.
    * **Instrumentalness:** Describe whether tracks have vocals, higher value says more tracks have vocals and vice versa.
    * **Popularity Score:**  Popularity of the music tracks.
    """)  

eight = ("""
    * **Acousticness:** Describe acoustic music, i.e. 
    usage of musical instruments without electrical amplification.
    * **Danceability:** Describe danceable music.
    * **Energy:** Describes energetic tracks e.g., 
    Heavy Metal is energetic, whereas Classical Music has low energy.
    * **Instrumentalness:** Describe whether tracks have vocals, higher value says more tracks have vocals and vice versa.
    * **Popularity Score:**  Popularity of the music tracks.
    * **Liveness:** Describe the presence of an audience in the music tracks.
    * **Tempo:** Describe the speed or pace of music tracks.
    * **Valence:** Describe the positivity and negativity in music tracks. 
    High-value says positive (e.g. happy, cheerful, euphoric), 
    whereas low-value state more negative (e.g. sad, depressed, angry).
    """)  

if features_numbers == len(primary):
    subset = primary
    feat_display = three
elif features_numbers == len(secondary):
    subset = secondary
    feat_display = five
else:
    subset = tertiary
    feat_display = eight

expander_bar = st.beta_expander("Parameters Interpretation")
expander_bar.markdown(feat_display)  

######################
# Plot
######################

# For space
st.text("\n\n")

if st.button('Show Plot'):

    start=datetime.now()

    client_ID = '4d500ecf52a3447685e7389ca8a1dae9'
    client_Secret = 'c5b32293c6fa4339893431280cce8ac1'

    token = Authorization(client_ID, client_Secret)

    first_artist_artist_id = GetArtistID(first_artist_name, token)
    second_artist_artist_id = GetArtistID(second_artist_name, token)

    first_artist_top_tracks = TopTracks(first_artist_artist_id, token)
    second_artist_top_tracks = TopTracks(second_artist_artist_id, token)

    first_artist_tracks_features = MultiTrackFeatures(first_artist_top_tracks, token)
    second_artist_tracks_features = MultiTrackFeatures(second_artist_top_tracks, token)

    first_artist_results = GetAnArtist(first_artist_artist_id, token)
    second_artist_results = GetAnArtist(second_artist_artist_id, token)

    column_names = ['danceability', 'energy', 'key', 'loudness', 'mode', 
                    'speechiness', 'acousticness', 'instrumentalness', 
                    'liveness', 'valence', 'tempo', 'popularity score']


    first_tracks_data = pd.DataFrame(data=first_artist_tracks_features, 
                                     columns=column_names)

    second_tracks_data = pd.DataFrame(data=second_artist_tracks_features, 
                                      columns=column_names)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
          r=np.int64(np.round(first_tracks_data[subset].mean() * 10)),
          theta=first_tracks_data[subset].columns.str.title(),
          fill='toself', 
          line_color ='#00ccb2',
          name=first_artist_results['name']
    ))
    
    fig.add_trace(go.Scatterpolar(
          r=np.int64(np.round(second_tracks_data[subset].mean() * 10)),
          theta=second_tracks_data[subset].columns.str.title(),
          fill='toself',
          line_color ='#ff8700',
          name=second_artist_results['name']
    ))

    fig.update_layout(
        font_size = 16, 
        showlegend=True,
        polar=dict(
            bgcolor = "rgb(54, 54, 54)",
            radialaxis=dict(visible=False),
            ),
    )

    st.plotly_chart(fig)

st.stop()        

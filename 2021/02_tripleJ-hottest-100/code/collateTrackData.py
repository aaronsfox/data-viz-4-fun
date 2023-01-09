# -*- coding: utf-8 -*-
"""

@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Script to collate the Spotify data from the hottest 100 playlists.
    The order in which the tracks are extracted from the playlists should
    represent the order in the hottest 100 - however, we don't label this here
    as there is a possibility that every now and then a track is missing, or 
    perhaps they aren't in the correct order.
    
"""

# %% Import packages

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import numpy as np
import requests
import shutil
import string

# %% Set-up

#Set spotify client
#Please replace these with your own - don't mess around with other peoples IDs!
cid = 'bbb3754194114a88aadb477923261062'
secret = 'ae7e6c9e8a1643c3bc455dfd0846ef96'
client_credentials_manager = SpotifyClientCredentials(client_id = cid,
                                                      client_secret = secret)
spotifyClient = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

##### TODO: add latest 2021 when available...

#Set the hottest 100 playlist links
playlistLinks = {1993: 'https://open.spotify.com/playlist/41hNkCFTDt1gupVdIpAoA9?si=61879a21d3eb4739',
                 1994: 'https://open.spotify.com/playlist/6eexOwD6tyZm7MrIQW39QD?si=885f8a65ea784231',
                 1995: 'https://open.spotify.com/playlist/6aMvxwcYAnpa2EMkIcaxV3?si=bc24552c718c4125',
                 1996: 'https://open.spotify.com/playlist/4urE2yjyJmaHKxKEBMabUe?si=af6fd7fcfac84631',
                 1997: 'https://open.spotify.com/playlist/720nBFTU24jBOZiJItHs3D?si=c5dce488ed314794',
                 1998: 'https://open.spotify.com/playlist/6T0cEfBWMhKud4swAF4nPP?si=534d4dd306df46f1',
                 1999: 'https://open.spotify.com/playlist/4YDkQgwepgg5MSOmPRizRP?si=908c16f08a574980',
                 2000: 'https://open.spotify.com/playlist/3d9tfqjeSb1VRttRZXdZ0Z?si=ecd1b6e458f749ad',
                 2001: 'https://open.spotify.com/playlist/0p0I4hShKybp57sNSQnvZY?si=e79b9d5b16e84984',
                 2002: 'https://open.spotify.com/playlist/390wkO5skVZCXQLthuWbmJ?si=78f05748a64b47cf',
                 2003: 'https://open.spotify.com/playlist/0P0Ca2yEwivn3gPsHIeasz?si=c979b88da2bd44ea',
                 2004: 'https://open.spotify.com/playlist/29sIMITJwuGk4yIVFboe9d?si=94703de5d5eb43f1',
                 2005: 'https://open.spotify.com/playlist/6sqPb1wMVbaha7NrISZqBh?si=2304766dce2f4b2c',
                 2006: 'https://open.spotify.com/playlist/00FrZIzaANk8rNw3E83jAO?si=63517e0134394ab4',
                 2007: 'https://open.spotify.com/playlist/56STZLC2lVTbiAAwp89kQB?si=be80e91fa1974c6c',
                 2008: 'https://open.spotify.com/playlist/0dOc1wWqi5R4d6IgMlLeca?si=7032b5a745f24af8',
                 2009: 'https://open.spotify.com/playlist/4buS7K023UJkH6OkBnMc1i?si=c753de107fd74d3d',
                 2010: 'https://open.spotify.com/playlist/5RsWfxmjNbn5BvFdrXKVt6?si=898d1aa6b3ef4454',
                 2011: 'https://open.spotify.com/playlist/2RHg1WYjBWT2EQ9QtaJTKd?si=0bfd90774c01414c',
                 2012: 'https://open.spotify.com/playlist/0ATly1Vhu2JLUggKJ4Kp1P?si=1de7c66a7a3241c2',
                 2013: 'https://open.spotify.com/playlist/73ppZmbaAS2aW9hmDTTDcb?si=8a791d8e9dba4080',
                 2014: 'https://open.spotify.com/playlist/4dFOvmZkquNlmMohTpHVk0?si=f7b242f4a05b4561',
                 2015: 'https://open.spotify.com/playlist/2KayK25tHCMTLioPz2OLQp?si=bd70a04642dd494d',
                 2016: 'https://open.spotify.com/playlist/5nSPdyDCKD4VzEuBDP5X25?si=6180ae38bb9f4906',
                 2017: 'https://open.spotify.com/playlist/5vSiOmiS1UflyJkPBfMvqP?si=808cd3cc80034c9b',
                 2018: 'https://open.spotify.com/playlist/1hlmJOyuxrfPZi8XvuURbT?si=a98fc0aa20ed4b66',
                 2019: 'https://open.spotify.com/playlist/11AlRNIZxRcLOCqXEpXFlc?si=c4f98812bba14715',
                 2020: 'https://open.spotify.com/playlist/4PUAMFQpzsvIjn1YJNt6Do?si=b9505f41321945da'}
                 #'2021': []
                 #'Decade': 'https://open.spotify.com/playlist/1qLoOFlMBRMBTeSnQ5guuc?si=7066ac2f1a314725'}

#Set dictionary to store data in
dataDict = {'hottestID': [], 'artist': [], 'artistURI': [], 'artistLink': [],
            'track': [], 'trackLink': [], 'duration': [], 'explicit': [],
            'acousticness': [], 'danceability': [], 'energy': [],
            'instrumentalness': [], 'liveness': [], 'speechiness': [],
            'valence': [], 'key': [], 'tempo': [], 'timeSignature': []}

# %% Extract data

#Loop through playlists
for playlistKey in list(playlistLinks.keys()):
    
    #Get current playlist link
    playlistLink = playlistLinks[playlistKey]
    
    #Get the playlist URI
    playlistURI = playlistLink.split('/')[-1].split('?')[0]
    
    #Extract track details
    for track in spotifyClient.playlist_tracks(playlistURI)['items']:
        
        #Extract track details and append to data dictionary
        #Hottest 100 id
        dataDict['hottestID'].append(playlistKey)
        #Artist name
        dataDict['artist'].append(track['track']['artists'][0]['name'])
        #Artist spotify URI
        dataDict['artistURI'].append(track['track']['artists'][0]['uri'])
        #Spotify artist link
        if len(track['track']['artists'][0]['external_urls']) > 0:
            dataDict['artistLink'].append(track['track']['artists'][0]['external_urls']['spotify'])
        else:
            dataDict['artistLink'].append(np.nan)
        #Track name
        dataDict['track'].append(track['track']['name'])
        #Spotify track link
        if len(track['track']['external_urls']) > 0:
            dataDict['trackLink'].append(track['track']['external_urls']['spotify'])
        else:
            dataDict['trackLink'].append(np.nan)
        #Duration (ms)
        dataDict['duration'].append(track['track']['duration_ms']/1000)
        #Track explicitness
        dataDict['explicit'].append(track['track']['explicit'])
        
        #Download track artwork
        #Get the image data
        if len(track['track']['album']['images']) > 0:
            imgData = requests.get(track['track']['album']['images'][0]['url'],
                                   stream = True)
            #Save the image
            #Removes punctuation here to avoid issues with file naming
            with open('..\\img\\track-artwork\\'+str(playlistKey)+'-'+track['track']['name'].translate(str.maketrans('', '', string.punctuation))+'.jpg', 'wb') as outFile:
                shutil.copyfileobj(imgData.raw, outFile)
        
        #Extract audio features and append to data dictionary
        audioFeatures = spotifyClient.audio_features(track['track']['uri'])[0]
        #Get the desired features
        #Need to check if track URI is valid for audio features
        ##### TODO: what to do about invalid URIs?????
        if audioFeatures is not None:
            dataDict['acousticness'].append(audioFeatures['acousticness'])
            dataDict['danceability'].append(audioFeatures['danceability'])
            dataDict['energy'].append(audioFeatures['energy'])
            dataDict['instrumentalness'].append(audioFeatures['instrumentalness'])
            dataDict['liveness'].append(audioFeatures['liveness'])
            dataDict['speechiness'].append(audioFeatures['speechiness'])
            dataDict['valence'].append(audioFeatures['valence'])
            dataDict['key'].append(audioFeatures['key'])
            dataDict['tempo'].append(audioFeatures['tempo'])
            dataDict['timeSignature'].append(audioFeatures['time_signature'])            
        else:
            dataDict['acousticness'].append(np.nan)
            dataDict['danceability'].append(np.nan)
            dataDict['energy'].append(np.nan)
            dataDict['instrumentalness'].append(np.nan)
            dataDict['liveness'].append(np.nan)
            dataDict['speechiness'].append(np.nan)
            dataDict['valence'].append(np.nan)
            dataDict['key'].append(np.nan)
            dataDict['tempo'].append(np.nan)
            dataDict['timeSignature'].append(np.nan)
    
    #Get the playlist cover image        
    
    #Get the cover image URL
    coverImageURL = spotifyClient.playlist_cover_image(playlistURI)[0]['url']
    #Get the image data
    imgData = requests.get(coverImageURL, stream = True)
    #Save the image
    with open('..\\img\\playlist-artwork\\coverImage_'+str(playlistKey)+'.jpg', 'wb') as outFile:
        shutil.copyfileobj(imgData.raw, outFile)
            
#Convert data dictionary to dataframe
trackData = pd.DataFrame.from_dict(dataDict)

# %% Export data

#Export to csv
#Original wide format
trackData.to_csv('hottest100_SpotifyFeatureData_wide.csv',
                 encoding = 'utf-8-sig',
                 index = False)
#Adapted long format
trackDataLong = pd.melt(trackData,
                        id_vars = ['hottestID','artist', 'track'],
                        value_vars = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence'])
trackDataLong.to_csv('hottest100_SpotifyFeatureData_long.csv',
                     encoding = 'utf-8-sig',
                     index = False)

# %%% ----- End of collateTrackData.py -----
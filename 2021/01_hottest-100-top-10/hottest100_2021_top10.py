# -*- coding: utf-8 -*-
"""
@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Script to create visualisation of 2021 hottest 100 top 10 audio feature data
    
    TODO:
        - triple j logo at top of viz
        - descriptive text at top of viz
        - spotify or triple J fonts?
        - bar chart for each characteristic in column, rows = song
		- song artwork + artist and title to the left of chart area
    
"""

# %% Import packages

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib import gridspec
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import requests
import shutil
from PIL import Image

# %% Set-up

#Add custom fonts for use with matplotlib
fontDir = [os.getcwd()+'\\fonts']
for font in font_manager.findSystemFonts(fontDir):
    font_manager.fontManager.addfont(font)

#Set matplotlib parameters
from matplotlib import rcParams
# rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Arial'
rcParams['font.weight'] = 'bold'
rcParams['axes.labelsize'] = 12
rcParams['axes.titlesize'] = 16
rcParams['axes.linewidth'] = 1.5
rcParams['axes.labelweight'] = 'bold'
rcParams['legend.fontsize'] = 10
rcParams['xtick.major.width'] = 1.5
rcParams['ytick.major.width'] = 1.5
rcParams['legend.framealpha'] = 0.0
rcParams['axes.edgecolor'] = 'white'
rcParams['axes.facecolor'] = 'black'
rcParams['xtick.color'] = 'white'
rcParams['ytick.color'] = 'white'
rcParams['savefig.dpi'] = 300
rcParams['savefig.format'] = 'pdf'

#Set spotify client
#Please replace these with your own - don't mess around with other peoples IDs!
cid = 'bbb3754194114a88aadb477923261062'
secret = 'ae7e6c9e8a1643c3bc455dfd0846ef96'
client_credentials_manager = SpotifyClientCredentials(client_id = cid,
                                                      client_secret = secret)
spotifyClient = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Set audio features to plot
audioFeatureList = ['acousticness', 'speechiness', 'danceability',
                    'energy', 'valence']

#Set colours to use for audio features
audioFeaturesColourList = ['#f4c20d', #gold
                           '#00b7eb', #sky blue
                           '#ff608b', #pink
                           '#1ed760', #lime green
                           '#f9ff37'] #yellow

# %% Get song data from playlist

#Set dictionary to store data in
dataDict = {'artist': [], 'track': [],
            'acousticness': [], 'danceability': [], 'energy': [],
            'instrumentalness': [], 'speechiness': [],
            'valence': []}

#Set playlist link
playlistLink = 'https://open.spotify.com/playlist/63QIqDjGODEw47s9Wa6xJK?si=698d33ea93134a8a'

#Get the playlist URI
playlistURI = playlistLink.split('/')[-1].split('?')[0]

#Extract track details
for track in spotifyClient.playlist_tracks(playlistURI)['items']:
    
    #Extract track details and append to data dictionary
    #Artist name
    dataDict['artist'].append(track['track']['artists'][0]['name'])
    #Track name
    dataDict['track'].append(track['track']['name'])
    
    #Download track artwork
    #Get the image data
    imgData = requests.get(track['track']['album']['images'][0]['url'],
                           stream = True)
    #Save the image
    with open('img\\'+track['track']['name']+'.jpg', 'wb') as outFile:
        shutil.copyfileobj(imgData.raw, outFile)
    
    #Extract audio features and append to data dictionary
    audioFeatures = spotifyClient.audio_features(track['track']['uri'])[0]
    #Get the desired features
    #Need to check if track URI is valid for audio features
    if audioFeatures is not None:
        dataDict['acousticness'].append(audioFeatures['acousticness'])
        dataDict['danceability'].append(audioFeatures['danceability'])
        dataDict['energy'].append(audioFeatures['energy'])
        dataDict['instrumentalness'].append(audioFeatures['instrumentalness'])
        dataDict['speechiness'].append(audioFeatures['speechiness'])
        dataDict['valence'].append(audioFeatures['valence'])
    else:
        dataDict['acousticness'].append(np.nan)
        dataDict['danceability'].append(np.nan)
        dataDict['energy'].append(np.nan)
        dataDict['instrumentalness'].append(np.nan)
        dataDict['liveness'].append(np.nan)
        dataDict['speechiness'].append(np.nan)
        dataDict['valence'].append(np.nan)
			
#Convert data dictionary to dataframe
trackData = pd.DataFrame.from_dict(dataDict)

#Sort track data by artist
#Use of key ignores case in sorting by artist
trackData = trackData.sort_values(by = 'artist',
                                  key = lambda col: col.str.lower()).reset_index(drop = True)

#Change JID song name to fit on figure
trackData['track'][4] = 'Bruuuh (with Denzel Curry)'

#Rename image file too
shutil.move('img\\Bruuuh (with Denzel Curry) - Remix.jpg',
            'img\\Bruuuh (with Denzel Curry).jpg')

# %% Create visualisation

#Create figure
fig = plt.figure(figsize = (11,16))

#Set figure colouring
fig.patch.set_facecolor('#000000')

#Create the desired grid of axes to work with

#Set grid size for axes
gridSpec = gridspec.GridSpec(10, 6)

#Update spacing of grid
gridSpec.update(left = 0.2, right = 0.95,
                bottom = 0.05, top = 0.85, 
                wspace = 0.2, hspace = 0.1)

#Add axes and place artwork
for trackInd in range(len(trackData)):
    
    #Create the axis to place the artwork on
    plt.subplot(gridSpec.new_subplotspec((trackInd,0),
                                         colspan = 1, rowspan = 1))
    
    #Load the image
    img = Image.open(f'img\\{trackData["track"][trackInd]}.jpg')
    
    #Show the image on axes
    plt.imshow(img)
    
    #Turn the axes off
    plt.gca().axis('off')
    
    #Add artist and track name
    #Artist
    plt.gca().text(-0.1, 0.5, trackData['artist'][trackInd],
                   font = 'Circular Std Black', fontsize = 16, color = 'white',
                   va = 'center', ha = 'right',
                   transform = plt.gca().transAxes)
    #Track
    plt.gca().text(-0.1, 0.15, trackData['track'][trackInd],
                   font = 'Circular Std Book', fontsize = 12, color = 'white',
                   va = 'center', ha = 'right',
                   transform = plt.gca().transAxes)

#Loop through and plot audio features
for featureInd in range(len(audioFeatureList)):
    
    #Add axes
    plt.subplot(gridSpec.new_subplotspec((0,featureInd+1),
                                         colspan = 1, rowspan = 10))
    
    #Get current axis
    ax = plt.gca()
    
    #Change y-axis origin to upper
    ax.invert_yaxis()
    
    #Despine all axes
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    #Set axes ticks to line up with track artwork
    ax.set_yticks(np.linspace(1/len(trackData)/2,
                              1 - 1/len(trackData)/2,
                              len(trackData)))
    
    #Add gridlines at y-ticks
    plt.grid(visible = True, which = 'major', axis = 'y',
             color = audioFeaturesColourList[featureInd],
             linestyle = '-', linewidth = 2, alpha = 0.75)
    
    #Remove y-ticks and labels
    ax.tick_params(axis = 'both', length = 0)
    ax.set_yticklabels([])
    
    #Set x and y limits
    ax.set_ylim([0,1])
    ax.set_xlim([0,1])
    
    #Extract values to plot
    audioVals = trackData[audioFeatureList[featureInd]].values
    
    #Add points over grid lines
    ax.scatter(np.flip(audioVals),
               np.linspace(1/len(trackData)/2, 1 - 1/len(trackData)/2,len(trackData)),
               s = 250, marker = 'o', facecolors = 'black',
               edgecolors = audioFeaturesColourList[featureInd],
               clip_on = False, zorder = 5)
                   
    #Add title
    plt.title(audioFeatureList[featureInd].capitalize(),
              color = audioFeaturesColourList[featureInd],
              font = 'Circular Std Bold', fontsize = 14,
              pad = 10)
    
    #Add music note symbol in highest ranked for current feature
    #Find index of maximum value
    maxInd = np.where(np.max(audioVals) == np.flip(audioVals))[0][0]
    #Set y-point based on index
    yPt = np.linspace(1/len(trackData)/2,
                      1 - 1/len(trackData)/2,
                      len(trackData))[maxInd]
    #Set x-point based on value
    xPt = np.max(audioVals)
    #Add text at set point
    ax.text(xPt, yPt, u'\u266b',
            color = audioFeaturesColourList[featureInd],
            fontsize = 12, ha = 'center', va = 'center',
            zorder = 6)
    
    #Set x-axis ticks and labels
    ax.set_xticks([])
    ax.set_xticklabels([])
    
#Add title
fig.text(0.5, 0.96,
         'Hottest 100 2021: My Votes',
         font = 'ABCSans', fontsize = 34, color = 'white',
         ha = 'center', va = 'center')

#Add supplementary text
fig.text(0.5, 0.92,
         'Audio features ranked on scale from 0%-100%. Top value in each category indicated by music note.',
         font = 'Circular Std Book', fontsize = 12, color = 'white',
         ha = 'center', va = 'center')
fig.text(0.5, 0.90,
         'Songs ordered alphabetically by artist.',
         font = 'Circular Std Book', fontsize = 12, color = 'white',
         ha = 'center', va = 'center')

#Add data source and details text
fig.text(0.995, 0,
         'Author: Aaron Fox (@aaron_s_fox) | Source: Spotify',
         font = 'Circular Std Bold', fontsize = 10, color = 'white',
         ha = 'right', va = 'bottom')

#Save figure
#Weird issues with figure ratio & spacing if not running this as a separate chunk
plt.savefig('hottest100_2021_top10.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 600)

# %%% ----- End of hottest100_2021_top10.py -----
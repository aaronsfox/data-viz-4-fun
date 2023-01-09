# -*- coding: utf-8 -*-
"""

@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    Twitter: @aaron_s_fox
    Github: aaronsfox
    
"""

# %% Import packages

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# %% Set-up

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
rcParams['savefig.dpi'] = 300
rcParams['savefig.format'] = 'pdf'

# %% Create viz

#Read in dataset
data = pd.read_csv('goalkicks.csv')

#Set title
figTitle = 'Goalkicks in Premier League'

#Set subtitle
figSubtitle = 'Average length of goalkicks among Premier League teams | 21-22 season | Data: Statsbomb via Fbref  By: Odriozolite'

#Create figure
fig, ax = plt.subplots(nrows = 1, ncols = 1, figsize = (10,6))
plt.subplots_adjust(left = 0.05, right = 0.95, top = 0.9, bottom = 0.1)

#Set limit
ax.set_xlim([-1,70])
ax.set_ylim([0,35])

#Select random ranks to text
ranksToText = [0, 1, 3, 5, 9, 11, 13, 15]

#Loop through teams and create the circles
for teamInd in range(len(data['team'])):
    #Create the circle
    goalKickCirc = plt.Circle((data['avg_goal_kick_len'][teamInd]/2,0),
                              radius = data['avg_goal_kick_len'][teamInd]/2,
                              facecolor = 'none', edgecolor = '#543659',
                              linewidth = 5, alpha = 0.6)
    #Add the circle
    ax.add_artist(goalKickCirc)
    
    #Get the image url
    imgUrl = data['url_logo_espn'][teamInd]
    
    #Get the image
    logoImg = io.imread(imgUrl)
    
    #Add image
    ax.imshow(logoImg, origin = 'lower',
               extent = (data['avg_goal_kick_len'][teamInd] - 1,
                         data['avg_goal_kick_len'][teamInd] + 1,
                         1, -1),
               zorder = 5,
               clip_on = False)
    
    # #Add text
    # ax.text(data['avg_goal_kick_len'][teamInd], -2,
    #         str(np.round(data['avg_goal_kick_len'][teamInd],2)),
    #         fontsize = 8, fontweight = 'normal',
    #         ha = 'center', va = 'center',
    #         clip_on = False)

    
#Add figure title using text
fig.text(0.01, 0.98, figTitle,
         fontsize = 18, fontweight = 'bold', ha = 'left', va = 'top')
fig.text(0.01, 0.93, figSubtitle,
         fontsize = 10, fontweight = 'normal', ha = 'left', va = 'top')

#Despine
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

#Turn off axes ticks
ax.set_xticks([])
ax.set_yticks([])

#Set figure and axes colouring
ax.set_facecolor('#f2f2f2')
fig.patch.set_facecolor('#f2f2f2')

#Add league logo
#Load image
leagueImg = plt.imread('Premier_League_Logo.png')
#Create offset image
imOffset = OffsetImage(leagueImg, zoom = 0.1)
#Create annotation box
annBox = AnnotationBbox(imOffset, (0.99,0.99),
                        #xybox = (0, 0),
                        frameon = False,
                        box_alignment = (1,1),
                        xycoords = fig.transFigure,
                        #boxcoords = 'offset points',
                        pad = 0)
#Add the image
ax.add_artist(annBox)

#Add annotations
#Chelsea and macnhester city
ax.text(15,8, 'Chelsea and Manchester City',
        fontsize = 10, fontweight = 'bold',
        ha = 'center', va = 'center')
ax.text(15,6.9, 'like to keep it short and build',
        fontsize = 10, fontweight = 'normal',
        ha = 'center', va = 'center')
ax.text(15,5.8, 'from the back.',
        fontsize = 10, fontweight = 'normal',
        ha = 'center', va = 'center')

#Add the line
plt.plot([24,24], [8.7, 5.0],
         color = 'black', linewidth = 1.5)

#Add annotations
#Burnley and everton
ax.text(66,27, 'Burnley and Everton',
        fontsize = 10, fontweight = 'bold',
        ha = 'center', va = 'center')
ax.text(66,25.9, "don't mess around",
        fontsize = 10, fontweight = 'normal',
        ha = 'center', va = 'center')
ax.text(66,24.8, 'with their goalkicks.',
        fontsize = 10, fontweight = 'normal',
        ha = 'center', va = 'center')

#Add the line
plt.plot([60,72], [23, 23],
         color = 'black', linewidth = 1.5,
         clip_on = False)

#Save figure
plt.savefig('vizBuzz_02.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

# %%% ----- End of vizBuzz_02.py -----
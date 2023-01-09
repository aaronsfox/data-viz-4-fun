# -*- coding: utf-8 -*-
"""
@author: 
    Aaron Fox
    Centre for Sport Research
    Deakin University
    aaron.f@deakin.edu.au
    
    Script to create visualisation of hottest 100 audio feature data
    
    TODO:
        - triple j logo at top of viz
        - descriptive text at top of viz
        - spotify or triple J fonts?
        - colour palette for each year?
        - X rows by 1 column subplot
        - years as the x-axis ticks
        - y values as the variable data values
        - playlist cover images at the top of the first subplot axes
        - label to x-axis ticks on the bottom subplot with year label
        - box plot with median and IQR, with no cap whiskers 25%-75%
        - strip/pointplot underneath with individual data values
        - annotate specific songs (e.g. max and min in certain variables)
		- use a single colour for each subplot but scale the alpha based on the median value
    
"""

# %% Import packages

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% Define functions

### TODO: define any functions here

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

#Load long format dataset for use
trackData = pd.read_csv('data\\hottest100_SpotifyFeatureData_long.csv')

# %%

### TODO: start code sections here...

#Get certain variable
varData = trackData.loc[trackData['variable'] == 'danceability', ]
#figure example
fig, ax = plt.subplots(figsize=(7, 6))
sns.stripplot(data = varData, x = 'hottestID', y = 'value',
              size = 3, jitter = True, linewidth = 0,
              alpha = 0.4, zorder = 1,
              ax = ax)
sns.boxplot(data = varData, x = 'hottestID', y = 'value',
            whis = 1.5, width = 0.6, fliersize = 0,
            zorder = 4,
            ax = ax)
ax.set_ylim([0.0,1.0])



# %%% ----- End of X.py -----
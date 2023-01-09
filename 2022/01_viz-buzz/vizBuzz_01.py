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
import matplotlib.pyplot as plt
import numpy as np

# %% Create viz

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

#Read dataset
data = pd.read_csv('movies.csv')

#Check variables
data['clean_test'].unique()
data['binary'].unique()

#Create variable that distributes to to year brackets
#Do this in a lame loop as I don't have time to figure out another way
yearCat = []
for year in data['year']:
    if year >= 1970 and year <= 1974:
        yearCat.append('1970-74')
    elif year >= 1975 and year <= 1979:
        yearCat.append('1975-79')
    elif year >= 1980 and year <= 1984:
        yearCat.append('1980-84')
    elif year >= 1985 and year <= 1989:
        yearCat.append('1985-89')
    elif year >= 1990 and year <= 1994:
        yearCat.append('1990-94')
    elif year >= 1995 and year <= 1999:
        yearCat.append('1995-99')
    elif year >= 2000 and year <= 2004:
        yearCat.append('2000-05')
    elif year >= 2005 and year <= 2009:
        yearCat.append('2005-09')
    elif year >= 2010:
        yearCat.append('2010-13')
data['yearCat'] = yearCat

#Count up those that meet each category and convert to percentage
totalMovies = data.groupby(['yearCat'])['year'].count().reset_index()

#COunt up by category and test value
testCount = data.groupby(['clean_test','yearCat'])['year'].count().reset_index(name = 'counts')

#Get zero year values
finalCount = pd.pivot_table(testCount,
                            index=['clean_test','yearCat'],
                            values='counts',                            
                            fill_value = 0,
                            dropna=False,
                            aggfunc=np.sum).reset_index()

#Calculate proportions
props = []
for ii in range(len(finalCount)):
    
    #Get year category
    yearCat = finalCount['yearCat'][ii]
    
    #Get value and divide by total in year
    props.append(finalCount['counts'][ii] / totalMovies.loc[totalMovies['yearCat'] == yearCat,['year']].values[0][0])

#Add to dataframe
finalCount['props'] = props

#Set list of year categories
yearCats = list(data['yearCat'].unique())
yearCats.reverse()

#Set list of clean tests
testVals = ['ok', 'dubious', 'men', 'notalk', 'nowomen']

#Set colours
cols = {'ok': '#008fd5', 'dubious':'#6bb2d5', 'men': '#ffc9bf', 'notalk': '#ff9380', 'nowomen': '#ff2700'}

#Set z orders 
z = {'ok': 5, 'dubious':4, 'men': 3, 'notalk': 2, 'nowomen': 1}

#Create figure window
fig,ax = plt.subplots(nrows = 1, ncols = 1, figsize=(7,6))

#Create base array to build bars on
baseProps = np.zeros(len(yearCats))

#Loop through and build stacked bar chart
for testResult in testVals:
    
    #Get the proportions
    currProps = finalCount.loc[finalCount['clean_test'] == testResult, ['props']].to_numpy().flatten()
    
    #Add together before plotting
    baseProps = baseProps + currProps
    
    #Add to bar graph
    ax.bar(yearCats, baseProps, color = cols[testResult], zorder = z[testResult])
    
#Set y-axis limits
ax.set_ylim([0,1])

#Set y-axis ticks and labels
ax.set_yticks([0,0.25,0.5,0.75,1.0])
ax.set_yticklabels(['0', '25', '50', '75', '100%'])

#Set xticks and labels
ax.set_xticks(ax.get_xticks()[::2])
ax.set_xticklabels(["1970 - \n'74", "1980 - \n'84", "1990 - \n'94",
                    "2000 - \n'04", "2010 - \n'13"])

#Despine
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['right'].set_visible(False)

#Squeeze x limits
ax.set_xlim([-0.5,8.5])

#Set figure and axes colouring
ax.set_facecolor('#f0f0f0')
fig.patch.set_facecolor('#f0f0f0')

#Add figure title using text
fig.text(0.01, 0.98, 'The Bechdel Test Over Time',
         fontsize = 16, fontweight = 'bold', ha = 'left', va = 'top')
fig.text(0.01, 0.94, 'How women are represented in movies',
         fontsize = 12, fontweight = 'normal', ha = 'left', va = 'top')

#Set vertical and horizontal spacing
plt.subplots_adjust(left = 0.07, right = 0.85)

#Add annotations
ax.text(ax.get_xlim()[1]+0.2, 0.96, "Fewer than\ntwo women",
        fontsize = 10, fontweight = 'normal', 
        va = 'center', ha = 'left',
        c = 'black')

ax.text(ax.get_xlim()[1]+0.2, 0.76, "Women don't\ntalk to each\nother",
        fontsize = 10, fontweight = 'normal', 
        va = 'center', ha = 'left',
        c = 'black')

ax.text(ax.get_xlim()[1]+0.2, 0.60, "Women only\ntalk about men",
        fontsize = 10, fontweight = 'normal', 
        va = 'center', ha = 'left',
        c = 'black')

ax.text(ax.get_xlim()[1]+0.2, 0.49, "Dubious",
        fontsize = 10, fontweight = 'normal', 
        va = 'center', ha = 'left',
        c = 'black')

ax.text(ax.get_xlim()[1]+0.2, 0.25, "Passes\nBechdel\nTest",
        fontsize = 10, fontweight = 'normal', 
        va = 'center', ha = 'left',
        c = 'black')

#Save figure
plt.savefig('vizBuzz_redemption.png', format = 'png', 
            facecolor = fig.get_facecolor(), edgecolor = 'none',
            dpi = 300)

# %%% ----- End of vizBuzz_01.py -----
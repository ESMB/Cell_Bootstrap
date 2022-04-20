#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 11:03:42 2022

@author: Mathew
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import bootstrap
import numpy as np


rng = np.random.default_rng()


pathlist=[]

tosave=""

pathlist.append("")


# Colors

color=[]
color.append('#0000ff')
color.append('#ff0000')
color.append('#008b00')
color.append('#ffd700')
i=0

Output_all = pd.DataFrame(columns=['Path','low','mean','high'])
# Read  file containing data
for path in pathlist:
    df=pd.read_csv(path, header=None)
    
    data = (df,)
    
# This calculates the confidence intervals. 

    res = bootstrap(data, np.std, confidence_level=0.95,
                    random_state=rng)
    print(res.confidence_interval)
    
    av=df.mean()
    
    av_min=av-res.confidence_interval[0]
    av_high=av+res.confidence_interval[1]
     
# This is to generate a histogram showing FRET after bootstrapping. 
    
    samples=df[0].to_numpy()
    my_samples = []
    for _ in range(9999):
        x = np.random.choice(samples, size=10, replace=True)
        my_samples.append(x.mean())
    
    plt.hist(my_samples,bins = 50,range=[0.1,0.5], rwidth=0.9,ec='black',color=color[i],alpha=0.8, label=str(i))
    plt.legend()
    plt.xlabel('Proximity ratio')
    plt.ylabel('#')
    plt.savefig(tosave+"histogram.pdf")

    i=i+1
    Output_all= Output_all.append({'Path':path,'low':av_min[0],'mean':av[0],'high':av_high[0]},ignore_index=True)

    Output_all.to_csv(tosave + '/' + 'all_metrics.csv', sep = '\t')

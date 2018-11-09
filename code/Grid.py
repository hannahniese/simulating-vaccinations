# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 16:03:44 2018

@author: markus
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import vacc as people
import time

people.get_started()

time.sleep(5)

# number of people
num = people.population
sqrtnum = int(np.sqrt(num))

population = np.empty((sqrtnum, sqrtnum))
i = 0
j = 0
while j < sqrtnum:
    population[i,j] = people.people_list[i + j*sqrtnum].get_status()
    i += 1
    if i >= sqrtnum:
        j += 1
        i = 0
    
# graphic
fig = plt.figure()
cmap = plt.get_cmap('brg', 8)
mat = plt.imshow(population, cmap=cmap, interpolation='nearest', animated=True)
cax = plt.colorbar(mat, ticks=np.arange(0, 8))
plt.clim(0, 8)
plt.grid(True)

    
mat.set_data(population)
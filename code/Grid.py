# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 12:16:03 2018

@author: timos
"""

import Spread_of_disease_without_vaccination as cl

population = 100
people_list = [0] * population


#create population
for x in range(0,population):
    people_list[x] = cl.People(False, 1, x)
 
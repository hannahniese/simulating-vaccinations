# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 16:00:00 2018

@author: timos
"""

import csv
import matplotlib.pyplot as plt


'''
Reads in a csv table and plots its content.
Important:
    First line of csv has to be description of data or empty!
    Second line is the labels of the axis
'''

filename = 'total infected people without initially infected' #is also title of plot

#read csv to data_list
with open('csv_to_plot/' + filename + '.csv', 'r') as datas:
    reader = csv.reader(datas)
    data_list = list(reader)

print(data_list[0][0]) #print description

data_list.pop(0) #delete first empty row

plt.xlabel(data_list[0][0])
plt.ylabel(data_list[0][1])
plt.title(filename)

data_list.pop(0) #delete second row with axis labels


x_list = []
y_list = []

#fill datas into x_list and y_list
for t in data_list:
    x_list.append(float(t[0]))
    y_list.append(float(t[1]))

#print(x_list)

plt.plot(x_list, y_list, color = 'navy')

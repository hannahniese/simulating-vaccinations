# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:23:50 2018

@author: markus
"""

import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import vacc
import game_theory_tools as tool


# parameters for the disease

#Population parameters
population = 5493 #number of people in our simulation
population_alive = 10000 #number of people alive at the start of the simulation
vaccinated_people = 0 #number of people, who are vaccinated
infected_people = 0 #number of currently infected people


daily_contacts_when_healthy = 2 #daily contacts of healthy people with other people
daily_contacts_when_sick = 1 #daily contacts of a sick person with other people

people_list = [0] * population #in this list, we store the people-objects
infected_people_list = [] #integer-list: we store for every day the total number 
                          #of currently infected people
vaccinated_people_list = [] #integer-list: stores for every day the number of 
                            #vaccinated people


#Diseases parameters
prob_for_diseases = 0 #Random probability (per day and person) to become
                            #sick without beeing infected by someone else
prob_for_contact_infection = 0.05 #probability to infect an other person, when
                                 #there is a contact
incubation_time = 2 #days until person realizes that it is sick (needed for daily contacts)
time_to_get_healthy = 10 #counts days from infection. After this time, a person
                         #becomes healty
                         
vacc.init_parameters(population, vaccinated_people, infected_people,\
        daily_contacts_when_healthy, daily_contacts_when_sick,\
        prob_for_diseases, prob_for_contact_infection,\
        incubation_time, time_to_get_healthy, population_alive)
                         

#create population in people_list
for x in range(0,population):
    people_list[x] = vacc.Network_Person(False, -1, x) 
    
tool.initial_infected(people_list, 0.005)

tsvfile = open("edges.tsv")
reader = csv.reader(tsvfile, delimiter='\t')
for row in reader:
    people_list[int(row[0])].add_contact(int(row[1]))
    
    
simulation_time = 200 
for days in range(0,simulation_time):
    
    
    #one day is over
    for x in range(0,population): 
        people_list[x].next_day()
        
    # TODO
    for x in range(0,population): 
        people_list[x].get_vaccinated()
        
    #looks, which people are infected during this day
    #updates infected_neighbors of all neighbors
    for x in range(0,population): 
        infections = people_list[x].start_infection()
        for i in infections:
            people_list[i].get_infected()
        if people_list[x].infected_days == incubation_time:
            for i in people_list[x].contacts:
                people_list[i].infected_contacts += 1
        if people_list[x].infected_days == 10:
            for i in people_list[x].contacts:
                people_list[i].infected_contacts -= 1
    

    #append the number of infected people of this day to infected_people_list
    infected_people_list.append(vacc.get_num_infected_people()) 
    # append the number of vaccinated people of this day to the vaccinated_people_list
    vaccinated_people_list.append(vacc.get_num_vaccinated_people())
    
        #if days > simulation_time * 0.4:
    #calculate average of infected people per day
#    if infected_people > 0: 
#        average += infected_people
#        count += 1

new_vaccinations = tool.discrete_gradient(vaccinated_people_list)
#plot
plt.xlabel('Time (days)')
plt.ylabel('Infected people')

plt.plot(infected_people_list)
#plt.plot(vaccinated_people_list)
plt.plot(new_vaccinations)
plt.show()
    

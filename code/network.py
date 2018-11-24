# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:23:50 2018

@author: markus
"""
## import packages
import csv
import numpy as np
import matplotlib.pyplot as plt
import random
import timeit
## import modules
import vacc
import game_theory_tools as tool

## start the time measurement of the simulation
start = timeit.default_timer()


### parameters for the simulation

## Population parameters
population = 4000 # number of people in the simulation
population_alive = 10000 #number of people alive at the start of the simulation
vaccinated_people = 0 # number vaccinated people
infected_people = 0 # number of infected people

## irrelevant for grid and network model
daily_contacts_when_healthy = 2 # daily contacts of healthy people with other people
daily_contacts_when_sick = 1 # daily contacts of a sick person with other people

## Lists of persons and number of infected/vaccinated people
people_list = [0] * population # list of Person objects (or derived class)
infected_people_list = [] # int-list: the total number of infected people on
                          # each day
vaccinated_people_list = [] # int-list: the total number of vaccinated people
                            # each day

## Diseases parameters
prob_for_diseases = 0.00001 # Random probability (per day and person) to become
                            # sick without beeing infected by someone else
prob_for_contact_infection = 0.01 # probability to infect an other person, when
                                  # there is a contact
incubation_time = 12 # Incubation Period of the diseasse
time_to_get_healthy = 42 # after that time a person becomes healthy again
                         
## Length of the Simulation
simulation_length = 400

## Initializes the global parameters for the Person Class
## !!!required!!!
vacc.init_parameters(population, vaccinated_people, infected_people,\
        daily_contacts_when_healthy, daily_contacts_when_sick,\
        prob_for_diseases, prob_for_contact_infection,\
        incubation_time, time_to_get_healthy, population_alive)
                         
## Initial values of the percieved cost of vaccination and infection
## for all people the same
percieved_vacc_cost = 0.001
percieved_infec_cost = 0.01
## create population in people_list
for x in range(0,population):
    people_list[x] = vacc.Network_Person(False, -1, x, percieved_vacc_cost, percieved_infec_cost) 

## set initial conditions    
tool.initial_infected(people_list, 0.001)
tool.initial_vaccinated(people_list, 0.3)

## make initial counts
count = 0
for x in people_list:
    if x.vaccinated == True:
        count += 1
print("Initially vaccinated:", count)
count = 0
for x in people_list:
    if x.infected_days != -1:
        count += 1
print("Initially infected:", count)

## import network from a tsv file
## the file has to have two column. One with the starting and one with the
## ending vertice of each arc. For undirected graphs both directions have
## to be given. The population has to be set manually to the number of vertices
#tsvfile = open("edges.tsv")
#reader = csv.reader(tsvfile, delimiter='\t')
#for row in reader:
#    people_list[int(row[0])].add_contact(int(row[1]))
    
## make random arcs with exponential distribution
for x in people_list:
    contacts = int(np.random.exponential(100))
    for i in range(contacts):
        a = random.randint(0,population-1)
        if a not in x.contacts:
            x.contacts.append(a)
        else:
            i = i-1
    
## simulation
for days in range(0,simulation_length):
    
    # iterate over the people_list every time step
    for x in range(0,population):
        people_list[x].next_day()
        people_list[x].get_vaccinated()
        # sick people infect randomly their contacts
        infections = people_list[x].start_infection()
        for i in infections:
            people_list[i].get_infected()
        # changes the parameters infected_contacts and infec_cost if the 
        # person becomes sick (incubation period) and healthy
        if people_list[x].infected_days == incubation_time:
            for i in people_list[x].contacts:
                people_list[i].infected_contacts += 1
                people_list[i].change_infec_cost_relative(1.5)
        if people_list[x].infected_days == time_to_get_healthy:
            for i in people_list[x].contacts:
                people_list[i].infected_contacts -= 1
                people_list[i].change_infec_cost_relative(-1.3)
    
    # removes and re-adds some vertices according to death rate
    for x in range(population):
        if random.random() < 0.00002:
            people_list[x].kill()
            people_list[x].get_born(False, -1)
        
    # Updates Infected_people_list and vaccinated_people_list
    count = 0
    for x in people_list:
        if x.infected_days != -1:
            count += 1
    infected_people_list.append(count)    
    
    count = 0
    for x in people_list:
        if x.vaccinated:
            count += 1
    vaccinated_people_list.append(count)    
            

    ##append the number of infected people of this day to infected_people_list
    #infected_people_list.append(vacc.get_num_infected_people()) 
    #append the number of vaccinated people of this day to the vaccinated_people_list
    #vaccinated_people_list.append(vacc.get_num_vaccinated_people())
    
## count the vaccinations at the end
count = 0
for x in people_list:
    if x.vaccinated:
        count += 1
print("Vaccinated at the end:", count)

new_vaccinations = tool.discrete_gradient(vaccinated_people_list)
# create the plot
plt.xlabel('Time (days)')
plt.ylabel('Infected people')

plt.plot(infected_people_list)
plt.plot(vaccinated_people_list)
plt.plot(new_vaccinations)
plt.show()

## print the time of the simulation
end = timeit.default_timer()
time = end - start
print("Running time:", time)
    

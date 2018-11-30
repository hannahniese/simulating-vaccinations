# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:23:50 2018

@author: markus
"""
"""
Markus:
    Alter
    days since immunization
    change vacc scares
    
    Momentan steckt man nur bis zur incubationperiod and
    
"""
## import packages
import csv
import numpy as np
import matplotlib.pyplot as plt
import random
import timeit
import matplotlib.ticker as ticker
## import modules
import vacc
import simulation_vaccination_tools as tool
import network_generator

## start the time measurement of the simulation
start = timeit.default_timer()


### parameters for the simulation

## Population parameters
population = 10000 # number of people in the simulation
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
prob_for_diseases = 0.0001 # Random probability (per day and person) to become
                            # sick by someone outside the network
prob_for_contact_infection = 0.5 # probability to infect an other person, when
                                  # there is a contact
incubation_time = 12 # Incubation Period of the diseasse
time_to_get_healthy = 42 # after that time a person becomes healthy again
start_being_infectious = 7 # number of days after which a infected person
                            # becomes infectious

                         
## Initial values of the percieved cost of vaccination and infection
## for all people the same
percieved_vacc_cost = 0.02
percieved_infec_cost = 1

# The probability for a person to meet a contact each day
probability_to_meet = 0.5
 
                           
## Length of the Simulation
simulation_length = 365

## Initializes the global parameters for the Person Class
## !!!required!!!
vacc.init_parameters(population, vaccinated_people, infected_people,\
        daily_contacts_when_healthy, daily_contacts_when_sick,\
        prob_for_diseases, prob_for_contact_infection,\
        incubation_time, time_to_get_healthy, population_alive,\
        start_being_infectious)
                         
## create population in people_list
for x in range(0,population):
    age = random.randint(0, 365000)
    people_list[x] = vacc.Network_Person(False, -1, x, percieved_vacc_cost,\
               percieved_infec_cost, age = age, length_immune_mean = 4380,\
               length_immune_sigma = 100) 

## set initial conditions    
tool.initial_infected(people_list, 0.01)
tool.initial_vaccinated(people_list, 0.3)

## make initial counts
print("Initially vaccinated:", vacc.get_num_vaccinated_people())
print("Initially infected:", vacc.get_num_infected_people())


### generate the network
# 1. Op: Directly using network_generator.generate_Albert_Barabasi()
# random network. Very slow. !!!Only use for population up to 1000!!!
# 2. Op: Import random Albert-Barabasi_Graph generated with 
# network_generator.create_barabasi_in_file() and import using
# network_generator.import_barabasi_graph()
# 3. Op: Import from a TSV file using network_generator.import_graph_from_tsv()
# !!! Important !!! For options 2 and 3 population (len(people_list)) HAS to be
# equal to the number of nodes in the imported graph

#network_generator.generate_Albert_Barbasi(people_list, 2, 3)
network_generator.import_barabasi_graph("Networks/barabasi_10000_2.txt", people_list)
#network_generator.import_graph_from_tsv("Networks/edges.tsv", people_list)
    

## simulation
for days in range(0,simulation_length):
    
    # iterate over the people_list every time step
    for x in range(0,population):
        people_list[x].next_day()
  #      people_list[x].get_vaccinated()
        # sick people infect randomly their contacts
        infections = people_list[x].start_infection(probability_to_meet)
        for i in infections:
            people_list[i].get_infected()
        # changes the parameters infected_contacts and infec_cost if the 
        # person becomes sick (incubation period) and healthy
        if people_list[x].infected_days == incubation_time:
            for i in people_list[x].contacts:
                people_list[i].infected_contacts += 1
                people_list[i].change_infec_cost_relative(1.2)
        if people_list[x].infected_days == time_to_get_healthy:
            for i in people_list[x].contacts:
                people_list[i].infected_contacts -= 1
                people_list[i].change_infec_cost_relative(0.9)
    
    # removes and re-adds some vertices according to death rate
#    for x in range(population):
#        if random.random() < 0.0000214: # probability to die at this day
#                                        # deathrate 8/1000 per year
#            people_list[x].kill()
#            people_list[x].get_born(False, -1)
        
    # Updates infected_people_list and vaccinated_people_list
    infected_people_list.append(vacc.get_num_infected_people())    
    vaccinated_people_list.append(vacc.get_num_vaccinated_people())
    
    # Calculate the average number of infected people for last 100 days
    if days > 100:
        average_100 = np.average(infected_people_list[days-100:days])
        if average_100 < 5 and random.random() < 0.01:
            tool.change_vaccination_cost_population(people_list, 1, 0.3)
    
## Count the vaccinations at the end
print("Vaccinated at the end:", vacc.get_num_vaccinated_people())
print("Maximal number of vaccinated people:", max(vaccinated_people_list))

gradient_vaccinations = tool.discrete_gradient(vaccinated_people_list)
gradient_infections = tool.discrete_gradient(infected_people_list)

## Graphic options
width_of_line = 3

## Create the plot
plt.axes().yaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1))
plt.xlabel('Time (days)')
plt.ylabel('Percentage of Population')

plt.plot(np.divide(infected_people_list, population), color = 'darkred', label = '% infected people',\
         linewidth = width_of_line)
#plt.plot(np.divide(gradient_infections, population), color = 'peru', label = '% change of infected people',\
#         linewidth = width_of_line)
plt.plot(np.divide(vaccinated_people_list, population), color = 'navy', label = '% vaccinated people',\
         linewidth = width_of_line)
#plt.plot(np.divide(gradient_vaccinations, population), color = 'cadetblue', label = '% change of vaccinated people',\
#         linewidth = width_of_line)
plt.legend(loc = 'best')
plt.show()

test = 0
for x in people_list:
    if x.days_since_immunization != 0:
        test += 1
print("Immune", test)


## print the time of the simulation
end = timeit.default_timer()
time = end - start
print("Running time:", time)
    

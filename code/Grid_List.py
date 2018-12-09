# -*- coding: utf-8 -*-
"""
Simulating vaccination
Created as part of the ETH course "Lecture with Computer Exercises: 
    Modelling and Simulating Social Systems in MATLAB (or Python)"
Find all information about the code in code/readme.txt
December 2018
@author: Hannah Niese, Markus Niese, Timo Schönegg
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import vacc
import simulation_vaccination_tools as tool
import datetime

# parameters for the disease

#Population parameters
population = 10000 #number of people in our simulation
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
prob_for_contact_infection = 0.1 #probability to infect an other person, when
                                 #there is a contact
incubation_time = 12 #days until person realizes that it is sick (needed for daily contacts)
time_to_get_healthy = 42 #counts days from infection. After this time, a person
                         #becomes healty

## Initial values of the percieved cost of vaccination and infection
## for all people the same
percieved_vacc_cost = 1
percieved_infec_cost = 20000    

                         
vacc.init_parameters(population, vaccinated_people, infected_people,\
        daily_contacts_when_healthy, daily_contacts_when_sick,\
        prob_for_diseases, prob_for_contact_infection,\
        incubation_time, time_to_get_healthy, population_alive)
                         
#create population in people_list
for x in range(0,population):
    if x == int(population/2 + np.sqrt(population)/2): #person is initially infected
            people_list[x] = vacc.Grid_Person(False, 1, x, percieved_vacc_cost, percieved_infec_cost)
            infected_people += 1
    else:
        people_list[x] = vacc.Grid_Person(False, -1, x, percieved_vacc_cost, percieved_infec_cost)
    

#Simulation
average = 0 #average number of sick people
count = 0 #needed to calculate average

simulation_time = 1000 #days of simulation

#file name is current date
now = datetime.datetime.now()
date = str(int(now.year/10)) + str(now.year % 10) + '-' + \
           str(int(now.month/10)) + str(now.month % 10) + '-' + \
           str(int(now.day/10)) + str(now.day % 10)
           
time = str(int(now.hour/10)) + str(now.hour % 10) + '-' + \
           str(int(now.minute/10)) + str(now.minute % 10) + '-' + \
           str(int(now.second/10)) + str(now.second % 10)

#create .txt file
f = open('grid_graphics/' + date + '_' + time + '.txt',"w+")

f.write("Population: %d\n" % population)
f.write("Prob_for_contact_infection: %d Prozent \n" % (prob_for_contact_infection*100))
f.write("***\n")

#simulate spread of infection
for days in range(0,simulation_time):
    
    daily_file_input = ""
    
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
        #print(infections)
        for i in infections:
            people_list[i].get_infected()
        if people_list[x].infected_days == incubation_time:
            neighbors = people_list[x].get_neighborhood()
            for i in neighbors:
                people_list[i].infected_neighbors += 1
        if people_list[x].infected_days == 10:
            neighbors = people_list[x].get_neighborhood()
            for i in neighbors:
                people_list[i].infected_neighbors -= 1
    
    #file input
    for x in range(0,population): 
        daily_file_input += str(people_list[x].get_status()) + ' '
        
    f.write(daily_file_input + '\n')
    
    #append the number of infected people of this day to infected_people_list
    infected_people_list.append(vacc.get_num_infected_people()) 
    # append the number of vaccinated people of this day to the vaccinated_people_list
    vaccinated_people_list.append(vacc.get_num_vaccinated_people())
    
        #if days > simulation_time * 0.4:
    #calculate average of infected people per day
    if infected_people > 0: 
        average += infected_people
        count += 1


f.close() 


new_vaccinations = tool.discrete_gradient(vaccinated_people_list)
#plot
plt.xlabel('Time (days)')
plt.ylabel('Infected people')

plt.plot(infected_people_list)
#plt.plot(vaccinated_people_list)
plt.plot(new_vaccinations)
plt.show()

if count != 0 and population != 0:
    percentage_infected_people = (float(average)/float(count))/float(population)*100 #average calculation
    print("In average", round(percentage_infected_people,1), "% of the population is infected.")

#for x in people_list:
#    print(x.infected_neighbors)

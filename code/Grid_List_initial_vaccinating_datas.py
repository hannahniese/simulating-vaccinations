# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 21:13:09 2018

@author: markus
"""
"""TODO auf die Welt bringen"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import vacc
import game_theory_tools as tool
import datetime
import random
import pathlib #to create folder

# parameters for the disease
population = 400 #number of people in our simulation
population_alive = 400 #number of people alive at the start of the simulation
    
#random numbers: this people are initialized infected
r0 = random.randint(0,population-1)
r1 = random.randint(0,population-1)
r2 = random.randint(0,population-1)

#create folder
now = datetime.datetime.now()
date = str(int(now.year/10)) + str(now.year % 10) + '-' + \
           str(int(now.month/10)) + str(now.month % 10) + '-' + \
           str(int(now.day/10)) + str(now.day % 10)
           
time = str(int(now.hour/10)) + str(now.hour % 10) + '-' + \
           str(int(now.minute/10)) + str(now.minute % 10) + '-' + \
           str(int(now.second/10)) + str(now.second % 10)
   
folder_name = 'vaccinations_graphics/datas_' + date + '_' + time
pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)

datas = open(folder_name + '/datas.txt',"w+")
datas.write("vacc_prob_init,vaccinated_people,immune_and_sick_people\n\n")

vacc_prob_init = 0 #probability of beeing infected at beginning of simulation (Percentage!)
    
for vacc_prob_init in range(0,100): 
    immune_and_sick_people = 0
    vaccinated_people2 = 0
        
    #for nn in range(0,20):        
    #Population parameters
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
    prob_for_diseases = 0 #0.000001 #Random probability (per day and person) to become
                                #sick without beeing infected by someone else
    prob_for_contact_infection = 0.07 #probability to infect an other person, when
                                     #there is a contact
    incubation_time = 2 #days until person realizes that it is sick (needed for daily contacts)
    time_to_get_healthy = 10 #counts days from infection. After this time, a person
                             #becomes healty
                             
    vacc.init_parameters(population, vaccinated_people, infected_people,\
            daily_contacts_when_healthy, daily_contacts_when_sick,\
            prob_for_diseases, prob_for_contact_infection,\
            incubation_time, time_to_get_healthy, population_alive)
                             
    #create population in people_list
    for x in range(0,population): #infected init
        if x == r0 or  x == r1 or  x == r2:
            people_list[x] = vacc.Grid_Person(False, 1, x)
            infected_people += 1
        elif random.random() < vacc_prob_init/100: #vaccinated init
            people_list[x] = vacc.Grid_Person(True, -1, x)
            vaccinated_people += 1
        else: #normal init
            people_list[x] = vacc.Grid_Person(False, -1, x)
    
    
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
    f = open(folder_name + '/' + str(vacc_prob_init) + '_' + date + '_' + time + '.txt',"w+")
    
    f.write("Population: %d\n" % population)
    f.write("Prob_for_contact_infection: %d Prozent \n" % (prob_for_contact_infection*100))
    f.write("***\n")
    
    #simulate spread of infection
    for days in range(0,simulation_time):
        
        daily_file_input = ""
        
        #one day is over
        for x in range(0,population): 
            people_list[x].next_day()
            
        '''
        # TODO
        for x in range(0,population): 
            people_list[x].get_vaccinated()
        '''
            
        #looks, which people are infected during this day
        for x in range(0,population): 
            infections = people_list[x].start_infection()
            #print(infections)
            for i in infections:
                people_list[i].get_infected()
        
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
    
    for x in range(0,population): 
        status = people_list[x].get_status()
        if(status != -1 and status != -2): #noch nie krank
            immune_and_sick_people += 1
        if(status == -2): #vaccinated
            vaccinated_people2 += 1
            
    print(str(vacc_prob_init) + ' : ' + str(vaccinated_people2) + ' : ' + str(immune_and_sick_people))
    
    datas.write(str(vacc_prob_init) + ',' + str(vaccinated_people2) + ',' + str(immune_and_sick_people) + '\n')
    
datas.close()

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


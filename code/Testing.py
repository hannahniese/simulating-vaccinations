# -*- coding: utf-8 -*-
"""
Simulating vaccination
Created as part of the ETH course "Lecture with Computer Exercises: 
    Modelling and Simulating Social Systems in MATLAB (or Python)"

Find all information about the code in code/readme.txt

December 2018
@author: Hannah Niese, Markus Niese, Timo Schönegg
"""
"""
Tis file containes the similar content to main.py, but is made to run the
simulation multible times with the same parameters. There are no graphs
produced in this file, but some results are saved in a file for further
investigation.
"""

## import packages
import csv
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt
## import modules
import vacc
import simulation_vaccination_tools as tool
import network_generator



def run():
    ### parameters for the simulation
    
    ## Population parameters
    population = 5493 # number of people in the simulation
    population_alive = 0 #number of people alive at the start of the simulation
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
    prob_for_diseases = 0.000001 # Random probability (per day and person) to become
                                # sick by someone outside the network
    prob_for_contact_infection = 0.5 # probability to infect an other person, when
                                      # there is a contact
    incubation_time = 12 # Incubation Period of the disease
    time_to_get_healthy = 42 # after that time a person becomes healthy again
    start_being_infectious = 7 # number of days after which a infected person
                                # becomes infectious
    re_vaccination_time = 2920 # time after which immune people should vaccinate again
    
                             
    ## Initial values of the percieved cost of vaccination and infection
    ## for all people the same
    percieved_vacc_cost = 1
    percieved_infec_cost = 20000
    minimal_infec_level = 0.001 # Minimal level of infection in the
                                # population apparent to one individual
    
    # The probability for a person to meet a contact each day
    probability_to_meet = 1
     
                               
    ## Length of the Simulation
    simulation_length = 8000
    
    ## Initializes the global parameters for the Person Class
    ## !!!required!!!
    vacc.init_parameters(population, vaccinated_people, infected_people,\
            daily_contacts_when_healthy, daily_contacts_when_sick,\
            prob_for_diseases, prob_for_contact_infection,\
            incubation_time, time_to_get_healthy, population_alive,\
            start_being_infectious, re_vaccination_time, minimal_infec_level)
                             
    ## create population in people_list
    for x in range(0,population):
        age = random.randint(0, 365000)
        people_list[x] = vacc.Network_Person(False, -1, x, percieved_vacc_cost,\
                   percieved_infec_cost, age = age, length_immune_mean = 4380,\
                   length_immune_sigma = 712) 
    
    ## set initial conditions    
    tool.initial_infected(people_list, 0.00)
    tool.initial_vaccinated(people_list, 0.0)
    
    ## make initial counts
#    print("Initially vaccinated:", vacc.get_num_vaccinated_people())
#    print("Initially infected:", vacc.get_num_infected_people())
    
    
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
    #network_generator.import_barabasi_graph("Networks/test_20000.txt", people_list)
    network_generator.import_graph_from_tsv("Networks/project90.tsv", people_list)
        
    days_since_opinion_change = 0   # saves the amount of days since 
                                    # tool.change_vaccination_cost_population()
                                    # was called the last time
    
    ## simulation
    for days in range(0,simulation_length):
        
        # iterate over the people_list every time step
        for x in range(0,population):
            people_list[x].next_day()
            people_list[x].get_vaccinated()
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
        for x in range(population):
            if random.random() < 0.0000214: # probability to die at this day
                                            # deathrate 8/1000 per year
                people_list[x].kill()
                people_list[x].get_born(False, -1, percieved_vacc_cost,\
                           percieved_infec_cost)
            
        # Updates infected_people_list and vaccinated_people_list
        infected_people_list.append(vacc.get_num_infected_people())    
        vaccinated_people_list.append(vacc.get_num_vaccinated_people())
        
        # Calculate the average number of infected people for last 100 days
        days_since_opinion_change +=1
        if days > 500:
            average_500 = np.average(infected_people_list[days-500:days])
            if average_500 < 5 and days_since_opinion_change > 500:
                #print(days)
                tool.change_vaccination_cost_population(people_list, 1.5, 0.3)
                days_since_opinion_change = 0
        
    immune_at_the_end = 0
    for x in people_list:
        if x.days_since_immunization != 0:
            immune_at_the_end += 1
            
    return(vacc.get_num_vaccinated_people(), max(vaccinated_people_list),\
           np.max(infected_people_list), np.argmax(infected_people_list),\
           np.min(vaccinated_people_list),\
           np.argmin(vaccinated_people_list), immune_at_the_end)
    

    
###############################################################################
### Run the program and save the results ###
###############################################################################
## open csv file to store data
with open('network_data/project90_2000_8000days.csv', mode='w') as file:
    file_writer = csv.writer(file, delimiter=',', lineterminator = '\n')
    file_writer.writerow(['time', 'curr_vacc', 'max_vacc', 'max_infec',\
                          'day_max_infec', 'vacc_min', 'day_vacc_min', 'curr_immune'])
    
    for i in range(10):
        start = timeit.default_timer()
        curr_vacc, max_vacc, max_infec, day_max_infec, vacc_min, day_vacc_min, curr_immune = run()
        end = timeit.default_timer()
        time = end - start
        file_writer.writerow([round(time, 2), curr_vacc, max_vacc, max_infec, day_max_infec, vacc_min, day_vacc_min, curr_immune])
        i += 1
        print(i)
print("end")
file.close()

    
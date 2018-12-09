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
This is the light test. It will produce a graph showing the outbreak of the
disease dependent on the percentage of people that were initially vaccinated

Find the description in code/readme.txt
"""
## import packages
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import random
## import modules
import vacc
import simulation_vaccination_tools as tool


### Function to import the graph
def import_barabasi_graph(path, people_list):
    """
    !!!Important!!!
    
    The number of elements in the people_list (variable population
    in network.py) has to be the same as the number of nodes of the imported
    graph
    
    !!!Important!!!
    
    import network from a txt file
    It has to be organized as an adjacency list. First entry of every line 
    is connected to all the following. Every connection will be added
    for both nodes. So the result is a undirected graph.
    Primarily used to import networks created with 
        create_barabasi_in_file(n,m,filename)
    All lines will be read except lines beginning with a '#'
    
    Args:
        path (str): path of the file that should be imported
    """
    txtfile = open(path, "r")
    reader = csv.reader(txtfile, delimiter=' ')
    for row in reader:
        if row[0][:1] != "#":
            first = int(row[0])
            for i in range(1,len(row)):
                people_list[first].add_contact(int(row[i]))
                people_list[int(row[i])].add_contact(first)
                

infected_to_not_vaccinated_list = []
total_infected_people_list = []
percentage_list = []

for percent in range (0,100,3): #change initially vaccinated people
     
    ### parameters for the simulation
    
    ## Length of the Simulation
    simulation_length = 500
   
    ## Population parameters
    population = 5000 # number of people in the simulation
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
    prob_for_diseases = 0.00001 # Random probability (per day and person) to become
                                # sick by someone outside the network
    prob_for_contact_infection = 0.5 # probability to infect an other person, when
                                      # there is a contact
    incubation_time = 12 # Incubation Period of the diseasse
    time_to_get_healthy = 42 # after that time a person becomes healthy again
    start_being_infectious = 7 # number of days after which a infected person
                                # becomes infectious
    re_vaccination_time = 2920 # time after which immune people should vaccinate again
    
                             
    ## Initial values of the percieved cost of vaccination and infection
    ## for all people the same
    percieved_vacc_cost = 1
    percieved_infec_cost = 1500
    
    # The probability for a person to meet a contact each day
    probability_to_meet = 0.5
    
    ## Initializes the global parameters for the Person Class
    ## !!!required!!!
    vacc.init_parameters(population, vaccinated_people, infected_people,\
            daily_contacts_when_healthy, daily_contacts_when_sick,\
            prob_for_diseases, prob_for_contact_infection,\
            incubation_time, time_to_get_healthy, population_alive,\
            start_being_infectious, re_vaccination_time)
                             
    ## create population in people_list
    for x in range(0,population):
        age = random.randint(0, 365000)
        people_list[x] = vacc.Network_Person(False, -1, x, percieved_vacc_cost,\
                   percieved_infec_cost, age = age, length_immune_mean = 4380,\
                   length_immune_sigma = 712) 
    
    ## set initial conditions    
    tool.initial_infected(people_list, 0.001)
    tool.initial_vaccinated(people_list, percent/100)
    
    ## make initial counts
    #211print("Initially vaccinated:", vacc.get_num_vaccinated_people())
    #211print("Initially infected:", vacc.get_num_infected_people())
    initially_vaccinated_out = vacc.get_num_vaccinated_people()
    initially_infected_out = vacc.get_num_infected_people()
    
    ### generate the network
    # 1. Op: Directly using network_generator.generate_Albert_Barabasi()
    # random network. Very slow. !!!Only use for population up to 1000!!!
    # 2. Op: Import random Albert-Barabasi_Graph generated with 
    # network_generator.create_barabasi_in_file() and import using
    # import_barabasi_graph()
    # 3. Op: Import from a TSV file using network_generator.import_graph_from_tsv()
    # !!! Important !!! For options 2 and 3 population (len(people_list)) HAS to be
    # equal to the number of nodes in the imported graph
    
    #network_generator.generate_Albert_Barbasi(people_list, 2, 3)
    import_barabasi_graph('Networks/barabasi_' + str(population) + '_2.txt', people_list)
    #network_generator.import_graph_from_tsv("Networks/edges.tsv", people_list)
        
    new_infected_people = vacc.get_num_infected_people() #after simulation: total amount of people, who were infected once
    
    ## simulation
    for days in range(0,simulation_length):
        
        # iterate over the people_list every time step
        for x in range(0,population):
            people_list[x].next_day()
            #people_list[x].get_vaccinated()
            # sick people infect randomly their contacts
            infections = people_list[x].start_infection(probability_to_meet)
            for i in infections:
                new_infected_people += people_list[i].get_infected()
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
        if days > 500:
            average_100 = np.average(infected_people_list[days-500:days])
            if average_100 < 5 and random.random() < 0.001:
                print(days)
                tool.change_vaccination_cost_population(people_list, 2, 0.3)
        
    ## Count the vaccinations at the end
    #211print("Vaccinated at the end:", vacc.get_num_vaccinated_people())
    #211print("Maximal number of vaccinated people:", max(vaccinated_people_list))
    #211print("Maximal number of infected people:", max(infected_people_list))
    vaccinated_people_after_500days_out = vacc.get_num_vaccinated_people()
    max_vaccinated_people_out = max(vaccinated_people_list)
    infected_people_after_500days_out = new_infected_people
    max_infected_people_out = max(infected_people_list)
    
    gradient_vaccinations = tool.discrete_gradient(vaccinated_people_list)
    gradient_infections = tool.discrete_gradient(infected_people_list)
    
    
    immune_people = 0
    for x in people_list:
        if x.days_since_immunization != 0:
            immune_people += 1
    #211print("Immune at the end:", test)
    immune_people_out = immune_people
    
     
    infected_to_not_vaccinated = (infected_people_after_500days_out-initially_infected_out) / (population - initially_vaccinated_out)
    
    infected_to_not_vaccinated_list.append(infected_to_not_vaccinated)
    total_infected_people_list.append(infected_people_after_500days_out)
    percentage_list.append(percent)
    
    
#fig, plt1 = plt.subplots()
#
##Plot: Probability to get infected if not vaccinated
#plt1.set_xlabel('Initially vaccinated people (%)')
#plt1.set_ylabel('Infected / not vaccinated people')
#plt1.set_title('Probability to get infected if not vaccinated')
#
#x_list = percentage_list
#y_list = infected_to_not_vaccinated_list
#
#plt1.plot(x_list, y_list, color = 'navy')
#
#plt.show()

fig, ax = plt.subplots()
ax.get_yaxis().set_major_formatter(
     ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
ax.xaxis.set_major_formatter(ticker.PercentFormatter(xmax = 1))

ax.set_ylim([0,5000])
ax.set_xlim([0,1])

#Plot: Total infected people without initially infected
ax.set_xlabel('Initially vaccinated people')
ax.set_ylabel('Infected people')
ax.set_title('People who got infected')

x_list = np.divide(percentage_list, 100)
y_list = total_infected_people_list

ax.plot(x_list, y_list, color = 'darkred')

plt.show()


# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:57:41 2018

@author: markus
"""

import random
import game_theory_tools as tool
import numpy as np


# function that initializes the global parameters
def init_parameters(p_population, p_vaccinated_people, p_infected_people,\
        p_daily_contacts_when_healthy, p_daily_contacts_when_sick,\
        p_prob_for_diseases, p_prob_for_contact_infection,\
        p_incubation_time, p_time_to_get_healthy, p_population_alive,\
        p_length_immunization):
    """
    initialize the global paramters needed by the class
    Args:
        p_population(int): the total population
        p_vaccinated_people(int): vaccinated people at the beginning
        p_infected_people(int): infected people at the beginning
        p_daily_contacts_when_healthy(int): number of contacts per day when the person is healthy
        p_prob_for_diseases(float): random probability to get infected by non-human sources
        p_prob_for_contact_infection(float): probability the infect another person when there is contact
        p_incubation_time(int): incubation time in days
        p_time_to_get_healthy(int): length of the disease in days
        p_population_alive(int): number of people alive at the beginning
        p_length_immunization(int): the number of days a person stays immune after
            vaccination or recovering from infection
    """
    global population
    population = p_population
    global vaccinated_people
    vaccinated_people = p_vaccinated_people
    global infected_people
    infected_people = p_infected_people
    global daily_contacts_when_healthy
    daily_contacts_when_healthy = p_daily_contacts_when_healthy
    global daily_contacts_when_sick
    daily_contacts_when_sick = p_daily_contacts_when_sick
    global prob_for_diseases
    prob_for_diseases = p_prob_for_diseases
    global prob_for_contact_infection
    prob_for_contact_infection = p_prob_for_contact_infection
    global incubation_time
    incubation_time = p_incubation_time
    global time_to_get_healthy
    time_to_get_healthy = p_time_to_get_healthy
    global population_alive
    population_alive = p_population_alive
    global length_immunization
    length_immunization = p_length_immunization

    
## getter-functions for global parameters
def get_num_infected_people():
    """
    returns the current number of infected people
    """
    return infected_people

def get_num_vaccinated_people():
    """
    returns the current number of vaccinated people
    """
    return vaccinated_people

def change_population_alive(change):
    """
        changes the value of population_alive by change
        
        raises error if the population alive would be bigger than population
    """
    if population_alive + change > population or population_alive + change < 0:
        raise Exception("Invalid amount of population_alive")
    #population_alive += change


# base class Person
class Person:
    """
    class Person
    
    Args: 
        vaccinated (boolean): true, if person is vaccinated
        infected_days (int): counts days since person is infected, -1 if person is healthy
        index (int): between 0 and population size, "Name" of a person (for identification)
        percieved_vacc_cost (float): percieved cost when vaccinating (side effects)
		percieved_infec_cost (float): the percieved cost when the person gets infected
        alive (bool): only alive people are counted in the simulation
        recoverd (bool): true, if the person has recoverd from the disease
        age (int): age in days
        days_since_immunization (int): days since either the last vaccination or the last infection
        
    Functions:
        get_vaccinated(self):
            sets vaccinated to true if tool.expected_gain() is positive
            
        get_infected(self):
            changes 'infected_days'-parameter to 0 and increases the number of
            currently infected people
            
        infect_other_people(self):
            Looking for random contacts in neighbourhood until 'daily_contacts'
            is reached. Infects randomly the person, to which it has a contact.
            
        next_day(self):
            Makes some people randomly sick (prob_for_diseases)
            Increases time_to_get_healthy of sick people
            If time_to_get_healthy is big enought peson becomes healthy (infected_days = -1)
        
        start_infection(self):
            Calls the infect_other_people() function, if person is sick
            
        kill(self):
            Kills a person by changing the alive variable to false
            
        get_born(self, vaccinated, infected_days, \
                 percieved_vacc_cost = 10e-4,\
				 percieved_infec_cost = 0.5):
            A dead person becomes alive initialized with the same attributes
            
        change_vacc_cost_relative(self, factor):
            Changes the percieved vaccination cost relativ

        change_infec_cost_relative(self, factor):
            Changes the percieved infection cost relativ
        
        get_status(self):
            returns the status (helthy, vacc, et.al.) as a int
        
        
    """
    
    def __init__(self, vaccinated, infected_days, index, \
                 percieved_vacc_cost, percieved_infec_cost,\
                 alive = True, recovered = False, age = 0,\
                 days_since_immunization = 0):
        self.vaccinated = vaccinated
        self.infected_days = infected_days
        self.index = index
        self.percieved_vacc_cost = percieved_vacc_cost
        self.percieved_infec_cost = percieved_infec_cost
        self.alive = alive
        self.recovered = recovered
        self.age = age
        self.days_since_immunization = days_since_immunization
        
        global population_alive
        population_alive += 1
        
        if self.vaccinated == True:
            global vaccinated_people
            vaccinated_people += 1
        
        
    def get_infected(self):
        """
           changes 'infected_days'-parameter to 0 and increases the number of
           currently infected people
    	"""
        if (not self.vaccinated) and (not self.recovered) and self.infected_days == -1: #person is healthy and not vaccinated
            self.infected_days = 0 #infection starts
            global infected_people
            infected_people += 1
    
    
    def next_day(self):
        """
            Makes some people randomly sick (prob_for_diseases)
            Increases time_to_get_healthy of sick people
            If time_to_get_healthy is big enought peson becomes healthy (infected_days = -1)
            increases the age by one day
            increases the days_since_immunization by one if the person was sick or vaccinated
            sets the days since immunization to 1 if person becomes healthy
        """
        global length_immunization
        self.age += 1
        #
        if self.days_since_immunization != 0:
            self.days_since_immunization += 1
            
        # reset recoverd and vaccinated of the immunization is no longer active
        if self.days_since_immunization == length_immunization:
            self.recoverd = False
            self.vaccinated = False
            
        # random infection without a contact to someone else
        if self.infected_days == -1: #person is healthy
            if random.random() <= prob_for_diseases: 
                self.get_infected() 
        else: #person is sick
            self.infected_days += 1 #increase days person is infected
            if self.infected_days > time_to_get_healthy: #person becomes healthy
                self.infected_days = -1
                self.days_since_immunization = 1
                self.recovered = True #person cannot become infected any more
                global infected_people
                infected_people -= 1
        
    def start_infection(self):    
        """
            Calls the infect_other_people() function, if person is sick
        """
        infections = []
        if self.infected_days >= 0 and self.infected_days <= incubation_time: #person is sick
            return self.infect_other_people()
        return infections
    
    
    def kill(self):
        """
            Kills a person by changing the alive-variable
        """
        global population_alive
        global vaccinated_people
        global infected_people
        
        self.days_since_immunization = 0
        self.age = 0
        if self.alive == True:
            self.alive = False
            
            population_alive -= 1
            self.recovered = False
            
            if self.vaccinated == True:
                self.vaccinated = False
                vaccinated_people -= 1
                
            
            if self.infected_days >= 0:
                infected_people -= 1
                self.infected_days = -1
            
#        else:
#            print("Person is still dead!")
            
    
    def get_born(self, vaccinated, infected_days, \
                 percieved_vacc_cost = 10e-4,\
				 percieved_infec_cost = 0.5):   #index stays the same
        """
            A dead person becomes alive
        """
        if self.alive == False:
            self.vaccinated = vaccinated
            self.infected_days = infected_days
            self.percieved_vacc_cost = percieved_vacc_cost
            self.percieved_infec_cost = percieved_infec_cost
            
            global population_alive
            population_alive += 1
            
            self.recovered = False
            
            if self.vaccinated == True:
                global vaccinated_people
                vaccinated_people += 1
        
        elif self.alive == True:
            print("Person is not dead!")
 
    
    def change_vacc_cost_relative(self, factor):
        """
            Changes the percieved vaccination cost relativ
        """
        self.percieved_vacc_cost *= factor
    
    
    def change_infec_cost_relative(self, factor):
        """
            Changes the percieved infection cost relativ
        """
        self.percieved_infec_cost *= factor
        
    def get_status(self):
        """
            returns
            -1 if the person is healthy
            -2 if the person is vaccinated
            -3 if the person is recovered
            -4 if the person is dead
            the number of sick days
        """
        if not self.alive:
            return -4
        if self.recovered:
            return -3
        elif self.vaccinated:
            return -2
        else:
            return self.infected_days
		
        
    
    
class List_Person(Person):
    
    def get_vaccinated(self):
        """
            sets vaccinated to true if tool.grid_expected_gain() is positive
    	"""
        global vaccinated_people
        if self.infected_days < 0 and not self.vaccinated and tool.expected_gain(vaccinated_people / \
          population_alive, infected_people / population_alive, self.percieved_vacc_cost,\
          self.percieved_infec_cost) > 0:
            self.vaccinated = True
            vaccinated_people += 1
    
    def infect_other_people(self):
        """
            Looking for random contacts in neighbourhood until 'daily_contacts'
            is reached. Infects randomly the person, to which it has a contact.
            Assumption: Person (self) is sick
        """
        infections = []
            
        # contacts: the number of contacts with other people, depending on incubation time
        contacts = daily_contacts_when_healthy
        if self.infected_days > incubation_time:
            contacts = daily_contacts_when_sick
        
        # index distance of possible contact person to person self
        contact_delta_index = 6
        # looks for possible contact persons by increasing contact_delta_index
        while contacts > 0:
            if random.random() <= 1: #we have a contact with a person "on the right"
                contacts -= 1
                #possible infection of contact person
                if random.random() <= prob_for_contact_infection: 
                    contact_index = (self.index + contact_delta_index)%population
                    infections.append(contact_index)
             
            if contacts > 0 and random.random() <= 1: #we have a contact with a person "on the left"
                contacts -= 1
                #possible infection of contact person
                if random.random() <= prob_for_contact_infection:
                    contact_index = (self.index - contact_delta_index)%population
                    infections.append(contact_index)
            
            contact_delta_index += 1
        return infections
    
    
    
    
class Grid_Person(Person):
    """
    Args:
        neighborhood (int): number of persons in the neighborhood (one can only make contact with the neighbors)
        infected_neighbors (int): number of people in proximity that are infected
    
    Functions:
        get_vaccinated(self):
            sets vaccinated to true if tool.grid_expected_gain() is positive
        
        get_neighborhood(self):
            returns a list of people with whom the person can have contact
            
        infect_other_people(self):
            Looks at all people in the neighborhood and infectes them with
            the probability prob_for_contact_infection
            Assumption: Person (self) is sick
            returns: array of the indices of the people that get infected
            
    """
    def __init__(self, vaccinated, infected_days, index, \
                 percieved_vacc_cost, percieved_infec_cost,\
                 alive = True, recovered = False, neighborhood = 9,\
                 age = 0, days_since_immunization = 0):
        super().__init__(vaccinated, infected_days, index, \
                 percieved_vacc_cost,\
				 percieved_infec_cost, alive, recovered, age,\
                 days_since_immunization)
        self.neighborhood = neighborhood
        self.infected_neighbors = 0
        
    def get_vaccinated(self):
        """
            sets vaccinated to true if tool.grid_expected_gain() is positive
            sets the days since immunization to 1
    	"""
        self.days_since_immunization = 1
        global vaccinated_people
        if self.infected_days < 0 and not self.vaccinated and tool.grid_expected_gain(vaccinated_people / \
          population_alive, infected_people / population_alive, self.percieved_vacc_cost,\
          self.percieved_infec_cost, self.infected_neighbors/self.neighborhood) > 0:
            self.vaccinated = True
            vaccinated_people += 1
        
    def get_neighborhood(self):
        """
        returns a list of people with whom the person can have contact
        
        returns: array of neighbors
        """
        sqrtnum = int(np.sqrt(population))
        neighbors = []
        for i in range(-1,2): # column
            for j in range(-1,2): # line
                if (i != 0 or j != 0) and \
                    ((self.index % sqrtnum) + i >= 0 and (self.index % sqrtnum) + i < sqrtnum) and \
                    (int(self.index/sqrtnum) + j >= 0 and int(self.index/sqrtnum) + j < sqrtnum):
                        contact_index = self.index + i + sqrtnum*j
                        neighbors.append(contact_index)
        return neighbors
    
    def infect_other_people(self):
        """
            Looks at all people in the neighborhood and infectes them with
            the probability prob_for_contact_infection
            Assumption: Person (self) is sick
            
            returns: array of the indices of the people that get infected
        """
        infections = []
        
        sqrtnum = int(np.sqrt(population))
        
        if sqrtnum * sqrtnum != population:
            raise Exception("Population has to be a quadratic number!")
    
        
        for i in range(-1,2): # column
            for j in range(-1,2): # line
                if (i != 0 or j != 0) and \
                    ((self.index % sqrtnum) + i >= 0 and (self.index % sqrtnum) + i < sqrtnum) and \
                    (int(self.index/sqrtnum) + j >= 0 and int(self.index/sqrtnum) + j < sqrtnum):
                    # possible infection of contact person
                    if random.random() <= prob_for_contact_infection: 
                        contact_index = self.index + i + sqrtnum*j
                        infections.append(contact_index)
                 
         
        return infections
    
    
    
class Network_Person(Person):
    
    def __init__(self, vaccinated, infected_days, index, \
                 percieved_vacc_cost, percieved_infec_cost,\
                 alive = True, recovered = False,\
                 age = 0, days_since_immunization = 0):
        super().__init__(vaccinated, infected_days, index, \
                 percieved_vacc_cost,\
				 percieved_infec_cost, alive, recovered, age,\
                 days_since_immunization)
        self.contacts = []
        self.infected_contacts = 0

    def add_contact(self, index):
        """
            Adds the index to the persons adjeciency list
            
            Args:
                index (int): index of the person to be added as contact
        """
        self.contacts.append(index)
        
    def infect_other_people(self):
        """
            goes through all contacts of an infected person and infects
            randomly some of the contacts
            
            Returns:
                List of indexes of people that get infected
        """
        infections = []
        for c in self.contacts:
            if random.random() < 0.2 and random.random() <= prob_for_contact_infection:
                infections.append(c)
        return infections
    
    def get_vaccinated(self):
        """
            sets vaccinated to true if the person is not infected,
            not vaccinated and tool.grid_expected_gain() is positive
            increases the global varible infected_people 
            sets the days_since_immizations to 1
    	"""
        self.days_since_immunization = 1
        global vaccinated_people
        if len(self.contacts) == 0:
            return
        if self.infected_days < 0 and not self.vaccinated and tool.expected_gain(vaccinated_people / \
          population_alive, infected_people / population_alive, self.percieved_vacc_cost,\
          self.percieved_infec_cost) > 0:
            self.vaccinated = True
            vaccinated_people += 1
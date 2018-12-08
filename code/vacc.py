# -*- coding: utf-8 -*-
"""
Simulating vaccination
Created as part of the ETH course "Lecture with Computer Exercises: 
    Modelling and Simulating Social Systems in MATLAB (or Python)"

Find all information about the code in code/readme.md

December 2018
@author: Hannah Niese, Markus Niese, Timo Schönegg
"""

## Import packages
import random
import simulation_vaccination_tools as tool
import numpy as np



## Function that initializes the global parameters
def init_parameters(p_population, p_vaccinated_people, p_infected_people,\
        p_daily_contacts_when_healthy, p_daily_contacts_when_sick,\
        p_prob_for_diseases, p_prob_for_contact_infection,\
        p_incubation_time, p_time_to_get_healthy, p_population_alive,\
        p_start_being_infectious = 0, p_re_vaccination_time = 100000,\
        p_minimal_infec_level = 0):
    """ Initialize the global paramters needed by the class
    
    !!! Needed if program uses class Person or a derived class !!!
    
    Args:
        p_population (int): The total population
        p_vaccinated_people (int): Vaccinated people at the beginning
        p_infected_people (int): Infected people at the beginning
        p_daily_contacts_when_healthy (int): Number of contacts per day when
            the person is healthy
        p_prob_for_diseases (float): Random probability to get infected by
            people outside of the system
        p_prob_for_contact_infection (float): Probability the infect another
            person when there is contact
        p_incubation_time (int): Incubation time in days
        p_time_to_get_healthy (int): Length of the disease in days
        p_population_alive (int): Number of people alive at the beginning
        p_start_being_infectious (int): Number of days after which a infected
            person can infect other people
        p_re_vaccination_time (int): Time after wich a person should vaccinate
            again
        p_minimal_infec_level (double): Minimal level of infection in the
            population apparent to one individual
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
    global start_being_infectious
    start_being_infectious = p_start_being_infectious
    global re_vaccination_time
    re_vaccination_time = p_re_vaccination_time
    global minimal_infec_level
    minimal_infec_level = p_minimal_infec_level


    
## getter-functions for global parameters
def get_num_infected_people():
    """ Returns the current number of infected people """
    return infected_people



def get_num_vaccinated_people():
    """ Returns the current number of vaccinated people """
    return vaccinated_people



def change_population_alive(change):
    """ Changes the value of population_alive by change
        
    Raises:
        error if the population alive would be bigger than population
    """
    global population_alive
    if population_alive + change > population or population_alive + change < 0:
        raise Exception("Invalid amount of population_alive")
    population_alive += change
    
    
    
def change_num_vaccinated_people(num):
    """ Changes the number of vaccinated people by num """
    global vaccinated_people
    vaccinated_people += num



def change_num_infected_people(num):
    """ Changes the number of infected people by num """
    global infected_people
    infected_people += num



## Base class Person
class Person:
    """
    class Person
    
    Args: 
        vaccinated (boolean): true, if person is vaccinated
        infected_days (int): counts days since person is infected,
            -1 if person is healthy
        index (int): between 0 and population size
        percieved_vacc_cost (float): percieved cost when vaccinating
            (side effects)
		percieved_infec_cost (float): the percieved cost when the person
            gets infected
        alive (bool): only alive people are counted in the simulation
        recovered (bool): true, if the person has recovered from the disease
        age (int): age in days
        days_since_immunization (int): days since either the last vaccination
            or the last infection
        length_immune_mean (int): the average of the length of the immunization
        length_immune_sigma (int): the standard deviation of the length of the
            immunization
        
    Functions:
        get_infected(self):
            changes 'infected_days'-parameter to 0 and increases the number of
            currently infected people
            return 1 if person becomes infected, otherwise returns 0

            
        next_day(self):
            Makes some people randomly sick (prob_for_diseases)
            Increases time_to_get_healthy of sick people
            If time_to_get_healthy is big enought peson becomes healthy
                (infected_days = -1)
        
        start_infection(self):
            Calls the infect_other_people() function, if person is sick
            
        kill(self):
            Kills a person by changing the alive variable to false
            
        get_born(self, vaccinated, infected_days, \
                 percieved_vacc_cost = 10e-4,\
				 percieved_infec_cost = 0.5):
            A dead person becomes alive initialized with the same attributes
            
        set_immunization(self, days_since_immunization, vaccinated = False,\
                         recovered = False):
            Sets either vaccinated of recovered to true and sets the
            days_since_immunization to the given value 
            
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
                 days_since_immunization = 0, length_immune_mean = 4380,\
                 length_immune_sigma = 300):
        self.vaccinated = vaccinated
        self.infected_days = infected_days
        self.index = index
        self.percieved_vacc_cost = percieved_vacc_cost
        self.percieved_infec_cost = percieved_infec_cost
        self.alive = alive
        self.recovered = recovered
        self.age = age
        self.days_since_immunization = days_since_immunization
        self.length_immunization = int(np.random.normal(length_immune_mean,\
                                                        length_immune_sigma))
        
        global population_alive
        population_alive += 1
        
        if self.vaccinated == True:
            change_num_vaccinated_people(1)
        
        
        
    def get_infected(self):
        """ Changes 'infected_days'-parameter to 0 and increases the number of
               currently infected people
            return 1 if person becomes infected, otherwise returns 0
    	"""
        if (not self.vaccinated) and (not self.recovered) and\
          self.infected_days == -1: #person is healthy and not vaccinated
            self.infected_days = 0 #infection starts
            change_num_infected_people(1)
            return 1
        
        return 0
    
    
    def next_day(self):
        """ Makes some people randomly sick (prob_for_diseases)
            Increases time_to_get_healthy of sick people
            If time_to_get_healthy is big enought peson becomes healthy
                (infected_days = -1)
            Increases the age by one day
            Increases the days_since_immunization by one if the person was 
                sick or vaccinated
            Sets the days since immunization to 1 if person becomes healthy
        """
        self.age += 1
        # increases the days_since_immunization if the person is immune
        if self.days_since_immunization > 0:
            self.days_since_immunization += 1
            
        # reset recovered and vaccinated if the immunization is not active
        if self.days_since_immunization == self.length_immunization:
            if self.vaccinated == True:
                change_num_vaccinated_people(-1)
                self.vaccinated = False
            self.recovered = False
            
        # random infection without a contact to someone else
        if self.infected_days == -1: #person is healthy
            if random.random() <= prob_for_diseases: 
                self.get_infected() 
        else: #person is sick
            self.infected_days += 1 #increase days person is infected
            if self.infected_days > time_to_get_healthy:
                self.infected_days = -1
                self.days_since_immunization = 1
                self.recovered = True #person cannot become infected any more
                change_num_infected_people(-1)
        
        
        
    def start_infection(self):    
        """ Calls the infect_other_people() function, if person is sick
        
        Returns:
            infections (list[int]): List of indeces, that have been infected
        """
        infections = []
        if self.infected_days >= 0 and self.infected_days >=\
          start_being_infectious and self.infected_days < incubation_time:
            return self.infect_other_people()
        return infections
    
    
    
    def kill(self):
        """ Kills a person by changing the alive-variable """
        global population_alive
        
        self.days_since_immunization = 0
        self.age = 0
        if self.alive == False:
            print("Person is still dead!")
        elif self.alive == True:
            self.alive = False
            
            population_alive -= 1
            self.recovered = False
            
            if self.vaccinated == True:
                self.vaccinated = False
                change_num_vaccinated_people(-1)
                
            if self.infected_days >= 0:
                change_num_infected_people(-1)
                self.infected_days = -1 
        
        
        
    def get_born(self, vaccinated, infected_days, \
                 percieved_vacc_cost = 1,\
				 percieved_infec_cost = 2000):   #index stays the same
        """ A dead person becomes reactivated """
        if self.alive == False:
            self.vaccinated = vaccinated
            self.infected_days = infected_days
            self.percieved_vacc_cost = percieved_vacc_cost
            self.percieved_infec_cost = percieved_infec_cost
            self.alive = True
            
            global population_alive
            population_alive += 1
            
            self.recovered = False
            
            if self.vaccinated == True:
                change_num_vaccinated_people(1)
        
        elif self.alive == True:
            print("Person is not dead!")
 
    
    
    def set_immunization(self, days_since_immunization, vaccinated = False,\
                         recovered = False):
        """Sets either vaccinated of recovered to true and sets the
            days_since_immunization to the given value
            
        Args:
            days_since_immunization (int): Sets the parameter to the given
                value
            vaccinated (bool): Sets vaccinated to given value
            recovered (bool): Sets recovered to the given value
            
        Raises:
            Exception, if both vaccinated and recovered are true or false
        """
        if vaccinated == recovered:
            raise Exception("vaccinated and recovered cannot be both true\
                            or false")
        if vaccinated:
            self.vaccinated = True
            self.recovered = False
            change_num_vaccinated_people(1)
        elif recovered:
            self.recovered = True
            self.vaccinated = False
        self.days_since_immunization = days_since_immunization
    
    
    
    def change_vacc_cost_relative(self, factor):
        """ Changes the percieved vaccination cost relativ """
        self.percieved_vacc_cost *= factor
    
    
    
    def change_infec_cost_relative(self, factor):
        """ Changes the percieved infection cost relativ """
        self.percieved_infec_cost *= factor
        
      
        
    def get_status(self):
        """
        Returns:
            -1 if the person is healthy
            -2 if the person is vaccinated
            -3 if the person is recovered
            -4 if the person is dead
            or the number of infected days days
        """
        if not self.alive:
            return -4
        if self.recovered:
            return -3
        elif self.vaccinated:
            return -2
        else:
            return self.infected_days
		
    
    
    
    
class Grid_Person(Person):
    """
    Args:
        neighborhood (int): Number of persons in the neighborhood
            (one can only make contact with the neighbors)
        infected_neighbors (int): Number of people in proximity that are
            infected
    
    Functions:
        get_vaccinated(self):
            Sets vaccinated to true if tool.grid_expected_gain() is positive
        
        get_neighborhood(self):
            Returns a list of people with whom the person can have contact
            
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
        """ Sets vaccinated to true if tool.grid_expected_gain() is positive.
            Sets the days since immunization to 1.
    	"""
        if self.infected_days < 0 and not self.vaccinated and\
              tool.grid_expected_gain(vaccinated_people / population_alive,\
              infected_people / population_alive, self.percieved_vacc_cost,\
              self.percieved_infec_cost,\
              self.infected_neighbors/self.neighborhood) > 0:
            self.vaccinated = True
            self.days_since_immunization = 1
            change_num_vaccinated_people(1)
        
        
        
    def get_neighborhood(self):
        """ Returns a list of people with whom the person can have contact
        
        Returns:
            List of neighbors
        """
        sqrtnum = int(np.sqrt(population))
        neighbors = []
        for i in range(-1,2): # column
            for j in range(-1,2): # line
                if (i != 0 or j != 0) and \
                     ((self.index % sqrtnum) + i >= 0 and\
                     (self.index % sqrtnum) + i < sqrtnum) and \
                     (int(self.index/sqrtnum) + j >= 0 and\
                     int(self.index/sqrtnum) + j < sqrtnum):
                        contact_index = self.index + i + sqrtnum*j
                        neighbors.append(contact_index)
        return neighbors
    
    
    
    def infect_other_people(self):
        """
            Looks at all people in the neighborhood and infectes them with
            the probability prob_for_contact_infection
            Assumption: Person (self) is sick
            
            Returns:
                Array of the indices of the people that get infected
        """
        infections = []
        
        sqrtnum = int(np.sqrt(population))
        
        if sqrtnum * sqrtnum != population:
            raise Exception("Population has to be a quadratic number!")

        for i in range(-1,2): # column
            for j in range(-1,2): # line
                if (i != 0 or j != 0) and \
                     ((self.index % sqrtnum) + i >= 0 and\
                     (self.index % sqrtnum) + i < sqrtnum) and \
                     (int(self.index/sqrtnum) + j >= 0 and\
                     int(self.index/sqrtnum) + j < sqrtnum):
                    # possible infection of contact person
                    if random.random() <= prob_for_contact_infection: 
                        contact_index = self.index + i + sqrtnum*j
                        infections.append(contact_index)
        return infections
    
    
    
    
    
class Network_Person(Person):
    """
    Args:
        contacts (list[int]): adjacency list of all the connected vertices
        infected_contacts (int): number of contacts that are infected
    
    Functions:
        add_contact(self, index):
            Adds that contact to the adjacency list
            
        get_degree(self):
            Returns the number of contacts (len(contacts))
            
        start_infection(self, probability_to_meet):    
            Calls the infect_other_people() function if person is sick
            and hands over the probability_to_meet
            
        infect_other_people(self, probability_to_meet):
            Looks at all contacts, meets them with probability to meet
            and if they meet infectes them with the probability
            prob_for_contact_infection
            
        get_vaccinated(self):    
            Sets vaccinated to true if the person is not infected,
            not vaccinated and tool.grid_expected_gain() is positive
            increases the global varible infected_people 
            sets the days_since_immizations to 1
            
    """
    def __init__(self, vaccinated, infected_days, index, \
                 percieved_vacc_cost, percieved_infec_cost,\
                 alive = True, recovered = False,\
                 age = 0, days_since_immunization = 0,\
                 length_immune_mean = 4380, length_immune_sigma = 300):
        super().__init__(vaccinated, infected_days, index, \
                 percieved_vacc_cost,\
				 percieved_infec_cost, alive, recovered, age,\
                 days_since_immunization, length_immune_mean,\
                 length_immune_sigma)
        self.contacts = []
        self.infected_contacts = 0



    def add_contact(self, index):
        """ Adds the index to the persons adjeciency list
            
            Args:
                index (int): index of the person to be added as contact
        """
        self.contacts.append(index)
       
        
        
    def get_degree(self):
        """
        Returns:
            The degree of the node (number of contacts)
        """
        return len(self.contacts)
    
    
    
    def start_infection(self, probability_to_meet):    
        """Calls the infect_other_people() function if person is sick
                and hands over the probability_to_meet
            
        Args:
            probability_to_meet (int): The probability of a Person to meet
                and possibly infect each of its contacts
        """
        infections = []
        if self.infected_days >= 0 and self.infected_days >\
          start_being_infectious:
            return self.infect_other_people(probability_to_meet)
        return infections
    
        
    
    def infect_other_people(self, probability_to_meet):
        """ Goes through all contacts of an infected person and infects
                randomly some of the contacts
            
        Args:
            probability_to_meet (int): The probability of a Person to meet
            and possibly infect each of its contacts
                    
        Returns:
            List of indexes of people that get infected
        """
        infections = []
        for c in self.contacts:
            if random.random() < probability_to_meet\
            and random.random() <= prob_for_contact_infection:
                infections.append(c)
        return infections
    
    
    
    def get_vaccinated(self):
        """
            Sets vaccinated to true if the person is not infected,
            not vaccinated and tool.grid_expected_gain() is positive
            increases the global varible infected_people.
            Sets the days_since_immizations to 1.
    	"""
        if len(self.contacts) == 0:
            return
        if self.infected_days < 0 and (self.days_since_immunization == 0 or\
          self.days_since_immunization > re_vaccination_time)\
          and tool.expected_gain(vaccinated_people / \
          population_alive, infected_people / population_alive,\
          self.percieved_vacc_cost, self.percieved_infec_cost,\
          prob_for_contact_infection, minimal_infec_level) > 0:
            if self.vaccinated == False:
                change_num_vaccinated_people(1)
                self.vaccinated = True
            self.days_since_immunization = 1
            
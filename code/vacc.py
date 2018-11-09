# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:57:41 2018

@author: markus
"""

import matplotlib.pyplot as plt
import random
import game_theory_tools as tool


##Population parameters
#population = 0
#vaccinated_people = 0
#infected_people = 0
#daily_contacts_when_healthy = 0
#daily_contacts_when_sick = 0
##Diseases parameters
#prob_for_diseases = 0
#prob_for_contact_infection = 0
#incubation_time = 0
#time_to_get_healthy = 0



def init_parameters(p_population, p_vaccinated_people, p_infected_people,\
        p_daily_contacts_when_healthy, p_daily_contacts_when_sick,\
        p_prob_for_diseases, p_prob_for_contact_infection,\
        p_incubation_time, p_time_to_get_healthy):
    """
    TODO
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


class Person:
    """
    class Person
    
    Args: 
        vaccinated (boolean): true, if person is vaccinated
        infected_days (int): counts days since person is infected, -1 if person is healthy
        index (int): between 0 and population size, "Name" of a person (for identification)
        percieved_vacc_risk = 10e-4 TODO
		percieved_infec_risk = 0.5 TODO
        
    Functions:
        get_vaccinated(self):
            TODO
            
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
        
        
    """

    
    def __init__(self, vaccinated, infected_days, index, \
                 percieved_vacc_risk = 10e-4,\
				 percieved_infec_risk = 0.5):
        self.vaccinated = vaccinated
        self.infected_days = infected_days
        self.index = index
        self.percieved_vacc_risk = percieved_vacc_risk
        self.percieved_infec_risk = percieved_infec_risk
		
        
    def get_vaccinated(self):
        """
            TODO
    	"""
        global vaccinated_people
        if self.infected_days < 0 and not self.vaccinated and tool.expected_gain(vaccinated_people / \
          population, infected_people / population, self.percieved_vacc_risk,\
          self.percieved_infec_risk) > 0:
            self.vaccinated = True
            vaccinated_people += 1



    def get_infected(self):
        """
           changes 'infected_days'-parameter to 0 and increases the number of
           currently infected people
    	"""
        if (not self.vaccinated) and self.infected_days == -1: #person is healthy and not vaccinated
            self.infected_days = 0 #infection starts
            global infected_people
            infected_people += 1
      
    def infect_other_people(self):
        """
            Looking for random contacts in neighbourhood until 'daily_contacts'
            is reached. Infects randomly the person, to which it has a contact.
            Assumption: Person (self) is sick
        """
        infections = []
        #contacts: the number of contacts with other people, depending on incubation time
        contacts = daily_contacts_when_healthy
        if self.infected_days > incubation_time:
            contacts = daily_contacts_when_sick
        
        #index distance of possible contact person to person self
        contact_delta_index = 6
        #looks for possible contact persons by increasing contact_delta_index
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
    
    
    def next_day(self):
        """
            Makes some people randomly sick (prob_for_diseases)
            Increases time_to_get_healthy of sick people
            If time_to_get_healthy is big enought peson becomes healthy (infected_days = -1)
        """
        #random infection without a contact to someone else
        if self.infected_days == -1: #person is healthy
            if random.random() <= prob_for_diseases: 
                self.get_infected()
                
        else: #person is sick
            self.infected_days += 1 #increase days person is infected
            if self.infected_days > time_to_get_healthy: #person becomes healthy
                self.infected_days = -1
                
                global infected_people
                infected_people -= 1
        
    def start_infection(self):    
        """
            Calls the infect_other_people() function, if person is sick
        """
        #print("G")
        infections = []
        if self.infected_days > 0: #person is sick
            return self.infect_other_people()
        return infections
 
    
def Grid_Person(Person):
    """
    TODO:
        should raise an error if population is not a quadratic number
        should infect people in a directions
    """
    
def Network_Person(Person):
    """
    TODO:
        project for a later time
    """


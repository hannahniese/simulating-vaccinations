# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 14:57:41 2018

@author: markus
"""

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
        p_incubation_time, p_time_to_get_healthy, p_population_alive):
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


class Person:
    """TODO Timo
    dead person ✓
    recovered ✓
    change percieved risks member funktion relativ!! ✓
    kill ✓
    """
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
				 percieved_infec_risk = 0.5, alive = True, recovered = False):
        self.vaccinated = vaccinated
        self.infected_days = infected_days
        self.index = index
        self.percieved_vacc_risk = percieved_vacc_risk
        self.percieved_infec_risk = percieved_infec_risk
        self.alive = alive
        self.recovered = recovered
		
        global population_alive
        population_alive += 1
    
        if self.vaccinated == True:
            global vaccinated_people
            vaccinated_people += 1
        
        
    def get_vaccinated(self):
        """
            TODO
    	"""
        global vaccinated_people
        if self.infected_days < 0 and not self.vaccinated and tool.expected_gain(vaccinated_people / \
          population_alive, infected_people / population_alive, self.percieved_vacc_risk,\
          self.percieved_infec_risk) > 0:
            self.vaccinated = True
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
        """später TODO Timo rückgabe Person ist gestorben"""
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
                self.recovered = True #person cannot become infected any more
                
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
    
    
    def kill(self):
        """
            Kills a person by changing the alive-variable
        """
        global alive
        global population_alive
        global vaccinated_people
        global infected_people
        
        if alive == True:
            alive = False
            
            population_alive -= 1
            self.recovered = False
            
            if self.vaccinated == True:
                self.vaccinated = False
                vaccinated_people -= 1
            
            if self.infected_days >= 0:
                infected_people -= 1
                self.infected_days = -1
        
        elif alive == False:
            print("Person is still dead!")
            
    
    def get_born(self, vaccinated, infected_days, \
                 percieved_vacc_risk = 10e-4,\
				 percieved_infec_risk = 0.5):   #index stays the same
        """
            A dead person becomes alive
        """
        if self.dead_person == True:
            self.vaccinated = vaccinated
            self.infected_days = infected_days
            self.percieved_vacc_risk = percieved_vacc_risk
            self.percieved_infec_risk = percieved_infec_risk
            
            global population_alive
            population_alive += 1
            
            self.recovered = False
            
            if self.vaccinated == True:
                global vaccinated_people
                vaccinated_people += 1
        
        elif self.dead_person == False:
            print("Person is not dead!")
        
        
    def dead_person(self):
        """
            Retuns true, if person is dead
        """
        return (not alive)
 
    
    def change_vacc_risk_relative(self, factor):
        """
            Changes the percieved vaccination risk relativ
        """
        self.percieved_vacc_risk *= factor
    
    
    def change_infec_risk_relative(self, factor):
        """
            Changes the percieved infection risk relativ
        """
        self.percieved_infec_risk *= factor
        
    def get_status(self):
        """
            returns
            -1 if the person is healthy
            -2 if the person is vaccinated
            -3 if the person is dead
            the number of sick days
        """
        if not self.alive:
            return -3
        elif self.vaccinated:
            return -2;
        else:
            return self.infected_days
		
        
    
class List_Person(Person):
    """TODO: Timo
        Implement the Person class for a list
    """
    
    
class Grid_Person(Person):
    """
    TODO: Timo
        should raise an error if population is not a quadratic number
        should infect people in a directions
    """
    def infect_other_people(self):
        """
            Looking for random contacts in neighbourhood until 'daily_contacts'
            is reached. Infects randomly the person, to which it has a contact.
            Assumption: Person (self) is sick
        """
        infections = []
        
        for i in range(-1,1):
            for j in range(-1,1):
                if i != 0 or j != 0:
                    #possible infection of contact person
                    if random.random() <= prob_for_contact_infection: 
                        contact_index = self.index + i + np.sqrt(population)*j
                        infections.append(contact_index)
                 
         
        return infections
    
    
def Network_Person(Person):
    """
    TODO:
        project for a later time
    """


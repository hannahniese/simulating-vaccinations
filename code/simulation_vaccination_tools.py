# -*- coding: utf-8 -*-
"""
Simulating vaccination
Created as part of the ETH course "Lecture with Computer Exercises: 
    Modelling and Simulating Social Systems in MATLAB (or Python)"

Find all information about the code in code/readme.md

December 2018
@author: Hannah Niese, Markus Niese, Timo Schönegg
"""
"""
This file contains a number of basic functions needed in various other files.
"""


### Import packages
import random
import numpy as np



def expected_gain(coverage_level, infec_level, vacc_cost, infec_cost,\
                  risk = 0.5, minimal_infec_level = 0):
	"""calculates the expectation expected gain if one vaccinates

	Args:
		coverage_level (double) : Vaccinated probortion of the population
		infec_level (double): The amount of people that are currently infected
        vacc_cost (double): The percieved cost when vaccinating
        infec_cost (doulbe): The percieved cost due to infection
		risk (double): risk of getting infected
        minimal_infec_level (double): The minimal infec_level precieved by 
            a person
            
	Returns:
		Expected gain when vaccinating
	"""
	infection_level = np.maximum(infec_level, minimal_infec_level)
	expect = - vacc_cost + infec_cost * infection_level *\
        (1 - coverage_level) * risk
	return expect



def grid_expected_gain(coverage_level, infec_level, vacc_cost, infec_cost,\
                  rate_in_neighborhood):
	"""calculates the expectation expected gain if one vaccinates

	Args:
		coverage_level (double) : Vaccinated proportion of the population
		infec_level (double): The amount of people that are currently infected
		risk (double): risk of vacc / risk of infection
        rate_in_neighborhood (double): The porpotion of people infected in
            the neighborhood
	
	Returns:
		expectation value
	"""
	expect = - vacc_cost + infec_cost * rate_in_neighborhood
	return expect



def discrete_gradient(array):
    """ Calculates the difference between an element in an array and the
        element before
    
    Args:
        array (array[int]): The array for which the daily change
            should be calculated
        
    Returns:
        Array with the daily change
    """
    res = [0]
    for i in range(1,len(array)):
        res.append(array[i]-array[i-1])
    return res



def initial_infected(people_list, proportion_infected):
    """calls get_infected on random persons in people_list
    
    Args:
        people_list: list elements of class person
        propotion_infected: the proportion of the element in the list that
        should get infected
        
    Returns:
        people_list
    """
    inf = len(people_list) * proportion_infected
    while inf > 0:
        rand = random.randint(0, len(people_list)-1)
        if people_list[rand].infected_days == -1 and\
          people_list[rand].vaccinated == False:
            people_list[rand].get_infected()
            inf -= 1
    return people_list       
    


def initial_vaccinated(people_list, proportion_vaccinated):
    """calls get_infected on random persons in people_list
    
    Args:
        people_list: list elements of class person
        propotion_vaccinated: the proportion of the element in the list that
        should get vaccinated
        
    Returns:
        people_list
    """
    inf = len(people_list) * proportion_vaccinated
    while inf > 0:
        rand = random.randint(0, len(people_list)-1)
        if people_list[rand].vaccinated == False and\
          people_list[rand].infected_days == -1:
            # set a random value to days since immunization up to 12 years
            #days_since_immunization = random.randint(0,4380)
            days_since_immunization = 1
            people_list[rand].set_immunization(days_since_immunization, True,\
                       False)
            inf -= 1
    return people_list



def change_infection_cost_population(people_list, factor, probability):
    """ Change the percieved_infec_cost by a factor for every Person
    with some probability
    
    Args:
        people_list (list of Person): The list of people whose parameter
            should be changed
        factor (float): The factor by which the percieved_infec_cost
            should be changed
        probability (float, between 0 and 1): probability of each person to get
            the percieved_infec_cost changed
    
    Returns:
        people_list (list of Person): The list of people whose parameter
            have been changed
    """
    for p in people_list:
        if random.random() < probability:
            p.change_infec_cost_relative(factor)
    return people_list



def change_vaccination_cost_population(people_list, factor, probability):
    """ Change the percieved_vacc_cost by a factor for every Person
    with some probability
    
    Args:
        people_list (list of Person): The list of people whose parameter
            should be changed
        factor (float): The factor by which the percieved_vacc_cost
            should be changed
        probability (float, between 0 and 1): probability of each person to get
            the percieved_vacc_cost changed
    
    Returns:
        people_list (list of Person): The list of people whose parameter
            have been changed
    """
    for p in people_list:
        if random.random() < probability:
            p.change_vacc_cost_relative(factor)
    return people_list
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 22:01:11 2018

@author: markus
"""
import random


def prob_infec(infec_level, coverage_level, risk = 0.5):
	"""calculates the probability of getting infected

	Args:
		infec_level (double): the amount of people that are currently infected
		coverage_level (double): proportion of the population that is vaccinated
		risk (double): the risk of getting infected
	
	Returns:
		the probability of one person to get infected
	"""
	prob = infec_level * (1 - coverage_level) * risk
	#prob = (1-coverage_level)
	return prob

def grid_prob_infec(infec_level, coverage_level,\
                    rate_in_neighborhood, risk = 0.1):
	"""calculates the probability of getting infected

	Args:
		infec_level (double): the amount of people that are currently infected
		coverage_level (double): proportion of the population that is vaccinated
		risk (double): the risk of getting infected
        rate_in_neighborhood (double): the porpotion of people infected in
        the neighborhood
        returns:
		the probability of one person to get infected
	"""
	prob = infec_level * (1 - coverage_level) * risk
	#prob = (1-coverage_level)
	return rate_in_neighborhood



def expect_value(vaccinate_probability, coverage_level, infec_level, risk):
	"""calculates the expectation value for an individual

	Args:
		vaccinate_probability (double): the probability of that person to get vaccinated
		coverage_level (double) : the proportion of the scociety that is vaccinated
		infec_level (double): the amount of people that are currently infected
		risk (double): risk of vacc / risk of infection
	
	Returns:
		expectation value
	"""
	expect = - risk * vaccinate_probability - (1 - vaccinate_probability) *\
	 prob_infec(infec_level, coverage_level)
	return expect


def expected_gain(coverage_level, infec_level, vacc_cost, infec_cost, risk = 0.5):
	"""calculates the expectation expected gain if one vaccinates

	Args:
		coverage_level (double) : the proportion of the scociety that is vaccinated
		infec_level (double): the amount of people that are currently infected
        vacc_cost (double): the percieved cost when vaccinating
        infec_cost (doulbe): the percieved cost due to infection
		risk (double): risk of vacc / risk of infection
	Returns:
		expectation value
	"""
	expect = - vacc_cost + infec_cost * infec_level * (1 - coverage_level) * risk
	return expect

def grid_expected_gain(coverage_level, infec_level, vacc_cost, infec_cost,\
                  rate_in_neighborhood):
	"""calculates the expectation expected gain if one vaccinates

	Args:
		coverage_level (double) : the proportion of the scociety that is vaccinated
		infec_level (double): the amount of people that are currently infecte
		risk (double): risk of vacc / risk of infection
        rate_in_neighborhood (double): the porpotion of people infected in
        the neighborhood
	
	Returns:
		expectation value
	"""
	expect = - vacc_cost + infec_cost * prob_infec(infec_level, coverage_level,\
                                                rate_in_neighborhood)
	return expect

def discrete_gradient(array):
    """calculates the difference between an element in an array and the element
    before
    
    Args:
        array (int array) : the array for which the daily change should be calculated
        
    Returns:
        array with the daily change
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
        if people_list[rand].infected_days == -1:
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
        if people_list[rand].vaccinated == False:
            # set a random value to days since immunization up to 12 years
            days_since_immunization = random.randint(0,4380)
            people_list[rand].set_immunization(days_since_immunization, True, False)
            inf -= 1
    return people_list


def change_infection_cost_population(people_list, factor, probability):
    """ Change the percieved_infec_cost by a factor for every Person
    with some probability
    
    Args:
        people_list (list of Person): The list of people whose parameter should be changed
        factor (float): The factor by which the percieved_infec_cost should be changed
        probability (float, between 0 and 1): probability of each person to get
            the percieved_infec_cost changed
    
    Returns:
        people_list (list of Person): The list of people whose parameter have been changed
    """
    for p in people_list:
        if random.random() < probability:
            p.change_infec_cost_relative(factor)
    return people_list

def change_vaccination_cost_population(people_list, factor, probability):
    """ Change the percieved_vacc_cost by a factor for every Person
    with some probability
    
    Args:
        people_list (list of Person): The list of people whose parameter should be changed
        factor (float): The factor by which the percieved_vacc_cost should be changed
        probability (float, between 0 and 1): probability of each person to get
            the percieved_vacc_cost changed
    
    Returns:
        people_list (list of Person): The list of people whose parameter have been changed
    """
    for p in people_list:
        if random.random() < probability:
            p.change_vacc_cost_relative(factor)
    return people_list
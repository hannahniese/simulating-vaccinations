# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 22:01:11 2018

@author: markus
"""

def prob_infec(infec_level, coverage_level, risk = 0.1):
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

def expected_gain(coverage_level, infec_level, risk_vacc, risk_infec):
	"""calculates the expectation expected gain if one vaccinates

	Args:
		coverage_level (double) : the proportion of the scociety that is vaccinated
		
		infec_level (double): the amount of people that are currently infected
		
		risk (double): risk of vacc / risk of infection
	
	Returns:
		expectation value
	"""
	expect = - risk_vacc + risk_infec * prob_infec(infec_level, coverage_level)
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

def initial_infected(population, proportion infected):
    """TODO Markus"""
    
"""TODO kill 
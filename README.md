# simulating-vaccinations

* Group Name: simulating-vaccinations
* Group participants names: Hannah Niese, Markus Niese, Timo Schönegg
* Project Title: Simulating the impact of vaccination rates on disease spreading scenarios
* Programming language: Python 

## General Introduction

Vaccinations may be described as the most significant achievement in the history of medicine, and have lead to the eradication of many of the most severe diseases that plagued (and frequently decimated) societies. 
However, in developed countries, vaccination opponents have convinced a number of people not to get vaccinations, which could potentially lead to a revival of diseases we already thought extinct. Therefore, modelling the influence of vaccination rates on disease spreading is a worthwile pursuit. 

> (States your motivation clearly: why is it important / interesting to solve this problem?)
> (Add real-world examples, if any)
> (Put the problem into a historical context, from what does it originate? Are there already some proposed solutions?)

## The Model

In our project we intend to simulate the behaviour of individuals using game theory and a SIR to model the trend of a disease. Every agent in our model tries to maximize their personal gain which is dependent on the perceived risk of side effects due to vaccination and the probability of infection, which itself is dependent on the number of vaccinated people. That means that the behaviour of one individual is affected by the behaviour of everyone else. To model that we will use the Nash-Equilibrium. The SIR, which is widely used in modelling the spread of diseases, will provide the parameters, several datasets on vaccination rates and effects of vaccination scares (UK 1970 polio, MMR starting 1998) will be used to test the model. 

> (Define dependent and independent variables you want to study. Say how you want to measure them.) (Why is your model a good abstraction of the problem you want to study?) (Are you capturing all the relevant aspects of the problem?)


## Fundamental Questions

How do vaccination rates influence the spreading of diseases?
What are the critical vaccination rates of a society?
How would policy measures (vaccinating all school children etc.) change the spreading of diseases?

> (At the end of the project you want to find the answer to these questions)
> (Formulate a few, clear questions. Articulate them in sub-questions, from the more general to the more specific. )

## Expected Results

Using our model, we will simulate different scenarios to find out under which circumstances a disease can be eradicated und under which a decrease in the vaccination rate can lead to an uptake in infections.
Comparing the effectivity of policy measures with regards to immunisation.

> (What are the answers to the above questions that you expect to find before starting your research?)

## References 

Heal, G., & Kunreuther, H. (2005). The vaccination game. Risk Management and Decision Processes Center Working Paper, (05-10).

Bauch, C. T., & Earn, D. J. (2004). Vaccination and the theory of games. Proceedings of the National Academy of Sciences, 101(36), 13391-13394.

> (Add the bibliographic references you intend to use)
> (Explain possible extension to the above models)
> (Code / Projects Reports of the previous year)


## Research Methods
Game-theory, SIR to model the spreading of diseases

> (Cellular Automata, Agent-Based Model, Continuous Modeling...) (If you are not sure here: 1. Consult your colleagues, 2. ask the teachers, 3. remember that you can change it afterwards)


## Other

https://ourworldindata.org/vaccination
https://www.gapminder.org/data/ search for 'vaccine'

Immunization coverage, system indicators and schedule, and disease incidence
http://www.who.int/immunization/monitoring_surveillance/data/en/

# Reproducibility

> (step by step instructions to reproduce your results. *Keep in mind that people reading this should accomplish to reproduce your work within 10 minutes. It needs to be self-contained and easy to use*. e.g. git clone URL_PROY; cd URL_PROY; python3 main.py --light_test (#--light test runs in less than 5minutes with up to date hardware)) 

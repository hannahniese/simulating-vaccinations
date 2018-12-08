Simulating vaccination
Created as part of the ETH course "Lecture with Computer Exercises: 
    Modelling and Simulating Social Systems in MATLAB (or Python)"


December 2018
@author: Hannah Niese, Markus Niese, Timo Schönegg

There are various files and different functionality in this project.
Here is a short description of all of them.

All the functions and classes have detailed Python documentation and
all logic elements and variables are described in comments.
For the numerical values of the parameters please refer to the report
(report/report.pdf) where they are described and justified.
All the parameters are specific to pertussis but you can change them
to simulate other diseases. The most important parameters that are not
specific for a special disease are the population size and the number
of simulated days.


We invite you to test our simulation and play around with the parameters.
If you have any remarks please do not hesitate to contact us.
nieseh@ethz.ch
mniese@ethz.ch
timosho@ethz.ch





###############################################################################
LIGHT TEST
###############################################################################

For the light test (20 min simulation of one graph) follow these steps:

LIGHT TEST: (20 minutes, one graph)
Reproduce the graph showing the number of people who get the disease in
dependence of how many people are vaccinated in the beginning (in percent).
People do not vaccinate themselves during simulation.

Follow these steps

1. Download the files:
    LIGHT_network_0_to_100_percent.py,
    vacc.py,
    simulation_vaccination_tools.py,
    network_generator.py,
    folder networks with file 'barabasi_5000_2.txt'
    (This is a network with 5000 people)


2. Make sure you have matplotlib, numpy, csv, random, timeit and networkx
installed.

3. Open your favourite python development environment e.g. Spyder, PyCharm etc.
Open the downloaded file LIGHT_network_0_to_100_percent.py 
Important: Do NOT change anything in this file. All parameters are set
to appropriate values.
Start the program.
It will iterate the percentage of vaccinated people from 0% to 100% with steps
of 3%. This might take 2-3 minutes, depending on the CPU of your computer. 
When finished, it will output the graph of people who were at least once
infected during the simulation time of 500 days. The graph might be in the
background.
Note that your graph is not as smooth as the corresponding graph in the report,
as that one is a average of multible simulations.

If you now want to play around a little bit, you can change the
following parameters:
Note that extreme values of the parameters may lead to extreme results.

- population (line 26):
      You need to create a new network graph for the new population!
      Remove therefore the comment in line 28 to use the function
      network_generator.create_barabasi_in_file
      (population, 2, 'barabasi_' + str(population) + '_2.txt')
      Make sure there are enought initially infected people (at least ~3)
      by changing the initially_infected_people variable (line 105).
              
- simulation_length (line 51):
      Change the time periode (in days) of the simulation.
      Be careful: if the periode is to short, some people are still sick and
      can infect other people, when the simulation ends.
      
- stepwidth of iteration  (line 40):
      Decrease the stepwith of the iteration throught the percentage of
      initially vaccinated people for more exact results.
      stepwidth needs to be an integer!








###############################################################################
FULL TEST
###############################################################################

There are different files with different functionalities:
main.py
To rund the basic network simulation run main.py.
This will execute the simulation for the parameters and the network given.
For the network there are three options:
1. Op: Directly using network_generator.generate_Albert_Barabasi()
    random network. Very slow. !!!Only use for population up to 1000!!!
2. Op: Import random Albert-Barabasi_Graph generated with 
    network_generator.create_barabasi_in_file() and import using
    network_generator.import_barabasi_graph()
3. Op: Import from a TSV file using network_generator.import_graph_from_tsv()
    !!! Important !!! For options 2 and 3 population (len(people_list)) HAS to
    be equal to the number of nodes in the imported graph
There are a number of networks provided in the networks folder.

The result will be displayed in a graph. You may need to change the scale 
on the y-axis to get the whole data on the graph

All the parameters are set such that the programm is directly executable.
If you want to change parameters, please refer to the comments in the code.
All the parameters are specific for pertussis.

Testing.py:
Same functionality as main.py but lets you run the simulation multiple
times with the same parameters.

grid.py:
For visualisation you can use grid.py. It works similar to the network model
but produces a txt file as output that can be animated with the processing
file grid_graphics/grid_graphics.pde. !!! The grid model is just for 
visualisation. It does have different parameters than the network model.
For all analysis the network model should be used !!!


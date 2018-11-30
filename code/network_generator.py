# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 20:08:34 2018

@author: markus
"""
import random
import numpy as np
import csv
import networkx

def generate_trivial_random_graph(people_list, min_contacts, max_contacts):
    """
    Generates a directed network where every Person in people_list gets
    a random number of edges betwenn min_contacts and max_contacts
    
    Args:
        people_list (list of Network_Person): The edges of the Network
        min_contacts (int): minimal number of contacts per Person
        max_contacts (int): maximal number of contacts per Person
    """
    population = len(people_list)
    for x in people_list:
        contacts = int(random.randint(min_contacts, max_contacts))
        for i in range(contacts):
            a = random.randint(0,population-1)
            if a not in x.contacts:
                x.contacts.append(a)
            else:
                i = i-1
    
def generate_Albert_Barbasi(people_list, m, seed_size):
    """ Generates a random Network with the Albert-Barabasi-Model
    
    Args:
        people_list (list of Network_Person): Nodes of Network
        m (int): Number of edges to attach from a new node to existing nodes
        seed_size (int): number of initially connected nodes
    """
    ## generate seed (these nodes are all connected to each other)
    for i in range(seed_size):
        for j in range(seed_size):
            if i != j:
                people_list[i].add_contact(j)
    ## get a degree list
    degree_list = get_degree_list(people_list)
    ## generate Albert Barabsi Network
    for i in range(seed_size, len(people_list)):
        nodes_to_connect = []
        while len(nodes_to_connect) < m:
            part_sum = 0.0
            rand = random.random()
            for n in range(i):
                base = part_sum
                step = part_sum + people_list[n].get_degree() /sum(degree_list)
                part_sum = step
                if rand >= base and rand < step:
                    if n in nodes_to_connect:
                        break
                    nodes_to_connect.append(n)
                    break
        for node in nodes_to_connect:
             add_edge(people_list, i, node, degree_list)
    
def get_degree_list(people_list):
    """
    Returns:
        A list which has for every index j the degree of people_list(j)
        (number of contacts)
    """
    degree_list = []
    for i in range(len(people_list)):
        degree_list.append(people_list[i].get_degree())
    return degree_list

def add_edge(people_list, node1, node2, degree_list = []):
    """adds undirected edge between two nodes in people_list and updates 
    the degree_list
    
    Args:
        people_list (list of Network_Person): Nodes of Network
        node1 (int): index of first node of the new edge
        node2 (int): index of second node of new edge
        degree_list (int list): The degree of every node in people_list
    """
    if len(degree_list) > np.maximum(node1, node2):
        degree_list[node1] += 1
        degree_list[node2] += 1
    people_list[node1].contacts.append(node2)
    people_list[node2].contacts.append(node1)
    
    
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
                
def create_barabasi_in_file(n, m, filename):
    """ Generates a random Network with the Albert-Barabasi-Model
    
    Args:
        n (int): Number of Nodes
        m (int): Number of edges to attach from a new node to existing nodes
        filename (str): File weill be stored under that name in the Networks
            folder. You should use txt format.
    """
    G = networkx.barabasi_albert_graph(n, m)
    networkx.write_adjlist(G,"Networks/"+filename)
    
def import_graph_from_tsv(path, people_list):
    """
    !!!Important!!!
    
    The number of elements in the people_list (variable population
    in network.py) has to be the same as the number of nodes of the imported
    graph
    
    !!!Important!!!
    
    import network from a tsv file
    the file has to have two column. One with the starting and one with the
    ending vertice of each arc. For undirected graphs both directions have
    to be given. The population has to be set manually to the number of
        vertices
    All lines will be read except lines beginning with a '#'
    
    Args:
        path (str): path of the tsv file
        people_list (list of Network_Person): Nodes of the network
    """
    tsvfile = open(path)
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        if row[0][:1] != "#":
            people_list[int(row[0])].add_contact(int(row[1]))
    
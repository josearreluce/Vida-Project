#Function file for graph

import numpy as np
import networkx as nx

import symptom
import condition

# Note: hashability required for nodes - instances of user-defined classes are hashable, which we use.
# Note: Can DEFINITELY be re-factored. Repetitive code is separate to emphasize different cases.


# Error Functions: Optional for validity checking ###

def noSymptom(): #Symptoms doesn't exist
    print("Error. Nonexistent symptom found.")
    return 0

def noCondition(): #Conditions doesn't exist
    print("Error. Nonexistent condition found.")
    return 0

# (1) Return an empty graph: For now, plain unweighted edges, with no clear distinction between symptom/condition nodes
def createGraph():
    return nx.Graph()


# (2) Add a symptom to the graph, with related symptoms, conditions
def addSymptom(G, s, symptoms, conditions):
    G.add_node(s)
  
    for i in range(len(symptoms)):
        G.add_edge(s, symptoms[i])
    for i in range(len(conditions)):
        G.add_edge(s, conditions[i])

    return G


# (3) Add a condition to the graph, with related symptoms
def addCondition(G, c, symptoms):
    G.add_node(c)
  
    for i in range(len(symptoms)):
        G.add_edge(c,symptoms[i])
  
    return G


# (4) Get related conditions given a symptom
def getRelatedConditions(G, symptom):  # Get related conditions given a symptom
    if type(symptom) != 'Symptom':  # Make sure we're actually using a symptom
        nosymptom()
    
    conditions = []
    neighbors = G.neighbors()
  
    for i in range(len(neighbors)):
        if type(neighbors[i]) == 'Symptom':  # Check the typing
            conditions.append(neighbors[i])

    return conditions


# (5) Get related symptom given a condition
def getRelatedSymptomsC(G, condition):
    if type(condition) != 'Condition':  # Make sure we're actually given a condition
        nocondition()

    symptoms = []
    neighbors = G.neighbors()
  
    for i in range(len(neighbors)):
        if type(neighbors[i]) == 'Condition':
            symptoms.append(neighbors[i])

    return symptoms


# (6) Get related symptoms given a symptom
def getRelatedSymptomsS(G, symptom):  # Get related symptoms given a symptom
    if type(condition) != 'Symptom':  # Make sure we're actually given a condition
        nocondition()

    symptoms = []
    neighbors = G.neighbors()

    for i in range(len(neighbors)):
        if type(neighbors[i]) == 'Symptom':
            symptoms.append(neighbors[i])

    return symptoms


# (7) Remove a symptom, and all
def removeSymptom(G, symptom):  # Remove a symptom from the graph, deleting associated edges
    G.remove_node(symptom)
    return G


# (8) Remove a condition from the graph, deleting associated edges
def removeCondition(G, condition):
  G.remove_node(condition)
  return G

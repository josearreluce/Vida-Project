#Test file for graph

import networkx as nx

import condition as c
import symptom as s

import graph as g

#Test Commposition : First tests for each function are very simple "sanity" tests: One involves a graph that will return
#nothing when the function is called, one involves a simple case with one edge + two nodes, and the last test is a complex test using a
#graph with multiple nodes and edges.

#NOTE(!): Ideally, we should check for equality between nodes instead of "number of neighbors" or "length of graph" to ensure correctness.
#however adding Symptoms/Condition edges is very simple, and it is almost impossible to add wrong nodes/edges.
#If there is a mistake, the number of neighbors will simply be off - otherwise, we have added exactly what we require.

#Furthermore, we are *writing test cases* - in order to check for exact equality of nodes, we require a lot more involved implementation.
#When we execute testing, we may test for exact nodes/edges, instead of number of neighbors, but we will use these test cases.

GG = g.createGraph() #Complex graph with 4 nodes - stronger test. #4 nodes, 4 edges (1 S-S edge, 3 S-C edges)
#### Visual of the connections
#C1-----S1

#C2-----(S1,S2)
#S1-----S2
S1 = s.Symptom(1, 1, 1, 1, 1, 1)
S2 = s.Symptom(2, 2, 2, 2, 2, 2)
C1 = c.Condition(1, 1, 1, 1, 1)
C2 = c.Condition(2, 2, 2, 2, 2)
g.addSymptom(GG, S1, [], [])
g.addSymptom(GG, S2, [S1], [])
g.addCondition(GG, C1, [S1], [])
g.addCondition(GG, C2, [S1, S2])


#createGraph test
def createTest():
  G = g.createGraph()
  res = (len(G) == 0)
  return res

#addSymptom test
def addSymptomSimple():
  G = g.createGraph()
  S1 = s.Symptom(1, 1, 1, 1, 1, 1)
  S2 = s.Symptom(2, 2, 2, 2, 2, 2)
  g.addSymptom(G, S1, [], [])
  res1 = (len(G) == 1)
  g.addSymptom(G, S2, [], [])
  res2 = (len(G) == 2)
  return res1 and res2

def addWithEdge():
  G = g.createGraph()
  S1 = s.Symptom(1, 1, 1, 1, 1, 1)
  S2 = s.Symptom(2, 2, 2, 2, 2, 2)
  g.addSymptom(G, S1, [], [])
  g.addSymptom(G, S2, [S1], [])
  res1 = (len(G) == 2)
  res2 = (len(G.edges()) == 1)
  return res1 and res2

def addComplex():
  S3 = s.Symptom(1, 1, 1, 1, 1, 1)
  g.addSymptom(GG, S3, [S1, S2], [C1, C2])
  res1 = (len(GG) == 5)
  res2 = (len(GG.edges()) == 7)
  res3 = (len(GG[S3]) == 4)
  res4 = (len(GG[S1]) == 4)
  res5 = (len(GG[S2]) == 3)
  res6 = (len(GG[C1]) == 2)
  res7 = (len(GG[C2]) == 3)
  return res1 and res2 and res3 and res4 and res5 and res6 and res7

#addCondition test
def addConditionSimple():
  G = g.createGraph()
  C1 = c.Condition(1, 1, 1, 1, 1, 1)
  C2 = c.Condition(2, 2, 2, 2, 2, 2)
  g.addCondition(G, C1, [])
  g.addCondition(G, C2, [])
  res1 = (len(G) == 2)
  return res1

def addConditionEdge():
  G = g.createGraph()
  C1 = c.Condition(1, 1, 1, 1, 1, 1)
  C2 = c.Condition(2, 2, 2, 2, 2, 2)
  g.addCondition(G, C1, [])
  g.addCondition(G, C2, [C1])
  res1 = (len(G) == 2)
  res2 = len(G.edges() == 1)

#getRelatedConditions test
def getNoRelatedSymptoms():
  G = g.createGraph()
  C1 = s.Symptom(1, 1, 1, 1, 1, 1)
  S1 = s.Symptom(2, 2, 2, 2, 2, 2)
  g.addCondition(G, C1, [])
  g.addSymptom(G, S1, [], [])
  related = g.getRelatedConditions(G, S1)
  res1 = (len(related) == 0)
  return res1

def getSomeRelatedSymptoms():
  G = g.createGraph()
  C1 = s.Symptom(1, 1, 1, 1, 1, 1)
  S1 = s.Symptom(2, 2, 2, 2, 2, 2)
  g.addCondition(G, C1, [])
  g.addSymptom(G, S1, [], [C1])
  related = g.getRelatedConditions(G, S1)
  res1 = (len(related) == 1)
  return res1

def getRelatedSymptomsComplex():

  S3 = s.Symptom(1, 1, 1, 1, 1, 1)
  C3 = c.Condition(1, 1, 1, 1, 1, 1)
  g.addSymptom(GG, S3, [S1, S2], [C1, C2])
  related = g.getRelatedConditions(GG, S3)
  res1 = (len(related == 2))
  related = g.getRelatedConditions(GG, S1)
  res2 = (len(related == 2))
  related = g.getRelatedConditions(GG, S2)
  res3 = (len(related == 1))
  
  g.addCondition(GG, C3, [S1])
  related = g.getRelatedConditions(GG, S1)
  res4 = (len(related == 2))
  
  return res1 and res2 and res3 and res4
  
  
#getRelatedSymptomsC test
def getNoRelatedSymptomsC():
  G = g.createGraph()
  C1 = s.Symptom(1, 1, 1, 1, 1, 1)
  S1 = s.Symptom(2, 2, 2, 2, 2, 2)
  g.addCondition(G, C1, [])
  g.addSymptom(G, S1, [], [])
  related = g.getRelatedConditionsC(G, C1)
  res1 = (len(related) == 0)
  return res1

def getSomeRelatedSymptomsC():
    G = g.createGraph()
    C1 = s.Symptom(1, 1, 1, 1, 1, 1)
    S1 = s.Symptom(2, 2, 2, 2, 2, 2)
    g.addCondition(G, C1, [])
    g.addSymptom(G, S1, [], [C1])
    related = g.getRelatedConditionsC(G, C1)
    res1 = (len(related) == 1)
    return res1
  
def getSomeRelatedSymptomsCComplex():
    related = g.getRelatedConditionsC(GG, C1)
    res1 = (len(related) == 1)
    return res1

#getRelatedSymptomsS test
def getNoRelatedSymptomsS():
    G = g.createGraph()
    S1 = s.Symptom(1, 1, 1, 1, 1, 1)
    S2 = s.Symptom(2, 2, 2, 2, 2, 2)
    g.addSymptom(G, S1, [])
    g.addSymptom(G, S2, [], [])
    related = g.getRelatedSymptomsS(G, S1)
    res1 = (len(related) == 0)
    return res1

def getSomeRelatedSymptomsS():
    G = g.createGraph()
    S1 = s.Symptom(1, 1, 1, 1, 1, 1)
    S2 = s.Symptom(2, 2, 2, 2, 2, 2)
    g.addSymptom(G, S1, [], [])
    g.addSymptom(G, S2, [S1], [])
    related = g.getRelatedSymptomsS(G, S1)
    res1 = (len(related) == 1)
    return res1
  
def getSomeRelatedSymptomsSComplex():
    related = g.getRelatedSymptomsS(GG, S1)
    res1 = (len(related) == 1)
    related = g.getRelatedSymptomsS(GG, S2)
    res2 = (len(related) == 1)
    return res1 and res2

#Removing Symptoms, Conditions, test (for both)
def removeSymptomTest():
    G = g.createGraph()
    S1 = s.Symptom(1, 1, 1, 1, 1, 1)
    S2 = s.Symptom(2, 2,2, 2, 2, 2)
    C1 = c.Condition(1, 1, 1, 1, 1, 1)
    g.addSymptom(G, S1, [], [])
    g.addSymptom(G, S2, [S1], [])
    g.addCondition(G, C1, [S1, S2])
    related = g.getRelatedSymptomsC(G, C1)
    res1 = (len(related == 2))
    res2 = (len(g.removeSymptom(G, S1)) == 1)
    res3 = (len(g.removeCondition(G, C1)) == 1)
    return res1 and res2 and res3

def removeSymptomTestComplex():
    res1 = (len(g.removeSymptom(GG, S1)) == 3)
    res2 = (len(g.removeSymptom(GG, S2)) == 3)
    res3 = (len(g.removeCondition(GG, C1)) == 3)
    return res1 and res2 and res3






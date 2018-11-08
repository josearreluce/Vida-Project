#Test file for graph

import networkx as nx

import condition as c
import symptom as s

import graph as g

#createGraph test
def createTest():
  G = g.createGraph()
  res = (len(G) == 0)
  return res

#addSymptom test
def addSymptomSimple():
  G = g.createGraph()
  S1 = s.Symptom(1,1,1,1,1,1)
  S2 = s.Symptom(2,2,2,2,2,2)
  g.addSymptom(G,S1,[],[])
  res1 = (len(G) == 1)
  g.addSymptom(G,S2,[],[])
  res2 = (len(G) == 2)
  return res1 and res2

def addWithEdge():
  G = g.createGraph()
  S1 = s.Symptom(1,1,1,1,1,1)
  S2 = s.Symptom(2,2,2,2,2,2)
  g.addSymptom(G,S1,[],[])
  g.addSymptom(G,S2,[S1],[])
  res1 = (len(G) == 2)
  res2 = len(G.edges() == 1)
  return res1 and res2

#addCondition test
def addConditionSimple():
  G = g.createGraph()
  C1 = c.Condition(1,1,1,1,1,1)
  C2 = c.Condition(2,2,2,2,2,2)
  g.addCondition(G,C1,[])
  g.addCondition(G,C2,[])
  res1 = (len(G) == 2)
  return res1

def addConditionEdge():
  G = g.createGraph()
  C1 = c.Condition(1,1,1,1,1,1)
  C2 = c.Condition(2,2,2,2,2,2)
  g.addCondition(G,C1,[])
  g.addCondition(G,C2,[C1])
  res1 = (len(G) == 2)
  res2 = len(G.edges() == 1)

#getRelatedConditions test
def getNoRelatedSymptoms():
  G = g.createGraph()
  C1 = s.Symptom(1,1,1,1,1,1)
  S1 = s.Symptom(2,2,2,2,2,2)
  g.addCondition(G,C1,[])
  g.addSymptom(G,S1,[],[])
  related = g.getRelatedConditions(G,S1)
  res1 = (len(related) == 0)
  return res1

def getSomeRelatedSymptoms():
  G = g.createGraph()
  C1 = s.Symptom(1,1,1,1,1,1)
  S1 = s.Symptom(2,2,2,2,2,2)
  g.addCondition(G,C1,[])
  g.addSymptom(G,S1,[],[C1])
  related = g.getRelatedConditions(G,S1)
  res1 = (len(related) == 1)
  return res1

#getRelatedSymptomsC test
def getNoRelatedSymptomsC():
  G = g.createGraph()
  C1 = s.Symptom(1,1,1,1,1,1)
  S1 = s.Symptom(2,2,2,2,2,2)
  g.addCondition(G,C1,[])
  g.addSymptom(G,S1,[],[])
  related = g.getRelatedConditionsC(G,C1)
  res1 = (len(related) == 0)
  return res1

def getSomeRelatedSymptomsC():
    G = g.createGraph()
    C1 = s.Symptom(1,1,1,1,1,1)
    S1 = s.Symptom(2,2,2,2,2,2)
    g.addCondition(G,C1,[])
    g.addSymptom(G,S1,[],[C1])
    related = g.getRelatedConditionsC(G,C1)
    res1 = (len(related) == 1)
    return res1

#getRelatedSymptomsS test
def getNoRelatedSymptomsC():
    G = g.createGraph()
    S1 = s.Symptom(1,1,1,1,1,1)
    S2 = s.Symptom(2,2,2,2,2,2)
    g.addSymptom(G,S1,[])
    g.addSymptom(G,S2,[],[])
    related = g.getRelatedSymptomsS(G,S1)
    res1 = (len(related) == 0)
    return res1

def getNoRelatedSymptomsC():
    G = g.createGraph()
    S1 = s.Symptom(1,1,1,1,1,1)
    S2 = s.Symptom(2,2,2,2,2,2)
    g.addSymptom(G,S1,[],[])
    g.addSymptom(G,S2,[S1],[])
    related = g.getRelatedSymptomsS(G,S1)
    res1 = (len(related) == 1)
    return res1

#Removing Symptoms, Conditions, test (for both)
def removeSymptomTest():
  G = g.createGraph()
  S1 = s.Symptom(1,1,1,1,1,1)
  S2 = s.Symptom(2,2,2,2,2,2)
  C1 = c.Condition(1,1,1,1,1,1)
  g.addSymptom(G,S1,[],[])
  g.addSymptom(G,S2,[S1],[])
  g.addCondition(G,C1,[S1,S2])
  related = g.getRelatedSymptomsC(G,C1)
  res1 = (len(related == 2))
  res2 = (len(g.removeSymptom(G,S1)) == 1)
  res3 = (len(g.removeCondition(G,C1)) == 1)
  return res1 and res2 and res3





print(createTest())
print(addSymptomSimple())
print(addWithEdge())
print(addConditionSimple())
print(getNoRelatedSymptons())
print(getSomeRelatedSymptoms)
print(getNoRelatedSymptomsC())
print(getSomeRelatedSymptomsC())






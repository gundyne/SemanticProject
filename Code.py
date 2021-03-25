# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 12:42:44 2021

@author: Dat
"""

import pandas as pd
import rdflib

from rdflib.Graph import Graph

earthquakes = pd.read_csv("earthquakes_data.tsv", sep='\t',header=0,skiprows=1).to_numpy()
#year = 1
#month = 2
#location = 9

permits = pd.read_excel("permitsbyusreg_cust.xls",sheet_name=1,header=0,skiprows=5).to_numpy().T[1:].T[:398]
#Date = 0
#Total = 1
#Northeast = 6
#Midwest = 8
#South = 10
#West = 10

#Creating the graph
g = Graph()

#West = 12

n = Namespace("http://web.csulb.edu/~016412147/CECS571/SemanticOntology/")
g = Graph()

g.bind('earthpermit', n)

#Class Creation
g.add( (n.Permit, RDFS.subClassOf, OWL.Thing) )
g.add( (n.Earthquake, RDFS.subClassOf, OWL.Thing) )

#Property Creation
#permit to month
g.add( (n.authorizedOn, RDFS.subPropertyOf, OWL.topObjectProperty) )
#earthquake to month
g.add( (n.shookOn, RDFS.subPropertyOf, OWL.topObjectProperty) )

g.add( (n.numberAuthorized, RDFS.subPropertyOf, OWL.topDataProperty) )
g.add( (n.month, RDFS.subPropertyOf, OWL.topDataProperty) )
g.add( (n.location, RDFS.subPropertyOf, OWL.topDataProperty) )

#sending the data
for i in range(permits.shape[0]):
    permitTest = BNode()
    g.add( (permitTest,RDFS.label,Literal(permits[i][0].date().isoformat()+" Permits")))
    g.add( (permitTest,n.numberAuthorized,Literal(permits[i][1] * 1000, datatype=XSD.integer))) 
    g.add( (permitTest,n.authorizedOn,(Literal(permits[i][0].date(), datatype=XSD.date)) ) )
    
for i in range(earthquakes.shape[0]):
    earthquakeTest = BNode()
    g.add( (earthquakeTest,n.shookOn,(Literal(datetime.date(earthquakes[i][1],earthquakes[i][2],1),  datatype=XSD.date)) ) )
    g.add( (earthquakeTest,n.location,(Literal(earthquakes[i][9], datatype=XSD.string)) ) )

#Exporting the graph
g.serialize("test.rdf", format="xml")


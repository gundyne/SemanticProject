import datetime
import numpy as np
import pandas as pd
from rdflib import Namespace, Graph, RDF, RDFS, OWL, Literal, XSD, URIRef

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
#West = 12

n = Namespace("http://example.org/")
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
    permitTest = URIRef("http://example.org/Permit/permit"+str(i))
    g.add( (permitTest,RDF.type,n.Permit) )
    g.add( (permitTest,n.numberAuthorized,Literal(int(permits[i][1] * 1000), datatype=XSD.integer)) )
    g.add( (permitTest,n.authorizedOn,Literal(permits[i][0].date(), datatype=XSD.date))) 
    
for i in range(earthquakes.shape[0]):
    earthquakeTest = URIRef("http://example.org/Earthquake/quake"+str(i))
    g.add( (earthquakeTest,RDF.type,n.Earthquake) )
    g.add( (earthquakeTest,n.shookOn,(Literal(datetime.date(earthquakes[i][1],earthquakes[i][2],1),  datatype=XSD.date)) ) )
    g.add( (earthquakeTest,n.location,(Literal(earthquakes[i][9], datatype=XSD.string)) ) )
    
#exporting file as .rdf file
g.serialize("test.owl", format="xml")
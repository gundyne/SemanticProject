import datetime
import numpy as np
import pandas as pd
from rdflib import Namespace, Graph, RDF, RDFS, OWL, Literal, XSD, URIRef

northeastStates = ["Connecticut", "Maine", "Massachusetts", 
                   "New Jersey", "New Hampshire", "New York", "Pennsylvania", "Rhode Island", "Vermont"]
midwestStates = ["Kansas", "Illinois", "Indiana", "Iowa", "Michigan", "Minnesota", "Missouri", "Nebraska", 
                 "North Dakota", "Ohio", "South Dakota", "Wisconsin"]
southStates = ["Alabama", "Arkansas", "Delaware", "D.C.", "Florida", "Georgia", 
               "Kentucky", "Louisiana", "Maryland", "Mississippi", "North Carolina",
               "Oklahoma", "South Carolina", "Tennessee", "Texas", "Virginia", "West Virginia"]
westStates = ["Alaska", "Arizona", "California", "Colorado", "Hawaii", "Idaho", "Montana", 
              "Nevada", "New Mexico", "Oregon", "Utah", "Washington", "Wyoming", "Hawaiian Islands"]

def get_Region(loc):
    state = loc.split(":")[0].split("-")[0].upper()
    if state in map(lambda i: i.upper(),northeastStates): return 1
    if state in map(lambda i: i.upper(),midwestStates): return 2
    if state in map(lambda i: i.upper(),southStates): return 3
    if state in map(lambda i: i.upper(),westStates): return 4
    return 0
    

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

p = Namespace("http://example.org/properties/")
g = Graph()

g.bind('earthpermit', n)

#Class Creation
g.add( (n.Permit, RDFS.subClassOf, OWL.Thing) )
g.add( (n.Earthquake, RDFS.subClassOf, OWL.Thing) )
g.add( (n.Month, RDFS.subClassOf, OWL.Thing) )
g.add( (n.Earthquake, OWL.disjointWith, n.Permit) )

g.add( (n.Region, RDFS.subClassOf, OWL.Thing) )
g.add( (n.Northeast, RDFS.subClassOf, n.Region) )
g.add( (n.Midwest, RDFS.subClassOf, n.Region) )
g.add( (n.South, RDFS.subClassOf, n.Region) )
g.add( (n.West, RDFS.subClassOf, n.Region) )
g.add( (n.All, RDFS.subClassOf, n.Region) )

#Property Creation
#permit to month
g.add( (p.authorizedOn, RDFS.subPropertyOf, OWL.topObjectProperty) )
#earthquake to month
g.add( (p.shookOn, RDFS.subPropertyOf, OWL.topObjectProperty) )
#permit to region
g.add( (p.talliedOn, RDFS.subPropertyOf, OWL.topObjectProperty) )
#earthquake to region
g.add( (p.locatedAt, RDFS.subPropertyOf, OWL.topObjectProperty) )

g.add( (p.numberAuthorized, RDFS.subPropertyOf, OWL.topDataProperty) )
g.add( (p.month, RDFS.subPropertyOf, OWL.topDataProperty) )
g.add( (p.location, RDFS.subPropertyOf, OWL.topDataProperty) )

#sending the data
for i in range(permits.shape[0]):
    permitTestA = URIRef("http://example.org/Permit/permitA"+str(i))
    permitTestN = URIRef("http://example.org/Permit/permitN"+str(i))
    permitTestM = URIRef("http://example.org/Permit/permitM"+str(i))
    permitTestW = URIRef("http://example.org/Permit/permitW"+str(i))
    permitTestS = URIRef("http://example.org/Permit/permitS"+str(i))
    g.add( (permitTestA,RDF.type,n.Permit) )
    g.add( (permitTestN,RDF.type,n.Permit) )
    g.add( (permitTestM,RDF.type,n.Permit) )
    g.add( (permitTestW,RDF.type,n.Permit) )
    g.add( (permitTestS,RDF.type,n.Permit) )
    g.add( (permitTestA,p.numberAuthorized,Literal(int(permits[i][1] * 1000), datatype=XSD.integer)) )
    g.add( (permitTestN,p.numberAuthorized,Literal(int(permits[i][6] * 1000), datatype=XSD.integer)) )
    g.add( (permitTestM,p.numberAuthorized,Literal(int(permits[i][8] * 1000), datatype=XSD.integer)) )
    g.add( (permitTestS,p.numberAuthorized,Literal(int(permits[i][10] * 1000), datatype=XSD.integer)) )
    g.add( (permitTestW,p.numberAuthorized,Literal(int(permits[i][12] * 1000), datatype=XSD.integer)) )
    monthTest = URIRef("http://example.org/Month/month"+str(i))
    g.add( (monthTest,RDF.type,n.Month) )
    g.add( (monthTest,p.month,Literal(permits[i][0].date(), datatype=XSD.date))) 
    g.add( (permitTestA,p.authorizedOn,monthTest)) 
    g.add( (permitTestN,p.authorizedOn,monthTest))
    g.add( (permitTestM,p.authorizedOn,monthTest))
    g.add( (permitTestW,p.authorizedOn,monthTest))
    g.add( (permitTestS,p.authorizedOn,monthTest))
    g.add( (permitTestA,p.talliedOn,n.All))
    g.add( (permitTestN,p.talliedOn,n.Northeast))
    g.add( (permitTestM,p.talliedOn,n.Midwest))
    g.add( (permitTestW,p.talliedOn,n.West))
    g.add( (permitTestS,p.talliedOn,n.South))
    
for i in range(earthquakes.shape[0]):
    earthquakeTest = URIRef("http://example.org/Earthquake/quake"+str(i))
    g.add( (earthquakeTest,RDF.type,n.Earthquake) )
    month = g.value(None, p.month, (Literal(datetime.date(earthquakes[i][1],earthquakes[i][2],1),  datatype=XSD.date)))
    g.add( (earthquakeTest,p.shookOn, month) )
    g.add( (earthquakeTest,p.location,(Literal(earthquakes[i][9], datatype=XSD.string)) ) )
    g.add( (earthquakeTest,p.magnitude,(Literal(earthquakes[i][13], datatype=XSD.decimal)) ) )
    regionNum = get_Region(earthquakes[i][9])
    if(regionNum == 1):
        g.add( (earthquakeTest,p.locatedAt, n.Northeast) )
    if(regionNum == 2):
        g.add( (earthquakeTest,p.locatedAt, n.Midwest) )
    if(regionNum == 3):
        g.add( (earthquakeTest,p.locatedAt, n.South) )
    if(regionNum == 4):
        g.add( (earthquakeTest,p.locatedAt, n.West) )
        
    
#exporting file as .rdf file
g.serialize("test.owl", format="xml")
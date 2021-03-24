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


#Exporting the graph
g.serialize("test.rdf", format="xml")


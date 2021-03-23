# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 12:42:44 2021

@author: Dat
"""

import pandas as pd
import rdflib

from rdflib.Graph import Graph


#Creating the graph
g = Graph()


#Exporting the graph
g.serialize("test.rdf", format="xml")


# PYTHON METADATA ADAPTATION FILE
# Using Anaconda - Python 3.9.13. 

import os
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import xml.dom.minidom
from xml.etree import ElementTree
import lxml.etree as etree



path = "/Users/thierryletendre/Desktop/CRDCN/RAD_Training/Resources/Data"
#path = '' # Insert path here
os.chdir(path)

# Setting up the dataset as a dataframe, will allow for editing
data = pd.read_csv('2025_03_27_WPDATA.csv')
df = pd.DataFrame(data)

# This line of code can be used to see the entire dataset in the shell.
#print(df.to_string())

#Renaming column names
df.rename(columns = {"title.fr": "Dataset Title (French)", 
                     "title.en": "Title", "summary.fr": "Summary French",
                     "summary.en": "Summary", "url": "Permalink",
                     "identifier": "Dataset ID"}, inplace = True)


# The way the data is organised, they are split by ">" and "|", and other symbols. 
# These represent the hierarchal nature of these subjects. 
# The following code is used to remove the hierarchal symbology.
 
df['splitsubs'] = df['Subjects'].str.split('>')

def cls(subjectlist):
    cleaned = [subject.split('|')[0] for subject in subjectlist]
    return cleaned


df['cleaned'] = df['splitsubs'].apply(cls)

print(df)

#print(df['cleaned'].to_string())


"""
for i in df['Subjects']:
  if type(i) == str:
    f = i.split('>')
    i.replace(to_replace = i, value = f)
    
    
"""






"""
counter = 0 

    if type(df['Subjects'][counter]) == str:
        df.replace(to_replace = df['Subjects'][counter],
           value="Omega Warrior")
        print(df['Subjects'][counter])
    counter += 1
"""
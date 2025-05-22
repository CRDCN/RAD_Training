# Automatic Citation formatter

# Importing used modules
import os
import pandas as pd
import numpy as np


# Setting and directing path
path = "/your/path/here"
os.chdir(path)



####################### Loading and Creating Dataframe #########################


# Setting up the dataset as a dataframe which will allow for editing
data = pd.read_csv('Dataset-Export-2025-March-12-1920(2).csv')
df = pd.DataFrame(data)
df.rename(columns = {"title.fr": "Dataset Title (French)", 
                     "title.en": "Title", "summary.fr": "Summary French",
                     "summary.en": "Summary", "url": "Permalink",
                     "identifier": "Dataset ID"}, inplace = True)



###################### Clean-up and Helpful variables ##########################


# Splitting sampling method/frequencies
df['Data Types'] = df['Data Types'].str.split('>')


# Creating a temporary column to identify URL Ref availabilty
df['is nan'] = df['URL Ref'].isna()


# Creating variables for frequently used string
sponsor = "Research Data Centre Program"
#sponsor_fr = "Programme des Centres de données de recherche"


citation_en = []
#citation_fr = []



############################# Citation While Loop ##############################


count2 = 0

while count2 != len(df['Data Types']):
    
    
    # Setting-up appropriate url variable as a function of the 'is nan' column
    if df['is nan'][count2] == True:
        url = df["Permalink"][count2]
        #url_fr = df["Permalink"][count2]

    else:
        url = df['URL Ref'][count2]
        #url_fr = df['URL Ref French'][count2]
    
    
    # Creation of citation for entries fitting these conditions
    if df['Data Types'][count2][0] == 'Longitudinal' and df['Data Types'][count2][1] == 'Administrative':
        
        citation_val_en = f'Statistics Canada. ({df["dataset_years_0_max_year"][count2]}). {df["Title"][count2]}. {sponsor}. {url}. Accessed [day] [month] [year].'
        citation_en.append(citation_val_en)
        
        #citation_val_fr = f'Statistique Canada. ({df["dataset_years_0_max_year"][count2]}). {df["Dataset Title (French)"][count2]}. {sponsor_fr}. {url_fr}. Accédé [jour] [mois] [année].'
        #citation_fr.append(citation_val_fr)
        
        count2 += 1
    
    
    
    # Creation of citation for entries fitting these conditions
    elif df['Data Types'][count2][0] == 'Longitudinal' and df['Data Types'][count2][1] == 'Integrated':
        
        citation_val_en = f'Statistics Canada. ({df["dataset_years_0_max_year"][count2]}). {df["Title"][count2]}. {sponsor}. {url}. Accessed [day] [month] [year].'
        citation_en.append(citation_val_en)
        
        #citation_val_fr = f"Statistique Canada. ({df['dataset_years_0_max_year'][count2]}). {df['Dataset Title (French)'][count2]}. {sponsor_fr}. {url_fr}. Accédé [jour] [mois] [année]."
        #citation_fr.append(citation_val_fr)
        
        count2 += 1     
    
    
    
    # Creation of citation for entries fitting these conditions
    # NOTE THAT THESE MAY EVANTUALLY BECOME REPEATED, AND AS SUCH, MAY REQUIRE SOME TUNING. THIS SHOULD AUTOMATICALLY BE FIXED IF THE ENTRY IS CHANGED FROM 'Single' to 'Repeated'    
    elif df['Data Types'][count2][0] == 'Longitudinal' and df['Data Types'][count2][1] == 'Survey':
        
        citation_val_en = f'Statistics Canada. ({df["dataset_years_0_max_year"][count2]}). {df["Title"][count2]}. {sponsor}. {url}. Accessed [day] [month] [year].'
        citation_en.append(citation_val_en)
        
        #citation_val_fr = f"Statistique Canada. ({df['dataset_years_0_max_year'][count2]}). {df['Dataset Title (French)'][count2]}. {sponsor_fr}. {url_fr}. Accédé [jour] [mois] [année]."
        #citation_fr.append(citation_val_fr)  
        
        count2 += 1



    # Creation of citation for entries fitting these conditions
    # NOTE THAT THESE MAY EVANTUALLY BECOME REPEATED, AND AS SUCH, MAY REQUIRE SOME TUNING. THIS SHOULD AUTOMATICALLY BE FIXED IF THE ENTRY IS CHANGED FROM 'Single' to 'Repeated'
    elif df['Data Types'][count2][0] == 'Cross-Sectional' and df['Data Types'][count2][1] == 'Single':
        
        # Checking recency of the data entry
        if df["dataset_years_0_max_year"][count2] < 2020:
            citation_val_en = f'Statistics Canada. ({df["dataset_years_0_max_year"][count2]}). {df["Title"][count2]}. {sponsor}. {url}. Accessed [day] [month] [year].'
            #citation_val_fr = f"Statistique Canada. (df["dataset_years_0_max_year"][count2]}). {df['Dataset Title (French)'][count2]}. {sponsor_fr}. {url_fr}. Accédé [jour] [mois] [année]."
        
        else:
            citation_val_en = f'Statistics Canada. (*PUB_YEAR*). {df["Title"][count2]}. {sponsor}. {url}. Accessed [day] [month] [year].'
            #citation_val_fr = f"Statistique Canada. (*ANNÉE_DE_PUBLICATION*). {df['Dataset Title (French)'][count2]}. {sponsor_fr}. {url_fr}. Accédé [jour] [mois] [année]." 
        
        
        citation_en.append(citation_val_en)
        #citation_fr.append(citation_val_fr)
        count2 += 1



    # Creation of citation for entries fitting these conditions
    elif df['Data Types'][count2][0] == 'Cross-Sectional' and df['Data Types'][count2][1] == 'Repeated':
        
        # Checking recency of the data entry
        if df["dataset_years_0_max_year"][count2] < 2020:
            citation_val_en = f'Statistics Canada. ({df["dataset_years_0_max_year"][count2]}). {df["Title"][count2]}. {sponsor}. {url}. Accessed [day] [month] [year].'
            #citation_val_fr = f"Statistique Canada. (df["dataset_years_0_max_year"][count2]}). {df['Dataset Title (French)'][count2]}. {sponsor_fr}. {url_fr}. Accédé [jour] [mois] [année]."
        
        else:
            citation_val_en = f'Statistics Canada. (*PUB_YEAR*). {df["Title"][count2]}. {sponsor}. {url}. Accessed [day] [month] [year].'
            #citation_val_fr = f"Statistique Canada. (*ANNÉE_DE_PUBLICATION*). {df['Dataset Title (French)'][count2]}. {sponsor_fr}. {url_fr}. Accédé [jour] [mois] [année]."            
        
        
        citation_en.append(citation_val_en)
        #citation_fr.append(citation_val_fr)
        count2 += 1    



######################## Clean-up and Output Creation ##########################


del df['is nan']

df['English Citation'] = np.asarray(citation_en)
#df['Citation française'] = np.asarray(citation_fr)


df.to_csv('Testing Citations.csv')
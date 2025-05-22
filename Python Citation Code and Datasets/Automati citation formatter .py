# Automatic Cittion formatter
import os
import json
import pandas as pd
import numpy as np
import datetime


path = "/Users/thierryletendre/Desktop/CRDCN/RAD_Training/Python Citation Code and Datasets"
os.chdir(path)


# Setting up the dataset as a dataframe which will allow for editing
data = pd.read_csv('Dataset-Export-2025-March-12-1920(2).csv')
df = pd.DataFrame(data)
df.rename(columns = {"title.fr": "Dataset Title (French)", 
                     "title.en": "Title", "summary.fr": "Summary French",
                     "summary.en": "Summary", "url": "Permalink",
                     "identifier": "Dataset ID"}, inplace = True)


df['Data Types'] = df['Data Types'].str.split('>')

current_time = datetime.datetime.now()
if current_time.month == 1:
    month_en = 'January'
    month_fr = 'janvier'
elif current_time.month == 2:
    month_en = 'February'
    month_fr = 'février'
elif current_time.month == 3:
    month_en = 'March'
    month_fr = 'mars'
elif current_time.month == 4:
    month_en = 'April'
    month_fr = 'avril'
elif current_time.month == 5:
    month_en = 'May'
    month_fr = 'mai'
elif current_time.month == 6:
    month_en = 'June'
    month_fr = 'juin'
elif current_time.month == 7:
    month_en = 'July'
    month_fr = 'juillet'
elif current_time.month == 8:
    month_en = 'August'
    month_fr = 'août'
elif current_time.month == 9:
    month_en = 'September'
    month_fr = 'septembre'
elif current_time.month == 10:
    month_en = 'October'
    month_fr = 'octobre'
elif current_time.month == 11:
    month_en = 'November'
    month_fr = 'novembre'
elif current_time.month == 12:
    month_en = 'December'
    month_fr = 'décembre'
    
    
citation_en = []
citation_fr = []
    
count2 = 0
while count2 != len(df['Data Types']):
    
    if df['Data Types'][count2][0] == 'Longitudinal' and df['Data Types'][count2][1] == 'Administrative':
        citation_val_en = f'Statistics Canada. (*PUB_YEAR*) {df["Title"][count2]}. Canadian Research Data Center Network. {df["Permalink"][count2]}. Accessed {current_time.day} {month_en} {current_time.year}.'
        citation_val_fr = f'Statistique Canada. (*ANNÉE_DE_PUBLICATION*) {df["Dataset Title (French)"][count2]}. Réseau canadien des Centres de données de recherche. {df["Permalink"][count2]}. Accédé {current_time.day} {month_en} {current_time.year}.'
        citation_en.append(citation_val_en)
        citation_fr.append(citation_val_fr)
        count2 += 1
    
    
    # NOTE THAT THESE MAY EVANTUALLY BECOME REPEATED, AND AS SUCH, 
    # MAY REQUIRE SOME TUNING. THIS SHOULD AUTOMATICALLY BE FIXED IF THE ENTRY
    # IS CHANGED FROM 'Single' to 'Repeated'
    
    elif df['Data Types'][count2][0] == 'Cross-Sectional' and df['Data Types'][count2][1] == 'Single':
        citation_val_en = f'Statistics Canada. (*PUB_YEAR*) {df["Title"][count2]}, {df["dataset_years_0_max_year"][count2]}. Canadian Research Data Center Network. {df["Permalink"][count2]}. Accessed {current_time.day} {month_en} {current_time.year}.'
        citation_val_fr = f'Statistique Canada. (*ANNÉE_DE_PUBLICATION*) {df["Dataset Title (French)"][count2]}, {df["dataset_years_0_max_year"][count2]}. Réseau canadien des Centres de données de recherche. {df["Permalink"][count2]}. Accédé {current_time.day} {month_en} {current_time.year}.'
        citation_en.append(citation_val_en)
        citation_fr.append(citation_val_fr)
        count2 += 1
    
    elif df['Data Types'][count2][0] == 'Longitudinal' and df['Data Types'][count2][1] == 'Integrated':
        citation_val_en = f'Statistics Canada. (*PUB_YEAR*) {df["Title"][count2]}, {df["dataset_years_0_max_year"][count2]}. Canadian Research Data Center Network. {df["Permalink"][count2]}. Accessed {current_time.day} {month_en} {current_time.year}.'
        citation_val_fr = f"Statistique Canada. (*ANNÉE_DE_PUBLICATION*) {df['Dataset Title (French)'][count2]}, {df['dataset_years_0_max_year'][count2]}. Réseau canadien des Centres de données de recherche. {df['Permalink'][count2]}. Accédé {current_time.day} {month_en} {current_time.year}."
        citation_en.append(citation_val_en)
        citation_fr.append(citation_val_fr)
        count2 += 1        
    
    elif df['Data Types'][count2][0] == 'Cross-Sectional' and df['Data Types'][count2][1] == 'Repeated':
        citation_val_en = f'Statistics Canada. (*PUB_YEAR*) {df["Title"][count2]}, *Change this text for chosen Year*. Canadian Research Data Center Network. {df["Permalink"][count2]}. Accessed {current_time.day} {month_en} {current_time.year}.'
        citation_val_fr = f"Statistique Canada. (*ANNÉE_DE_PUBLICATION*) {df['Dataset Title (French)'][count2]}, *Remplacer ce texte par l'année choisie*. Réseau canadien des Centres de données de recherche. {df['Permalink'][count2]}. Accédé {current_time.day} {month_en} {current_time.year}."
        citation_en.append(citation_val_en)
        citation_fr.append(citation_val_fr)
        count2 += 1    
    
    
    elif df['Data Types'][count2][0] == 'Longitudinal' and df['Data Types'][count2][1] == 'Survey':
        citation_val_en = f'Statistics Canada. (*PUB_YEAR*) {df["Title"][count2]}, *Change this text for chosen Year*. Canadian Research Data Center Network. {df["Permalink"][count2]}. Accessed {current_time.day} {month_en} {current_time.year}.'
        citation_val_fr = f"Statistique Canada. (*ANNÉE_DE_PUBLICATION*) {df['Dataset Title (French)'][count2]}, *Remplacer ce texte par l'année choisie*. Réseau canadien des Centres de données de recherche. {df['Permalink'][count2]}. Accédé {current_time.day} {month_en} {current_time.year}."
        citation_en.append(citation_val_en)
        citation_fr.append(citation_val_fr)       
        count2 += 1


df['English Citation'] = np.asarray(citation_en)
df['Citation française'] = np.asarray(citation_fr)


y = df.to_string()


print(y)

df.to_csv('Testing Citations.csv')
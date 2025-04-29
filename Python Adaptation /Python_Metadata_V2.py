# Whatever chat GPT spat out

import os
import pandas as pd
import numpy as np

# Read the CSV file (adjust the file path as needed)
path = "/Users/thierryletendre/Desktop/CRDCN/RAD_Training/Resources/Data"
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

df.fillna('', inplace=True)

df['Subjects'] = df['Subjects'].str.split('>')


count = 0
list_count = 0
merged_list = []

while count != (len(df['Subjects'])):
    
    if list_count == len(df['Subjects'][count]):
        
        for i in df['Subjects'][count]:
            if isinstance(i, list):
                merged_list.extend(i)
            
            else:
                merged_list.append(i)
        
        concatenation = "; ".join(merged_list)
        df['Subjects'][count] = concatenation
        count += 1
        list_count = 0
        merged_list = []
    
    elif '|' in df['Subjects'][count][list_count]:
        
        df['Subjects'][count][list_count] = df['Subjects'][count][list_count].split('|')
        list_count += 1
    
    else:
        list_count += 1 


# Function to split the concatenated subjects into multiple columns
# Split the string in the specified column by semicolon and whitespace
# Determine the maximum number of elements in any row
# Create new columns for each split element

def text_to_columns(data, column):
    split_columns = data[column].str.split(';\\s*')
    max_elements = max(split_columns.apply(len))
    
    for i in range(1, max_elements + 1):
        new_column_name = f"subjen_{i}"
        data[new_column_name] = split_columns.apply(lambda x: x[i-1].strip() if len(x) >= i else None)
    
    return data

# Apply the text_to_columns function
df = text_to_columns(df, "Subjects")






# Read the translations CSV file (adjust the file path as needed)
translations_path = "/Users/thierryletendre/Desktop/CRDCN/RAD_Training/Resources/Data/subject_translations.csv"
subjectsdata = pd.read_csv(translations_path)

# Function to translate subjects
def translate_subject(subject, translations):
    if isinstance(subject, list):
        translated_subjects = [translations.loc[translations['subject_title'].str.lower().str.strip() == s.lower().strip(), 'subject_fr'].values[0] if not translations.loc[translations['subject_title'].str.lower().str.strip() == s.lower().strip(), 'subject_fr'].empty else np.nan for s in subject]
        
        return '; '.join([s for s in translated_subjects if pd.notna(s)])
    
    else:
        subject_to_match = subject.lower().strip()
        translation = translations.loc[translations['subject_title'].str.lower().str.strip() == subject_to_match, 'subject_fr']
        
        if not translation.empty:
            return translation.values[0]
        
        else:
            return np.nan



#Translating column names

# Function to translate columns
# Create the list of columns to translate
# Apply the translations to all the columns
def translate_columns(data, translations):
    subj_cols = [col for col in data.columns if col.startswith("subjen_")]
    
    for column in subj_cols:
        data[f"{column}_fr"] = data[column].apply(lambda x: 
                                                  translate_subject(x, translations))
        
        return data

# Apply the translate_columns function
df = translate_columns(df, subjectsdata)

# Combine translated subjects into a single column
fr_cols = [col for col in df.columns if col.endswith("_fr")]
df['subjects_fr'] = df[fr_cols].apply(lambda row: '; '.join(row.dropna()), axis=1)


# Create keywords from various fields in the data
df['keywords.en'] = ""
df['keywords.fr'] = ""

df['keywords.en'] = df.apply(lambda row: 
                             list(set([row['Acronym']] + 
                                      [row[f"subjen_{i}"] for i in range(1, 14) 
                                       if pd.notna(row[f"subjen_{i}"])])), axis=1)


df['keywords.fr'] = df.apply(lambda row: 
                             list(set(["CDR"] + 
                                      [row['Acronym French']] + 
                                      [row[f"subjen_{i}_fr"] for i in range(1, 14) 
                                       if pd.notna(row[f"subjen_{i}_fr"])])), axis=1)




"""

# Add constant values to specific columns
import_df['creators.ROR'] = "https://ror.org/05k71ja87"
import_df['creators.en'] = "Statistics Canada"
import_df['creators.fr'] = "Statistique Canada"
import_df['contributors.ROR'] = "https://ror.org/0042y9w49"
import_df['contributors.en'] = "Canadian Research Data Centre Network"
import_df['contributors.fr'] = "Réseau canadien de centre de données de recherche"
import_df['publisher.ROR'] = "https://ror.org/05k71ja87"
import_df['publisher.en'] = "Statistics Canada"
import_df['publisher.fr'] = "Statistique Canada"
import_df['rights.en'] = "Access to data is restricted to researchers with approved projects working on RDC (Research Data Centre) infrastructure. For instructions on how to apply, please visit: https://crdcn.ca/publications-data/access-crdcn-data/. Output released from the RDC is subject to the Statistics Canada Open License available at [http://www.statcan.gc.ca/eng/reference/licence-eng]. The raw data may not be copied or shared."
import_df['rights.fr'] = "L'accès aux données est réservé aux chercheurs dont les projets sont approuvés et qui travaillent avec l'infrastructure du CDR (Centre de données de recherche). Pour obtenir des instructions sur la manière de soumettre une proposition, veuillez consulter le site : https://crdcn.ca/publications-data/acceder-aux-donnees-des-cdr/?lang=fr. Les résultats provenant du CDR sont sous la licence ouverte de Statistique Canada disponible à l'adresse suivante : [https://www.statcan.gc.ca/fr/reference/licence]. Les données brutes ne peuvent être ni copiées ni partagées."
import_df['series.en'] = "RDC Masterfiles"
import_df['series.fr'] = "Fichiers-maîtres du CDR"
import_df['access'] = "Restricted"

# Drop unnecessary columns
export_df = import_df.drop(columns=['splitsubs', 'Subjects'])
export_df = export_df.drop(columns=[col for col in export_df.columns if col.endswith("_fr") and col.startswith("subjen_")])

# Define the mapping and convert to JSON
def datacite_conversion(data):
    datacite = {
        "data": {
            "attributes": {
                "titles": [
                    {"title": data['title.en'], "lang": "en"},
                    {"title": data['title.fr'], "lang": "fr"}
                    ],
                "creators": [
                    {"creator": data['creators.en'], "lang": "en", "ROR": data['creators.ROR']},
                    {"creator": data['creators.fr'], "lang": "fr", "ROR": data['creators.ROR']}
                    ],
                "contributors": [
                    {"contributor": data['contributors.en'], "lang": "en", "ROR": data['contributors.ROR']},
                    {"contributor": data['contributors.fr'], "lang": "fr", "ROR": data['contributors.ROR']}
                    ],
                "publisher": [
                    {"publisher": data['publisher.en'], "lang": "en", "ROR": data['publisher.ROR']},
                    {"publisher": data['publisher.fr'], "lang": "fr", "ROR": data['publisher.ROR']}
                    ],
                "keywords": [
                    {"keywords": data['keywords.en'], "lang": "en"},
                    {"keywords": data['keywords.fr'], "lang": "fr"}
                    ],
                "rights": [
                    {"rights": data['rights.en'], "lang": "en"},
                    {"rights": data['rights.fr'], "lang": "fr"}
                    ],
                "summary": [
                    {"summary": data['summary.en'], "lang": "en"},
                    {"summary": data['summary.fr'], "lang": "fr"}
                    ],
                "series": [
                    {"series": data['series.en'], "lang": "en"},
                    {"series": data['series.fr'], "lang": "fr"}
                    ],
                "url": data['url'],
                "identifier": data['identifier'],
                "access": data['access'],
                "date": data['Date']
            }
        }
    }
    return datacite

json_ex = [datacite_conversion(export_df.iloc[i]) for i in range(len(export_df))]

json_output = json.dumps(json_ex, indent=4, ensure_ascii=False)

# Write the JSON output to a file

output_path = "F:/CRDCN data/lunaris_transform/Data/json_dictionary"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(json_output)

"""
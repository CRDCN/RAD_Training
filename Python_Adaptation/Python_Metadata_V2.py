# Restricted Metadata JSON file creator
# This code was created with Macintosh


# Importing modules necessary in the process of converting the CSV file to JSON
import os
import json
import pandas as pd
import numpy as np



####################### Loading and Creating Dataframe #########################


# Read the CSV file (adjust the file path as needed)
path = "/Your/Path/Here"
os.chdir(path)


# Setting up the dataset as a dataframe which will allow for editing
data = pd.read_csv('2025_03_27_WPDATA.csv')
df = pd.DataFrame(data)


#Renaming column names in the newly created dataframe
df.rename(columns = {"title.fr": "Dataset Title (French)", 
                     "title.en": "Title", "summary.fr": "Summary French",
                     "summary.en": "Summary", "url": "Permalink",
                     "identifier": "Dataset ID"}, inplace = True)



####################### Removing Hierarchal Symbols ############################

"""
Note: Subject terms are divided by ">" and "|" symbols. 
      These represent the hierarchal nature of these subjects. 
      The following code is used to remove this hierarchal symbology.
"""

# Replacing NaN (Null) values with empty strings to facilitate editing
df.fillna('', inplace=True)

# Seperating strings at every ">" 
df['Subjects'] = df['Subjects'].str.split('>')


"""
Note: The use of the above line prevents using the same approach for other 
      symbols such as "|". To circumvent this issue, a while loop (see below) 
      was used to parse through the now seperate strings, to then run
      .split('|').

"""

# Creating necessary while loop talies and empty list
count = 0
list_count = 0
merged_list = []


# Code keeps going for as long as it hasn't parsed through the entire list of subjects
while count != (len(df['Subjects'])):
    
    # If list_count is equal to the length of the indexed list
    if list_count == len(df['Subjects'][count]):
        
        # For all strings in the indexed list
        for i in df['Subjects'][count]:
            
            # If the indexed list itself contains a list (of strings), add all of them to "merged_list"
            if isinstance(i, list):
                merged_list.extend(i)
            
            # otherwise, add the singular string to the merged list.
            else:
                merged_list.append(i)
        
        # take all strings in "merged_list", join them with ; in one string, update dataframe value
        concatenation = "; ".join(merged_list)
        df['Subjects'][count] = concatenation
        
        # Updating counters to go on to the next indexed list, refresh merged_list
        count += 1
        list_count = 0
        merged_list = []
    
    # If a string contains |, split them there into their own strings
    elif '|' in df['Subjects'][count][list_count]:
        
        df['Subjects'][count][list_count] = df['Subjects'][count][list_count].split('|')
        list_count += 1
    
    else:
        list_count += 1 



################## Creating Individual Columns for Subjects ####################


# Function to split the concatenated subjects into multiple columns
def text_to_columns(data, column):
    
    # Split the string in the specified column by semicolon and whitespace
    split_columns = data[column].str.split(';\\s*')
    max_elements = max(split_columns.apply(len))
    
    # Determine the maximum number of elements in any row
    for i in range(1, max_elements + 1):
        
        # Create new columns for each split element
        new_column_name = f"subjen_{i}"
        data[new_column_name] = split_columns.apply(lambda x: x[i-1].strip() if len(x) >= i else "")
    
    return data

# Apply the text_to_columns function
df = text_to_columns(df, "Subjects")



########################## Loading Translation File ############################


# Read the translations CSV file (adjust the file path as needed)
translations_path = "/path/to/translation/file"
subjectsdata = pd.read_csv(translations_path)



############################ Translation Functions #############################


# Function to translate subjects
def translate_subject(subject, translations):
    if isinstance(subject, list):
        translated_subjects = [translations.loc[translations['subject_title'].str.lower().str.strip() == s.lower().strip(), 'subject_fr'].values[0] 
                               if not translations.loc[translations['subject_title'].str.lower().str.strip() == s.lower().strip(), 'subject_fr'].empty 
                               else np.nan for s in subject]
        
        return '; '.join([s for s in translated_subjects if pd.notna(s)])
    
    else:
        subject_to_match = subject.lower().strip()
        translation = translations.loc[translations['subject_title'].str.lower().str.strip() == subject_to_match, 'subject_fr']
        
        if not translation.empty:
            return translation.values[0]
        
        else:
            return np.nan



# Function to translate columns -- This function calls the one above.
def translate_columns(data, translations):
    
    # Create the list of columns to translate
    global subj_cols
    subj_cols = [col for col in data.columns if col.startswith("subjen_")]


    # Apply the translations to all the columns
    for column in subj_cols:
        data[f"{column}_fr"] = data[column].apply(lambda x: 
                                                  translate_subject(x, translations))
        
    return data



########################### Translation and Clean-up ###########################


# Apply the translate_columns function
df = translate_columns(df, subjectsdata)


# Replacing empty strings with NaN values to facilitate concatenation
df = df.replace('', np.nan)
df['subjects_en'] = df[subj_cols].apply(lambda row: '; '.join(row.dropna()), axis=1)


# Combine translated subjects into a single column
fr_cols = [col for col in df.columns if col.endswith("_fr")]
df['subjects_fr'] = df[fr_cols].apply(lambda row: '; '.join(row.dropna()), axis=1)



##################### Keyword Creation & Constant Values #######################


# Create keywords from various fields in the data
df['keywords.en'] = ""
df['keywords.fr'] = ""

df['keywords.en'] = df.apply(lambda row: 
                             list(set([row['Acronym']] + 
                                      [row[f"subjen_{i}"] for i in range(1, 14) 
                                       if pd.notna(row[f"subjen_{i}"])])), axis=1)


# problem here seems to be specifically the _fr

df['keywords.fr'] = df.apply(lambda row: 
                             list(set(["CDR"] + 
                                      [row['Acronym French']] + 
                                      [row[f"subjen_{i}_fr"] for i in range(1, 14) 
                                       if pd.notna(row[f"subjen_{i}_fr"])])), axis=1)


# Add constant values to specific columns
df['creators.ROR'] = "https://ror.org/05k71ja87"
df['creators.en'] = "Statistics Canada"
df['creators.fr'] = "Statistique Canada"
df['contributors.ROR'] = "https://ror.org/0042y9w49"
df['contributors.en'] = "Canadian Research Data Centre Network"
df['contributors.fr'] = "Réseau canadien de centre de données de recherche"
df['publisher.ROR'] = "https://ror.org/05k71ja87"
df['publisher.en'] = "Statistics Canada"
df['publisher.fr'] = "Statistique Canada"
df['rights.en'] = "Access to data is restricted to researchers with approved projects working on RDC (Research Data Centre) infrastructure. For instructions on how to apply, please visit: https://crdcn.ca/publications-data/access-crdcn-data/. Output released from the RDC is subject to the Statistics Canada Open License available at [http://www.statcan.gc.ca/eng/reference/licence-eng]. The raw data may not be copied or shared."
df['rights.fr'] = "L'accès aux données est réservé aux chercheurs dont les projets sont approuvés et qui travaillent avec l'infrastructure du CDR (Centre de données de recherche). Pour obtenir des instructions sur la manière de soumettre une proposition, veuillez consulter le site : https://crdcn.ca/publications-data/acceder-aux-donnees-des-cdr/?lang=fr. Les résultats provenant du CDR sont sous la licence ouverte de Statistique Canada disponible à l'adresse suivante : [https://www.statcan.gc.ca/fr/reference/licence]. Les données brutes ne peuvent être ni copiées ni partagées."
df['series.en'] = "RDC Masterfiles"
df['series.fr'] = "Fichiers-maîtres du CDR"
df['access'] = "Restricted"



###################### File Clean-up & Formatting Function #####################


# Drop unnecessary columns (these are substituted by the 'keyword' columns)
export_df = df.drop(columns = ['Subjects'])
export_df = export_df.drop(columns = [col for col in export_df.columns if col.startswith("subjen_")])


# Define the mapping and convert to JSON
def datacite_conversion(data):
    datacite = {
        "data": {
            "attributes": {
                "titles": [
                    {"title": data['Title'], "lang": "en"},
                    {"title": data['Dataset Title (French)'], "lang": "fr"}
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
                    {"summary": data['Summary'], "lang": "en"},
                    {"summary": data['Summary French'], "lang": "fr"}
                    ],
                "series": [
                    {"series": data['series.en'], "lang": "en"},
                    {"series": data['series.fr'], "lang": "fr"}
                    ],
                "url": data['Permalink'],
                "identifier": data['Dataset ID'],
                "access": data['access'],
                "date": data['Date']
            }
        }
    }
    return datacite



############################## JSON File Creation ##############################


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        return super(NpEncoder, self).default(obj)


json_ex = [datacite_conversion(export_df.iloc[i]) for i in range(len(export_df))]
json_output = json.dumps(json_ex, indent = 2, ensure_ascii=False, cls = NpEncoder)


output_path = "/your/output/file/directory/here"

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(json_output)


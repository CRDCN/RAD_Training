# Whatever chat GPT spat out


import pandas as pd
import numpy as np

# Read the CSV file (adjust the file path as needed)
file_path = "/Users/thierryletendre/Desktop/CRDCN/RAD_Training/Resources/Data/2025_03_27_WPDATA.csv"
import_df = pd.read_csv(file_path)

# Rename columns
import_df = import_df.rename(columns = {"title.fr": "Dataset Title (French)", 
                     "title.en": "Title", "summary.fr": "Summary French",
                     "summary.en": "Summary", "url": "Permalink",
                     "identifier": "Dataset ID"
                     })

# Split the 'Subjects' column by '>'
import_df['splitsubs'] = import_df['Subjects'].str.split('>')

# Trim whitespace from each subject
#import_df['splitsubs'] = import_df['splitsubs'].apply(lambda x: [subject.strip() for subject in x])

# Function to clean the subjects by removing everything after a pipe character
def cls(subjectlist):
    cleaned = [subject.split('|')[0] for subject in subjectlist]
    return cleaned

# Function to concatenate the cleaned subjects into a single string separated by semicolons
def cct(vec):
    return '; '.join(vec)

# Apply the cleaning function
import_df['splitsubs'] = import_df['splitsubs'].apply(cls)

# Apply the concatenation function
import_df['subjects_en'] = import_df['splitsubs'].apply(cct)

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
import_df = text_to_columns(import_df, "subjects_en")

# Read the translations CSV file (adjust the file path as needed)
translations_path = "F:/CRDCN data/lunaris_transform/Data/subject_translations.csv"
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

# Function to translate columns
# Create the list of columns to translate
# Apply the translations to all the columns
def translate_columns(data, translations):
    subj_cols = [col for col in data.columns if col.startswith("subjen_")]
    
    for column in subj_cols:
        data[f"{column}_fr"] = data[column].apply(lambda x: translate_subject(x, translations))
        
        return data

# Apply the translate_columns function
import_df = translate_columns(import_df, subjectsdata)

# Combine translated subjects into a single column
fr_cols = [col for col in import_df.columns if col.endswith("_fr")]
import_df['subjects_fr'] = import_df[fr_cols].apply(lambda row: '; '.join(row.dropna()), axis=1)

# Create keywords from various fields in the data
import_df['keywords.en'] = ""
import_df['keywords.fr'] = ""

import_df['keywords.en'] = import_df.apply(lambda row: list(set([row['Acronym']] + [row[f"subjen_{i}"] for i in range(1, 14) if pd.notna(row[f"subjen_{i}"])])), axis=1)
import_df['keywords.fr'] = import_df.apply(lambda row: list(set(["CDR"] + [row['Acronym.French']] + [row[f"subjen_{i}_fr"] for i in range(1, 14) if pd.notna(row[f"subjen_{i}_fr"])])), axis=1)








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

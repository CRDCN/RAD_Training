##This file creates the JSON output required by the Lunaris team to read in and index the CRDCN dataset database. The output of this file needs to be uploaded to a persistent URL to be harvested by the Lunaris system.

##read in the data, with the foreign library, many different types of data can be read in. Our export type here is a .csv (comma separated value). A very common format for text-data
library(foreign)
setwd("S:/CRDCN/RAD_Training/") #office
#setwd("C:/Users/gibso/Documents/CRDCN/RAD_Training)
#alternate
import<-read.csv("Resources/Data/2025_05_01_WPDATA.csv")
##This is where we begin to transform our output file to match the Schema provided by Lunaris
library(dplyr)
library(tidyr)
library(purrr)
##First we rename the columns
import<- import %>% rename(title.fr=Dataset.Title..French., title.en=Title, summary.fr=Summary.French, summary.en=Summary, url=Permalink, identifier=Dataset.ID)

##Next we apply any transformations we need to make the output make sense. Our subjects are separated by ">" and organized in a hierarchical way that we need to suppress
import_subs<- strsplit(import$Subjects,">")
import$splitsubs<- import_subs
import$splitsubs<-lapply(import_subs, trimws)
cls<- function(subjectlist){
  cleaned<- gsub("\\|.*","", subjectlist)
  return(cleaned)
}
cct<- function(vec){
  return(paste(vec,collapse="; "))
}

import$splitsubs<-lapply(import$splitsubs, cls)
import$subjects_en<-sapply(import$splitsubs,cct)

##Now I need to re-add multilanguage versions of the subjects
text_to_columns <- function(data, column) {
  # Split the string in the specified column by semicolon and whitespace
  split_columns <- strsplit(as.character(data[[column]]), ";\\s*")
  
  # Determine the maximum number of elements in any row
  max_elements <- max(sapply(split_columns, length))
  max_length<<- max_elements
  
  # Create new columns for each split element
  for (i in 1:max_elements) {
    new_column_name <- paste0("subjen_", i)
    data[[new_column_name]] <- sapply(split_columns, function(x) if(length(x) >= i) trimws(x[i]) else NA)
  }
  
  return(data)
}

import<-text_to_columns(import,"subjects_en")

## insheet the dataframe of translations
subjectsdata<-read.csv("Resources/Data/subject_translations.csv")
translate_subject <- function(subject, translations) {
  if (length(subject) > 1) {
    translated_subjects <- map_chr(subject, ~ {
      subject_to_match <- trimws(tolower(.x))
      translation <- translations$subject_fr[tolower(trimws(translations$subject_title)) == subject_to_match]
      if (length(translation) > 0) {
        return(translation[1]) # Take the first match if multiple exist (shouldn't happen with unique titles)
      } else {
        return(NA_character_)
      }
    })
    return(paste(na.omit(translated_subjects), collapse = ";"))
  } else {
    subject_to_match <- trimws(tolower(subject))
    translation <- translations$subject_fr[tolower(trimws(translations$subject_title)) == subject_to_match]
    if (length(translation) > 0) {
      return(translation[1])
    } else {
      return(NA_character_)
    }
  }
}

translate_columns <- function(data, translations) {
  ##create the list of columns to translate
  subj_cols <- grep("^subjen_", colnames(data), value=TRUE)
  ##now apply the translations to all the columns
  for (column in subj_cols) {
    data[[paste0(column, "_fr")]] <- map(data[[column]], ~ translate_subject(.x, translations))
  }
  return(data)
}

import <- translate_columns(import, subjectsdata)

fr_cols <- grep("_[0-9]+_fr$", colnames(import), value = TRUE)
import <- import %>%
  rowwise() %>%
  mutate(subjects_fr = paste(na.omit(unlist(c_across(all_of(fr_cols)))), collapse = ";")) %>%
  ungroup()

##Create keywords from various fields in the data
import$keywords.en<-""
import$keywords.fr<-""

import <- import %>%
  rowwise() %>%
  mutate(
      keywords.en = list({
      acronym <- Acronym
      subjen_cols_en_base <- paste0("subjen_", 1:13)
      subjects_en <- character(0)
      for (col in subjen_cols_en_base) {
        if (col %in% names(.)) {
          value <- .[[col]][1]
          if (!is.na(value)) {
            subjects_en <- c(subjects_en, value)
          }
        }
      }
      keywords_list <- c()
      if (!is.na(acronym) && trimws(acronym) != "") {
        keywords_list <- c(keywords_list, trimws(acronym))
      }
      keywords_list <- c(keywords_list, trimws(subjects_en))
      if (!is.na(acronym) && trimws(acronym) != "") {
        keywords_list <- c(keywords_list, trimws(acronym))
      }
      unique(keywords_list)
      }),
    keywords.fr = list({
      acronym_fr <- Acronym.French
      subjen_cols_fr_base <- paste0("subjen_", 1:13, "_fr")
      subjects_fr <- character(0)
      for (col in subjen_cols_fr_base) {
        if (col %in% names(.)) {
          value <- .[[col]][1]
          if (!is.na(value)) {
            subjects_fr <- c(subjects_fr, value)
          }
        }
      }
      keywords_list_fr <- c("CDR")
      if (!is.na(acronym_fr) && trimws(acronym_fr) != "") {
        keywords_list_fr <- c(keywords_list_fr, trimws(acronym_fr))
      }
      keywords_list_fr <- c(keywords_list_fr, trimws(na.omit(subjects_fr)))
      if (!is.na(acronym_fr) && trimws(acronym_fr) != "") {
        keywords_list_fr <- c(keywords_list_fr, trimws(acronym_fr))
      }
      unique(keywords_list_fr)
      })
  ) %>%
  ungroup()

##Some of my columns will have the same value for everything and don't appear in my database
import$creators.ROR<-"https://ror.org/05k71ja87"
import$creators.en<-"Statistics Canada"
import$creators.fr<-"Statistique Canada"
import$contributors.ROR<-"https://ror.org/0042y9w49"
import$contributors.en<-"Canadian Research Data Centre Network"
import$contributors.fr<-"Réseau canadien de centre de données de recherche"
import$publisher.ROR<-"https://ror.org/05k71ja87"
import$publisher.en<-"Statistics Canada"
import$publisher.fr<-"Statistique Canada"
import$rights.en<- "Access to data is restricted to researchers with approved projects working on RDC (Research Data Centre) infrastructure. For instructions on how to apply, please visit: https://crdcn.ca/publications-data/access-crdcn-data/. Output released from the RDC is subject to the Statistics Canada Open License available at [http://www.statcan.gc.ca/eng/reference/licence-eng]. The raw data may not be copied or shared."
import$rights.fr<- "L'accès aux données est réservé aux chercheurs dont les projets sont approuvés et qui travaillent avec l'infrastructure du CDR (Centre de données de recherche). Pour obtenir des instructions sur la manière de soumettre une proposition, veuillez consulter le site : https://crdcn.ca/publications-data/acceder-aux-donnees-des-cdr/?lang=fr. Les résultats provenant du CDR sont sous la licence ouverte de Statistique Canada disponible à l'adresse suivante : [https://www.statcan.gc.ca/fr/reference/licence]. Les données brutes ne peuvent être ni copiées ni partagées."
import$series.en<- "RDC Masterfiles"
import$series.fr<- "Fichiers-maîtres du CDR"
import$access<- "Restricted"

##Now we drop all the columns that we don't need to be at our final state before we output the result.

export<- import %>% select(-splitsubs, -Subjects)
export<- export %>% select(-matches("_[0-9]+_fr$"))

##Begin the export, start by defining the mapping (you might need to change and add fields). If you don't have multilingual information, you can simplify this greatly.
library(jsonlite)
datacite_conversion <- function(data) {
  datacite <- list( ##open main list
    data = list( ##open data row list
      attributes = list( ##open attribute list
        titles = list(
          list(title = data$title.en, lang = "en"),
          list(title = data$title.fr, lang = "fr")
        ),
        creators = list(
          list(creator = data$creators.en, lang = "en", ROR=data$creators.ROR),
          list(creator = data$creators.fr, lang = "fr", ROR=data$creators.ROR)
        ),
        contributors = list(
          list(contributor = data$contributors.en, lang = "en", ROR = data$contributors.ROR),
          list(contributor = data$contributors.fr, lang = "fr", ROR = data$contributors.ROR)
        ),
        publisher = list(
          list(publisher = data$publisher.en, lang = "en",ROR = data$publisher.ROR),
          list(publisher = data$publisher.fr, lang = "fr",ROR = data$publisher.ROR)
        ),
        keywords = c(
          map(data$subjects_en[[1]], ~list(keyword = .x, lang = "en")),
          map(data$subjects_fr[[1]], ~list(keyword = .x, lang = "fr"))
        ),
        rights = list(
          list(rights = data$rights.en, lang = "en"),
          list(rights = data$rights.fr, lang = "fr")
        ),
        summary = list(
          list(summary = data$summary.en, lang = "en"),
          list(summary = data$summary.fr, lang = "fr")
        ),
        series = list(
          list(series = data$series.en, lang="en"),
          list(series = data$series.fr, lang="fr")
        ),
        url = data$url,
        identifier = data$identifier,
        access = data$access,
        date = data$Date
      ) # Closing attributes list
    ) # Closing data row list
  ) # Closing main list
}

json_ex<-lapply(1:nrow(export), function(i) datacite_conversion(export[i,]))

json_output<-toJSON(json_ex, pretty=TRUE, auto_unbox= TRUE)

write(json_output, file="Resources/Data/json_dictionary")



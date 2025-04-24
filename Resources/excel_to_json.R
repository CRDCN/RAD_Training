## This file converts the data from an excel spreadsheet into JSON suitable for passing to an indexing service
## Before you begin, you should:
## 1. Make sure that your excel file is organized row-wise. I.e. there is one row in your spreadsheet for each data item you want to create an entry for.
## 2. Make sure the column headers match what is being requested in terms of field names.
## 3. Ensure that your excel file contains all the information in the way you want to present it. If you have keywords for example, they should be separated by something standard, ex. pollution; pm2.5; air quality; urban
## 4. Make sure your excel file does not contain any formulas or other special-to-excel transformations, this code will import what it sees.

## To begin, please enter the file-path for the folder your data is in

filepath<-"C:/Path/to/your/file"

## Now provide the name of the file and the extension, note this might be an .xlsx or .xls file depending on the version of excel it was created/saved with

filename<-"yourfilename.xlsx"


#This script renames folders created for contractors (title using the PROD_ID (ASIN))
#with the actual offer ID (found in the BRAND_ID column of the gear PO, csv)

import os
import pandas as pd
import difflib

#prompt user to provide cvs file.
gear_po = raw_input("Enter the csv file you want to use. Must be written as filename.csv: ")

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

name = gear_po
path = '/Users'

your_path = find(name, path)

print your_path

######################################################################################
#assign your csv dataframe to the variable rename_df
rename_df = pd.read_csv(your_path)

#select out brand id, produd id, and create folder columns
rename_folder_df = rename_df.loc[:,['BRAND_ID','PRODUCT_ID (ASIN)', 'CREATE_FOLDER']] 

#select just the create_folder column
rename_create_folder = rename_folder_df.ix[:,2]; 

#remove the rows that don't require a folder (they are empty/filled with NaN)
#by removing all the NaNs in the CREATE_FOLDER column
for i in rename_create_folder:
    rename_prodid_list = rename_folder_df.dropna(subset = ['CREATE_FOLDER'])

######################################################################################    
#create a tuple of the dataframe 
rename_subset = rename_prodid_list[['BRAND_ID', 'PRODUCT_ID (ASIN)']]
rename_tuples = [tuple(x) for x in rename_subset.values]

#Rename the directory B to directory A. os.rename(B, A)

for i in rename_tuples:
    #format A so that it drops the trailing zeros
    try:
        A = format(i[0], '.0f')
    except:
        A = str(i[0])
    try:
        B = format(i[1], '.0f')
    except:
        B = str(i[1])
    
#go up one folder by removing the length of the csv name 
#(n_dir is new directory, but dont want to reuse new_dir)
    n_dir = your_path[0:len(your_path)-len(gear_po)]
    
#The below tries to match files to avoid dealing with spaces or trailing  
    try:
        #os.rename(n_dir + A, n_dir + B)
        os.rename(n_dir + B, n_dir + A)
    except:
        files = os.listdir(n_dir) #look what's in your directory
        if len(difflib.get_close_matches(B, files,1)) > 0:
#see if you have close match (> 0 means there is at least one match)
#difflib gives you a list of matches, you want to grab the first of the ones it finds
            C = difflib.get_close_matches(str(B), files,1)[0] 
#C = the closest match to the file you want [0] means look at the first term}
            os.rename(n_dir + C, n_dir + A) #rename using closest match instead of B
        else:
            print 'HELP! no file or close match'
            pass

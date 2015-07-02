#### Create folders from a gear PO csv where the folder titles 
#### are listed in the PROD_ID (ASIN) column, use the CREATE_FOLDER column
#### to specify which row you want to use to name your newly created folder 

#import the package you need to start
import pandas as pd
import os

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

#prompt user to provide cvs file.
name = raw_input("Enter the csv file you want to use. Must be written as filename.csv: ")
path = '/Users'

csv_path = find(name, path)

###############################################################################
#read in the csv file and call it gear_op_df
gear_op_df = pd.read_csv(csv_path)


#select the columns in csv_path labeled BRAND_ID, CREATE_FOLDER, Color Code, ITEM COLOR
#CREATE_FOLDER is the column with 1s that indicate when a (has to added by hand)
#call it prodid_folder_df (which means the product ids that should be assigned folders)
prodid_folder_df = gear_op_df.loc[:,['PRODUCT_ID (ASIN)', 'CREATE_FOLDER', 'Color Code', 'ITEM COLOR']]


#assign a variable prodid to PRODUCT_ID column, create_folder to CREATE_FOLDER column, 
#color_code to the Color Code column, and Item color column 

prodid = prodid_folder_df.ix[:,0];
create_folder = prodid_folder_df.ix[:,1]; 
color_code = prodid_folder_df.ix[:,2];
item_color = prodid_folder_df.ix[:,3]; 

#removes rows that have NA or no value in the CREATE_FOLDER COLUMN
#dropna, drops nas in the column you specify by name
prodid_list = prodid_folder_df.dropna(subset = ['CREATE_FOLDER']) 

##############################################################################

#create folders from the product_id list
#using the make folder function os.mkdir()
#you should now see the folders on your desktop
folder_list = prodid_list.ix[:,0];

##create a method to index you color code column
color_code_na = prodid_list.ix[:,2] #select the color code column 
color_codes_na_strings = [] #initialize an empty column
for index in color_code_na.keys(): #re-index the keys to that they go 0 to n
    #color_codes_na_strings.append( str(int(color_code_na[index]))) #YOU NEED A LINE THAT CHECKS IF THIS IS AN INT OR STR
    color_codes_na_strings.append( str((color_code_na[index]))) #ASSUME INDEX IS A STRING

##create a method to index you item color column
##Item color has backslashes in it will THIS BE A PROBLEM?
item_color_na = prodid_list.ix[:,3] #select the item color column (na doesn't mean anything)
item_color_na_strings = [] #initialize an empty column
for index in item_color_na.keys(): #re-index the keys to that they go 0 to n
    item_color_na_strings.append( str((item_color_na[index]))) #ASSUME INDEX IS A STRING (I think this is a fair bet)


new_dir = csv_path[0:len(csv_path)-len(name)]
new_name = name[0:len(name)-4] #remove .csv from name   
os.mkdir(new_dir + new_name)
##############################################################################
for index, i in enumerate(folder_list): #enumerate allows you to keep count of your index while you loop
    #i_nofloat = format(i, '.0f') ###updated this for PO where the product ID is an object (combination of numbers and letters)
                                  ## rather than numerics (floats) or a string/ need a check before you convert to string          
    #os.mkdir(new_dir + i_nofloat) ###commented this out to do code below

    try:
        str(i) == i
            #os.mkdir(new_dir + new_name + '/' + i_nofloat)
        try:
            os.mkdir(new_dir + new_name + '/' + i)
        except:
            (os.mkdir(new_dir + new_name + '/' + i + '_' + color_codes_na_strings[index]),
             os.mkdir(new_dir + new_name + '/' + i + '_' + item_codes_na_strings[index]))
    except:
        int(i) == i
        i_nofloat = format(i, '.0f')
        try:
            os.mkdir(new_dir + new_name + '/' + i_nofloat)
        except:
            (os.mkdir(new_dir + new_name + '/' + i_nofloat + '_' + color_codes_na_strings[index]),
             os.mkdir(new_dir + new_name + '/' + i_nofloat + '_' + item_codes_na_strings[index]))
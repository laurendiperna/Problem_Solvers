#Create a script that executes a line of code for the terminal in a python script
#This code uses webkit2png and is meant to provide a screenshot of 
#multiple urls, save each one with a specific
#name, and store them in a given file

import pandas as pd
import subprocess #this module has a definition 'call' that lets you execute
				  #command line language from a script

#NOTE MAKE SURE TO ENTER IN 'directory_path' and 'excel_path' below, you make have to manually write
#out the path for the directory_path variable in the def screenshot_urls below

def screenshot_urls(url, filename):
	"""
	screenshot_urls takes two arguments url (a string of your website) and filename
	(the name you want your file to be saved with). It then calls the package webkit2png
	which takes a 'full page' (-F) screenshot and saves it to the 'directory '-D'
	that is specifically stated, and saves it with the name '[filename]-full.png
	"""
	subprocess.call(["webkit2png", "-F", "-D", directory_path,
	 "-o", filename, url])
	 
#assign your csv dataframe to the variable screenshot_df
#excel_path points to the location of the saved csv where you'll pull 'url' and 'filename'
#ENTER THE PATH TO YOUR FILE WITH YOUR URL AND FILE NAME HERE
excel_path = ""
#ENTER THE PATH TO THE DIRECTORY WHERE YOU WANT ALL YOUR SCREENSHOT FILES STORED
directory_path = ""
screenshot_df = pd.read_csv(excel_path)

#create a tuple of the dataframe (You can replace 'CampaignName' and 'Archive URL' with the column titles in your csv file)
subset = screenshot_df[['CampaignName', 'Archive URL']]
tuples = [tuple(x) for x in subset.values]

#Loop over the tuples that is structured (url, filename)
#call your definition, with the variables assigned above
for filename, url in tuples:
	screenshot_urls(url, filename)
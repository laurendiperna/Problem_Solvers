### This script crops and saves images in a specified folder
### To execute this file, assign the path name to the specified folder to the 'directory' variable and run in python
##########################################################################################
##########################################################################################
#First import the packages and modules you need to run this code:
import os
import sys
import json
from PIL import Image

from autocrop_input import crop_ratio, path

#Manually change the ratio and path name in the file autocrop_input.py

ratio = crop_ratio
directory = path

# Look through the list of files in your directory (excluding hidden files)
# Replace all spaces in file names with underscores
for filename in os.listdir(directory):
    
    if not filename.startswith('.'):
        newfilename = filename.replace(' ', '_')
        os.rename(directory +'/'+ filename, directory +'/'+ newfilename)

##########################################################################################
# This definition ignores all hidden files
# it takes one variable that contains the full path to a directory
# it initializes an empty folder where all the found visible folders will be stored
# it looks for files that start with '.' and only returns files that don't start with '.'
# note: you may run into trouble with dropbox folders that a 'Icon/r' hidden file

def no_hidden_files(folder_name):
    visible_file = []
    visible_file = filter( lambda f: not f.startswith('.'), folder_name)
    return visible_file
##########################################################################################
# Create a list of activity folders that includes path names
# remove all the hidden files with the hidden files definition
Activities_folder_w_hidden_files = os.listdir(directory)
Activities_folder = no_hidden_files(Activities_folder_w_hidden_files)

##########################################################################################
# This definition checks if an item is in a list you provide
# In this code its used to see if an image has already been cropped by checking a
# dictionary that stores the original image and cropped image as a key/value pair

def is_in_list(item, list_name):
    if item in list_name:
        return item

##########################################################################################
# Check if your dictionary already exists, if it doesn't,
# create an empty dictionary called 'activity_folder_dict'
try:
    with open(directory + '/activity_folder_dict.json', 'r') as fp2:
        activity_folder_dict = json.load(fp2)
except:
    activity_folder_dict = {}

# Make your cropped folder for each activity folder
for activity_folder in Activities_folder:
    
    # Create the folder where the cropped images go for each activity folder:
    # Check if the folder already exists, create if it doesn't
    cropped_folder = directory +'/' + activity_folder + '/' + activity_folder.rstrip('\n') + '_cropped'
    
    if not os.path.exists(cropped_folder):
        os.makedirs(cropped_folder)

    # Added .rstrip('\n') to second activity_folder so that there are no new lines
    # Determine how many files are in each folder, use that number to start your counter
    # the first time a cropped folder is created count = 0, because the folder is empty
    cropped_folder_path = directory + '/' + activity_folder + '/' + activity_folder.rstrip('\n') + '_cropped'
    count = len(no_hidden_files(os.listdir(cropped_folder_path))) #count the number of non-hidden files in your cropped folder

    # Store the path name to the images folder:
    image_folder_path = os.listdir(directory + '/' +  activity_folder)

    # Initialize your list of images found in one activity folder
    activity_folder_image_list = []

# Create a list with all the images in an activity folder
for image_file in image_folder_path: #inserted variable here
    if '.jpg' in image_file:
        activity_folder_image_list.append(image_file)

    # Determine if an image has already been cropped, and remove it from your list
    # of images to crop
    activity_folder_image_list[:]=[original_image for original_image in activity_folder_image_list
                                   if not is_in_list(original_image, activity_folder_dict)]
# Crop each image and save the image as the [activy name]_[number].jpg
for image in activity_folder_image_list:
    
    im = Image.open(directory + '/' + activity_folder + '/' + image)
        # The newly cropped image should have a 1.076 width to height ratio (or another ratio you provide in the input file)
        
        # Image.size[1] is the second entry for the images dimensions (aka height)
        #1.076 (730 x 678)
        ori_height = int(im.size[1]) #This makes the height dimension an integer
        ori_width = int(im.size[0])  #This makes the width dimension an integer
        #Determine how to crop the image so that either the height or the width is reduced to fit within the rectangle
        #dimensions of the original images
        #There are three scenarios to consider: 1) original width > original height 2) original width > original height
        # 3) original width = original height
        
        #The following checks whether the original image is horizontal, vertical, or a square
        #assign the desired ratio as the variable 'ratio':
        
        #First check if width is greater than the height:
        if (ori_width/float(ori_height)) > 1: #you need to make one of the numbers a float so your result is a float
            #the height is the limiting dimensions to crop this image so the width has to be reduced while
            #keeping the height the same as in the original image.
            new_width = int(ratio*ori_height) #make sure your new_width is an integer
            # im.crop(box) where box is a 4 tuple with the first two terms defining the location of your box's
            # top left corner and the second two terms defining distance of the right and bottom edge from the
            # top left coordinate which starts at (0,0). Best way to think about it is your width and height terms
            # provide the area of your box and the xleft and top terms define how far over your box is shifted from the
            # 0,0 vertical axis
            xleft = int((ori_width - new_width)/float(2)) # x coordinate for the top left corner point
            top = 0# y coordinate for the top left corner point (moving down from (0,0))
            width = new_width # the width of your new box
            height = ori_height # the height of your new box
            box = (xleft, top, xleft+width, top+height)
        #if the height is greater than the width, the width stays fixed and you adjust the height
        
        
        elif (ori_width/float(ori_height)) < 1:
            new_height = int(ori_width/float(ratio)) #make sure your new_width is an integer
            xleft = 0 # x coordinate for the top left corner point
            top = int((ori_height - new_height)/float(2)) # y coordinate for the top left corner point
            width = ori_width # x coord for the bottom right corner point
            height = new_height #y coord for the bottom right corner point
            box = (xleft, top, xleft+width, top+height)
        
        
        #if the height and the width are equal then you have to check what ratio you are cropping to, to
        #determine which dimension to reduce
        elif (ori_width/float(ori_height)) == 1 and ratio < 1:
            new_width = int(ratio*ori_height)
            xleft = int((ori_width - new_width)/float(2)) # x coordinate for the top left corner point
            top = 0# y coordinate for the top left corner point (moving down from (0,0))
            width = new_width # the width of your new box
            height = ori_height # the height of your new box
            box = (xleft, top, xleft+width, top+height)
        
        
        elif (ori_width/float(ori_height)) == 1 and ratio > 1:
            new_height = int(ori_width/float(ratio)) #make sure your new_width is an integer
            xleft = 0 # x coordinate for the top left corner point
            top = int((ori_height - new_height)/float(2)) # y coordinate for the top left corner point
            width = ori_width # x coord for the bottom right corner point
            height = new_height #y coord for the bottom right corner point
            box = (xleft, top, xleft+width, top+height)
        
        
        else:
            print 'dang something went wrong!'
        
        
        # Assign the area of the cropped image to the variable 'area'
        area = im.crop(box)
        
        #save the cropped image to the folder '[activity]_cropped' and add _[number.jpg]
        
        # Add 1 to the total count of folders in each activity
        count += 1
        # save the cropped image with a new dimensions
        # you can add ('_'+) if you want an underscore before the count number
        area.save(directory + '/' + activity_folder + '/' +
                  activity_folder.rstrip('\n') + '_cropped'+ '/' + activity_folder.rstrip('\n') + str(count) + '.jpg')
            
                  # Assigning the saved image as 'saved_cropped_image'
                  saved_cropped_image = directory + '/' + activity_folder + '/' + activity_folder.rstrip('\n') + '_cropped'+ '/' + activity_folder.rstrip('\n') + str(count) + '.jpg'
                  
                  # Store key value pairs of your original image
                  # (called 'image' in this loop and the 'saved_cropped_image')
                  activity_folder_dict [image] = saved_cropped_image
                  
                  #make sure you store your json file in the right directory
                  with open(directory + '/activity_folder_dict.json', 'w') as fp:
                      json.dump(activity_folder_dict, fp)


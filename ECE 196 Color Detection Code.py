# ECE 196 Color Detection Code
import numpy as np 
import time
import cv2
import itertools
import matplotlib.pyplot as plt; 
from PIL import Image
from numpy import interp

# Environmental Variables 
import os 
from dotenv import load_dotenv 
load_dotenv(); 


def checkColor(colorValue, boundaryColors): 
    for i in range(3): 
        if colorValue[i] > boundaryColors[i*2] or colorValue[i] < boundaryColors[i*2 + 1]: # Check against max and min value
            return (0, 0, 0); # If it is greater than the max or less than the min return a white pixel 
    return colorValue; 

def checkDirection(imageArray): # 3 directions left, right, and straight, 1 = left, 2 = right, 3 = straight 
    directions = [0, 0, 0]
    sections = [0, standardImageSize//3, standardImageSize-standardImageSize//3, standardImageSize]; 
    for i in range(3): 
        directions[i] = np.sum(imageArray[:, sections[i]:sections[i+1], :]); 
    return directions.index(max(directions)) + 1; 

def checkDirectionIntegral(imageArray): # Change direction with integral control 
    directions = list(itertools.repeat(0, standardImageSize)); 
    for i in range(standardImageSize): 
        directions[i] = (np.sum(imageArray[:, i, :])); # Checks 1 width column in image 
    print(max(directions)); 
    return int(interp((directions.index(max(directions)) + 1), [1, standardImageSize], [180, 0])); # Maps image width to angle range 

def RGBdetection(imageArray, rMax, rMin, gMax, gMin, bMax, bMin): 
    boundaryColors = [rMax, rMin, gMax, gMin, bMax, bMin]; 

    for i in range(imageArray.shape[0]): # image height
        for j in range(imageArray.shape[1]): # image width
            imageArray[i][j] = checkColor(imageArray[i][j], boundaryColors); 
        
    return imageArray; 

# Low HSV values
# lowHSV = (36, 25, 25); 
# High HSV Values
# highHSV = (70, 255, 255); 

lowHSV = (20, 70, 70); 
highHSV = (135, 255, 255); 

def HSVdetection(anImage): 
    theImage = cv2.imread(anImage); 
    theImage = cv2.resize(theImage, (standardImageSize, standardImageSize)); 
    hsvImage = cv2.cvtColor(theImage, cv2.COLOR_BGR2HSV); 
    theMask = cv2.inRange(hsvImage, (lowHSV), (highHSV)); 
    sliceMask = theMask > 0; 
    desiredColorImage = np.zeros_like(theImage, np.uint8); 
    desiredColorImage[sliceMask] = theImage[sliceMask];  
    return np.array(desiredColorImage);  

# RGB Range for algae detection
rMax = 180; gMax = 255; bMax = 178; 
rMin = 4; gMin = 132; bMin = 0; 


standardImageSize = 100; 
testImagePath = os.getenv('testImagePath'); 
image = Image.open(testImagePath);  
image = image.resize((standardImageSize, standardImageSize)); 
imageArray = np.array(image); 


# arrayFinal = RGBdetection(imageArray, rMax, rMin, gMax, gMin, bMax, bMin); 
arrayFinal = HSVdetection(testImagePath); 
direction = checkDirectionIntegral(arrayFinal); 
print("Angle: ", direction); 
'''
if direction == 1: 
    print("Turn left.")
if direction == 2: 
    print("Turn right.")
if direction == 3: 
    print("Go straight.")
'''

imageFinal = Image.fromarray(arrayFinal.astype('uint8'), 'RGB'); 
fig, ax = plt.subplots(1, 2)
ax[0].imshow(image); ax[1].imshow(imageFinal); 
plt.show(); 
print("End."); 

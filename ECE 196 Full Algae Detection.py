# ECE 196 Full Algae Detection
import numpy as np 
import socket 
import time
import cv2
import itertools
import msvcrt 
import matplotlib.pyplot as plt; 
from PIL import Image
from numpy import interp 

# Environmental variables
import os 
from dotenv import load_dotenv 
load_dotenv(); 


def HSVdetection(theImage): 
    # theImage = cv2.imread(anImage); 
    # theImage = cv2.resize(theImage, (standardImageSize, standardImageSize)); 
    hsvImage = cv2.cvtColor(theImage, cv2.COLOR_BGR2HSV); 
    theMask = cv2.inRange(hsvImage, (lowHSV), (highHSV)); 
    sliceMask = theMask > 0; 
    desiredColorImage = np.zeros_like(theImage, np.uint8); 
    desiredColorImage[sliceMask] = theImage[sliceMask];  
    return np.array(desiredColorImage);  

def checkDirection(imageArray): # 3 directions left, right, and straight 1 = left, 2 = straight, 3 = right 
    directions = [0, 0, 0]
    sections = [0, standardImageSize//3, standardImageSize-standardImageSize//3, standardImageSize]; 
    for i in range(3): 
        directions[i] = np.sum(imageArray[:, sections[i]:sections[i+1]]); 
        # print(directions[i]); 
    maxGreen = max(directions); 
    if maxGreen > 500000: # thresholdValue
        return directions.index(maxGreen) + 1;  
    return 2; 

def checkDirectionIntegral(imageArray): # Change direction with integral control 
    directions = list(itertools.repeat(0, standardImageSize)); 
    for i in range(standardImageSize): 
        directions[i] = (np.sum(imageArray[:, i, :])); # Checks 1 width column in image 
    maxGreen = max(directions); 
    # print(maxGreen); 
    # print(directions.index(maxGreen)); 
    if maxGreen > thresholdValue: 
        return str(int(interp((directions.index(max(directions)) + 1), [1, standardImageSize], [180, 0]))); # Maps image width to angle range 
    else: 
        return "90"; # Middle angle, makes boat go straight
    
def getImageFromStream(streamURL): 
    theStream = cv2.VideoCapture(streamURL); 
    if not theStream.isOpened: 
        print("Stream failed to open!"); 
        return False; 
    else: 
        streamSuccess, theFrame = theStream.read(); 
        if streamSuccess: 
            time.sleep(1); 
            cv2.imwrite(imagePath, theFrame); 
        else: 
            print("Failed to get frame!"); 
    return True; 

def printPlot(arrayFinal): 
    fig, ax = plt.subplots(1, 2) 
    ax[0].imshow(np.array(Image.open(imagePath))); 
    ax[1].imshow(arrayFinal); 
    plt.show(); 
    return 0; 

# HSV Range for algae detection
# Indoor HSV 
lowHSV = (40, 0, 0); 
highHSV = (80, 180, 180); 

# Outdoor HSV 
# lowHSV = (0, 0, 140); 
# highHSV = (35, 90, 255); 

# ESP32 / Stream Information
ESP_IP = os.getenv('ESP_IP'); 
serverPort = os.getenv('serverPort'); 
streamURL = os.getenv('streamURL'); 
streamURL2 = os.getenv('streamURL2'); # Sometimes it switches ?
imagePath = os.getenv('imagePath'); 
standardImageSize = 320; # changed for our camera pixel width 320
thresholdValue = 20000; 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as theSocket:
    theSocket.connect((ESP_IP, serverPort)); 
    theCamera = cv2.VideoCapture(streamURL); 
    lastTime = time.time(); 
    theSignalInterval = 2; 
    while True:
        if msvcrt.kbhit():
            break; 
        theVideo, anImage = theCamera.read(); 
        
        # getImageFromStream(streamURL); 
        arrayFinal = HSVdetection(anImage); 
        cv2.imshow("Algae Feed", arrayFinal); 
        cv2.imshow("Original Feed", anImage); 
        # printPlot(arrayFinal); 
        theDirection = checkDirectionIntegral(arrayFinal); 
        theDirection = str(theDirection); 
        # print(theDirection); 
        if time.time() - lastTime > theSignalInterval:
            lastTime = time.time();  
            print("Sent Signal !", theDirection); 
            theSocket.sendall(theDirection.encode()); 
            # theResponse = theSocket.recv(1024);  
            # print(theResponse); 
        # time.sleep(1); 
        cv2.waitKey(1);  

print("End."); 

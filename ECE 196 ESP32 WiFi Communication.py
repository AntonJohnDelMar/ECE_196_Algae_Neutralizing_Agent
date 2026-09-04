# ECE 196 ESP32 WiFi Communication 
import socket 
import time
import cv2
import subprocess
import numpy as np 
from PIL import Image

# Environmental Variables 
import os 
from dotenv import load_dotenv 
load_dotenv(); 

ESP_IP = os.getenv('ESP_IP'); 
serverPort = os.getenv('serverPort'); 
streamURL = os.getenv('streamURL'); 
imagePath = os.getenv('imagePath'); 

theStream = cv2.VideoCapture(streamURL); 
if not theStream.isOpened(): 
    print("Failed to open stream!"); 
else: 
    readSuccess, theFrame = theStream.read(); 
    if readSuccess: 
        cv2.imwrite(imagePath, theFrame); 
    else: 
        print("Failed to capture frame!"); 
theStream.release(); 

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as theSocket:
    theSocket.connect((ESP_IP, serverPort)); 
    byteString = "1"; # [0x1].encode('utf-8') 
    theSocket.sendall(byteString.encode()); 
    theResponse = theSocket.recv(1024).decode(); 
    print(theResponse); 



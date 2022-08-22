#class clickable entity and subclass inventory
from calendar import c
from re import X
from tkinter import Y
import pyautogui
import time
import numpy as np
from pyHM import mouse
from windmouse import wind_mouse
from speed import speed


class clickableEntity(object): #same as inventory slot except the central tendency size and random walk count are modifiable
    def __init__(self, centralTendency,numberRandWalks):
        self.centralTendency = centralTendency #this is the radius in pixels of each coords central tendency. A good value for an inventory spot on my thinkpad is ~7
        self.numberRandWalks = numberRandWalks #this is the number of one pixel random walks a click will take. A good value for an inventory spot on my thinkpad is 300. 
        
    def getcoords(self):
        input("position your mouse at coord 1 and press enter")
        coord1 = pyautogui.position()
        print("recorded coord 1 as "+ str(coord1))
        input("position your mouse at coord 2 and press enter")
        coord2 = pyautogui.position()
        print("recorded coord 2 as "+ str(coord2))
        input("position your mouse at coord 3 and press enter")
        coord3 = pyautogui.position()
        print("recorded coord 3 as "+ str(coord3))    
        self.coords = [coord1, coord2, coord3] 
     

    def genclick(self): #randomizes a click location and clicks
        coordpick = np.random.randint(1,4) #selects which of the coords to start with
        #print("coordpick is "+str(coordpick))
        if coordpick == 1:
            x,y = self.coords[0]
        elif coordpick == 2:
            x,y = self.coords[1]
        else:
            x,y = self.coords[2]
        
        #this part shifts the coord a random, linearly distributed amount from coord to widen central tendency
        x += np.random.randint((self.centralTendency * -1), (self.centralTendency +1)) 
        y += np.random.randint((self.centralTendency * -1), (self.centralTendency +1)) 

        #this part shifts the coord again using a random walk (binomial distro?) to conceal the linear distribution
        xshift = 0
        yshift = 0 #these are the amounts that the click will be shifted
        
        for i in range(self.numberRandWalks): # adds numberRandWalks random +1s and -1s to xshift and y shift. change this value to increase the amount of random walk
            xshift += np.random.randint(-1,2) #resolves randomly to -1 or 1
            yshift += np.random.randint(-1,2) #resolves ramdonly to -1 or 1
        #print("xshift is %s and yshift is %s" %(str(xshift), str(yshift)))
        
        x += xshift
        y += yshift

        try: #this fucking mouse move keeps causing exceptions. no idea why, the inputs into it look good, I blame god. the try is an attempt to 
            #mouse.move(x,y, multiplier=.2) #this moves the mouse to the final point
            wind_mouse(pyautogui.position()[0], pyautogui.position()[1], x,y, speed = speed(mean = .6, min = .55, max =.75))
            time.sleep(np.random.normal(loc=.2, scale=.03))
            pyautogui.click()
            time.sleep(np.random.normal(loc=.1, scale=.02))
        except: #basically aborts the move/click attempt and continues on with loop
            log = open('log.txt', 'w')
            report = "move/click failed at %s | x = %s | y = %s | mouse pos. = %s \n" %(time.time(),  x,y, pyautogui.position())
            log.write(report)            
            print('Click failed, retry')
            time.sleep(np.random.normal(6,1))
            self.genclick()

    def dropclick(self): #dropclick for an inventory slot
        coordpick = np.random.randint(1,4) #selects which of the coords to start with
        #print("coordpick is "+str(coordpick))
        if coordpick == 1:
            x,y = self.coords[0]
        elif coordpick == 2:
            x,y = self.coords[1]
        else:
            x,y = self.coords[2]
        
        #this part shifts the coord a random, linearly distributed amount from coord to widen central tendency
        x += np.random.randint((self.centralTendency * -1), (self.centralTendency +1)) 
        y += np.random.randint((self.centralTendency * -1), (self.centralTendency +1)) 

        #this part shifts the coord again using a random walk (binomial distro?) to conceal the linear distribution
        xshift = 0
        yshift = 0 #these are the amounts that the click will be shifted
        
        for i in range(self.numberRandWalks): # adds numberRandWalks random +1s and -1s to xshift and y shift. change this value to increase the amount of random walk
            xshift += np.random.randint(-1,2) #resolves randomly to -1 or 1
            yshift += np.random.randint(-1,2) #resolves ramdonly to -1 or 1
        #print("xshift is %s and yshift is %s" %(str(xshift), str(yshift)))
        
        x += xshift
        y += yshift

        try: #this fucking mouse move keeps causing exceptions. no idea why, the inputs into it look good, I blame god. the try is an attempt to 
            #mouse.move(x,y, multiplier=.2) #this moves the mouse to the final point
            wind_mouse(pyautogui.position()[0], pyautogui.position()[1], x,y, speed = speed(mean = .6, min = .55, max =.75))
            pyautogui.keyDown('shift')
            time.sleep(np.random.normal(loc=.2, scale=.03))
            pyautogui.click()
            time.sleep(np.random.normal(loc=.1, scale=.02))
            pyautogui.keyUp('shift')
        except: #basically aborts the move/click attempt and continues on with loop
            pyautogui.click() #this is risky, but should prevent iron buildup in inventory. exceptions cause iron buildup somehow
            log = open('log.txt', 'w')
            report = "move/click failed at %s | x = %s | y = %s | mouse pos. = %s \n" %(time.time(), x,y, pyautogui.position())
            log.write(report)            
            print('Click failed, retry')
            time.sleep(np.random.normal(6,1))
            self.genclick()

class inventorySlot(clickableEntity): #an inventory slot
    def __init__(self, centralTendency,numberRandWalks):
        self.centralTendency = centralTendency #this is the radius in pixels of each coords central tendency. A good value for an inventory spot on my thinkpad is ~7
        self.numberRandWalks = numberRandWalks #this is the number of one pixel random walks a click will take. A good value for an inventory spot on my thinkpad is 300. 


    def genClickInventorySlot(self): #random walk model away from coords
        coordpick = np.random.randint(1,4) #selects which of the coords to start with
        #print("coordpick is "+str(coordpick))
        if coordpick == 1:
            x,y = self.coords[0]
        elif coordpick == 2:
            x,y = self.coords[1]
        else:
            x,y = self.coords[2]
        
        #this part shifts the coord a random, linearly distributed amount from coord to widen central tendency
        x += np.random.randint((self.centralTendency * -1), (self.centralTendency +1)) 
        y += np.random.randint((self.centralTendency * -1), (self.centralTendency +1)) 

        #this part shifts the coord again using a random walk (binomial distro?) to conceal the linear distribution
        xshift = 0
        yshift = 0 #these are the amounts that the click will be shifted
        
        for i in range(self.numberRandWalks): # adds numberRandWalks random +1s and -1s to xshift and y shift. change this value to increase the amount of random walk
            xshift += np.random.randint(-1,2) #resolves randomly to -1 or 1
            yshift += np.random.randint(-1,2) #resolves ramdonly to -1 or 1
        #print("xshift is %s and yshift is %s" %(str(xshift), str(yshift)))
        
        x += xshift
        y += yshift

        try: #this fucking mouse move keeps causing exceptions. no idea why, the inputs into it look good, I blame god. the try is an attempt to 
            mouse.move(x,y, multiplier=.2) #this moves the mouse to the final point
            pyautogui.keyDown('shift')
            time.sleep(np.random.normal(loc=.2, scale=.03))
            pyautogui.click()
            time.sleep(np.random.normal(loc=.1, scale=.02))
            pyautogui.keyUp('Shift')
        except: #basically aborts the move/click attempt and continues on with loop
            log = open('log.txt', 'w')
            report = "\n move/click failed at %s | count = %s | x = %s | y = %s | mouse pos. = %s \n" %(time.time(), count, x,y, pyautogui.position())
            log.write(report)            
            print('Click failed, retry')
            time.sleep(np.random.normal(6,1))
            self.genClickInventorySlot()



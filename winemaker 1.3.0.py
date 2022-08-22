#winemaker 
# todo:
#you've modified clickableEntity to use wind_mouse. check it works
#you've not written the whole program yet, so far you've got to inv_grape clicking (I think)
#YOU"VE FORGOTTEN THE DUMP INVENTORY STEP. itshould happen around line 128

from calendar import c
import pyautogui
import time
import numpy as np
from pyHM import mouse
import cv2 as cv
from cv2 import threshold
from cv2 import _InputArray_STD_BOOL_VECTOR
import numpy as np
import os
from windmouse import wind_mouse
from windowcapture import WindowCapture
from vision import Vision
import pyautogui
from pyHM import Mouse
import time
from action import Action
import breakRoller
import clickableEntity
from speed import speed
from tickdropper import tick_dropper

#instructions
#start with 14 wines in inventory (I think)
#bank x set to 14
#visible water jug and grapes, but NO VISIBLE WINE IN BANK
#no wine, jug or grapes in tab window
#you must put a brick on space key

BANK_GRAPE_THRESHOLD = .92
INV_GRAPE_THRESHOLD =.92
INV_JUG_THRESHOLD = .92
IN_BANK_THRESHOLD = .8
OUT_BANK_THRESHOLD = .8 #THIS ONE IS DIFFERENT. it's satisfied when it's LESS than OUT_BANK_THRESHOLD confident that it's IN a bank
WINE_THRESHOLD = .92

# initialize the WindowCapture class
wincap = WindowCapture('RuneLite - Vessacks')

# initialize the Vision class
inv_jug_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\inv_jug.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
inv_grape_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\inv_grape.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
in_bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\in_bank.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
wine_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\wine.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_jug_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\bank_jug.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_grape_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\bank_grape.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)

#gets the coords for bank E
#decent parameters are (2,10) for slots and (5,30) for rocks on samsung monitor
#decent parameters are (7,300) for slots and unknown for rocks on samsumg monitor



inv_jug = clickableEntity.clickableEntity(2,10)
print("we will now take coords for inv_jug slot" )
inv_jug.getcoords()

inv_grape = clickableEntity.clickableEntity(2,10)
print("we will now take coords for inv_grape slot" )
inv_grape.getcoords()

bank = clickableEntity.clickableEntity(5,30)
print("we will now take coords for bank window")
bank.getcoords()

bank_dump = clickableEntity.clickableEntity(2,10)
print("we will now take coords for bank_dump" )
bank_dump.getcoords()

bank_jug = clickableEntity.clickableEntity(2,10)
print("we will now take coords for bank_jug slot" )
bank_jug.getcoords()

bank_grape = clickableEntity.clickableEntity(2,10)
print("we will now take coords for bank_grape slot" )
bank_grape.getcoords()

bank_x = clickableEntity.clickableEntity(2,7)
print("we will now take coords for bank_x slot" )
bank_x.getcoords()

inventory = clickableEntity.clickableEntity(2,10)
print("we will now take coords for the inventory bag" )
inventory.getcoords()




#this determines how long to run for
count = 0
startTime = time.time()

countOrSecond = input('would you like to run for #seconds or #counts? (s/c)')
if countOrSecond == 's':
    durationSeconds = float(input('please input number of seconds to run (1h= 3600, 6h=21600'))
    
elif countOrSecond == 'c':
    durationCount = int(input('please enter the number of counts to perform'))
    
else:
    print('you\'ve messed something up, quitting program now' )

input('Ready? press enter to begin')



def normdistwait(mean, standarddev):
    #normal distribution determines how long to wait between rock clicks
    time.sleep(np.random.normal(loc=mean,scale=standarddev))

count = 0
startTime = time.time()

while True: #run loop 
    #get us into the bank
    bank.genclick()
    
    #check we're in bank
    in_bank_confidence = 0
    enter_bank_start = time.time()
    while in_bank_confidence < IN_BANK_THRESHOLD:
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        all_in_bank_window, best_in_bank_window, in_bank_confidence = in_bank_vision.find(screenshot, IN_BANK_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
        
        if in_bank_confidence > IN_BANK_THRESHOLD:
            print('in bank with confidence %s' % in_bank_confidence)
            break

        print('in_bank_confidence = %s' % in_bank_confidence)

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()

        enter_bank_wait = time.time() - enter_bank_start
        if enter_bank_wait > 10:
            heel_cooler = np.random.normal(3,.3)
            print('waited %s, not in bank. reclicking and heel cooling %ss' %(enter_bank_wait, heel_cooler))
            bank.genclick()
            time.sleep(heel_cooler)
        if enter_bank_wait > 15:
            print('PROBLEM(!) waited %s, still not in bank. exiting...' % enter_bank_wait)
            exit()

    print('in bank w confidence %s' % in_bank_confidence)
    time.sleep(.3 + abs(np.random.normal(0,.3)))

    #bank dump
    bank_dump.genclick()

    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_wine_window, best_wine_window, wine_confidence = wine_vision.find(screenshot, WINE_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()

    #check we're not seeing too many wines
    wine_dump_start = time.time()
    while len(all_wine_window) > 1:
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        all_wine_window, best_wine_window, wine_confidence = wine_vision.find(screenshot, WINE_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        wine_dump_wait = time.time() - wine_dump_start 
        if wine_dump_wait > 2:
            heel_cooler = np.random.normal(3,.3)
            print('waited %s, wines not dumped. reclicking and heel cooling %ss' %(wine_dump_wait, heel_cooler))
            bank_dump.genclick()
            time.sleep(heel_cooler)
        if wine_dump_wait > 15:
            print('PROBLEM(!) waited %s, wines still not dumped. exiting...' % wine_dump_wait)
    
    print('post wine dump. num wines = %s | wine_confidence %s' %(len(all_wine_window), wine_confidence))

    time.sleep(.3 + abs(np.random.normal(0,.3)))

    #click us a grape
    bank_grape.genclick()

    #check we got grapes
    all_inv_grape_window = []
    grape_click_start = time.time()
    while len(all_inv_grape_window) < 13:
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        all_inv_grape_window, best_inv_grape_window, inv_grape_confidence = inv_grape_vision.find(screenshot, INV_GRAPE_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()

        grape_click_wait = time.time() - grape_click_start
        if grape_click_wait > 1:
            heel_cooler = np.random.normal(3,.3)
            print('waited %s, not seeing enough grapes. reclicking and heel cooling %ss' %(grape_click_wait, heel_cooler))
            bank_grape.genclick()
            time.sleep(heel_cooler)
        if grape_click_wait > 15:
            print('PROBLEM(!) waited %s, still not enough grapes. exiting...' % grape_click_wait)
            exit()
    
    print('got %s (>13) grapes. grape_confidence %s' % (len(all_inv_grape_window), inv_grape_confidence))
    
    time.sleep(.3 + abs(np.random.normal(0,.3)))

    #click us a jug
    bank_jug.genclick()

    #check we got jugs
    all_inv_jug_window = []
    jug_click_start = time.time()
    while len(all_inv_jug_window) < 13:
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        all_inv_jug_window, best_inv_jug_window, inv_jug_confidence = inv_jug_vision.find(screenshot, INV_JUG_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()

        jug_click_wait = time.time() - jug_click_start
        if jug_click_wait > 1:
            heel_cooler = np.random.normal(3,.3)
            print('waited %s, not seeing enough jugs. reclicking and heel cooling %ss' %(jug_click_wait, heel_cooler))
            bank_jug.genclick()
            time.sleep(heel_cooler)
        if jug_click_wait > 15:
            print('PROBLEM(!) waited %s, still not enough jugs. exiting...' % jug_click_wait)
            exit()

    print('got %s (>13) jugs. jug_confidence %s' % (len(all_inv_jug_window), inv_jug_confidence))

    time.sleep(.3 + abs(np.random.normal(0,.3)))

    #click us an exit
    bank_x.genclick()


    #check we're not in bank
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_in_bank_window, best_in_bank_window, in_bank_confidence = in_bank_vision.find(screenshot, IN_BANK_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()
    exit_bank_start = time.time()
    while in_bank_confidence > OUT_BANK_THRESHOLD: ####note: I'm doing something WIERD here
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        all_in_bank_window, best_in_bank_window, in_bank_confidence = in_bank_vision.find(screenshot, IN_BANK_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()

        exit_bank_wait = time.time() - exit_bank_start
        if exit_bank_wait > 2:
            heel_cooler = np.random.normal(3,.3)
            print('waited %s, still in bank. reclicking and heel cooling %ss' %(exit_bank_wait, heel_cooler))
            bank.genclick()
            time.sleep(heel_cooler)
        if exit_bank_wait > 15:
            print('PROBLEM(!) waited %s, still in bank. exiting...' % exit_bank_wait)
    
    print('I think were out of the bank | in_bank_confidence = %s ' % in_bank_confidence)


    #click us an inv_grape 
    inv_grape.genclick()
    time.sleep(abs(np.random.normal(.3,.2)))

    #click us an inv_jug
    inv_jug.genclick()
    
    time.sleep(.6 + abs(np.random.normal(0,.1)))
    pyautogui.keyDown('space')
    time.sleep(abs(np.random.normal(.15,.03)))
    pyautogui.keyUp('space')
    
    screenshot = wincap.get_screenshot()
    screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
    all_inv_grape_window, best_inv_grape_window, inv_grape_confidence = inv_grape_vision.find(screenshot, INV_GRAPE_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        exit()

    grapewatch_start = time.time()
    while len(all_inv_grape_window) > 0:
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        all_inv_grape_window, best_inv_grape_window, inv_grape_confidence = inv_grape_vision.find(screenshot, INV_GRAPE_THRESHOLD, debug_mode='rectangles', return_mode = 'allPoints + bestPoint + confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        grapewatch_wait = time.time() - grapewatch_start
        print('I see %s grapes | grapewatching for %ss ' % (len(all_inv_grape_window), round(grapewatch_wait,1) ))

        if grapewatch_wait > 40:
            print('PROBLEM(!) grapewatch_time = %s. reclicking procedure active' %grapewatch_wait)
            inventory.genclick()
            print('clicked inventory')
            time.sleep(abs(np.random.normal(.3,.2)))
            inv_jug.genclick()
            print('clicked jug')
            time.sleep(abs(np.random.normal(.3,.2)))
            inv_grape.genclick()
            print('clicked grape')
            wait_time = np.random.uniform(2,3)
            print('reclick complete. waiting %s... ' % wait_time)
            time.sleep(wait_time)

        if grapewatch_wait > 60:
            print('PROBLEM(!) grapewatch_time = %s. giving up, exiting...')
            exit()

    print('num grapes is %s/0. starting new cycle' % len(all_inv_grape_window))

    breakRoller.breakRoller(odds = 40)

    #this is the count/seconds section
    count += 1
    runTime = round(time.time() - startTime,0)
    countSec = round(count/runTime,2)
    print('count = %s | runTime = %s seconds | count/sec = %s '%(count, runTime, countSec))

    #termination conditions
    if pyautogui.position() == pyautogui.Point(0,0):
        print('quitting program')
        quit()
    if countOrSecond == 's' and runTime > durationSeconds:
        print('quitting program')
        quit()
    if countOrSecond == 'c' and count > durationCount:
        print('quitting program')
        quit()
    

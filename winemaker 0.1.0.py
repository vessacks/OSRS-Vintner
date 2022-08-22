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

BANK_GRAPE_THRESHOLD = .92
INV_GRAPE_THRESHOLD =.92
INV_JUG_THRESHOLD = .92
IN_BANK_THRESHOLD = .92
OUT_BANK_THRESHOLD = .8 #THIS ONE IS DIFFERENT. it's satisfied when it's LESS than OUT_BANK_THRESHOLD confident that it's IN a bank
WINE_THRESHOLD = .92

# initialize the WindowCapture class
wincap = WindowCapture('RuneLite - Vessacks')

# initialize the Vision class
inv_jug_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\inv_jug.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
inv_grape_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\inv_grape.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\bank.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
in_bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\in_bank.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
wine_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\wine.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)

#unnessesary-- used for testing accuracy of vision on other projects
bank_x_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\winemaker\\image library\\bank_x.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
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

bank_x = clickableEntity.clickableEntity(2,10)
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
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()

        enter_bank_wait = time.time() - enter_bank_start
        if enter_bank_wait > 2:
            heel_cooler = np.random.normal(3,.3)
            print('waited %s, not in bank. reclicking and heel cooling %ss' %(enter_bank_wait, heel_cooler))
            bank.genclick()
            time.sleep(heel_cooler)
        if enter_bank_wait > 15:
            print('PROBLEM(!) waited %s, still not in bank. exiting...' % enter_bank_wait)
    
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
    all_inv_grape_window = 0
    grape_click_start = time.time()
    while all_inv_grape_window < 13:
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
    all_inv_jug_window = 0
    jug_click_start = time.time()
    while all_inv_jug_window < 13:
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

        if grapewatch_wait > 25:
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


    Rock2.genclick()
    normdistwait(1.45,.1)
    Rock3.genclick()
    normdistwait(1.2,.1)

    inv_jug.dropclick()
    normdistwait(.02,.002)
    inv_grape.dropclick()
    normdistwait(.02,.002)
    slot3.dropclick()
    normdistwait(.02,.002)
   
    #breakroller
    breakRoller.breaktime()

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
    

#####
# initialize the WindowCapture class
wincap = WindowCapture('RuneLite - Vessacks')


# initialize the Vision class
sand_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\sand.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
weed_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\weed.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
rune_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\rune.png', method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\bank.png',method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_x_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\bank_x.png',method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
bank_dump_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\bank_dump.png',method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)
spellcast_vision = Vision('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\spellcast.png',method = cv.TM_CCOEFF_NORMED, imread = cv.IMREAD_GRAYSCALE)

#initialize the action class
sand_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\sand.png')
weed_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\weed.png')
rune_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\rune.png')
bank_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\bank.png')
bank_x_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\bank_x.png')
bank_dump_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\bank_dump.png')
spellcast_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\spellcast.png')
withdraw_18_action = Action('C:\\Users\\Jeff C\\Downloads\\Code\\OpenCV files\\superglass make\\image library\\withdraw_18.png')

#todo:
#1 when you're done, remove the debug mode and stop drawing the screen for speed
#2 test your theory about putting waitkeys and new screenshots in between all actions

#notes: start next to bank, inventory contents don't matter
#I've set up imshows and new screenshots for every action because I think that reduces opencv fuckups. remember-- if you perform the same operation twice in a row without this you CAN get reduced confidence like crazy

#setup
# set up a new bank image
#1 have bank withdraw set to 1
#2 have bank withdraw x set to 18
#3 have bank set to tab with astrals, sand buckets, giant seaweed. sand bucket must have at least 2 objects before them to ensure the correct offset
#have smoke staff equipped
#have lunar spellbook  OPEN
#in a bank tab with weed,sand and astral
#no weed, sand or astral in the bank tab


BANK_THRESHOLD = .63
BANK_THRESHOLD_RECLICK = .2
BANK_X_THRESHOLD = .85
BANK_DUMP_THRESHOLD = .85
SPELLCAST_THRESHOLD = .85
SAND_THRESHOLD = .85
WEED_THRESHOLD = .85
RUNE_THRESHOLD = .85

WITHDRAW_18_OFFSET = [-117,64] #these are the coord offsets between a righclick point and the withdraw 18 dropdown option

def wait():
    wait = (.06 + abs(np.random.uniform(0,.02)))
    return wait

def speed():
    speed = np.random.normal(.78,.3)
    while speed > .85 or speed < .6:
        speed = np.random.normal(.75,.08)
    return speed

def tick_dropper(odds=100):
    if np.random.randint(0,odds) == 1:
        time.sleep(.6)


s_or_c = input('would you like to run in seconds or counts? please enter \'s\' or \'c\'')

if s_or_c == 's':
    quit_after_seconds = float(input('please enter the number of seconds to run for, then press enter. 1h = 3600s, 6h = 21600'))
if s_or_c == 'c':
    quit_after_counts = int(input('please enter the number of counts to run for, then press enter. about 8s per count.'))
else:
    print('you\'ve screwed something up. try running this program again. exiting...')
    exit()

runStart = time.time()
count = 0

def superglass_make():    
    while True:

        #waiting a bit for spell to cast
        sleepytime = 1.8 + abs(np.random.normal(0,.1))
        time.sleep(sleepytime)        

        #below is the old way of entering the bank and finding bank dump. to return to this method, change sleepytime action (first thing in loop) to 1.8 seconds,and delete everything between sleepytime and this comment
        
        #enter bank
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        bank_confidence = bank_vision.find(screenshot, threshold = BANK_THRESHOLD, return_mode= 'confidence')
        if bank_confidence[1] < BANK_THRESHOLD:
            print(' PROBLEM(!) bank confidence %s | BANK_THRESHOLD %s | Continuing anyway...' %( bank_confidence[1], BANK_THRESHOLD))
            #exit()
        else:
            print('bank confidence %s | BANK_THRESHOLD %s | Continuing...' %( bank_confidence[1], BANK_THRESHOLD))
        bank_screenPoint = wincap.get_screen_position(bank_confidence[0])
        bank_clickPoint = bank_action.click(bank_screenPoint, speed = speed(), wait = wait())
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        
        #look for bank dump: this takes a variable amount of time
        bank_dump_confidence = [[0,0],0]
        search_start = time.time()
        search_time = 0
        while bank_dump_confidence[1] < BANK_DUMP_THRESHOLD:
            screenshot = wincap.get_screenshot()
            screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
            bank_dump_confidence = bank_dump_vision.find(screenshot, threshold = BANK_DUMP_THRESHOLD, return_mode= 'confidence')
            if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()

            search_time = time.time() - search_start
            if search_time > 2:
                screenshot = wincap.get_screenshot()
                screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
                bank_confidence = bank_vision.find(screenshot, threshold = BANK_THRESHOLD, return_mode= 'confidence')
                if cv.waitKey(1) == ord('q'):
                    cv.destroyAllWindows()
                    exit()
                if bank_confidence[1] < BANK_THRESHOLD_RECLICK:
                    print('2+ seconds since bank click. PROBLEM(!) bank confidence %s below BANK_THRESHOLD DISABLED(!) %s | continuing anyway...' %( bank_confidence[1], BANK_THRESHOLD))
                    exit()
                else:
                    print('2+ seoncds inactivity. attempting reclick on bank and sleeping ~.6s. bank confidence %s | BANK_THRESHOLD DISABLED(!) %s | Continuing...' %( bank_confidence[1], BANK_THRESHOLD))
                bank_screenPoint = wincap.get_screen_position(bank_confidence[0])
                bank_clickPoint = bank_action.click(bank_screenPoint, speed = speed(),wait = wait())
                #wait to get to bank
                time.sleep(.3 + abs(np.random.normal(0,.3)))
                #check if recovery worked
                screenshot = wincap.get_screenshot()
                screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
                bank_dump_confidence = bank_dump_vision.find(screenshot, threshold = BANK_DUMP_THRESHOLD, return_mode= 'confidence')
                if cv.waitKey(1) == ord('q'):
                    cv.destroyAllWindows()
                    exit()
                if bank_dump_confidence[1] > BANK_DUMP_THRESHOLD:
                    print('in_bank confidence = %s. reclick worked, continuing...' % bank_dump_confidence[1])
                    break


            if search_time > 20:
                print('PROBLEM(!) 20s+ inactivity. multiple reclicks failed. giving up, exitting...')
                exit()
        

        #this code should be redundant but I'm leaving it in anyway for debugging
        
        if bank_dump_confidence[1] < BANK_DUMP_THRESHOLD:
            print('bank_dump_confidence %s | BANK_DUMP_THRESHOLD %s | Exiting...' %( bank_dump_confidence[1], BANK_DUMP_THRESHOLD))
            exit()
        else:
            print('bank_dump_confidence %s | BANK_DUMP_THRESHOLD %s | Continuing...' %( bank_dump_confidence[1], BANK_DUMP_THRESHOLD))
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        bank_dump_confidence = bank_dump_vision.find(screenshot, threshold = BANK_DUMP_THRESHOLD, return_mode= 'confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        bank_dump_screenPoint = wincap.get_screen_position(bank_dump_confidence[0])
        bank_dump_clickPoint = bank_dump_action.click(bank_dump_screenPoint, speed = speed(),wait = wait())

        tick_dropper()

        #take two rune
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        rune_confidence = rune_vision.find(screenshot, threshold = RUNE_THRESHOLD, debug_mode= 'rectangles', return_mode= 'confidence')
        if rune_confidence[1] < RUNE_THRESHOLD:
            print('rune confidence %s | RUNE_THRESHOLD %s | Exiting...' %( rune_confidence[1], RUNE_THRESHOLD))
            exit()
        else:
            print('rune confidence %s | RUNE_THRESHOLD %s | Continuing...' %( rune_confidence[1], RUNE_THRESHOLD))
        rune_screenPoint = wincap.get_screen_position(rune_confidence[0])
        rune_clickPoint = rune_action.click(rune_screenPoint, speed = speed(),wait = wait())
        time.sleep(abs(np.random.normal(.14,.01)))
        pyautogui.click()  
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()
        
        
        tick_dropper()


        #take three weed
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        weed_confidence = weed_vision.find(screenshot, threshold = WEED_THRESHOLD, debug_mode= 'rectangles', return_mode= 'confidence')
        if weed_confidence[1] < WEED_THRESHOLD:
            print('weed confidence %s | WEED_THRESHOLD %s | Exiting...' %( weed_confidence[1], WEED_THRESHOLD))
            exit()
        else:
            print('weed confidence %s | WEED_THRESHOLD %s | Continuing...' %( weed_confidence[1], WEED_THRESHOLD))
        weed_screenPoint = wincap.get_screen_position(weed_confidence[0])
        weed_clickPoint = weed_action.click(weed_screenPoint, speed = speed(), wait = wait())
        time.sleep(abs(np.random.normal(.14,.01)))
        pyautogui.click()  
        time.sleep(abs(np.random.normal(.14,.01)))
        pyautogui.click() 
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()    

        tick_dropper()

        #right click sand
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        sand_confidence = sand_vision.find(screenshot, threshold = SAND_THRESHOLD, debug_mode= 'rectangles', return_mode= 'confidence')
        if sand_confidence[1] < SAND_THRESHOLD:
            print('sand confidence %s | SAND_THRESHOLD %s | Exiting...' %( sand_confidence[1], SAND_THRESHOLD))
            exit()
        else:
            print('sand confidence %s | SAND_THRESHOLD %s | Continuing...' %( sand_confidence[1], SAND_THRESHOLD))
        sand_screenPoint = wincap.get_screen_position(sand_confidence[0])
        sand_clickPoint = sand_action.rightClick(sand_screenPoint, speed = speed())
        if cv.waitKey(1) == ord('q'):
                cv.destroyAllWindows()
                exit()    

        sleepytime = abs(np.random.normal(0,.05))
        time.sleep(sleepytime)

        #click withdraw 18
        withdraw_18_screenPoint = [sand_clickPoint[0]+WITHDRAW_18_OFFSET[0], sand_clickPoint[1]+WITHDRAW_18_OFFSET[1]]
        withdraw_18_clickPoint = withdraw_18_action.click(withdraw_18_screenPoint, speed = speed(), wait = wait())

        tick_dropper()

        #exit the bank
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        bank_x_confidence = bank_x_vision.find(screenshot, threshold = BANK_X_THRESHOLD, debug_mode= 'rectangles', return_mode= 'confidence')
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()        

        if bank_x_confidence[1] < BANK_X_THRESHOLD:
            print('bank_x confidence %s | BANK_X_THRESHOLD %s | Exiting...' %( bank_x_confidence[1], BANK_X_THRESHOLD))
            #exit()
        else:
            print('bank_x confidence %s | BANK_X_THRESHOLD %s | Continuing...' %( bank_x_confidence[1], BANK_X_THRESHOLD))
        bank_x_screenPoint = wincap.get_screen_position(bank_x_confidence[0])
        bank_x_clickPoint = bank_x_action.click(bank_x_screenPoint, speed = speed(), wait = wait())
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()        

        sleepytime = .15 + abs(np.random.normal(0,.05))
        time.sleep(sleepytime)

        #cast spell
        screenshot = wincap.get_screenshot()
        screenshot = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        spellcast_confidence = spellcast_vision.find(screenshot, threshold = SPELLCAST_THRESHOLD, debug_mode= 'rectangles', return_mode= 'confidence')
        if spellcast_confidence[1] < SPELLCAST_THRESHOLD:
            print('spellcast confidence %s | SPELLCAST_THRESHOLD %s | exitting...' %( spellcast_confidence[1], SPELLCAST_THRESHOLD))
            exit()
        else:
            print('spellcast confidence %s | SPELLCAST_THRESHOLD %s | Continuing...' %( spellcast_confidence[1], SPELLCAST_THRESHOLD))
        spellcast_screenPoint = wincap.get_screen_position(spellcast_confidence[0])
        spellcast_clickPoint = spellcast_action.click(spellcast_screenPoint, speed = speed(), wait = wait())
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit()        





        #debuggery below
        if s_or_c == 's':
            runTime = time.time() - runStart
            if runTime >= quit_after_seconds:
                print('finished after running for %s seconds' % runTime)
                exit()
            print('runtime = %s | seconds remaining = %s' %(runTime, (quit_after_seconds - runTime)))
        if s_or_c == 'c':
            global count
            count = count + 1
            if count >= quit_after_counts:
                print('finished after running %s counts. exitting.. ' % count)
                exit()
            print('count = %s | counts remaining %s' % (count, (quit_after_counts - count)))

while True:
    superglass_make()
    breakRoller.breakRoller(odds = 300, minseconds = 60, maxseconds = 200)


#!/usr/bin/env python
## Author: Brad Shepard
## Version: Aug 2 2014
## Initial commit to github

#####Imports and Setup#####
import time
import json		#for wundeground api
from time import sleep
import os
import subprocess
import urllib2					  #for reading webform settings
from datetime import datetime, timedelta          #for the time on the rpi end
from ConfigParser import SafeConfigParser
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.IN)
import sys
import gspread

#from twython import Twython
#from apscheduler.scheduler import Scheduler       #this will let us check the calender on a regular interval; may not need; 3.0 is diff API

state = 0  #state 0 = idle; state 1=play
button = True
currentChannel=1


#os.system("sudo mpd")
os.system("sudo mpc clear")      #Clear mpc playlist


parser = SafeConfigParser()                       # initiate Parser and read the configuration file
parser.read('sb.cfg')

#************************************************************************************# 
#****           Global variables: wakeup.cfg file                                ****#
#************************************************************************************# 
device = parser.get('user_settings', 'device')
email = parser.get('google_credentials', 'email')
password = parser.get('google_credentials', 'password')
#weather
wunderground_api_key = parser.get('wunderground','api')
#twitter
consumer_key = parser.get('twitter','CONSUMER_KEY')
consumer_secret = parser.get('twitter','CONSUMER_SECRET')
access_key = parser.get('twitter','ACCESS_KEY')
access_secret = parser.get('twitter','ACCESS_SECRET')


print "Configuration success"

#************************************************************************************# 
#****           User variables through Google spreadsheet                        ****#
#************************************************************************************# 

print email
print password
gc = gspread.login(email,password)
print "gspread success"
#sheet=gc.open("Stonebridge").Stations
sheet=gc.open("Stonebridge")
mainsheet=sheet.worksheet("Stations")
cell=mainsheet.find(device)


Station1=mainsheet.cell(cell.row, cell.col+1).value
print Station1
Station2=mainsheet.cell(cell.row, cell.col+2).value
print Station2
Station3=mainsheet.cell(cell.row, cell.col+3).value
Station4=mainsheet.cell(cell.row, cell.col+4).value
Station5=mainsheet.cell(cell.row, cell.col+5).value
Station6=mainsheet.cell(cell.row, cell.col+6).value


#************************************************************************************# 
#****           Function for Main Loop                            
#************************************************************************************# 
def MainLoop_func(state,button,currentChannel,channelCount):
    buttonCount=0
    time_loop_start=time.time()
    print "currentChannel = "+ str(currentChannel)
    print "channelCount = "+ str(channelCount)
    while(True):
        time_loop_diff = time.time()-time_loop_start
        if (time_loop_diff>10):
            time_loop_start=time.time()
            Twitter_check_func()
        if(button==False):
            buttonCount = buttonCount+1
	    print buttonCount
            if buttonCount > 10:
                print "###########Shutdown################"
                Shutdown(state)
                       
            if(GPIO.input(16)==True):
                buttonCount = 0
                if(state==0):
                    Startup(state)
                elif(currentChannel<channelCount):
	            currentChannel = currentChannel + 1
                    MPC_func(currentChannel)
                else:
                    currentChannel = 1
                    MPC_func(currentChannel)
        
        button = GPIO.input(16)
        print button
       
        sleep(.1)

#************************************************************************************# 
#****           Function for startup (first button press)                           
#************************************************************************************# 
def Startup(state):
    Time_func()
    Weather_func()
    currentChannel = 1
#    Twitter_func()
    MPC_func(currentChannel)
    state = 1



    MainLoop_func(state,button,currentChannel,channelCount)
#************************************************************************************# 
#****           Function for shutdown (buttonheld)                           
#************************************************************************************# 
def Shutdown(state):
    state = 0
    os.system("sudo mpc stop")
    time_spch="./speech.sh The current time is "+(datetime.now()).strftime("%I:%M")
    os.system(time_spch)
    shutdown_spch="./speech.sh Turning off radio now"
    os.system(shutdown_spch)
 
    sleep(5)
    MainLoop_func(state,button,currentChannel,channelCount)
    

#************************************************************************************# 
#****           Function to play MPC                        
#************************************************************************************# 
def MPC_func(currentChannel):
    print "MPC Function"
    os.system("sudo mpc volume 100")
    cmd = subprocess.Popen("sudo mpc play " + str(currentChannel),shell=True,stdout = subprocess.PIPE)
    print str(currentChannel) + ": " + cmd.stdout.readline()
#************************************************************************************# 
#****           Function to play current TIME                            
#************************************************************************************# 
def Time_func():
    print "Telling Time"
    time_spch="./speech.sh The current time is "+(datetime.now()).strftime("%I:%M")
    os.system(time_spch)
#************************************************************************************# 
#****           Function to check for Twitter messages                         
#************************************************************************************# 
def Twitter_check_func():
    print "Check for Twitter Messages"
    
    
#************************************************************************************# 
#****           Function to play Twitter messages                         
#************************************************************************************# 
def Twitter_func():
    print "Twitter Messages"
    api = Twython(consumer_key,consumer_secret,access_key,access_secret)
#   user_timeline = api.get_home_timeline(count=2)
    search_results = api.search(q ='eleanorgurganus', count=5)

    for tweet in search_results['statuses']:
        print 'Tweet from @%s Date: %s' % (tweet['user']['screen_name'].encode('utf-8'),tweet['created_at'])
        print tweet['id_str']
        tweettext = tweet['text'][1:]
        
        print "text is"+tweettext

        twitter_spch="./speech.sh New message "
        os.system(twitter_spch)
        twitter_spch="./speech.sh %s"%(tweettext)
        os.system(twitter_spch)


#************************************************************************************# 
#****           Function to play current WEATHER                                 ****#
#************************************************************************************# 
def Weather_func():

#           Wunderground API    :  Get weather info              #

    f = urllib2.urlopen('http://api.wunderground.com/api/'+wunderground_api_key+'/geolookup/conditions/q/NC/Wilmington.json')
    json_string = f.read()
    parsed_json = json.loads(json_string)
    location = parsed_json['location']['city']
    weather =parsed_json['current_observation']['weather']
    temp_f = parsed_json['current_observation']['temp_f']
    feelslike_f =parsed_json['current_observation']['feelslike_f']
    wind_string =parsed_json['current_observation']['wind_string']
    f.close()

    print "Weather"
    temp_spch="./speech.sh The current temperature in %s is %s Fahrenheit" % (location,temp_f)
    os.system(temp_spch)
#    temp_spch="./speech.sh The weather today will be %s"%(weather)
#    os.system(temp_spch)
#    temp_spch="./speech.sh Winds are %s"%(wind_string)
#    os.system(temp_spch)

#************************************************************************************# 
#****           Function to load URLS                                          ****#
#************************************************************************************# 
def LoadURL_func():
    
    os.system("sudo mpc add "+Station1)
    os.system("sudo mpc add "+Station2)
    os.system("sudo mpc add "+Station3)
    os.system("sudo mpc add "+Station4)
    os.system("sudo mpc add "+Station5)
    os.system("sudo mpc add "+Station6)

    #talk_news
#   os.system("sudo mpc add http://crystalout.surfernetwork.com:8001/WFMN-FM_MP3")
#   os.system("sudo mpc add http://64.78.234.173:8056")
#   os.system("sudo mpc add http://freestreams.alldigital.net:8000/freestream301")
#   os.system("sudo mpc add http://wolfstream.unr.edu:8000/")

    #music
#   os.system("sudo mpc add http://69.175.13.130:8400")  #doowop
#   os.system("sudo mpc add http://vprclassical.streamguys.net/vprclassical64.mp3")
#   os.system("sudo mpc add http://74.208.98.253:8246") #old time radio music

    #old time
#   os.system("sudo mpc add http://184.154.145.114:8097") #old radio shows

    #book
#   os.system("sudo mpc add http://74.208.98.253:8224") #radio books

    cmd = subprocess.Popen("sudo mpc playlist",shell=True, stdout=subprocess.PIPE)
    stations=cmd.stdout.readlines()

    global channelCount
    channelCount=len(stations)

    print "initial channelCount= " + str(channelCount)
    
    os.system("sudo mpc volume 0")

    index = 1
#i dont know if this is necessary
    while (index<channelCount):
        os.system("sudo mpc play " + str(index))
        index = index + 1
        sleep(3)
    os.system("sudo mpc stop")

    

#####Schedule start####

LoadURL_func()		#Call function to load URLs
MainLoop_func(state,button,currentChannel,channelCount)















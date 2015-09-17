import json
import datetime
import numpy as np
import pylab as pl
import pygmaps
import webbrowser
from pprint import pprint

def func1(alicedata):
    alice_list=[]
    with open(alicedata) as data_file:    
        for line in data_file:
            alice_list.append(json.loads(line))
    return(alice_list)

def func2(alicedata):
    alice_list=func1(alicedata)
    print("The first 10 signal entries in the file are:")
    for i in range(0,10):
        pprint(alice_list[i])

def func3(alicedata):
    alice_list=func1(alicedata)
    signals=[]
    print('Different signal names in the data file are:')
    for i in range (0,len(alice_list)):
        if alice_list[i]['name'] not in signals:
            signals.append(alice_list[i]['name'])
            print(alice_list[i]['name'])
    signal_name=input('Enter the signal name you want to find the number of occurences and range of:')
    count=0
    values=[]
    for i in range (0,len(alice_list)):
        if alice_list[i]['name']==signal_name:
            count+=1
            values.append(alice_list[i]['value'])
    r=max(values)-min(values)
    print("The no. of occurences of {0} is {1}".format(signal_name,count))
    print("The range of {0} is {1} with minimum value= {2} and maximum value= {3}".format(signal_name,r,min(values),max(values)))

def func4(alicedata):
    alice_list=func1(alicedata)
    #Calculating vehicle trip time:
    times=[]
    for i in range (0,len(alice_list)):
        times.append(alice_list[i]['timestamp'])
    max_time = datetime.datetime.fromtimestamp(max(times))
    min_time = datetime.datetime.fromtimestamp(min(times)) 
    print('The largest time stamp is for {0}'.format(max_time.strftime('%Y-%m-%d %H:%M:%S')))
    print('The smallest time stamp is for {0}'.format(min_time.strftime('%Y-%m-%d %H:%M:%S')))
    diff = max_time - min_time     
    hours = (diff.seconds) / 3600
    print ('\nThe vehicle trip time period in Hours:')
    print (str(hours) + ' Hours')
    print ('\nThe vehicle trip time period in Minutes:')
    minutes = (diff.seconds) / 60
    print (str(minutes) + ' Minutes')
    print ('\nThe vehicle trip time period in Seconds:')
    print (str(diff.seconds) + ' secs')

    #Calculating vehicle trip distance:
    distances=[]
    for i in range (0,len(alice_list)):
        if alice_list[i]['name']=='odometer':
            distances.append(alice_list[i]['value'])
    distance=distances[-1]-distances[0]
    print('\nThe vehicle trip distance over which the data was recorded is {0} miles'.format(distance))

def func5(alicedata):
    alice_list=func1(alicedata)
    signal_name=input('Enter the signal name you want a plot of:')
    signal_values=[]
    timestamps=[]
    for i in range (0,len(alice_list)):
        if alice_list[i]['name']==signal_name:
            signal_values.append(alice_list[i]['value'])
            timestamps.append(alice_list[i]['timestamp'])
    pl.plot(timestamps,signal_values)
    pl.title(signal_name)
    pl.xlabel('timestamps')
    pl.ylabel('values')
    pl.show()

def func6(alicedata):
    alice_list=func1(alicedata)
    speeds=[]
    for i in range (0,len(alice_list)):
        if alice_list[i]['name']=='vehicle_speed':
            speeds.append(alice_list[i]['value'])
    max_speed=max(speeds)
    print("Maximum speed of Alice's vehicle is {0} miles/hour".format(max_speed))
    avg_speed=sum(speeds)/len(speeds)
    print("Average speed of Alice's vehicle is {0} miles/hour".format(avg_speed))

def func7(alicedata):
    alice_list=func1(alicedata)
    latitudes=[]
    longitudes=[]
    alice_path=[]
    for i in range(0,len(alice_list)):
        if alice_list[i]['name']=='latitude':
            latitudes.append(alice_list[i]['value'])

        if alice_list[i]['name']=='longitude':
            longitudes.append(alice_list[i]['value'])

    for i in range(0,len(latitudes)):
        alice_path.append((latitudes[i],longitudes[i])) 

    mymap = pygmaps.maps(40.797997,-73.967575,14)
    mymap.addpath(alice_path,"#00FF00")
    mymap.draw('./mymap.html')

def func8(alicedata):
#To calculate the period for which Alice's car was idle
    alice_list=func1(alicedata)
    idle_times=[]
    speed_list=[]
    for i in range (0,len(alice_list)):
        if alice_list[i]['name']=='vehicle_speed':
            speed_list.append(alice_list[i])
    idle_time=0
    for i in range (1,len(speed_list)-1):
        if speed_list[i]['value']==0 and speed_list[i-1]['value']==0 and speed_list[i+1]['value']==0:
            idle_time=idle_time+(speed_list[i+1]['timestamp']-speed_list[i]['timestamp'])
    print ("\nThe period for which Alice's vehicle was idle is:")
    print (str(idle_time) + ' secs')        
    

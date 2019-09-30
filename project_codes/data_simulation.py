import requests
import json
import datetime
import random

# LIFX Data Simulation
lifx_log ='https://inf-552.firebaseio.com/project/LIFX/Log/%s.json'
switch = ['On','Off']
current = None
for i in range(0,100):
    status = random.choice(switch)
    if status == current:
        continue
    else:
        # Update Status
        stat_fb = 'https://inf-552.firebaseio.com/project/LIFX.json'
        r = requests.patch(stat_fb,data=json.dumps({"Status":status}))
    # Update count of 'off' switch  
    month = str(4)
    day = str(random.randint(1,21))
    year = 2019
    date = "%s-%s-%s" % (month,day,year)
    
    date_log = 'https://inf-552.firebaseio.com/project/LIFX/Log/%s/Count.json'%date
    r = requests.get(date_log)
    # Add Date to LIFX Log
    if json.loads(r.content) == None:
        log = 'https://inf-552.firebaseio.com/project/LIFX/Log/%s.json'%date
        r = requests.patch(log,data=json.dumps({"Count" : 1}))  
    # Update Switch Count for day
    else:
        log = 'https://inf-552.firebaseio.com/project/LIFX/Log/%s/Count.json'%date
        r = requests.get(log)
        js = json.loads(r.content,encoding = 'UTF-8')
        update = int(js) + 1
        r = requests.patch(lifx_log%date,data = json.dumps({"Count":update}))

    current = status


# NEST Data Simulation
nest_log = 'https://inf-552.firebaseio.com/project/Nest/Log.json'
current = None
for i in range(0,200):
    temp = random.randint(65,89)
    if current == temp:
        continue
    else:
        # Store Previous Temperature in Log Before updating
        month = str(4)
        day = str(random.randint(1,22))
        year = 2019
        date = "%s-%s-%s" % (month,day,year)
        
        # Check if Date Has been Added To Log and update log
        log = 'https://inf-552.firebaseio.com/project/Nest/Log/%s.json'%date
        r = requests.get(log)
        # Add Date to Nest Log
        if json.loads(r.content) == None:
            log = 'https://inf-552.firebaseio.com/project/Nest/Log.json'
            r = requests.patch(log,data=json.dumps({date : [temp]}))  
        # Update Temperature for day
        else:
            date_log = 'https://inf-552.firebaseio.com/project/Nest/Log/%s.json'
            r = requests.get(date_log%date)
            ls = json.loads(r.content,encoding = 'UTF-8')
            ls.append(temp)
            r = requests.patch(nest_log,data = json.dumps({date:ls}))
            
        # Update Current Temperature
        curr = 'https://inf-552.firebaseio.com/project/Nest.json'
        r = requests.patch(curr,json.dumps({'Current':str(temp)}))


# Ring Data Simulation
ring_log = 'https://inf-552.firebaseio.com/project/Ring/Chimes_Log/Dates.json'

# Initalize DND Node 
ring = 'https://inf-552.firebaseio.com/project/Ring.json'
r = requests.patch(ring,data = json.dumps({'Do_Not_Disturb':'On'}))
for i in range(0,200):
    month = str(4)
    day = str(random.randint(1,21))
    year = 2019
    date = "%s-%s-%s" % (month,day,year)
        
    # Check if Date Has been Added To Log and update log
    log = 'https://inf-552.firebaseio.com/project/Ring/Chimes_Log/Dates/%s.json'%date
    r = requests.get(log)
    # Add Date to Nest Log
    if json.loads(r.content) == None:
        r = requests.patch(ring_log, data=json.dumps({date:str(1)})) 
    # Update # of Cimes for Date in Log
    else:
        r = requests.get(log)
        js = json.loads(r.content,encoding = 'UTF-8') 
        update = int(js) + 1
        r = requests.patch(ring_log,data = json.dumps({date:update}))

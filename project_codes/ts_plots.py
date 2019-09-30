import pyrebase
import numpy as np
import pandas as pd
import base64
import matplotlib.pyplot as plt


# Firebase API config
config = {
    "apiKey": "AIzaSyDFjqF-fR1Lb95iHp8XeZRzwCCCoWTpDQ4",
    "authDomain": "inf-552.firebaseapp.com",
    "databaseURL": "https://inf-552.firebaseio.com",
    "projectId": "inf-552",
    "storageBucket": "inf-552.appspot.com",
    "messagingSenderId": "381457764919"}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

# NEST Log
log_values = db.child("project/Nest/Log").get()
ts_dict = {}
# Store values for last 30 days for Time Series
for elem in log_values.each()[-30:]:
    # Values for simulated
    if type(elem.val()) == type([]):
        temps = elem.val()
        
    # Values for inputted
    else:
        t = elem.val()
        temps = list(t.values())
        
    slash = elem.key().rfind('-')
    date = elem.key()[0:slash]
    ts_dict[date] = temps
# Get Mean temperature for TS plot
means = []
dates = sorted(list(ts_dict.keys()),key=lambda d: tuple(map(int, d.split('-'))))
for date in dates:
    temps = ts_dict[date]
    temps =  [int(i) for i in temps]
    means.append(np.mean(temps))
    
# Plot TS
x = dates
y = means
plt.figure(figsize=(20,10))
plt.plot(x,y,color='r')
plt.grid()
plt.title('Average Temperate Changes (Past 30 Days)',fontsize=30)
plt.xlabel('Date',fontsize=15)
plt.ylabel('Average Temperature',fontsize=15);
plt.savefig('nest_ts.jpg')

# Ring Log
log_values = db.child("project/Ring/Chimes_Log/Dates").get()
ts_dict = {}
# Store values for last 30 days for Time Series
for elem in log_values.each()[-30:]:
    slash = elem.key().rfind('-')
    date = elem.key()[0:slash]
    ts_dict[date] = elem.val()
# Get Mean temperature for TS plot
counts = []
dates = sorted(list(ts_dict.keys()),key=lambda d: tuple(map(int, d.split('-'))))
for date in dates:
    count = ts_dict[date]
    count =  int(count)
    counts.append(count)
    
# Plot TS
x = dates
y = counts
plt.figure(figsize=(20,10))
plt.plot(x,y,color='r')
plt.grid()
plt.title('# of Chimes (Past 30 Days)',fontsize=30)
plt.xlabel('Date',fontsize=15)
plt.ylabel('# Chimes',fontsize=15);
plt.savefig('ring_ts.jpg')

image_file = open('ring_ts.jpg','rb')
encoded_img = base64.b64encode(image_file.read())

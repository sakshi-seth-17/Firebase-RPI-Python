from picamera import PiCamera
import pyrebase
from datetime import datetime, timedelta
import os
from humidity import *
import firebase_admin
from firebase_admin import credentials, firestore
from userdefined import *
#from rpi import *
import time
from dht import *


'''
Ref to firebase database 
  https://www.codespeedy.com/connecting-firebase-with-python/ 
  
  
'''
cred = credentials.Certificate("db-key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

'''
    Get IP address of the Raspberry Pi
'''
def raspberryIP():
    routes = json.loads(os.popen("ip -j -4 route").read())
    for r in routes:
        if r.get("dev") == "wlan0" and r.get("prefsrc"):
            ip = r["prefsrc"]
        break
    return ip
    
'''
    Save image to firebase storage
'''

def storeImage(firebaseConfig,storageBucket):

    firebase = pyrebase.initialize_app(firebaseConfig)
    storage = firebase.storage()
    
    camera = PiCamera()
    now = datetime.now()
    dt = now.strftime("%d%m%Y%H:%M:%S")
    name = dt+".jpg"
    camera.capture(name)
    #storage.child(name).put(name)
    storage.child("{}/{}".format(storageBucket,name)).put(name)
    os.remove(name)
    camera.close()
    print("Image stored")
    return name.replace(".jpg","")
    
'''
    Store Humidity, Temperature, IP Address and Motion data in firebase database
'''
    
def storeKPI(collectionN, docName,motion):
    doc_ref = db.collection(collectionN).document(docName)
    data = getparams()  #Humidity and Temperature   
    data["motion"] = motion   #Currently set to None
    data["ipAddress"] = raspberryIP()   #IP address of the RPI
    data["thermal"] = str(getThermal()) #Thermal matrix
    doc_ref.set(data)
    print("KPI stored")


    

configData = readJson("/home/path_to/Firebase-RPI/config.json")

motion = None
while True:
    docName = storeImage(configData["firebaseConfig"],configData["storageBucket"])
    storeKPI(configData["collection"],docName,motion)
    #time.sleep(1800)
    time.sleep(5)
    
    
    '''
        For motion detection
    '''
    
    '''now = datetime.now()
    now_time = now.strftime("%H:%M")
    future = now + timedelta(hours=0, minutes=0, seconds=30)
    future_time = future.strftime("%H:%M")
    print("Current Time =", now_time)
    print("future_time =", future_time)
    
    motion = 0
    while datetime.now().strftime("%H:%M") != future_time:
        flag = geMotionData()
        if flag == 1:
            motion = 1
            time.sleep(int((future-datetime.now()).total_seconds()))'''

import time
import math
from machine import I2C, Pin

i2c = I2C(scl=Pin(22), sda=Pin(21))
#arduino_Addr = 0x8 #Die I2C Adresse des Arduino-Slaves

def byteAbfragen(addr):#
    try:
        a = int.from_bytes(i2c.readfrom(addr,1),"little")
        return a #ließt den geforderten Wert vom Arduino aus und gibt ihn zurück
    except:
        print("fehler")
        time.sleep_us(700)
        sensorenAbfragen(addr)
    
def posAbfragen(addr):
    try:
        a = int.from_bytes(i2c.readfrom(addr,4),"big")
        if a > 2147483648:
            a = a-4294967296
        return a #ließt den geforderten Wert vom Arduino aus und gibt ihn zurück
    except:
#         print("fehler")
        time.sleep_us(1000)
        posAbfragen(addr)

def sendPosCode(addr, kp, ki, kd,target):
    kp = int(kp*100)
    ki = int(ki*100)
    kd = int(kd*100)
    i2c.writeto(addr, kp.to_bytes(2,'big') + ki.to_bytes(2,'big') + kd.to_bytes(2,'big') + target.to_bytes(4, 'big'))
    


def sensorenAbfragen(addr):
    #Fragt alle Messwerte der Ultraschallsensoren des Arduinos ab
    wert=0
    sensorValues = list(range(7))
    while wert < 255:
        wert = byteAbfragen(addr)
        if type(wert) != type(5):
            print("Hier")
            wert = 0
    for i in range(7):
        try:
            sensorValues[i] = byteAbfragen(addr)
        except:
            sensorenAbfragen(addr)
    for i in range(7):
        if sensorValues[i] == None:
            sensorenAbfragen(addr)
    return sensorValues

def sprung(addr,kp,ki,kd,impuls):
    sendPosCode(addr,kp,ki,kd,impuls)
    time.sleep(4)
    sendPosCode(addr,kp,ki,kd,0)
    time.sleep(3)
    sendPosCode(addr,0,0,0,0)
    
def calibrate(addr, kkrit, errorTry = 5, calibrateErrorTime = 4, calibrateTarget = 1000, calibrateInterval = 3, calibrateKkritIncrement = 1):
    
    sendPosCode(addr,kkrit,0,0,calibrateTarget);
    for i in range(errorTry):
        time.sleep(0.5)
        val = checkIfStable(addr, kkrit, errorTime = calibrateErrorTime,target = calibrateTarget, interval = calibrateInterval, kkritIncrement = calibrateKkritIncrement)
        if val[0] == True:
            kkrit = val[1]
            sendPosCode(addr,8.4,89.176,0.190,0)
            time.sleep(3)
            sendPosCode(addr,kkrit,0,0,calibrateTarget)
        else:
            kkrit = val[1]
            break
            
            
    
    tkrit = measureTkrit(addr, target = calibrateTarget, errorTime = calibrateErrorTime, interval = calibrateInterval)    
    time.sleep(1)
    sendPosCode(addr,8.4,89.176,0.190,0)
    time.sleep(3)
    sendPosCode(addr,0,0,0,0)
    try:
        kr = 0.6*kkrit
        ki = kr/(0.5*tkrit)
        kd = kr * 0.12 * tkrit
        return [kkrit,tkrit,kr,ki,kd]
    except:
        print("Error at Kkrit: ", kkrit)

def checkIfStable(addr,kkrit,target = 1000, interval = 3, errorTime = 4 , measureInterval = 10000, kkritIncrement = 1):
    start = time.ticks_us()
    lastVal = posAbfragen(addr)
    time.sleep_us(measureInterval)
    while time.ticks_diff(time.ticks_us(),start) < 1000 * 1000 * errorTime:
        newVal = posAbfragen(addr)
        if newVal <= target + interval and newVal >= target -interval and abs(newVal-lastVal) <= 1:
            kkrit += kkritIncrement
            return [True,kkrit]         
        time.sleep_us(measureInterval)
        lastVal = newVal
    return [False, kkrit]

def measureTkrit(addr, target = 1000, interval = 3, errorTime = 4 , measureInterval = 1):
    start = time.ticks_us()
    counter = 0
    lastVal = posAbfragen(addr)
    tkrit = [None,None,None,None,None,None,None,None,None,None,None]
    time.sleep_us(measureInterval)
    while counter < 11 and time.ticks_diff(time.ticks_us(),start) < 1000 * 1000 * errorTime:
        newVal = posAbfragen(addr)
        if newVal <= target + interval and newVal >= target -interval and abs(newVal-lastVal) >= 1:
            tkrit[counter] = time.ticks_diff(time.ticks_us(),start) / (1000*1000)
            time.sleep(0.05)
            counter += 1
        time.sleep_us(measureInterval)
        lastVal = newVal
    try:
        tkrit = (tkrit[10]-tkrit[0])/5
        return tkrit
    except:
        tkrit = "error"
        
def alleMotoren(kp,ki,kd,target):
    for i in range(4):
        addr = i+9
        sendPosCode(addr,kp,ki,kd,target[i])
        time.sleep_us(1000)
        
def sinus(kp,ki,kd,amp,freq,pause,versuche):#
    for i in range(versuche):
        target =  [-int(amp*math.sin(freq*i)),int(amp*math.sin(freq*i)),-int(amp*math.sin(freq*i)),int(amp*math.sin(freq*i))]
        alleMotoren(kp,ki,kd,target)
        check = [False,False,False,False]
        while check != [True,True,True,True]:
            for i in range(4):
                if posAbfragen(i+9) <= target[i]+10 and posAbfragen(i+9) >= target[i]-10:
                    check[i] = True
                else:
                    check[i] = False
                    time.sleep_us(50)                    
        time.sleep_us(pause)
    alleMotoren(kp,ki,kd,[0,0,0,0])
    time.sleep(2)
    alleMotoren(0,0,0,[0,0,0,0])
    
def moveTo(steps, kp = 30,ki = 20,kd = 0,speed = 50, accuracy = 5):
    currPos = [posAbfragen(9),posAbfragen(10),posAbfragen(11),posAbfragen(12)]
    biggestVal = [0,0,0,0]
    for i in range(4):
        biggestVal[i] = steps[i]
        biggestVal[i] = abs(biggestVal[i])
    biggestVal.sort(reverse = True)
    if biggestVal[0] == 0:
        return True
    target = currPos
    for i in range(biggestVal[0]+1):
#         for n in range(4):
#             target[n] = int(steps[n]/biggestVal[0]*i+currPos[n])
        target = [int(steps[0]/biggestVal[0]*i+currPos[0]),int(steps[1]/biggestVal[0]*i+currPos[1]),int(steps[2]/biggestVal[0]*i+currPos[2]),int(steps[3]/biggestVal[0]*i+currPos[3])]
        alleMotoren(kp,ki,kd,target)
        check = [False,False,False,False]
        while check != [True,True,True,True]:
            for a in range(4):
                if posAbfragen(a+9) <= target[a]+accuracy and posAbfragen(a+9) >= target[a]-accuracy:
                    check[a] = True
                else:
                    check[a] = False
                    time.sleep_us(100)                    
        time.sleep_us(speed)

def alleMotorenAus():
    alleMotoren(0,0,0,[0,0,0,0])
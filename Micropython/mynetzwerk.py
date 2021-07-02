import network
import time
import ntptime
import socket
import webseiten
import myi2c


#ssid = "Buschbergnetzwerk"
#password = "stehtaufdemrouter"

wlan = network.WLAN(network.STA_IF)

# wlan = network.WLAN(network.STA_IF) # create station interface
# wlan.active(True)       # activate the interface
# wlan.scan()             # scan for access points
# wlan.isconnected()      # check if the station is connected to an AP
# wlan.connect(ssid, password) # connect to an AP
# wlan.config('mac')      # get the interface's MAC address
# wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

# ap = network.WLAN(network.AP_IF) # create access-point interface
# ap.config(essid='ESP-AP') # set the ESSID of the access point
# ap.config(max_clients=10) # set how many clients can connect to the network
# ap.active(True)         # activate the interface




def do_connect(ssid, password):
    start = time.ticks_ms()
    wlan.active(False)
    wlan.active(True)
    time.sleep(0.5)
    if not wlan.isconnected():
        #print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected() and start +10000 > time.ticks_ms():
            pass
    #print('network config:', wlan.ifconfig())
#     if wlan.isconnected():
#         return True
#     else:
#         return False
        
def checkVerbindung(ssid,password):
    if wlan.isconnected():
        print("SSID: " + wlan.config("essid"))
        print("IP: ", wlan.ifconfig()[0]) #(ip, subnet, gateway, dns)
        return True
    else:
        print("Keine Verbindung zum WLAN")
        print("Versuchtes Netzwerk: " + ssid)
        print("Versuchtes Passwort: " + password)
        
        return False

def setzeZeit():
    if wlan.isconnected() == True:
        ntptime.settime()
    else: print("Netzwerkfehler, RTC konnte nicht gestellt werden.")

def zeigeZeit():
    zeit = time.localtime() 
    sekunden = time.mktime(zeit) + 3600
    zeit = time.localtime(sekunden)
    print("{:02d}:{:02d}:{:02d}".format(zeit[3],zeit[4],zeit[5]) + "  " + "{:02d}.{:02d}.{:04d}".format(zeit[2],zeit[1],zeit[0]))
    return "{:02d}:{:02d}:{:02d}".format(zeit[3],zeit[4],zeit[5]) + "  " + "{:02d}.{:02d}.{:04d}".format(zeit[2],zeit[1],zeit[0])

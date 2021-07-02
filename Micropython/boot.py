# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
gc.collect()

############ Ab hier geht eigene Leistung los

# import mymatrix as m
# import myi2c
# import myroboter as mr
import datenSpeicher as ds
import gCodeInterpreter as gi
import motorKommandos as mk
import konfig

import mynetzwerk
from webseiten import startHTTP, log, daten, hp #Größtenteils nicht selbst erstellt
# import SD
import time

#default Netzwerkdaten für mein WLAN zuhause
ssid = konfig.ssid
password = konfig.password

#ssid = "Vodafone-1935"
#password = "Ug886TPuGF4aeFab"

# ssid = "AndroidAP"
# password = "passwort"

# Systemtaktzeit beim Testen
aktualisieren = True
zeitIntervall = 200 * 1000

setup = True
loop = False


def setup():
    #Mit Netzwerk Verbinden
    print("Mit WLAN Verbinden...")
    myi2c.display.fill(0)
    myi2c.displayTextLine("Mit WLAN",0)
    myi2c.displayTextLine("Verbinden...",1)
    myi2c.display.show()
    mynetzwerk.do_connect(ssid, password)
    #mynetzwerk.checkVerbindung(ssid,password)
    #time.sleep(10)
    if mynetzwerk.wlan.isconnected() == True:
        print("SSID: " + mynetzwerk.wlan.config("essid"))
        print("IP: ", mynetzwerk.wlan.ifconfig()[0]) #(ip, subnet, gateway, dns)
        myi2c.displayTextLine("SSID: ",0)
        myi2c.displayTextLine(mynetzwerk.wlan.config("essid"),1)
        myi2c.displayTextLine("IP: ",2)
        myi2c.displayTextLine(mynetzwerk.wlan.ifconfig()[0],3)
        myi2c.display.show()
    else:
        print("Keine Verbindung zum WLAN")
        print("Versuchtes Netzwerk: " + ssid)
        print("Versuchtes Passwort: " + password)
        myi2c.displayTextLine("Versuchte SSID: ",0)
        myi2c.displayTextLine(ssid,1)
        myi2c.displayTextLine("Versuchtes Passwort: ",2)
        myi2c.displayTextLine(password,3)
        myi2c.display.show()
    #time.sleep(3)

    #RTC stellen und ausgeben
    mynetzwerk.setzeZeit()
    #mynetzwerk.zeigeZeit()
    myi2c.displayTextLine(mynetzwerk.zeigeZeit()[:8],5)
    myi2c.display.show()
    
    hp.add("Homepage") #Hier können allgemeine Infos angezeigt werden
    daten.add("Daten: ") #Hier können aktuelle Fahrzeugdaten abgebildet werden
    log.add("LOG: ") #Daten LOG zum auslesen
    startHTTP() #startet den Webserver
    webrepl.start()
    
    
    setup = False
    loop = True
    return True

def loop():
    while loop:
        
        start = time.ticks_us()     
        currentMicros = time.ticks_us()
        while time.ticks_diff(time.ticks_us(),start) <= 15 * zeitIntervall:
            if aktualisieren == True:
                 if time.ticks_diff(time.ticks_us(),currentMicros) >= zeitIntervall:
                     myi2c.displayTextLine(mynetzwerk.zeigeZeit()[:8],5)
                     myi2c.werteAktualisieren()
                     currentMicros = time.ticks_us()
        break

#setup()
#loop()
    
    
def do_connect(ssid, pwd):
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(ssid, pwd)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
 
# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
 
# Attempt to connect to WiFi network
do_connect(konfig.ssid, konfig.password)
 
import webrepl
webrepl.start()

import myi2c2
# import dof_robotArm
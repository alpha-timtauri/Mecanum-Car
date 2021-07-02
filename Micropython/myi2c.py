import time
from machine import I2C, Pin

#Für den Bildschirm
#Die Bibliothiek wurde nicht sebst erstellt
from ssd1306 import SSD1306_I2C

#Für den Beschleunigungssensor
#Die Bibloithek wurde nicht selbst erstellt
from micropython_mpu6050.mpu6050 import MPU6050

#default Messwerte
temp = 21 #21°C
accel = [0,0,1] #Ein g nach unten
gyro = [0,0,0] #Keine Drehung
i2c = I2C(scl=Pin(22), sda=Pin(21))
#mpu6050_int = Pin(14, Pin.IN, Pin.PULL_UP) #Nur aktivieren, wenn ein Interrupt-Pin gewünscht ist
arduino_Addr = 0x8 #Die I2C Adresse des Arduino-Slaves
#mpu = MPU6050(i2c) #Den Beschleunigungssensor initialisieren
#display = SSD1306_I2C(128, 64, i2c) #Das Display initialisieren

#i2c.scan() #Scant alle verfügbaren I2C Geräte
#i2c.writeto(0x8,"Harald und seine 40 Räuber ") #Beispiel Write-Befehl

def werteAktualisieren():
    #Messwerte des Beschleunigungssensors aktualisieren
    newTemp = mpu.get_temp_data(i2c)
    newAccel = mpu.get_accel_data(i2c)
    newGyro = mpu.get_gyro_data(i2c)
    global temp
    global accel
    global gyro
    
    #Wenn ein Messfehler aufgetreten ist, also keine Daten empfangen werden konnten, werden die letzten Werte wiederverwendet
    if newTemp == None:
        newTemp = temp
    if newAccel == None:
        newAccel = accel
    if newGyro == None:
        newGyro = gyro

    temp = newTemp
    accel = newAccel
    gyro = newGyro
    
    displayAktualisieren()
    
def displayTextLine(text, line, pos=0):
    #Schreibt Text auf die gewünschte Line auf dem Bildschirm
    
    x = 10 * pos #x-Position
    y = (line) * 11 #y-Position
    display.fill_rect(x,y,128-10*pos,11,0) #Die angepeilte Line erst mit einem Rechteck löschen
    display.text(text,x,y) #Alles anzeigen

def displayAktualisieren():
    #Zeigt die letzten Werte des Beschleunigungssensors an
    displayTextLine("T: " + str(temp)[0:4],0)
    displayTextLine("x:" + str(accel[0])[0:4] + " a:" + str(gyro[0])[0:4],1)
    displayTextLine("y:" + str(accel[1])[0:4] + " b:" + str(gyro[1])[0:4],2)
    displayTextLine("z:" + str(accel[2])[0:4] + " c:" + str(gyro[2])[0:4],3)
    display.show()

def longAbfragen(befehl):
    #Befehl an den Arduoino senden, der eine Zahl zurückverlangt
    
    i2c.writeto(arduino_Addr,befehl) #Fragt nach bestimmtem Wert
    time.sleep_us(10000) #Warten bis der Arduino vom Empfangs- in den Sendemodus wechselt
    return int.from_bytes(i2c.readfrom(arduino_Addr,4),"little") #ließt den geforderten Wert vom Arduino aus und gibt ihn zurück

def entfernungenAbfragen():
    #Fragt alle Messwerte der Ultraschallsensoren des Arduinos ab
    
    entfernungen = list(range(6))
    for i in range(6):
        entfernungen[i] = longAbfragen("entfernung" + str(i) + " ")
    return entfernungen

def voltageAbfragen():
    #Fragt den Akustand in Volt ab
    voltage = longAbfragen("voltage ")/1000
    return voltage

def geschwindigkeitAendern(motorNummer, veloPhi):
    #Ändert die eingespeicherte Geschwindigkeit für einen Motor am Arduino
    
    veloPhi = abs(veloPhi) #Nur positive Geschwindigkeiten sind erlaubt. Richtungskommandos werden extra gesendet
    i2c.writeto(arduino_Addr,"f" + str(motorNummer) + " ") #Ankündigungskommando für den Arduino
    time.sleep_us(100000)
    i2c.writeto(arduino_Addr,str(veloPhi) + " ") #Ausführungskommando
    time.sleep_us(100000)
    
def motor(motorNummer, geschwindigkeit):
    #Sendet eine Fahrbefehl für einen Motor an den Arduino
    
    #Richtung feststellen
    if geschwindigkeit < 0:
        Richtung = "RW"
    else:
        Richtung = "VW"
    geschwindigkeitAendern(motorNummer, geschwindigkeit) #Ändert die vorgesehene Geschwindigkeit
    time.sleep_us(50000)
    i2c.writeto(arduino_Addr,"motor" + str(motorNummer) + Richtung + " ") #Schaltet dem Motor ein
    time.sleep_us(100000)
    
def getRichtung(geschwindigkeit):
    if geschwindigkeit < 0:
        Richtung = "RW"
    else:
        Richtung = "VW"
    return Richtung

def alleMotoren(veloPhi):
    #Sendet Fahrkommandos für alle Motoren
    #veloPhi aus motorKommandos.py wird benötigt
    i2c.writeto(arduino_Addr,"Q f " + str(abs(veloPhi[0])) + " " + str(abs(veloPhi[1])) + " " + str(abs(veloPhi[2])) + " " + str(abs(veloPhi[3])) + " " + " ")
    time.sleep_us(100000)
    i2c.writeto(arduino_Addr,"Q Motoren " + getRichtung(veloPhi[0]) + " " + getRichtung(veloPhi[1]) + " " + getRichtung(veloPhi[2]) + " " + getRichtung(veloPhi[3]) + " " + " ")
    time.sleep_us(100000)
#altes Übertragungsformat, war zu langsam
#     motor(1, veloPhi[0])
#     motor(2, veloPhi[1])
#     motor(3, veloPhi[2])
#     motor(4, veloPhi[3])
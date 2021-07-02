#sd initialisieren
import machine, os
from sdcard import sdcard
from machine import SPI, Pin

spisd = SPI(-1, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
sd = sdcard.SDCard(spisd, Pin(5))
os.mount(sd, "/sd")

######Beispielbefehle

#verfügbare Dateien auflisten
#os.listdir('/sd')

#neue Datei erstellen und darin schreiben
#myFile = open("/sd/new.txt","w")
#myFile.write("\nhello World!")
#myFile.close()

#an existierende Datei anhängen
#myFile = open("/sd/new.txt","a")
#myFile.write("\nhello World!")
#myFile.close()

#aus Datei lesen
#myFile = open("/sd/new.txt","r")
#myFile.read()
#myFile.read()
#myFile.close()

def konfigLesen(stichwort):
    #Ließt die Konfigurationsdatei aus
    #In der Datei können Informationen wie der Netzwerkname und Paswort gespeichert werden
    for n in range(len(os.listdir('/sd'))):
        #Überprüft, ob es eine Konfugurationsdatei gibt
        if os.listdir('/sd')[n] == "konfig.txt":
            konfig = open("/sd/konfig.txt","r")
            for line in konfig:
                line = konfig.readline()
                if stichwort in line:
                    line = line.split(" = ")
                    print(line)
                else:
                    print(line)
            konfig.close()
            

def sdWechsel():
    #Muss ausgeführt werden, wenn die SD Karte gewechselt wurde
    global sd
    os.umount(sd,"/sd")
    sd = sdcard.SDCard(spisd, Pin(5))
    os.mount(sd, "/sd")

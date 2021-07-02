#datenspeicher
import konfig
import gCodeInterpreter as gi
mode = konfig.kurzeDatei #Modus für kurze gCode Dateien, bei dem alle Befehlt in einer Liste gespeichert werden. Ungeeignet für große Dateien
commandList = [] #Besagte Liste

letzteZeile = 0 #Laufvariable für die letzte ausglesene Zeile in einer geöffneten Datei

filename = 'Aufrollerabdeckung - Kopie.gcode' #Name der Datei, die augelesen werden soll
f=open(filename)
def openFile():
    #Öffnet die Datei, auch wenn bereits offen
    global filename
    global f
    f=open(filename)
    global letzteZeile
    letzteZeile = 0
def gCodeLesen():
    #Ließt den gesamten Code einer Datei zeilenweise aus
    global filename
    #filename = 'Aufrollerabdeckung - Kopie.gcode'
    with open(filename) as f:
            for line in f:
                if zeileAuswerten(line) == []:
                    True
                else:
                    gCodeBefehl = zeileAuswerten(line)
                    print(gCodeBefehl)
                    gi.gCodeInQueue(gCodeBefehl)
                    gi.queueAbarbeiten(gi.queue)
                    
    f.close()            
def gCodeLine(index):
    #Die Datei muss vorher geöffnet werden
    #gezählt wird immer von der letzten ausgelesenen Zeile aus
    #Bsp.: ds.gCodeLine(213)); Ließt die Zeile 213 der Datei aus
    #      ds.gCodeLine(1)); Ließt die nächste Zeile - also 214 - aus
    #Bsp.: ds.gCodeLine(213));openFile();ds.gCodeLine(213)); Ließt zweimal die Zeile 213 aus
    global filename
    global f
    global letzteZeile
    #Wenn die benötigte Zeile bereits augelesen wurde, wird die Datei erneut göffnet
    if index <= letzteZeile:
        openFile()
    index = index-letzteZeile
    
        
    for i in range(index):
        line = f.readline()
        letzteZeile += 1
        if zeileAuswerten(line) == []:
            #Wenn in der Zeile kein bekannter Befehl steht, gib nichts zurück
            True
        elif i == index-1:
            #print(zeileAuswerten(line))
            return zeileAuswerten(line)
        else:
            True
                
                
def zeileAuswerten(line):
    #Wertet eine Zeile aus, alle relevanten gCode Befehle werden verstanden
    #Neue können aber hinzugefügt werden
    data = [] #Die Ausgabe wird vorbereitet, an diese Liste werden die Befehle angehangen, falls mehrere in einer Zeile stehen
    if ";" in line:
        #";" Zeigen Kommentare in .gCode Dateien an
        line = line.split(";")[0] #Kommentare werden entsorgt
                      
    if "F" in line:
        #"F" steht für Feedrate und wird als Geschwindigkeit interpretiert
        #Geschwindigkeitsänderungen müssen vor den Bewegungsbefehlen erkannt werden!
        global commandList
        commandListe(F(line))
        data.append(F(line))
    
    if "G00" in line or "G0" in line:
        global commandList
        commandListe(G00(line))
        data.append(G00(line))
    
    if "G01" in line or "G1" in line:
        global commandList
        commandListe(G01(line))
        data.append(G01(line))
    
    if "G02" in line:
        data.append(G02(line))
        global commandList
        commandListe(G02(line))
    
    if "G03" in line:
        data.append(G03(line))
        global commandList
        commandListe(G03(line))
        
    if "G04" in line:
        data.append(G04(line))
        global commandList
        commandListe(G04(line))
    
    if "G17" in line:
        data.append(G17())
        global commandList
        commandListe(G17())
        
    if "G21" in line:
        data.append(G21())
        global commandList
        commandListe(G21())
    
    if "G28" in line:
        data.append(G28(line))
        global commandList
        commandListe(G28(line))
        
    if "G68" in line:
        data.append(G68(line))
        global commandList
        commandListe(G68(line))
        
    if "G90" in line:
        data.append(G90())
        global commandList
        commandListe(G90())
        
    if "G91" in line:
        data.append(G91())
        global commandList
        commandListe(G91())
        
    if "G92" in line:
        data.append(G92(line))
        global commandList
        commandListe(G92(line))
    return data
                    
def commandListe(anweisung):
    #Fügt Befehle in die commandList hinzu, nur wenn mode == True für kurze Dateien
    global mode
    global commandList
    if mode == True:
        commandList.append(anweisung)

######## Es folgen die Auswertungsanweisungen für die verarbeitbaren Befehle
        #Reine "Anweisungsbefehle" werden nur als String wieder ausgegeben
        #Komplexere Befehle speichern ihre Werte zusätzlch in einer Liste, die ausgegeben wird


def G00(zeile):
    command = "G00"
    Gx = []
    Gy = []
    Gz = []
    if "X" in zeile:
        Gx = buchstabeMitZahl(zeile,"X")
        #print("x"+Gx)
    if "Y" in zeile:
        Gy = buchstabeMitZahl(zeile,"Y")
        #print("y"+Gy)
    if "Z" in zeile:        
        Gz = buchstabeMitZahl(zeile,"Z")
        #print("z"+Gz)
    #print("Print"+str([command,Gx,Gy,Gz]))
    return [command,Gx,Gy,Gz]
    
def G01(zeile):
    command = "G01"
    Gx = []
    Gy = []
    Gz = []
    if "X" in zeile:
        Gx = buchstabeMitZahl(zeile,"X")
        #print("x"+Gx)
    if "Y" in zeile:
        Gy = buchstabeMitZahl(zeile,"Y")
        #print("y"+Gy)
    if "Z" in zeile:        
        Gz = buchstabeMitZahl(zeile,"Z")
        #print("z"+Gz)
    #print("Print"+str([command,Gx,Gy,Gz]))
    return [command,Gx,Gy,Gz]
    
def G02(zeile):
    command = "G02"
    Gx = []
    Gy = []
    Gz = []
    Gi = []
    Gj = []
    if "X" in zeile:
        Gx = buchstabeMitZahl(zeile,"X")
        #print("x"+Gx)
    if "Y" in zeile:
        Gy = buchstabeMitZahl(zeile,"Y")
        #print("y"+Gy)
    if "Z" in zeile:        
        Gz = buchstabeMitZahl(zeile,"Z")
        #print("z"+Gz)
    if "I" in zeile:
        Gi = buchstabeMitZahl(zeile,"I")
        #print("i"+Gi)
    if "J" in zeile:        
        Gj = buchstabeMitZahl(zeile,"J")
    return [command,Gx,Gy,Gz,Gi,Gj]
    
def G03(zeile):
    command = "G03"
    Gx = []
    Gy = []
    Gz = []
    Gi = []
    Gj = []
    if "X" in zeile:
        Gx = buchstabeMitZahl(zeile,"X")
        #print("x"+Gx)
    if "Y" in zeile:
        Gy = buchstabeMitZahl(zeile,"Y")
        #print("y"+Gy)
    if "Z" in zeile:        
        Gz = buchstabeMitZahl(zeile,"Z")
        #print("z"+Gz)
    if "I" in zeile:
        Gi = buchstabeMitZahl(zeile,"I")
        #print("i"+Gi)
    if "J" in zeile:        
        Gj = buchstabeMitZahl(zeile,"J")
    return [command,Gx,Gy,Gz,Gi,Gj]

def G04(zeile):
    command = "G04"
    Gp = []
    Gs = []
    if "P" in zeile:
        Gp = buchstabeMitZahl(zeile,"P")
        #print("x"+Gx)
    if "S" in zeile:
        Gs = buchstabeMitZahl(zeile,"S")
        #print("y"+Gy)
    return [command,Gp,Gs]

def G17():
    command = "G17"
    return [command]

def G21():
    command = "G21"
    return [command]

def G28(zeile):
    command = "G28"
    Gx = []
    Gy = []
    Gz = []
    if "X" in zeile:
        Gx = buchstabeMitZahl(zeile,"X")
        #print("x"+Gx)
    if "Y" in zeile:
        Gy = buchstabeMitZahl(zeile,"Y")
        #print("y"+Gy)
    if "Z" in zeile:        
        Gz = buchstabeMitZahl(zeile,"Z")
        #print("z"+Gz)
    return [command,Gx,Gy,Gz]

def G68(zeile):
    command = "G68"
    Gx = []
    Gy = []
    Gz = []
    Gr = []
    if "X" in zeile:
        Gx = buchstabeMitZahl(zeile,"X")
        #print("x"+Gx)
    if "Y" in zeile:
        Gy = buchstabeMitZahl(zeile,"Y")
        #print("y"+Gy)
    if "Z" in zeile:        
        Gz = buchstabeMitZahl(zeile,"Z")
        #print("z"+Gz)
    if "R" in zeile:
        Gr = buchstabeMitZahl(zeile,"R")
    return [command,Gx,Gy,Gz,Gr]
        
def G90():
    command = "G90"
    return [command]

def G91():
    command = "G91"
    return [command]

def G92(zeile):
    command = "G92"
    Gx = []
    Gy = []
    Gz = []
    Ge = []
    if "X" in zeile:
        Gx = buchstabeMitZahl(zeile,"X")
        #print("x"+Gx)
    if "Y" in zeile:
        Gy = buchstabeMitZahl(zeile,"Y")
        #print("y"+Gy)
    if "Z" in zeile:        
        Gz = buchstabeMitZahl(zeile,"Z")
        #print("z"+Gz)
    if "E" in zeile:
        Ge = buchstabeMitZahl(zeile,"E")
    return [command,Gx,Gy,Gz,Ge]

def F(zeile):
    command = "F"
    
    return [command,buchstabeMitZahl(zeile,"F")]

def buchstabeMitZahl(zeile,strBuchstabe):
    #Eine Zeile im gCode kann aus mehreren relevanten Infos bestehen, die
    #durch ein Leerzeichen getrennt sind und mit einem zuordnenden Buchtaben
    #eingeleitet werden
    
    #Hier wird der mit dem strBuchstabe beginnende Teil der Zeile isoliert und zurückgegeben
    for i in range(len(zeile.split(' '))):
        if zeile.split(' ')[i][0] == strBuchstabe:
            wert = zeile.split(' ')[i]
    ergebnis=wert[1:];

#     if float(ergebnis) % 1 == 0:
#         return int(ergebnis)
#     else:
#         return float(ergebnis)
    if ergebnis == "":
        return []
    return float(ergebnis)

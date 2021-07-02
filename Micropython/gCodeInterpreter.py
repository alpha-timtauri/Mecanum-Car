#gCode Interpereter
import mymatrix as m
import myroboter as mr
import motorKommandos as mk
import konfig

#mode 2d == True aktiviert den 2D-Modus, hier werden die Z-Kommandos als toolHight gespeichert und es wird nur um Z rotiert
#der 2D_Modus muss im konfig.py initialisiert werden
toolHight = 0

absoluteMode = False #G90
relativeMode = True #G91

metric = True #G21

ursprung = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]] #Homing G28
absolutePos = ursprung #G92
currentPos = ursprung

feedRate = [2200] #F

xyPlane = True #Arbeitsebene G17
xzPlane = False #G18
yzPlane = False #G19




queue = []
def gCodeInQueue(gCodeBefehl):
    #gCodeBefehl muss Liste sein
    #gCode Befehl besteht aus [[F,Zahlenwert],[strGCommand,wert1,wert2,...]] oder nur [strGCommand,wert1,wert2,...] oder nur [strGCommand]
    global queue
    n = len(gCodeBefehl)
    if gCodeBefehl[0][0] == "F":
        queue.append(gCodeBefehl[0])
        queue.append(gCodeBefehl[1])
    else:
        queue.append(gCodeBefehl[0])
    
def queueAbarbeiten(schlange):
    #global queue
    if len(schlange) == 0:
        print("fertig")
    else:
        kommando = schlange.pop(0)
        print(kommando)
        befehlAusführen(kommando)
        queueAbarbeiten(schlange)
            #queueAbarbeiten(schlange)
            


def befehlAusführen(befehl):
    # Get the function from switcher dictionary
    switcher = {
        "F": F,
        "G00": G00,
        "G01": G01,
        "G02": G02,
        "G03": G03,
        "G04": G04,
        "G17": G17,
        "G21": G21,
        "G28": G28,
        "G68": G68,
        "G90": G90,
        "G91": G91,
        "G92": G92,
    }   
    func = switcher.get(befehl[0], lambda: "Invalid command")
    # Execute the function
    if len(befehl) == 1:
        return func()
    else:
        print(befehl[1:])
        return func(befehl[1:])
    
def leereListeWird0(werteListe):
    #manche Befehle können nicht mit leeren Einträgen in einer Liste arbeiten. Dafür deren [] Ausdrücke durch Nullen ersetzt
    for i in range(len(werteListe)):
        if werteListe[i] == []:
            werteListe[i] = 0
    return werteListe

def F(wert):
    #wert = leereListeWird0(wert)
    global feedRate
    feedRate = wert
    print("feedRate = "+str(feedRate))

def G00(werte):
    G01(werte)
    
def G01(werte):
    global currentPos
    if konfig.mode2d == True: #Höhe des Tools im 2D-Modus
        global toolHight
        if absoluteMode == True and relativeMode == False:
            for i in range(len(werte)):
                if werte[i] == []:
                    werte[i] = currentPos[i][3]
            toolHight = werte[2]
        else:
            werte = leereListeWird0(werte)
            toolHight += werte[2]
            
        newPos = mr.awtohm([[werte[0]],[werte[1]],[0]])
        newPos = absoluteToRelative(newPos) #Falls der absolut-Modus aktiv ist, wird die benötigte neue newPos umgerechnet 
    else:
        newPos = mr.awtohm([[werte[0]],[werte[1]],[werte[2]]])
        newPos = absoluteToRelative(newPos) #Falls der absolut-Modus aktiv ist, wird die benötigte neue newPos umgerechnet 
    estimatetPos = m.matmul(currentPos,newPos)
    mk.motorKommandos(newPos) ########### HIER! Muss zum Testen des Programms auskommentiert werden, wenn keine Motoren angechlossen sind!
    currentPos = estimatetPos
    print(currentPos)
    
def G02(werte):
    #Motorkommandos
    print("G02 wird nicht unterstützt")
    
def G03(werte):
    #Motorkommandos
    print("G03 wird nicht unterstützt")

def G04(werte):
    #Warten
    werte = leereListeWird0(werte)
    time.sleep_ms(werte[0])
    time.sleep(werte[1])

def G17():
    global xyPlane
    global xzPlane
    global yzPlane
    xyPlane = True
    xzPlane = False
    yzPlane = False
    
def G21():
    global metric
    metric =  True
    
def G28(werte):
    G01(werte)
    if(currentPos != m.ones(4)):
        unformatiert = mr.hmtoaw(mr.matrixInverse(currentPos))
        G01([unformatiert[0][0],unformatiert[1][0],unformatiert[2][0]])
    
def G68(werte):
    werte = leereListeWird0(werte)
    if werte[0:3] != [0,0,0]:
        print("nur Drehungen um die aktuelle Position werden unterstützt")
    else:
        newPos = mr.awtohm([[0],[0],[werte[3]]])
        newPos = absoluteToRelative(newPos) #Falls der absolut-Modus aktiv ist, wird die benötigte neue newPos umgerechnet 
        global currentPos
        estimatetPos = m.matmul(currentPos,newPos)
        mk.motorKommandos(newPos)
        currentPos = estimatetPos
        print(currentPos)

def G90():
    global absoluteMode
    global relativeMode
    absoluteMode = True #G90
    relativeMode = False #G91
    
def G91():
    global absoluteMode
    global relativeMode
    absoluteMode = False #G90
    relativeMode = True #G91
    
def G92(werte):
    print("G92 wird nicht unterstützt")
    
def absoluteToRelative(absoluteNewPos):
    #Muss im absoluten Modus (G90) benutzt werden und wandelt die angegebenen alsoluten Befehle in relative um
    if absoluteMode == True and relativeMode == False:
        global currentPos
        relativeNewPos = m.matmul(m.matmul(ursprung,mr.matrixInverse(currentPos)),absoluteNewPos)
        #currentPos = m.matmul(currentPos,relativeNewPos)
        return relativeNewPos
    else:
        return absoluteNewPos
        
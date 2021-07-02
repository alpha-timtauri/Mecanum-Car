#myRoboter
#enthält alle nötigen Funktionen für den Umgang mit Positiondaten im Matrixverfahren

import math
import mymatrix
import konfig

#Einheitsvektoren 3d
e1 = [[1],[0],[0]]
e2 = [[0],[1],[0]]
e3 = [[0],[0],[1]]

#EInheitsvektoren 2d
ex = [[1],[0]]
ey = [[0],[1]]

#Trigonometrische Funktionen mit Winkeln in Grad
def s(grad):
    return math.sin(grad * math.pi / 180)

def c(grad):
    return math.cos(grad * math.pi / 180)

def t(grad):
    return math.tan(grad * math.pi / 180)

def aS(wert):
    return math.asin(wert)*180/math.pi

def aC(wert):
    return math.acos(wert)*180/math.pi

def aT(wert):
    return math.atan(wert)*180/math.pi

#Rotationsmatrizen
def rotX(phi):
    ergebnis = [[1,0,0],[0,c(phi),-s(phi)],[0,s(phi),c(phi)]]
    return ergebnis
    
def rotY(phi):
    ergebnis = [[c(phi),0,s(phi)],[0,1,0],[-s(phi),0,c(phi)]]
    return ergebnis
    
def rotZ(phi):
    ergebnis = [[c(phi),-s(phi),0],[s(phi),c(phi),0],[0,0,1]]
    return ergebnis

def rot(vektor3x1): #Reihenfolge: XYZ
    ergebnis = mymatrix.matmul(mymatrix.matmul(rotX(vektor3x1[0][0]),rotY(vektor3x1[1][0])),rotZ(vektor3x1[2][0]))
    return ergebnis

def rot2d(phi):
    ergebnis = [[c(phi),-s(phi)],[s(phi),c(phi)]]
    return ergebnis

def hmtoaw(matrix):
    #Wandelt homogene Matrizen in Achs-Winkel Vektoren um
    
    #3d
    if mymatrix.size(matrix) == [4,4]:
        if konfig.mode2d == False:
            print("Unfertig! Funktioniert noch nicht")
            
            for n in  range(3):
                ergebnis[n][0] = matrix[n][3] #X,Y,Z werden eingetragen
            return ergebnis
        
        elif konfig.mode2d == True:
            ergebnis = mymatrix.zeros(6,1) #Ergebnisvektor wird aufgespannt
            ergebnis[5][0] = aC(matrix[0][0]) #Winkel wird eingetragen
            for n in  range(3):
                ergebnis[n][0] = matrix[n][3] #X,Y,Z werden eingetragen
            return ergebnis
    
    #2d
    elif mymatrix.size(matrix) == [3,3]:
        ergebnis = mymatrix.zeros(3,1) #Ergebnisvektor wird aufgespannt
        ergebnis[2][0] = aC(matrix[0][0]) #Winkel wird eingetragen
        for n in  range(2):
            ergebnis[n][0] = matrix[n][2] #X,Y,Z werden eingetragen
        return ergebnis
    else:
        print("Dimensionsfehler")

def awtohm(vektor):
    #Achs-Winkel Vektor wird in homogene Matrix umgewandelt
    
    #3d und mode2d aus
    if mymatrix.size(vektor) == [6,1]:
        ergebnis = homogeneMatrix(rot(vektor[3:]),[[vektor[0][0]],[vektor[1][0]],[vektor[2][0]]])
        return ergebnis
    
    elif mymatrix.size(vektor) == [3,1]:
        #3d aber mode2d an
        if konfig.mode2d == False:
            ergebnis = homogeneMatrix(rot2d(vektor[2][0]),[[vektor[0][0]],[vektor[1][0]]])
            return ergebnis
        #2d
        elif konfig.mode2d == True:
            ergebnis = homogeneMatrix(rotZ(vektor[2][0]),[[vektor[0][0]],[vektor[1][0]],[0]])
            return ergebnis
    else:
        print("Dimensionsfehler")

def homogeneMatrix(rot,trans):
    #erstellt eine homogene Matrix aus einer Rotationsmatrix und einem Translationsvektor
    
    #3d
    if mymatrix.size(rot) == [3,3] and mymatrix.size(trans) == [3,1]:
        ergebnis = mymatrix.ones(4)
        for n in  range(3):
            for m in range(3):
                ergebnis[n][m] = rot[n][m]
            ergebnis[n][3] = trans[n][0]
        return ergebnis
    #2d
    elif mymatrix.size(rot) == [2,2] and mymatrix.size(trans) == [2,1]:
        ergebnis = mymatrix.ones(3)
        for n in  range(2):
            for m in range(2):
                ergebnis[n][m] = rot[n][m]
            ergebnis[n][2] = trans[n][0]
        return ergebnis
    else:
        print("Dimensionsfehler")

def matrixInverse(a):
    #berechnet die inverse, aber nur von einer homogenen Matrix
    
    rang = mymatrix.size(a)[0]
    #Ergebnismatrix erzeugen
    rotTrans = mymatrix.zeros(rang-1,rang-1)
    #Rotationsmatrix abgreifen und direkt tranponieren
    for n in  range(rang-1):
        for m in range(rang-1):
            rotTrans[n][m] = a[m][n]
    #Einzelvektoren abgreifen
    #dafür die letzte Zeile der Matrix löschen und dann transponieren
    zwischenMatrix = mymatrix.zeros(rang-1,rang)
    #Rotationsmatrix abgreifen und direkt tranponieren
    for n in  range(rang-1):
        for m in range(rang):
            zwischenMatrix[n][m] = a[n][m]
    vektorMatrix = mymatrix.mattrans(zwischenMatrix)    
    
    inverse = mymatrix.zeros(rang,rang)
    #Rotationsmatrix abgreifen und direkt tranponieren
    for n in  range(rang-1):
        for m in range(rang-1):
            inverse[n][m] = rotTrans[n][m]
        for m in range(rang):
            inverse[rang-1][m] = 0
        inverse[rang-1][rang-1] = 1
        for n in range(rang-1):
            inverse[n][rang-1] = -mymatrix.skalarProdukt(mymatrix.mattrans(vektorMatrix[n]),mymatrix.mattrans(vektorMatrix[rang-1]))
    return inverse


# def armPosAngletoCart(vektor4x1):
#     servoAuto0pos = mymatrix.ones(4)
#     servo01pos = awtohm([[0],[0],[23.5],[0],[0],[vektor4x1[0][0]]])
#     servo12pos = awtohm([[80],[0],[0],[0],[0],[-vektor4x1[0][0]]])
#     gelenk2pos = awtohm([[0],[80],[0],[0],[0],[vektor4x1[0][0]]])
#     gelenk3pos = awtohm([[0],[65],[0],[-90],[-90],[0]])
#     pos0TCP = mymatrix.ones(4)
#     
#     pos0TCP = mymatrix.matmul(pos0TCP,servoAuto0pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,servo01pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,servo12pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,gelenk2pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,gelenk3pos)
#     
#     return pos0TCP
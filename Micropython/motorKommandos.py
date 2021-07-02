#motorKommandos
import math
import myroboter as mr
import mymatrix as m
import gCodeInterpreter as gi
import myi2c2
from time import sleep

#Fahrzeugdefinition

#Phi1    ^X   Phi2
#        |        
#   Y<---|             
#                 
#Phi3         Phi4

#Fahrzeugwerte für das benutzt Fahrzeug in mm

l = 108 #Y-Abstand der Räder / 2
rho1 = 82 #Abstand Mittelpunkt zur Hinterachse 
rho2 = 82 #Abstand Mittelpunkt zur Vorderachse
R = 40 #Radius der Räder
pulsePerRotation = 660
pulsePerMM = pulsePerRotation / (math.pi * 2 * R)


veloXY = [0,0,0] #[vx,vy,vPsi] Bewegungsgeschwindigkeit vom Fahrzeugmittelpunkt aus
veloPhi = [0,0,0,0] #Drehgeschwindigkeiten der Räder


def motorKommandos(bewegungsMatrix):
    #Führt die Motorkommandos aus, die für eine Bewegung notwendig sind
    
    aw = mr.hmtoaw(bewegungsMatrix) #Umwandlung in Achs-Winkel Vektor
    polKoord = m.cart2pol([aw[0][0],aw[1][0]]) #X und Y in Polarkkordinaten angeben
    #Rotationswinkel speichern
    if len(aw) == 6:
        psi = aw[5][0]
    elif len(aw) == 3:
        psi = aw[2][0]
    if psi == 0 and polKoord[0] == 0:
        pass
    else:
        if psi == 0: #Reine Translationsbewegung
            timeToMove = polKoord[0] / gi.feedRate[0] #in Sekunden
        elif polKoord[0] == 0: #Reine Rotationsbewegung
            timeToMove == math.radians(psi) * R / gi.feedRate[0] #in Sekunden
        else: #Alles andere wird nicht unterstützt
            True
        global veloXY
        veloXY = [aw[0][0]*pulsePerMM,aw[1][0]*pulsePerMM,math.radians(psi)*pulsePerMM] #Alle einträge berechnen
        global veloPhi    
        veloPhi = VeloPhi(veloXY)
        myi2c2.moveTo(veloPhi)
        #myi2c.alleMotoren(veloPhi) #Befehle an den Arduino senden
        #sleep(timeToMove) #warten bis die Zeit um ist
        #veloXY = [0,0,0]
        #veloPhi = VeloPhi(veloXY)

        #myi2c.alleMotoren(veloPhi) #Anhalten befehlen
        sleep(1)
    
def VeloPhi(VeloXY):
    #berechnet die nötigen drehgschwindigkeiten der einzelnen Motoren über die kinematischen Beziehungen
    
    steps1 = int((VeloXY[0] - VeloXY[1] - (l+rho2) * VeloXY[2]) )
    steps2 = int((VeloXY[0] + VeloXY[1] + (l+rho2) * VeloXY[2]) )
    steps3 = int((VeloXY[0] + VeloXY[1] - (l+rho1) * VeloXY[2]) )
    steps4 = int((VeloXY[0] - VeloXY[1] + (l+rho1) * VeloXY[2]) )
    return [steps2,steps1,steps3,steps4] #Reihenfolge ergiebt sich aus der Motoranordnung auf der Leiterplatte

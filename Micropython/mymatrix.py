#mymatrix
#Enthält alle benötigten mathematischen Operationen
import cmath
import math
def size(a):
    #Gibt die Höhe und Breite einer Matrix zurück
    if type(a[0]) == int or type(a[0]) == float:
        currentsize = [1,len(a)]
    else:
        currentsize = [len(a),len(a[0])]
    #print ("Höhe" );print (len(a));  print("Breite");  print(len(a[1]))
    return currentsize

def matmul(a,b):
    #Einfache MAtrixmultiplikation
    if size(a)[1] != size(b)[0]:
        print("Dimensionsfehler")
    else:
        #leere Ergebnismatrix erstellen
        ergebnis = list(range(size(a)[0]))
        for i in range(len(ergebnis)):
            ergebnis[i] = list(range(size(b)[1]))

        #Multiplikation durchführen
        for n in  range(size(ergebnis)[0]):
            for m in range(size(ergebnis)[1]):
                ergebnis[n][m] = zwischenergebnis(n,m,a,b)
    return ergebnis

def zwischenergebnis(posZ, posS, zeile, spalte):
    #Zwischenergebnis berechnen an jeder Stelle der Ergebnismatrix
    #"zeile" und "spalte" sind jeweils die zu multiplizierenden Matrizen
    zwischenergebnis = 0
    for k in range(size(zeile)[1]):
        zwischenergebnis += zeile[posZ][k]*spalte[k][posS]
    return zwischenergebnis

def zeros(a,b):
    #Matrix aus "Nullen" erstellen
    
    #Matrix erzeugen
    ergebnis = list(range(a))
    for i in range(a):
        ergebnis[i] = list(range(b))
    
    #Nullen einfügen
    for n in  range(size(ergebnis)[0]):
        for m in range(size(ergebnis)[1]):
            ergebnis[n][m] = 0
    return ergebnis
                
def ones(a):
    #Symetrische Matrix im Einsen auf der Hauptdiagonalen erstellen
    
    #Matrix erstellen
    ergebnis = zeros(a,a)
    
    #Matrix leeren
    for n in  range(a):
        ergebnis[n][n] = 1
    return ergebnis

def mattrans(a):
    #Transponieren
    
    #Ergebnismatrix erzeugen
    ergebnis = zeros(size(a)[1],size(a)[0])
    if size(a)[0] == 1:
        for m in range(size(ergebnis)[0]):
            ergebnis[m][0] = a[m]
    #Transponieren
    else:
        for n in  range(size(ergebnis)[0]):
            for m in range(size(ergebnis)[1]):
                ergebnis[n][m] = a[m][n]
    return ergebnis

def speedMatrix(a):
    #Funktion um schnell und unkompliziert eine quadratsche Matrix zum testen zu erstellen
    #a ist ein Zeilenvektor, der in eine quadratische Matrix aufgebrochen wird
    #Möglich sind 2x2, 3x3 und 4x4 Matrizen
    
    if len(a)==4:
        ergebnis = zeros(2,2)
        i=0
        for n in  range(2):
            for m in range(2):
                ergebnis[n][m] = a[i]
                i+=1
        return ergebnis
    elif len(a)==9:
        ergebnis = zeros(3,3)
        i=0
        for n in  range(3):
            for m in range(3):
                ergebnis[n][m] = a[i]
                i+=1
        return ergebnis
    elif len(a)==16:
        ergebnis = zeros(4,4)
        i=0
        for n in  range(4):
            for m in range(4):
                ergebnis[n][m] = a[i]
                i+=1
        return ergebnis
    else:
        print("Der Vektor hat die falsche Länge. Es können nur 2x2, 3x3 oder 4x4 Matrizen erstellt werden.")

def skalarProdukt(a,b):
    #Berechnet das Skalarprodunkt von zwei Spalten-Vektoren
    
    if (size(a)[0] != size(b)[0]) or (size(a)[1] != 1) or (size(b)[1] != 1):
        print("Dimensionsfehler")
    else:
        ergebnis = 0
        for i in range(size(a)[0]):
            ergebnis += a[i][0] * b[i][0]
        return ergebnis
    
def pol2cart(werte):
    #Wandelt 2d Polarkoordinaten in kartesische Koordinaten um
    
    x = werte[0] * math.cos(math.radians(werte[1]))
    y = werte[0] * math.sin(math.radians(werte[1]))
    return[x, y]
    
def cart2pol(werte):
    #Wandelt 2d karteschische Koordinaten in Porlarkoordinaten um
    
    """returns r, theta(degrees)
    """
    r = (werte[0] ** 2 + werte[1] ** 2) ** .5
    theta = math.degrees(math.atan2(werte[1],werte[0]))
    return [r, theta]

def eliminate(r1, r2, col, target=0):
    #Funktion für den Gauss
    
    fac = (r2[col]-target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]

def gauss(a):
    #Normaler Gauss für die Inverse
    
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i+1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                raise ValueError("Matrix is not invertible")
        for j in range(i+1, len(a)):
            eliminate(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminate(a[i], a[j], i)
    for i in range(len(a)):
        eliminate(a[i], a[i], i, target=1)
    return a

def inverse(a):
    #Normale Inversenberechnung
    #Funktioniert nicht immer bei homognen Matrizen, dafür wird die entsprechende Funktion aus mymatrix.py verwendet
    
    tmp = [[] for _ in a]
    for i,row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [0]*i + [1] + [0]*(len(a)-i-1))
    gauss(tmp)
    ret = []
    for i in range(len(tmp)):
        ret.append(tmp[i][len(tmp[i])//2:])
    return ret


def getMatrixMinor(m,i,j):
    #Funktion für den Gauss
    
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #Berechnet die Determinante einer Matrix
    
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant
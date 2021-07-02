#robotArm
import mymatrix
import myroboter
from konfig import servo0_offset, servo1_offset, servo2_offset
from myi2c import i2c
from time import sleep, sleep_ms
import servo


servos = servo.Servos(i2c, min_us = 500)
lastPos = [87, 0, 170, 180]


servos.position(2,170)
sleep(0.5)
servos.position(1,0)
sleep(0.5)
servos.position(3,180)
servos.position(0,87)
sleep(1)

def roboPos(nummer):
    
    # Get the function from switcher dictionary
    switcher = {
        0: pos0,
        1: pos1,
        2: pos2,
        3: pos3,
        4: pos4,
        5: pos5,
        6: pos6,
        100: clawClosed,
        101: clawOpen,
    }   
    func = switcher.get(nummer, lambda: "Invalid command")
    # Execute the function
    return func()    
    
def pos0():
    moveTo(1,0,15)
    moveTo(2,170,15)

def pos1():
    moveTo(1,0,15)
    moveTo(2,130,15)
    
def pos2():
    moveTo(2,120,15)
    moveTo(1,90,15)
    
def pos3():
    moveTo(1,90,15)
    moveTo(2,45,15)
    
def pos4():
    moveTo(2,50,15)
    moveTo(1,180,15)
    
def pos5():
    moveTo(1,180,15)
    moveTo(2,120,15)
    
def pos6():
    moveTo(1,90,15)
    moveTo(2,180,15)
    
def clawClosed():
    moveTo(3,35,2)
    
def clawOpen():
    moveTo(3,180,2)
    
def clap(howOften):
    for i in range(howOften):
        clawOpen()
        clawClosed()
    clawOpen()
    
def moveTo(motor, destination, speed):
    if destination < lastPos[motor]:
        for i in range(lastPos[motor]-destination):
            servos.position(motor, lastPos[motor]-1)
            sleep_ms(speed)
            lastPos[motor] -= 1
    elif destination > lastPos[motor]:
        for i in range(destination-lastPos[motor]):
            servos.position(motor, lastPos[motor]+1)
            sleep_ms(speed)
            lastPos[motor] += 1
    
def demo():
#     pos0()
#     pos1()
#     pos0()
#     pos1()
#     pos0()
#     pos5()
#     clap(3)
#     pos0()
    
    pos2()
    pos4()
    clawClosed()
    pos3()
    moveTo(0,60,15)
    pos2()
    pos4()
    clawOpen()
    moveTo(1,100,15)
    pos2()
    pos0()
    moveTo(0,87,15)
    moveTo(0,60,15)
    pos2()
    pos4()
    clawClosed()
    moveTo(1,100,15)
    pos2()
    moveTo(0,87,15)
    pos2()
    pos4()
    clawOpen()
    moveTo(1,100,15)
    pos2()
    pos0()
    moveTo(0,87,15)


def armPosAngletoCart(vektor4x1):
    
    #Vom Fahrzeugursprung zu dem Drehpunkt von servo0
    tu0 = myroboter.awtohm([[50],[0],[32],[0],[0],[0]])
    F0 = myroboter.awtohm([[0],[0],[0],[0],[0],[vektor4x1[0][0]]])
    
    #Von servo0 zu dem Drehpunkt von servo1
    t01 = myroboter.awtohm([[0],[0],[23.5],[-90],[0],[-90]])
    F1 = myroboter.awtohm([[0],[0],[0],[0],[0],[vektor4x1[1][0]-servo1_offset]])
    
    #Von servo1 zu dem oberen Gelenk in dem servo2 dreht
    t12 = myroboter.awtohm([[80],[0],[0],[0],[0],[0]])
    F2 = myroboter.awtohm([[0],[0],[0],[0],[0],[-vektor4x1[2][0]-servo2_offset]])
    
    #Von dem Gelenk zu dem nächsten Gelenk
    t23 = myroboter.awtohm([[-80],[0],[0],[0],[0],[vektor4x1[2][0]]])
    
    #Von dem Gelenk zum TCP
    t3TCP = myroboter.awtohm([[0],[65],[0],[-90],[90],[0]])
    
    
#     servoAuto0pos = myroboter.awtohm([[50],[0],[32],[0],[0],[vektor4x1[0][0]-servo0_offset]])
#     servo01pos = myroboter.awtohm([[0],[0],[23.5],[-90],[0],[-90]])
#     servo1drehung = myroboter.awtohm([[0],[0],[0],[0],[0],[vektor4x1[1][0]-servo1_offset]])
#     servo12pos = myroboter.awtohm([[80],[0],[0],[0],[0],[-vektor4x1[2][0]-servo2_offset]])
#     gelenk2pos = myroboter.awtohm([[-80],[0],[0],[0],[0],[vektor4x1[2][0]]])
#     gelenk3pos = myroboter.awtohm([[0],[65],[0],[-90],[90],[0]])
#     pos0TCP = mymatrix.ones(4)
#     
#     pos0TCP = mymatrix.matmul(pos0TCP,servoAuto0pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,servo01pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,servo1drehung)
#     pos0TCP = mymatrix.matmul(pos0TCP,servo12pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,gelenk2pos)
#     pos0TCP = mymatrix.matmul(pos0TCP,gelenk3pos)

    pos0TCP = mymatrix.ones(4)
    pos0TCP = mymatrix.matmul(pos0TCP,tu0)
    pos0TCP = mymatrix.matmul(pos0TCP,F0)
    pos0TCP = mymatrix.matmul(pos0TCP,t01)
    pos0TCP = mymatrix.matmul(pos0TCP,F1)
    pos0TCP = mymatrix.matmul(pos0TCP,t12)
    pos0TCP = mymatrix.matmul(pos0TCP,F2)
    pos0TCP = mymatrix.matmul(pos0TCP,t23)
    pos0TCP = mymatrix.matmul(pos0TCP,t3TCP)

    return pos0TCP
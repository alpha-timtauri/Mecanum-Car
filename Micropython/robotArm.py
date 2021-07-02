import mymatrix
import myroboter

servo0_offset = -87
servo1_offset = 45
servo2_offset = -60
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
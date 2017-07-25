
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


import sys
import numpy
from numpy.linalg import inv
import math
import time

import lib.shader as sh
import lib.viewpoint as vp
import lib.matrix as matrix
import lib.parser as parser
import lib.overall as overall
import lib.drawExpe as draw
import lib.expe as libExpe

import lib.teston as teston


test = False #to display .obj or experience
expe = False

pdpE = False #to enable pdp on cursor or not
start = False #if the experience is starting => True, else False
initDone = False #indicate if the the shader have been already created
techAdapt = False #indicate if the score must be store for user adaption time

targetOrder = [0, 4, 8, 3, 7, 2, 6, 1, 5, 0] #the ISO order of targets

picture_vbos, pointing_vbos, target_vbos = None, None, None
pi_shader, po_shader, ta_shader = None, None, None

vertic_picture = [] #array to store picture (.obj or expe environment)
norm_picture = []

vertic_picture_down = [] #array of go down environment
norm_picture_down = []

vertic_picture_up = [] #array of rising environment
norm_picture_up = []

vertic_target = [] #array of targets
norm_target = []
color_target = []

numExpe = 0 #the array index of experience array
expeArray = [] #all random configurations by technique

nameFile = None #name of .obj (test)
name = None #name of user (expe)

mouse = numpy.array([0, 0, None, None, 0, 0]) #informations about mouse
tech_feedback = numpy.array([]) #

angleRot = 0.0
thetaCible = 0.0
heightCible = 0.0

amplitudeCible = 0 #radius between 2 targets consecutive in ISO order
rayonCible = 0
nbCibles = 0
envCenter = [0,0,0]
env_haut_bas = 0 #indicate if the ring R must be low(=0) or high(=height)
hauteur = 0 #height of rings and targets high 
nbAnneaux = 0
symetrieCible = 0 #-1 for left targets high OR 1 for right targets high

nbClicError = 0
nbClicOnTarget = 0
t1 = 0
nbRepetition = 5 #number of same experience
techUsed = -1 #technique wich is used

lightVec = [] #position of light

#==============================ADJUSTABLE VARIABLES==============================#
    #CAMERA
axisRot = [0, 1, 0] #Define axis of rotation
angle0 = 0 #center of arc of a circle rotation OR -1 to turn continu
arcAngle = math.pi/20 #value arc of a circle
speed = 7 # 1 => speed = pi/1000
pdp = [0., 0., 0.] # point around which one pivots at initial OR fix according to the technique
pdpClic = [0., 0., 0.]
sens = 1 #sense of rotation initial
initPosCamera = [0, 0, 0] #initial position of camera
    #WINDOW
window_w , window_h = 900, 900
    #ORDER OF VERTICES (use only for .odb format)
reverse = 1
#================================================================================#



#MVP var
class Camera:
    def __init__(self, fov = 45, ratio = 4/3, near = 0.1, far = 1000, position = [0,0,1.], looking = [0,0,0], up = [0,1,0]):
        self.fov = fov
        self.ratio = ratio
        self.near = near
        self.far = far
        self.position = position
        self.looking = looking
        self.up = up

camera = Camera(ratio = window_w/window_h, position = initPosCamera)


def createModel():
    """"""
def setParam(nameUser, tech):
    """"""
def changeVar(expeNum):
    """"""
def initLight(shaderArray, lightVec):
    """"""
def init_env():
    """initialise window param"""
def init():
    """initialise vertices of picture, declare and build the shaders
       -return : ID of program shaders"""
def projection():
    """build matrix (vec4) of projection"""
def new_object_position():
    """"""
def init_projections():
    """Intialise the camera and call shaders program"""
def mouse_intersection(mouse_x, mouse_y, camera, win_w, win_h):
    '''Computation of the intersection between the mouse ray and the scene
    We assume the viewport bottom left corner is 0, 0'''
def mouse_passive(x, y):
    """get the coord of mouse pointer when there are not other entry"""
def mouse_button(button, state, x, y):
    """"""
def keyboard(key, x, y):
    """get the touch which are pressed"""
def cursor_feedback(p):
    """get the mouse pointer to print it
    -return numpy.append(arr, z, axis=1)"""
def idle():
    """function called when there are no other event"""
def runExperience():
    """"""
def controlClicks(t):
    """"""
def display():
    """Display in real time the pointer of our pad or by eye tracking"""


#########################################
#           END OF DECLARATION          #
#########################################

def createModel():

    global vertic_picture, norm_picture, vertic_picture_up, norm_picture_up, vertic_picture_down, norm_picture_down
    global vertic_target, norm_target, color_target

    global thetaCible, env_haut_bas, envCenter, heightCible


    if test:
        #parse file in
        vertic_picture, norm_picture = parser.parse(nameFile, reverse) #the 2nd parameter is used to inverse vertices
        cameraZ = 10
        camera.position[2] = 10 #set the remoteness camera

        vertic_picture = numpy.array(vertic_picture, dtype='float32')
        norm_picture = numpy.array(norm_picture, dtype='float32')

    elif expe:
        vertic_target, norm_target = draw.drawCibles(amplitudeCible, rayonCible, hauteur, nbCibles, symetrieCible)
        color_target = draw.initTargetsColor(nbCibles)

        vertic_target = numpy.array(vertic_target, dtype='float32')
        norm_target = numpy.array(norm_target, dtype='float32')
        color_target = numpy.array(color_target, dtype='float32')

        thetaBis = libExpe.thetaBis()
        amplitudeEnv = 2 * math.cos(thetaBis) * amplitudeCible #determine amplitude of ring at width given
        vertic_picture_up,    norm_picture_up,    cameraZ = draw.drawEnv(amplitudeEnv, rayonCible*2, hauteur, nbAnneaux, 1) #rising environment
        vertic_picture_down,  norm_picture_down,  cameraZ = draw.drawEnv(amplitudeEnv, rayonCible*2, hauteur, nbAnneaux, 0) #go down environment

        vertic_picture_up = numpy.array(vertic_picture_up, dtype='float32')
        norm_picture_up = numpy.array(norm_picture_up, dtype='float32')
        vertic_picture_down = numpy.array(vertic_picture_down, dtype='float32')
        norm_picture_down = numpy.array(norm_picture_down, dtype='float32')

        x, y = libExpe.posTarget(0, amplitudeCible) #first target position
        envCenter = [x, y, 0]
        if env_haut_bas == 1: #decide the direction of the slope
            vertic_picture = vertic_picture_up
            norm_picture = norm_picture_up
        elif env_haut_bas == 0:
            vertic_picture = vertic_picture_down
            norm_picture = norm_picture_down
        env_haut_bas = 1 - env_haut_bas #inversion of environment for the next target

        vertic_picture = libExpe.mooveObject(vertic_picture, envCenter) #translate environment to be center at the 1st target
        thetaCible = libExpe.thetaTarget(targetOrder[0]) #set the thetaCible of the 1st target
        heightCible = hauteur * env_haut_bas #set the height of the 1st target
        camera.position[2] = 100 #set the remoteness camera

    return [0,cameraZ,cameraZ*2] #to set light position

def setParam():
    global expe, pdpE, name, expeArray, numExpe, techAdapt, techUsed

    #get back arguments
    techUsed = int(sys.argv[2])
    if len(sys.argv) == 3:
        techAdapt = True
        numExpeStart = 0
    elif len(sys.argv) == 4:
        techAdapt = False
        name = sys.argv[3]
        numExpeStart = 0
    elif len(sys.argv) == 5:
        techAdapt = False
        name = sys.argv[3]
        numExpeStart = int(sys.argv[4])
    else:
        print("setParam: Wrong number argument")

    
    numExpe = numExpeStart
    expe = True
    if techUsed == 0:
        pdpE = False
    elif techUsed == 1 or techUsed == 2:
        pdpE = True

    if not techAdapt:
        strTech = "T"+str(techUsed+1)
    else:
        strTech = "T"+str(techUsed+1)+"_test"
        
    expeArray = libExpe.getTabExpe(strTech, nbRepetition, techAdapt)

def changeVar(expeNum):
    global rayonCible, nbCibles, amplitudeCible, hauteur, nbAnneaux, symetrieCible

    currentExpe = expeArray[expeNum]
    amplitudeCible = currentExpe[2]
    rayonCible = currentExpe[3]/2
    nbCibles = 9
    hauteur = currentExpe[4]
    nbAnneaux = 13 #MUST BE ODD
    symetrieCible = currentExpe[5]

    #decide the level of ring at choosen amplitude
    if symetrieCible == -1:
        env_haut_bas = 1
    elif symetrieCible == 1:
        env_haut_bas = 0


def initLight(shaderArray, lightVec):
    for shader in shaderArray:
        glUseProgram(shader)
        unif_light = glGetUniformLocation(shader, 'light')
        glUniform3fv(unif_light, 1, lightVec)


def init_env():
    global angleRot
    
    glutInitDisplayString('double rgba samples=8 depth core')
    glutInitWindowSize(window_w, window_h)
    glutInitWindowPosition (1000, 0)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow('myFirstWindow')
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glEnable (GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glFrontFace(GL_CW)
    glDepthFunc(GL_LESS)
    #glutSetCursor(GLUT_CURSOR_NONE)

    if (angle0 >= 0 and angle0 <= 2*math.pi):
        angleRot = angle0
    else:
        angleRot = 0.0

    print('Environment booted')

def init():
    global picture_vbos, pointing_vbos, target_vbos

    pointer_sh_attr = [3]

    #creation of shaders
    try:
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        print('VAO created')
    except ValueError:
        print()
        print()
        print(ValueError)
        print()
        sys.exit()
    
    picture_vbos = glGenBuffers(2)
    pointing_vbos = glGenBuffers(1)
    target_vbos = glGenBuffers(3)
    
    ###picture shader###
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)
    glVertexAttribPointer(picture_vbos[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(picture_vbos[0])
    
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[1])
    glBufferData(GL_ARRAY_BUFFER, norm_picture, GL_DYNAMIC_DRAW)
    glVertexAttribPointer(picture_vbos[1], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(picture_vbos[1])
    
    picture_sh = sh.create('../shader/picture_vert.glsl',
                            None,
                            '../shader/picture_frag.glsl',
                            [picture_vbos[0], picture_vbos[1]],
                            ['position', 'normale'])
    if not picture_sh:
        exit(1)
    print('Picture shader created')
    
    ###pointer shader###
    tech_model = numpy.array([])
    glBindBuffer(GL_ARRAY_BUFFER, pointing_vbos)
    glBufferData(GL_ARRAY_BUFFER, tech_model.astype('float32'), GL_DYNAMIC_DRAW)
    glVertexAttribPointer(pointer_sh_attr[0], 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(pointer_sh_attr[0])
    
    pointer_sh = sh.create('../shader/pointer_vert.glsl',
                            None,
                            '../shader/pointer_frag.glsl',
                            pointer_sh_attr,
                            ['in_vertex'])
    if not pointer_sh:
        exit(1)
    print('Pointer shader created')

    ###targets shader###
    if expe:
        glBindBuffer(GL_ARRAY_BUFFER, target_vbos[0])
        glBufferData(GL_ARRAY_BUFFER, vertic_target, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(target_vbos[0], 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(target_vbos[0])

        glBindBuffer(GL_ARRAY_BUFFER, target_vbos[1])
        glBufferData(GL_ARRAY_BUFFER, norm_target, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(target_vbos[1], 3, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(target_vbos[1])

        glBindBuffer(GL_ARRAY_BUFFER, target_vbos[2])
        glBufferData(GL_ARRAY_BUFFER, color_target, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(target_vbos[2], 4, GL_FLOAT, GL_FALSE, 0, None)
        glEnableVertexAttribArray(target_vbos[2])

        targets_sh = sh.create('../shader/target_vert.glsl',
                               None,
                               '../shader/target_frag.glsl',
                               [target_vbos[0], target_vbos[1], target_vbos[2]],
                               ['position', 'normale', 'color'])

        if not targets_sh:
            exit(1)
        print("Targets shader created")
    else:
        targets_sh = None
    
    return picture_sh, pointer_sh, targets_sh

def projection(shader, matp, matm, mato):
    unif_p = glGetUniformLocation(shader, 'projection_mat')
    glUniformMatrix4fv(unif_p, 1, False, matp)
    
    unif_m = glGetUniformLocation(shader, 'modelview_mat')
    glUniformMatrix4fv(unif_m, 1, False, matm)
    
    unif_o = glGetUniformLocation(shader, 'object_mat')
    glUniformMatrix4fv(unif_o, 1, False, mato)

def new_object_position():
    global sens, angleRot

    if speed != 0:
        angleRot = angleRot + (speed * math.pi/1000 * (sens-0.5)*2)
        if angle0 != -1:
            if angleRot >= (angle0+arcAngle/2) or angleRot <= (angle0-arcAngle/2):
                sens = 1 - sens

    m_persp_object = matrix.pivot(axisRot, angleRot, pdp, [0,0,0])
     
    glUseProgram(pi_shader)
    projection(pi_shader, camera.persp_projection, camera.persp_modelview, m_persp_object)

    if expe:
        glUseProgram(ta_shader)
        projection(ta_shader, camera.persp_projection, camera.persp_modelview, m_persp_object)

def init_projections(po_shader):
    
    camera.ortho_projection = vp.orthographic(0, window_w, 0, window_h, 0.1, 1000)
    camera.ortho_modelview = numpy.identity(4)
    
    camera.persp_projection  = vp.perspective(camera.fov, camera.ratio, camera.near, camera.far).T
    camera.persp_modelview = numpy.array(matrix.m_lookAt(camera.position, camera.looking, camera.up))
    
    glUseProgram(po_shader)
    projection(po_shader, camera.ortho_projection, camera.ortho_modelview, None)


def mouse_intersection(mouse_x, mouse_y, camera, win_w, win_h):

    
    winZ = glReadPixels(mouse_x, mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    if winZ > 0.999:
        return [str("inf"), str("inf"), str("inf")]
    
    viewport    = [0, 0, win_w, win_h] 
    i = inv(numpy.matmul(camera.persp_projection.T, camera.persp_modelview.reshape(4,4).T))
  
    vector = numpy.array([2*(mouse_x - viewport[0])/viewport[2] - 1, 2*(mouse_y - viewport[1])/viewport[3] - 1, (2 * winZ) - 1, 1])
    p = numpy.matmul(i,vector)

    return p[0:3]/p[3]

def mouse_passive(x, y):
    global mouse

    mouse[0] = x
    mouse[1] = glutGet(GLUT_WINDOW_HEIGHT) - y
    glutPostRedisplay()

def mouse_button(button, state, x, y):
    t = time.time()
    pdpT = pdpClic
    angleRotT = angleRot

    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        if expe:
            controlClicks(t, angleRotT, pdpT)

def keyboard(key, x, y):

    if key == b'x' or key == b'X' or b'\x1b':
        overall.stopApplication()
    else:
        print("Useless key:", key)

def cursor_feedback(p_mouse):
    left    = numpy.array([1,0])
    up      = numpy.array([0,1])
    r_mouse = 5
    arr = []
    new_mouse = [0.0, 0.0]

    new_mouse[0] = (int(p_mouse[0]) - window_w/2) * camera.position[2] / window_w
    new_mouse[1] = (int(p_mouse[1]) - window_h/2) * camera.position[2] / window_h

    nb_steps = 4
    step = 2*math.pi/nb_steps
    for i in range(nb_steps):
        arr.append(p_mouse)
        arr.append(p_mouse + r_mouse*math.cos((i+1)*step)*left + r_mouse*math.sin((i+1)*step)*up)
        arr.append(p_mouse + r_mouse*math.cos(i*step)*left + r_mouse*math.sin(i*step)*up)
    
    z_mouse = numpy.zeros((len(arr),1), dtype='float32')
    return numpy.append(arr, z_mouse, axis=1)

def idle():
    glutPostRedisplay()

def showCurrentExpe():
    print("Tech :", expeArray[numExpe][0], "| ID :", expeArray[numExpe][1], "| Height :", expeArray[numExpe][4], "| No", numExpe+1,"/", len(expeArray))

def runExperience():
    global numExpe, lightVec

    if numExpe == (len(expeArray)):
        print()
        print("\t\tFIN de la technique", expeArray[0][0])
        print()
        overall.stopApplication()
    changeVar(numExpe)
    lightVec = createModel()
    showCurrentExpe()
    numExpe += 1

    if initDone:
        glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[0])
        glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[1])
        glBufferData(GL_ARRAY_BUFFER, norm_picture, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, target_vbos[0])
        glBufferData(GL_ARRAY_BUFFER, vertic_target, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, target_vbos[1])
        glBufferData(GL_ARRAY_BUFFER, norm_target, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ARRAY_BUFFER, target_vbos[2])
        glBufferData(GL_ARRAY_BUFFER, color_target, GL_DYNAMIC_DRAW)


    glutPostRedisplay()

#this function is call when expe is True
def controlClicks(t, angleRotT, pdpT):
    global nbClicError, nbClicOnTarget, t1
    global color_target, vertic_picture, norm_picture, envCenter, env_haut_bas, thetaCible, start, heightCible
    
    if (not start):
        if(libExpe.isAtCenter(2, pdpClic)):
            t1 = t
            start = True
            color_target = draw.changeTargetsColor (nbCibles, targetOrder[nbClicOnTarget])
            color_target = numpy.array(color_target, dtype='float32')

            glBindBuffer(GL_ARRAY_BUFFER, target_vbos[2])
            glBufferData(GL_ARRAY_BUFFER, color_target, GL_DYNAMIC_DRAW)

    else:
        if(libExpe.isInTarget(thetaCible, heightCible, angleRotT, amplitudeCible, rayonCible, pdpT, techUsed)):
            nbClicOnTarget += 1

            if nbClicOnTarget == 1:
                thetaCible = libExpe.thetaTarget(targetOrder[nbClicOnTarget])
                heightCible = hauteur * (1-env_haut_bas)
                color_target = draw.changeTargetsColor(nbCibles, targetOrder[nbClicOnTarget])
                envCenter = [0,0,0]
            
            elif(nbClicOnTarget < 10):
                if not techAdapt:
                    duree = t - t1
                    libExpe.saveData(name, techUsed, amplitudeCible, (rayonCible*2), hauteur, symetrieCible, nbClicError, duree)
                    t1 = t
                    nbClicError = 0

                thetaCible = libExpe.thetaTarget(targetOrder[nbClicOnTarget])
                x, y = libExpe.posTarget(libExpe.thetaTarget(targetOrder[nbClicOnTarget-1]), amplitudeCible)
                color_target = draw.changeTargetsColor(nbCibles, targetOrder[nbClicOnTarget])
                envCenter = [x, y, 0]
                
                if nbClicOnTarget != 5:
                    if env_haut_bas == 0:
                        vertic_picture = vertic_picture_down
                        norm_picture = norm_picture_down
                    else:
                        vertic_picture = vertic_picture_up
                        norm_picture = norm_picture_up
                    heightCible = hauteur * env_haut_bas
                    env_haut_bas = 1 - env_haut_bas
                
                        
            else:
                if not techAdapt:
                    duree = t - t1
                    libExpe.saveData(name, techUsed, amplitudeCible, (rayonCible*2), hauteur, symetrieCible, nbClicError, duree)
                    nbClicError = 0

                nbClicOnTarget = 0
                start = False
                runExperience()

            if start:
                color_target = numpy.array(color_target, dtype='float32')
            
                #loading of array in buffers
                glBindBuffer(GL_ARRAY_BUFFER, target_vbos[2])
                glBufferData(GL_ARRAY_BUFFER, color_target, GL_DYNAMIC_DRAW)

                glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[0])
                glBufferData(GL_ARRAY_BUFFER, libExpe.mooveObject(vertic_picture, envCenter), GL_DYNAMIC_DRAW)

                glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[1])
                glBufferData(GL_ARRAY_BUFFER, norm_picture, GL_DYNAMIC_DRAW)

        else:
            nbClicError += 1
    glutPostRedisplay()


def main():
    print('====> START')
    global pi_shader, po_shader, ta_shader
    global nameFile, reverse, test, initDone, pdpE
    
    glutInit(sys.argv)
    #===================GET BACK PARAM===================#
    if sys.argv[1] == "test":
        if len(sys.argv) < 4:
            print("Nombre d'argument incorrect")
            overall.stopApplication()
        test = True
        print("Début essai ...")
        nameFile = sys.argv[2]
        pdpE = bool(int((sys.argv[3])))
        lightVecTest = createModel()

    elif sys.argv[1] == "expe":
        setParam()
        print("Début expérimentation ...")
        runExperience()

    if not test and not expe:
        print("Les arguments passé sont incorrects")
        overall.stopApplication()
    #====================================================#

    init_env()
    
    pi_shader, po_shader, ta_shader = init()
    if expe:
        initLight([pi_shader, ta_shader], lightVec)
    elif test:
        initLight([pi_shader], lightVecTest)
    
    init_projections(po_shader)

    initDone = True
    
    glutDisplayFunc(display)
    glutPassiveMotionFunc(mouse_passive)
    if expe:
        glutMouseFunc(mouse_button)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    global tech_feedback, pdp, pdpClic

    new_object_position()

    
    #display object at screen
    glUseProgram(pi_shader)
    #According the thechnique choosen screening of triangles change
    if expe:
        glDrawArrays(GL_TRIANGLE_STRIP, 0, int(len(vertic_picture)/3))
    elif test:
        glDrawArrays(GL_TRIANGLES, 0, int(len(vertic_picture)/3))

    if expe:
        glDisable(GL_DEPTH_TEST)
        glUseProgram(ta_shader)
        glDrawArrays(GL_TRIANGLES, 0, int(len(vertic_target)/3))
        glEnable(GL_DEPTH_TEST)
    #Intersection between the mouse ray and the scene
    if  mouse[0] > 0 and mouse[0] < window_w and \
        mouse[1] > 0 and mouse[1] < window_h:
        pdpbis = mouse_intersection(mouse[0], mouse[1], camera, window_w, window_h)
        if pdpbis[0]  != "inf":
            if pdpE:
                pdp = pdpbis
            pdpClic = pdpbis


    # if test:
    #     #display pointer at screen
    #     tech_feedback = cursor_feedback(mouse[:2])
    #     print(tech_feedback)

    #     glDisable(GL_DEPTH_TEST)
    #     glUseProgram(po_shader)
    #     glBindBuffer(GL_ARRAY_BUFFER, pointing_vbos)
    #     glBufferData(GL_ARRAY_BUFFER, tech_feedback.astype('float32'), GL_DYNAMIC_DRAW)
    #     glDrawArrays(GL_TRIANGLES, 0, len(tech_feedback))
    #     glEnable(GL_DEPTH_TEST)

    glutSwapBuffers()

    return

if __name__ == '__main__': main()



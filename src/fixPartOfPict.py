
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *


import sys
import numpy
import math
import time

import lib.shader as sh
import lib.viewpoint as vp
import lib.matrix as matrix
import lib.parser as parser
import lib.overall as overall
import lib.drawExpe as draw
import lib.expe as libExpe


test = False
expe = False
pdpE = False

targetOrder = [0, 4, 8, 3, 7, 2, 6, 1, 5, 0]

picture_vbos, pointing_vbos, target_vbos = None, None, None #TODO add target_vbos
pi_shader, po_shader, ta_shader = None, None, None #TODO add ta_shader

vertic_picture = []
norm_picture = []

vertic_picture_bas = []
norm_picture_bas = []

vertic_picture_haut = []
norm_picture_haut = []

vertic_target = []
norm_target = []
color_target = []



nameFile = None

mouse = numpy.array([0, 0, None, None, 0, 0])
tech_feedback = numpy.array([])

angleRot = 0.0
thetaCible = 0.0
amplitude = 0 #rayon entre l'origine et une cible quelconque
rayonCible = 0
nbCibles = 0
envCenter = [0,0,0]
env_haut_bas = 0
hauteur = 0
nbAnneaux = 0

nbClicError = 0
nbClicOnTarget = 0


#==============================VARIABLES REGLABLES==============================#
    #CAMERA
axisRot = [0, 1, 0] #Défini l'axe autour du quel on fait la rotation
angle0 = 0 #le centre de l'arc de cercle de la rotation | -1 pour tourner continu
arcAngle = math.pi / 6 #la valeur de l'arc de cercle
speed = 1 # 1 => vitesse = pi/1000
pdp = [0., 0., 0.] #point de pivot initial ou fixe selon la technique
sens = 1 #sens de rotation initial ou continu si angle0 = -1
initPosCamera = [0, 0, 4] #position initiale de la camera
    #FENETRE
window_w , window_h = 900, 900
    #ORDRE DES SOMMETS
reverse = -1
#===============================================================================#



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



def init_env():
    """initialise window param"""
def init():
    """initialise vertices of picture, declare and build the shaders
       -return : ID of program shaders"""
def projection():
    """build matrix (vec4) of projection"""
def init_projections():
    """Intialise the camera and call shaders program"""
def mouse_intersection(mouse_x, mouse_y, camera, win_w, win_h):
    '''Computation of the intersection between the mouse ray and the scene
    We assume the viewport bottom left corner is 0, 0'''
def mouse_passive(x, y):
    """get the coord of mouse pointer when there are not other entry"""
def keyboard(key, x, y):
    """get the touch which are pressed"""
def cursor_feedback(p):
    """get the mouse pointer to print it
    -return numpy.append(arr, z, axis=1)"""
def display():
    """Display in real time the pointer of our pad or by eye tracking"""
def idle():
    """function called when there are no other event"""


#########################################
#           END OF DECLARATION          #
#########################################


def init_env():
    global angleRot
    
    glutInitDisplayString('double rgba samples=8 depth core')
    glutInitWindowSize(window_w, window_h)
    glutInitWindowPosition (1110, 0)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutCreateWindow('myFirstWindow')
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
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
    global vertic_picture, norm_picture, vertic_picture_haut, norm_picture_haut, vertic_picture_bas, norm_picture_bas
    global vertic_target, norm_target, color_target

    global amplitude, thetaCible, rayonCible, nbCibles, env_haut_bas, amplitudeBis, hauteur


    pointer_sh_attr = [5]

    if test:
        #parse fichier d'entree
        vertic_picture, norm_picture = parser.parse(nameFile, reverse) #le 2eme param sert à inverser les sommets
    elif expe:
        #cré le modèle
        amplitude = 10
        rayonCible = 1
        nbCibles = 9
        env_haut_bas = 0
        hauteur = 10
        nbAnneaux = 2
        vertic_picture, norm_picture, cameraZ, vertic_target, norm_target = draw.drawExpe(amplitude, rayonCible, hauteur, nbAnneaux, env_haut_bas, nbCibles)

        color_target, thetaCible = draw.changeTargetsColor(nbCibles, targetOrder[0])
        
        vertic_picture = numpy.array(vertic_picture, dtype='float32')
        norm_picture = numpy.array(norm_picture, dtype='float32')

        vertic_target = numpy.array(vertic_target, dtype='float32')
        norm_target = numpy.array(norm_target, dtype='float32')
        color_target = numpy.array(color_target, dtype='float32')

        amplitude = libExpe.newRadius(amplitude) #le 2*rayon entre l'origine et une cible est différent de distance entre 2 cibles

        vertic_picture_haut, norm_picture_haut, n = draw.drawEnv(amplitude, rayonCible, hauteur, nbAnneaux, 1)
        vertic_picture_bas,  norm_picture_bas,  n = draw.drawEnv(amplitude, rayonCible, hauteur, nbAnneaux, 0)

        vertic_picture_haut = numpy.array(vertic_picture_haut, dtype='float32')
        norm_picture_haut = numpy.array(norm_picture_haut, dtype='float32')
        vertic_picture_bas = numpy.array(vertic_picture_bas, dtype='float32')
        norm_picture_bas = numpy.array(norm_picture_bas, dtype='float32')


        camera.position[2] = 55

    #creation des shaders
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
    pointing_vbos = [glGenBuffers(1)]
    target_vbos = glGenBuffers(3) #ajout glGenBuffers #TODO
    
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
    glBindBuffer(GL_ARRAY_BUFFER, pointing_vbos[0])
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
    #TODO create targets shader ...
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
        glVertexAttribPointer(target_vbos[2], 3, GL_FLOAT, GL_FALSE, 0, None)
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
    
    #retourne les ID des programmes shaders
    return picture_sh, pointer_sh, targets_sh #TODO return targets_sh

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

    m_persp_pi = matrix.pivot(axisRot, angleRot, pdp, envCenter)
    m_persp_ta = matrix.pivot(axisRot, angleRot, pdp, [0,0,0])
     
    glUseProgram(pi_shader)
    projection(pi_shader, camera.persp_projection, camera.persp_modelview, m_persp_pi)

    #TODO add gestion pivotement ta_shader
    if expe:
        glUseProgram(ta_shader)
        projection(ta_shader, camera.persp_projection, camera.persp_modelview, m_persp_ta)

def init_projections(po_shader):
    
    camera.ortho_projection = vp.orthographic(0, window_w, 0, window_h, -1.0, 1.0).T
    camera.ortho_modelview = numpy.identity(4)
    
    camera.persp_projection  = vp.perspective(camera.fov, camera.ratio, camera.near, camera.far).T
    camera.persp_modelview = numpy.array(matrix.m_lookAt(camera.position,
                                                        camera.looking,
                                                        camera.up))
    new_object_position()
    
    glUseProgram(po_shader)
    projection(po_shader, camera.ortho_projection, camera.ortho_modelview, None)


def mouse_intersection(mouse_x, mouse_y, camera, win_w, win_h):
    
    '''Computation of the intersection between the mouse ray and the scene
    We assume the viewport bottom left corner is 0, 0'''
    z = glReadPixels( mouse_x, mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)[0][0];
    if z > 0.999:
        return [0, 0, 0]
    
    modelview   = camera.persp_modelview.reshape((4,4))
    projection  = camera.persp_projection
    viewport    = [0, 0, win_w, win_h];
    
    winX = mouse_x;
    winY = mouse_y;
    winZ = glReadPixels( mouse_x, mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT);
    
    return gluUnProject( winX, winY, winZ, modelview, projection, viewport)

def mouse_passive(x, y):
    global mouse

    mouse[0] = x
    mouse[1] = glutGet(GLUT_WINDOW_HEIGHT) - y
    glutPostRedisplay()

def mouse_button(button, state, x, y):
    global nbClicError, nbClicOnTarget, color_target, envCenter, env_haut_bas, thetaCible, vertic_picture, norm_picture

    t = time

    if(button == GLUT_LEFT_BUTTON and state == GLUT_DOWN):
        print(thetaCible)
        
        if(libExpe.isInTarget(thetaCible, angleRot, amplitude, rayonCible, pdp)):
            if(nbClicOnTarget == 0):
                #TODO positionner centre env sur cible 1 (x = amplitude, y = 0, z = cible1.height) ET avec le nouveau rayon
                    #démarrer le chrono (t1 = time)
                x, y = libExpe.posTarget(thetaCible, amplitude)
                color_target, thetaCible = draw.changeTargetsColor(nbCibles, targetOrder[nbClicOnTarget+1])
                envCenter = [x, y, 0]
                #TODO vertic_picture for glBindBuffer and glBufferData = vertic_picture de env_haut_bas
                if env_haut_bas == 0:
                    vertic_picture = vertic_picture_bas
                else:
                    vertic_picture = vertic_picture_haut
                env_haut_bas = 1 - env_haut_bas
                norm_picture = norm_picture_bas

                glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[1])
                glBufferData(GL_ARRAY_BUFFER, norm_picture, GL_DYNAMIC_DRAW)

            elif (nbClicOnTarget < 9):
                x, y = libExpe.posTarget(thetaCible, amplitude)
                color_target, thetaCible = draw.changeTargetsColor(nbCibles, targetOrder[nbClicOnTarget+1])
                envCenter = [x, y, 0]
                #TODO vertic_picture for glBindBuffer and glBufferData = vertic_picture de env_haut_bas
                if nbClicOnTarget != 7:
                    if env_haut_bas == 0:
                        vertic_picture = vertic_picture_bas
                    else:
                        vertic_picture = vertic_picture_haut
                env_haut_bas = 1 - env_haut_bas
            else:
                # TODO :
                #     save (t = t1 - t)
                #     changer ID => repartir état initial avec nouvel ID
                #     nbClicError = 0 & nbClicOnTarget = 0
                print("FIN !", nbClicError)

            color_target = numpy.array(color_target, dtype='float32')
        
            #chargement des tableaux dans les buffers
            glBindBuffer(GL_ARRAY_BUFFER, target_vbos[2])
            glBufferData(GL_ARRAY_BUFFER, color_target, GL_DYNAMIC_DRAW)

            glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[0])
            glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)            

            nbClicOnTarget += 1

        else:
            nbClicError += 1
    glutPostRedisplay()

def keyboard(key, x, y):

    if key == b'x' or key == b'X' or b'\x1b':
        overall.stopApplication()
    else:
        print("Useless key:", key)

def cursor_feedback(p):
    left    = numpy.array([1,0])
    up      = numpy.array([0,1])
    r = 5
    arr = []
    
    nb_steps = 20
    step = 2*math.pi/nb_steps
    for i in range(nb_steps):
        arr.append(p)
        arr.append(p + r*math.cos((i+1)*step)*left + r*math.sin((i+1)*step)*up)
        arr.append(p + r*math.cos(i*step)*left + r*math.sin(i*step)*up)
    
    z = numpy.zeros((len(arr),1), dtype='float32')
    return numpy.append(arr, z, axis=1)

def idle():
    glutPostRedisplay()

def main():
    print('====> START')
    global pi_shader, po_shader, ta_shader, nameFile, reverse, test, expe, pdpE #TODO add ta_shader
    
    glutInit(sys.argv)
    #on récupère les paramètres passé
    #===================GET BACK PARAM===================#
    if len(sys.argv) > 4:
       print("Nombre d'argument incorrect")
       overall.stopApplication()

    elif sys.argv[1] == "test":
        if len(sys.argv) < 4:
            print("Nombre d'argument incorrect")
            overall.stopApplication()
        test = True
        print("Début essai ...")
        nameFile = sys.argv[2]
        pdpE = bool(int((sys.argv[3])))

    elif sys.argv[1] == "expe":
        if len(sys.argv) < 3:
            print("Nombre d'argument incorrect")
            overall.stopApplication()
        expe = True
        pdpE = bool(int(sys.argv[2]))
        print("Début expérimentation ...")

    if not test and not expe:
        print("Les arguments passé sont incorrects")
        overall.stopApplication()
    #====================================================#

    init_env()
    
    pi_shader, po_shader, ta_shader = init() #TODO add ta_shader
    
    init_projections(po_shader)
    
    glutDisplayFunc(display)
    glutPassiveMotionFunc(mouse_passive)
    glutMouseFunc(mouse_button)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    global tech_feedback, pdp

    #faire la rotation deplacer le point de pivot (pdp)
    new_object_position()
    
    #display object at screen
    glUseProgram(pi_shader)
    ##technique de d'affichage des triangles différentes
    if expe:
        glDrawArrays(GL_TRIANGLE_STRIP, 0, int(len(vertic_picture)/3))
    elif test:
        glDrawArrays(GL_TRIANGLES, 0, int(len(vertic_picture)/3))

    #TODO
    if expe:
        glUseProgram(ta_shader)
        glDrawArrays(GL_TRIANGLES, 0, int(len(vertic_target)/3))

    #Intersection between the mouse ray and the scene
    if pdpE:
        if  mouse[0] >= 0 and mouse[0] <= window_w and \
            mouse[1] >= 0 and mouse[1] <= window_h:
            pdpbis = mouse_intersection(mouse[0], mouse[1], camera, window_w, window_h)
            if pdpbis[0]  != "inf":
                pdp = pdpbis

    #display pointer at screen
    tech_feedback = cursor_feedback(mouse[:2])

    glUseProgram(po_shader)
    glDrawArrays(GL_TRIANGLES, 0, int(len(tech_feedback)/3))

    glutSwapBuffers()

    return

if __name__ == '__main__': main()



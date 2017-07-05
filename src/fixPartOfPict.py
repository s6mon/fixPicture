
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

test = False
expe = False

picture_vbos, pointing_vbos = None, None
window_w , window_h = 900, 900
pi_shader, po_shader = None, None
vertic_picture = []
norm_picture = []
pdp = [0., 0., 0.]

nameFile = None
reverse = -1

mouse = numpy.array([0, 0, None, None, 0, 0])
tech_feedback = numpy.array([])


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

camera = Camera(ratio = window_w/window_h)

angleRot, sens, angle1, angle2 = 0.0, 1.0, -math.pi, -math.pi/6


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
    glutSetCursor(GLUT_CURSOR_NONE)
    
    print('Environment booted')

def init():
    global picture_vbos, pointing_vbos
    global vertic_picture, norm_picture
    global vertices_tab


    pointer_sh_attr = [5]
    
    if test:
        #parse fichier d'entree
        vertic_picture, norm_picture = parser.parse(nameFile, reverse) #le 2eme param sert à inverser les sommets
    elif expe:
        #=====================TEST=======================#
        # draw.ring(vertic_picture, norm_picture, [0., 0., 0.], 1, 1.2, 0, 4)
        # draw.ringAskew(vertic_picture, norm_picture, [0., 0., 0.], 2, 4, 0, 2, 4)
        # draw.ring(vertic_picture, norm_picture, [0., 0., 0.], 4.1, 4.3, 2, 50)
        #draw.ringAskew(vertic_picture, norm_picture, [0., 0., 0.], 4.5, 6.5, 2, 0, 50)
        #================================================#

        distance = draw.drawExpe(vertic_picture, norm_picture, [0., 0., 0.], 10, 2, 5, 1)
        camera.position[2] = (distance + 5.)
        print(camera.position[2])

        vertic_picture = numpy.array(vertic_picture, dtype='float32')
        norm_picture = numpy.array(norm_picture, dtype='float32')


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
    
    #retourne les ID des programmes shaders
    return picture_sh, pointer_sh

def projection(shader, matp, matm, mato):
    unif_p = glGetUniformLocation(shader, 'projection_mat')
    glUniformMatrix4fv(unif_p, 1, False, matp)
    
    unif_m = glGetUniformLocation(shader, 'modelview_mat')
    glUniformMatrix4fv(unif_m, 1, False, matm)
    
    unif_o = glGetUniformLocation(shader, 'object_mat')
    glUniformMatrix4fv(unif_o, 1, False, mato)

def new_object_position():
    global angleRot, angle, sens
    axe = [0., 1., 0.]
    m_persp_object = matrix.pivot(axe, angleRot, [0., 0., 0.])
    
    # if angleRot >= angle1:
    #     sens = -1
    # elif angleRot <= angle2:
    #     sens = 1
    
    # if sens == 1:
    angleRot += math.pi/1000
    # elif sens == -1:
    #     angleRot -= math.pi/1000
    
    glUseProgram(pi_shader)
    projection(pi_shader, camera.persp_projection, camera.persp_modelview, m_persp_object)

def init_projections(pi_shader, po_shader):
    
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
        return [str("inf"), str("inf"), str("inf")]
    
    viewport    = [0, 0, win_w, win_h];
    
    i = inv(numpy.matmul(camera.persp_projection.T, camera.persp_modelview.reshape((4,4)).T))
    
    winZ = glReadPixels( mouse_x, mouse_y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT);
    
    vector = numpy.array([2*(mouse_x - viewport[0])/viewport[2] - 1, 2*(mouse_y - viewport[1])/viewport[3] - 1, 2*winZ-1, 1])
    p = numpy.matmul(i,vector)
    return p[0:3]/p[3]

def mouse_passive(x, y):
    global mouse

    mouse[0] = x
    mouse[1] = glutGet(GLUT_WINDOW_HEIGHT) - y
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
    global pi_shader, po_shader, nameFile, reverse, test, expe
    
    glutInit(sys.argv)
    #on récupère les paramètres passé
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
        reverse = int(sys.argv[3])

    elif sys.argv[1] == "expe":
        expe = True
        print("Début expérimentation ...")

    if not test and not expe:
        print("Les arguments passé sont incorrects")
        overall.stopApplication()

    init_env()
    
    pi_shader, po_shader = init()
    
    init_projections(pi_shader, po_shader)
    
    glutDisplayFunc(display)
    glutPassiveMotionFunc(mouse_passive)
    glutKeyboardFunc(keyboard)
    glutIdleFunc(idle)
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    global tech_feedback, pdp
    new_object_position()
    
    #display object at screen
    glUseProgram(pi_shader)
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)
    
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[1])
    glBufferData(GL_ARRAY_BUFFER, norm_picture, GL_DYNAMIC_DRAW)

    if expe:
        glDrawArrays(GL_TRIANGLE_STRIP, 0, int(len(vertic_picture)/3))
    elif test:
        glDrawArrays(GL_TRIANGLES, 0, int(len(vertic_picture)/3))

    
    #Intersection between the mouse ray and the scene
    if  mouse[0] >= 0 and mouse[0] <= window_w and \
        mouse[1] >= 0 and mouse[1] <= window_h:
        pdpbis = mouse_intersection(mouse[0], mouse[1], camera, window_w, window_h)
        if pdpbis[0]  != "inf":
            pdp = pdpbis

    #display pointer at screen
    tech_feedback = cursor_feedback(mouse[:2])
    
    glUseProgram(po_shader)
    glBindBuffer(GL_ARRAY_BUFFER, pointing_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, tech_feedback.astype('float32'), GL_DYNAMIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, len(tech_feedback))

    glutSwapBuffers()

    return

if __name__ == '__main__': main()



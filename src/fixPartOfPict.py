
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


picture_vbos, pointing_vbos = None, None
window_w , window_h = 800,600
pi_shader, po_shader = None, None
vertic_picture = []
nameFile = None

mouse = numpy.array([0, 0, None, None, 0, 0])
tech_feedback = numpy.array([])



def init_env():
    """initialise window param"""
def init():
    """initialise vertices of picture, declare and build the shaders
       -return : ID of program shaders"""
def projection():
    """build matrix (vec4) of projection"""
def init_projections():
    """Intialise the camera and call shaders program"""
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
    global window_h, window_w

    window_h = 1080
    window_w = 800

    glutInitDisplayString('double rgba samples=8 depth core')
    glutInitWindowSize(window_w, window_h)
    glutInitWindowPosition (1120, 0)
    glutCreateWindow('myFirstWindow')
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glutSetCursor(GLUT_CURSOR_NONE)

    print('Environment booted')

    global changeVue
    changeVue = False

def init():
    global picture_vbos, pointing_vbos
    global vertic_picture
    pointer_sh_attr = [5]

    #parse fichier d'entree
    vertic_picture = parser.parse(nameFile)
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

    picture_vbos = glGenBuffers(1)
    pointing_vbos = [glGenBuffers(1)]

    ###picture shader###
    tech_model = numpy.array([])
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos)
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_STATIC_DRAW)
    glVertexAttribPointer(picture_vbos, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(picture_vbos)
    picture_sh = sh.create('../shader/picture_vert.glsl',
                            None,
                            '../shader/picture_frag.glsl',
                            [picture_vbos],
                            ['position'])
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


def projection(shader, matp, matm, matv):
    unif_p = glGetUniformLocation(shader, 'projection_mat')
    unif_m = glGetUniformLocation(shader, 'modelview_mat')
    unif_v = glGetUniformLocation(shader, 'view_mat')
    

    glUniformMatrix4fv(unif_p, 1, False, matp.T)
    glUniformMatrix4fv(unif_m, 1, False, matm.T)
    glUniformMatrix4fv(unif_v, 1, False, matv)
    

def init_projections(pi_shader, po_shader):

    m_persp_projection  = vp.perspective(45.0, window_w/window_h, 0.01, 10000.)
    m_persp_modelview  = numpy.identity(4)
    m_persp_modelview[2][3] = -7.5 #on modifie la position de l'observateur sur l'axe des Z

    m_ortho_projection = numpy.identity(4)
    m_ortho_projection = vp.orthographic(0, window_w, 0, window_h, -1.0, 1.0)
    m_ortho_modelview = numpy.identity(4)

    radius = 10
    camX = numpy.cos(time.time()) * radius
    camZ = numpy.sin(time.time()) * radius
    
    view = matrix.m_lookAt([camX,  0.0, camZ],
                           [0.0,  0.0, 0.0],
                           [0.0,  1.0, 0.0])    


    glUseProgram(pi_shader)
    projection(pi_shader, m_persp_projection, m_persp_modelview, view)

    glUseProgram(po_shader)
    projection(po_shader, m_ortho_projection, m_ortho_modelview, view)

def mouse_passive(x, y):
    global mouse

    mouse[0] = x
    mouse[1] = glutGet(GLUT_WINDOW_HEIGHT) - y
    glutPostRedisplay()

def keyboard(key, x, y):

    if key == b'x':
        overall.stopApplication()

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
    init_projections(pi_shader, po_shader)
    glutPostRedisplay()


def main():
    print('====> START')
    global pi_shader, po_shader, nameFile

    glutInit(sys.argv)
    if len(sys.argv) < 2:
       print("Nombre d'argument incorrect")
       overall.stopApplication()
    else:
       nameFile = sys.argv[1]
    #nameFile = "exemple19.obj"
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

    global tech_feedback
    global window_w, window_h
    global vertic_picture

    init_projections(pi_shader, po_shader)
    
    #display picture at screen
    glUseProgram(pi_shader)
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos)
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_STATIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, int(len(vertic_picture)/3))

    #TODO add normale array 

    #display pointer at screen
    tech_feedback = cursor_feedback(mouse[:2])
    
    glUseProgram(po_shader)
    glBindBuffer(GL_ARRAY_BUFFER, pointing_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, tech_feedback.astype('float32'), GL_DYNAMIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, len(tech_feedback))

    glutSwapBuffers()

    return

if __name__ == '__main__': main()



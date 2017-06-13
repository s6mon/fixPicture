
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys
import numpy
import math

import lib.shader as sh
import lib.viewpoint as vp

picture_vbos, pointing_vbos = None, None
window_w , window_h = 800,600
pi_shader, po_shader = None, None
vertic_picture = None

mouse = numpy.array([0, 0, None, None, 0, 0])

tech_feedback = numpy.array([])


def display():
    """Display in real time the pointer of our pad or by eye tracking"""
def init_projection():
    """Intialise the camera and call shaders program"""
def projection():
    """build matrix (vec4) of projection"""
def init():
    """initialise vertices of picture, declare and build the shaders
       -return : ID of program shaders"""
def init_env():
    """initialise window param"""


#fonction pour parser fichier d'entrée
#def parse():

def init_env():
    global window_h, window_w

    window_h = 800
    window_w = 800

    glutInitDisplayString('double rgba samples=8 depth core')
    glutInitWindowSize(window_w, window_h)
    glutCreateWindow('myFirstWindow')
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glutSetCursor(GLUT_CURSOR_NONE)

    print('Environment booted')

def init():
    global picture_vbos, pointing_vbos

    global vertic_picture
    pointer_sh_attr = [5]

    #parser le fichier image d entree
    #TODO fonction pour parser fichier d'entrée
    vertic_picture = numpy.array([
        0.0, 1.0, 0.0,
        1.0, 0.0, 0.0,
        -1.0, 0.0, 0.0,

        0.0, -1.0, 0.0,
        -1.0, 0.0, 0.0,
        1.0, 0.0, 0.0
        ], dtype='float32')

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
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)
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


def projection(shader, matp, matm):
    unif_p = glGetUniformLocation(shader, 'projection_mat')
    unif_m = glGetUniformLocation(shader, 'modelview_mat')

    glUniformMatrix4fv(unif_p, 1, False, matp.T)
    glUniformMatrix4fv(unif_m, 1, False, matm.T)

def init_projections(pi_shader, po_shader):

    m_persp_projection  = vp.perspective(45.0, window_w/window_h, 0.01, 10000.)
    m_persp_modelview  = numpy.identity(4)
    m_persp_modelview[2][3] = -7.5

    m_ortho_projection = numpy.identity(4)
    m_ortho_projection = vp.orthographic(0, window_w, 0, window_h, -1.0, 1.0)
    m_ortho_modelview = numpy.identity(4)

    glUseProgram(pi_shader)
    projection(pi_shader, m_persp_projection, m_persp_modelview)

    glUseProgram(po_shader)
    projection(po_shader, m_ortho_projection, m_ortho_modelview)

def mouse_passive(x, y):
    global mouse

    mouse[0] = x
    mouse[1] = glutGet(GLUT_WINDOW_HEIGHT) - y
    glutPostRedisplay()

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


def main():
    print()
    global pi_shader, po_shader

    glutInit(sys.argv)
    init_env()

    pi_shader, po_shader = init()
    print('Starting of display')
    init_projections(pi_shader, po_shader)

    glutDisplayFunc(display)
    glutPassiveMotionFunc(mouse_passive)
    glutMainLoop()
    return

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    global tech_feedback
    global window_w, window_h

    init_projections(pi_shader, po_shader)
    
    #display picture at screen
    glUseProgram(pi_shader)
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos)
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, len(vertic_picture))



    #display pointer at screen
    tech_feedback = cursor_feedback(mouse[:2]) 
    glUseProgram(po_shader)
    glBindBuffer(GL_ARRAY_BUFFER, pointing_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, tech_feedback.astype('float32'), GL_DYNAMIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, len(tech_feedback))
    
    glutSwapBuffers()
    return

if __name__ == '__main__': main()



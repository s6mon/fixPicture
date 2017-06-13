
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import sys
import numpy
import math

import lib.shader as sh
import lib.viewpoint as vp

picture_vbos = None
window_w , window_h = 800,600
t_shader = None
vertic_picture = None


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
    glClearColor(0.0, 0.0, 0.0, 1.0)

    print('Environment booted')

def init():
    global picture_vbos
    global vertic_picture

    pictureID = GLuint()
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

    #picture shader
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos)
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)
    glVertexAttribPointer(picture_vbos, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(picture_vbos)
    picture_sh = sh.create('../shader/picture_vert.glsl',
                            None,
                            '../shader/picture_frag.glsl',
                            [picture_vbos],
                            ['position'])
    print('Picture shader created')

    #pointer shader
    #TODO

    #retourne les ID des programmes shaders
    return picture_sh


def projection(shader, matp, matm):
    unif_p = glGetUniformLocation(shader, 'projection_mat')
    unif_m = glGetUniformLocation(shader, 'modelview_mat')

    glUniformMatrix4fv(unif_p, 1, False, matp.T)
    glUniformMatrix4fv(unif_m, 1, False, matm.T)

def init_projections(t_shader):
    global m_persp_projection, m_persp_modelview

    m_persp_projection  = vp.perspective(45.0, window_w/window_h, 0.01, 10000.)
    
    m_persp_modelview  = numpy.identity(4)
    m_persp_modelview[2][3] = -7.5

    glUseProgram(t_shader)
    projection(t_shader, m_persp_projection, m_persp_modelview)

def main():
    print()
    global t_shader

    glutInit(sys.argv)
    init_env()

    t_shader = init()
    print('Starting of display')
    init_projections(t_shader)

    glutDisplayFunc(display)
    glutMainLoop()
    return

def display():

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glUseProgram(t_shader)
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos)
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, len(vertic_picture))
    
    glutSwapBuffers()
    return

if __name__ == '__main__': main()




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
window_w , window_h = 800, 1080
pi_shader, po_shader = None, None
vertic_picture = []
norm_picture = []

nameFile = None

mouse = numpy.array([0, 0, None, None, 0, 0])
tech_feedback = numpy.array([])

#MVP var
class Camera:
    def __init__(self, fov = 45, ratio = 4/3, near = 0.1, far = 1000, position = [0,0,10], looking = [0,0,0], up = [0,1,0]):
        self.fov = fov
        self.ratio = ratio
        self.near = near
        self.far = far
        self.position = position
        self.looking = looking
        self.up = up

camera = Camera(ratio = window_w/window_h)
angleRot, sens, angle1, angle2 = 0.0, 1.0, 0.0, 0.0


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

    pointer_sh_attr = [5]
    
    #parse fichier d'entree
    vertic_picture, norm_picture = parser.parse(nameFile)

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
    
    #passage du tableau des normales
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
    angleRot += math.pi/100
    pointPivot = [0.0, 0.0, -1.0]
    m_persp_object = matrix.pivot(axe, angleRot, pointPivot)
    if angleRot >= angle1:
        sens = -1
    elif angleRot <= angle2:
        sens = 1

    if sens == 1:
        angleRot += math.pi/1000
    elif sens == -1:
        angleRot -= math.pi/1000
    
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
    
    def radian(a):
        return a*math.pi/180.
    
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
    global pi_shader, po_shader, nameFile
    
    glutInit(sys.argv)
    if len(sys.argv) < 2:
       print("Nombre d'argument incorrect")
       overall.stopApplication()
    else:
       nameFile = sys.argv[1]
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
    new_object_position()
    
    #display object at screen
    glUseProgram(pi_shader)
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, vertic_picture, GL_DYNAMIC_DRAW)
    
    glBindBuffer(GL_ARRAY_BUFFER, picture_vbos[1])
    glBufferData(GL_ARRAY_BUFFER, norm_picture, GL_DYNAMIC_DRAW)
    
    glDrawArrays(GL_TRIANGLES, 0, int(len(vertic_picture)/3))
    
    print(mouse_intersection(mouse[0], mouse[1], camera, window_w, window_h))
    
    #display pointer at screen
    tech_feedback = cursor_feedback(mouse[:2])
    
    glUseProgram(po_shader)
    glBindBuffer(GL_ARRAY_BUFFER, pointing_vbos[0])
    glBufferData(GL_ARRAY_BUFFER, tech_feedback.astype('float32'), GL_DYNAMIC_DRAW)
    glDrawArrays(GL_TRIANGLES, 0, len(tech_feedback))

    glutSwapBuffers()

    return

if __name__ == '__main__': main()



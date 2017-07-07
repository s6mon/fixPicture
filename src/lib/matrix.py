from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import numpy
import math

from . import overall

def m_perspective(fov, aspect, near, far):
	"""build perspective matrix"""
def setMatrixUniforms(pm, mvm):
	"""set ID of projection and model view matrix"""
def m_identity():
	"""return identity matrix 4x4"""
def m_mult(a, b):
	"""multipli 2 matrix"""
def v_normalize(v):
	"""normalize matrix"""
def v_cross(u, v):
	"""crossing matrix"""
def m_lookAt(eye, center, up):
	"""lookAt function"""
def m_rotation(vecteur, angle):
	"""prend en param le vecteur qui indique sur quel vecteur on pivote
	et de quel angle on pivote"""
def multAny(a, b):
	""""""
def m_translate(x, y, z):
	"""Translate object retourne une matrice 4x4 de translation"""
def pivot(axis, angleRot, pointPivot):
	"""retourne la matrice qui va pivoter autour d'un point de pivot"""

#########################################
#			END OF DECLARATION			#
#########################################


def m_perspective(fov, aspect, near, far):

	d = 1/Math.tan(fov/2.)
	mat = numpy.identity(4)
    
	mat[0] = d/aspect;
	mat[5] = d
	mat[10] = (near + far)/(near - far)
	mat[14] = 2*near*far/(near-far)
	mat[11] = -1
	mat[15] = 0

	return mat

def setMatrixUniforms(pm, mvm):
	print("we'll try to pass argument to shader")
	PMatrix = gl.getUniformLocation(sh, "PMatrix")
	gl.uniformMatrix4fv(PMatrix, false, pm)

	MVMatrix = gl.getUniformLocation(sh, "MVMatrix")
	gl.uniformMatrix4fv(MVMatrix, false, mvm)

def m_identity():
    return [1,0,0,0,
            0,1,0,0,
            0,0,1,0,
            0,0,0,1]


def m_mult(a, b):
	i, j = 0, 0
	M = m_identity()
	while i < 4:
		while j < 4:
			M[i*4 + j] = a[i*4]*b[j] + a[i*4+1]*b[j+4] + a[i*4+2]*b[j+8] + a[i*4+3]*b[j+12]
			j += 1
		i += 1
		j = 0

	return M

def v_normalize(v):
	try:
		n = numpy.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
	except ValueError:
		print()
		print()
		print(ValueError)
		print()
		exit(0)
	return [v[0]/n, v[1]/n, v[2]/n]

def v_cross (u,v):
	return [u[1]*v[2] - u[2]*v[1],
            u[2]*v[0] - u[0]*v[2],
            u[0]*v[1] - u[1]*v[0]]

def m_lookAt(eye, center, up):
	f = v_normalize([   center[0] - eye[0],
	                    center[1] - eye[1],
	                    center[2] - eye[2]  ])
	_up = v_normalize(up)
	s = v_cross(f, _up)
	u = v_cross(v_normalize(s), f)
	R = [   s[0],   u[0],   -f[0],  0,
	        s[1],   u[1],   -f[1],  0,
	        s[2],   u[2],   -f[2],  0,
	        0,      0,      0,      1   ]

	T = [   1,      0,      0,      0,
	        0,      1,      0,      0,
	        0,      0,      1,      0,
	        -eye[0],-eye[1],-eye[2], 1 ]
	return m_mult(T, R)

def m_rotation(vecteur, angle):
	v = v_normalize(vecteur)
	s = math.sin(angle)
	c = math.cos(angle)
	C = 1 - c

	sx = s * v[0]
	sy = s * v[1]
	sz = s * v[2]
	Cx = C * v[0]
	Cy = C * v[1]
	Cz = C * v[2]
	Cxy = Cy * v[0]
	Cyz = Cz * v[1]
	Czx = Cx * v[2]

	T = numpy.array([v[0] * Cx + c,    Cxy - sz,      Czx + sy,      0.0,
					   Cxy + sz,       v[1] * Cy + c, Cyz - sx,      0.0,
					   Czx - sy,       Cyz + sx,      v[2] * Cz + c, 0.0,
					   0.0,            0.0,           0.0,           1.0])

	return T

def multAny (a, b):
	#mat(nxn) * mat(1xn)
	aSize = len(a)
	bSize = len(b)

	if(aSize/bSize) != bSize:
		print("Taille de mat 1 :", aSize, "\nTaille de mat 2: ", bSize, "\nType mat attendu mat1(nxn) mat2(1xn)")
		overall.stopApplication()
	
	i = bSize
	j = 0
	M = []
	while(i > 0):
		M.append(0)
		i -= 1

	while i < bSize:
		j = 0
		while j < bSize:
			M[i] = a[i*bSize + j] * b[j] + M[i]
			j += 1
		i += 1 
	return M

def m_translate(point):
	x = point[0]
	y = point[1]
	z = point[2]
	M = numpy.identity(4)
	M[3][0] = x
	M[3][1] = y
	M[3][2] = z
	M = M.reshape(16)
	return M


def pivot(axis, angleRot, pointPivot):
    
    
    translationI = m_translate([-x for x in pointPivot])
    rotation = m_rotation(axis, angleRot)
    translation = m_translate(pointPivot)
    
    return m_mult(translationI, m_mult(rotation, translation))











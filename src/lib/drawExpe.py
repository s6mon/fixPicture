import numpy
import math
import re
import operator

from . import matrix
from . import overall
from . import expe as libExpe


vertices_tmp = []
normales_tmp = []

xList = []
yList = []
zList = []

CONST_RISE_RING = 0
COLOR_CIRCLE = (0, 0, 0, 0)
COLOR_TARGET = (0.3, 0, 0.5, 1)
COLOR_PAUSE  = (0, 1, 0, 1)

NB_TRIANGLES_TARGETS = 30
NB_TRIANGLES_STRIP_RINGS = 50

N_FLAT = [0.0, 0.0, 1.0]

nbRingsToDraw = 0
numCurrentRing = 0
nbRingsIn = 0

def drawExpe (amplitude, width, height, nbRings, H0, nbTargets):
	""""""
def drawEnv (amplitude, width, height, nbRings, H0):
	"""fonction qui à partir d'un anneau donné renvoie l'image d'expe associé
	H0 = 0 ou 1"""
def drawCibles (amplitude, width, height, nbCibles, H0):
	""""""
def ring (radius1, radius2, height, nbSegments):
	"""calcule les sommets de triangles pour faire des anneaux"""
def ringAskew (radius1, radius2, height1, height2, nbSegments):
	""""""
def circle (position, radius, nbSegments):
	""""""
def changeTargetsColor (nbCibles, numCible):
	""""""
def fullList(objectList, maList, n):
	""""""
def v_sub (v1, v2):
	""""""
def verticeCompute(theta, radius, height, position):
	""""""
def normaleCompute(v1, v2, v3):
	""""""
def fittsLaw_Id (A, W):
	"""retourne Id"""
def fittsLaw_W (Id, A):
	"""retourne W"""
def law_H (A, a, H):
	"""retourne H"""
def law_a (A, nbRings, num):
	"""retourne amplitude courante"""
def maxAxis():
	"""find delata max"""

#########################################
#           END OF DECLARATION          #
#########################################


class Ring:
	def __init__(self, amplitude = 0.0):
		self.amplitude = amplitude
		self.width = 0
		self.height = 0

def drawExpe (amplitude, width, height, nbRings, H0, nbTargets):
	vertices_Env = []
	normales_Env = []
	size = 0
	vertices_Tar = []
	normales_Tar = []

	if(amplitude < nbRings*width or amplitude == 0 or nbRings < 0 or nbTargets < 0):
		print("Wrong argument passed to draw.drawExpe")
		overall.stopApplication()
	vertices_Env, normales_Env, size = drawEnv(amplitude, width, height, nbRings, H0)
	vertices_Tar, normales_Tar = drawCibles(amplitude, width/2, height, nbTargets, H0)
	return vertices_Env, normales_Env, size, vertices_Tar, normales_Tar


def drawEnv (amplitude, width, height, nbRings, H0):
	global vertices_tmp, normales_tmp, nbRingsToDraw, numCurrentRing, nbRingsIn
	vertices_tmp = []
	normales_tmp = []
	nbRingsIn = nbRings
	
	rings = []
	Id = fittsLaw_Id(amplitude, width)
	step = amplitude / (nbRings+1)

	nbRingsToDraw = (nbRings + 1) + 3
	
	#lorsque H0 est à 1 on monte, on descend sinon
	i = 0
	bis = amplitude - libExpe.newRadius(amplitude)

	if H0 == 0:
		alternance = H0
	else:
		alternance = 1 - H0
	while i <= nbRingsToDraw:

		rings.append(Ring(amplitude = (law_a(amplitude, nbRings, i) )))
		amplitudeCurrent = rings[i].amplitude
		rings[i].width = fittsLaw_W(Id, amplitudeCurrent)
		if(H0 == 1):
			rings[i].height = law_H(amplitude, amplitudeCurrent, height) * alternance
		else:
			rings[i].height = law_H_inv(amplitude, amplitudeCurrent, height) * alternance + ((1-alternance) * height)
		alternance = 1 - alternance
		i += 1

	#showRings(rings)
	#calculer les sommets des anneaux et les sommets des anneaux oblique (cone coupé)
	i = 0
	while i < nbRingsToDraw:
		
		radius1 = rings[i].amplitude - (rings[i].width / 2)
		radius2 = rings[i].amplitude + (rings[i].width / 2)
		height = rings[i].height
		ring (radius1, radius2, height, NB_TRIANGLES_STRIP_RINGS)
		numCurrentRing = i + 1

		#dessine les cônes
		if (i < (nbRingsToDraw - 1)):
			radius1 = rings[i].amplitude + (rings[i].width / 2)
			radius2 = rings[i+1].amplitude - (rings[i+1].width / 2)
			height1 = rings[i].height
			height2 = rings[i+1].height
			ringAskew(radius1, radius2, height1, height2, NB_TRIANGLES_STRIP_RINGS)
		i += 1

	#Anneaux central pour que le pdp fonctionne
	print(rings[0].amplitude)
	print(rings[0].width/2)
	ring (0, rings[0].amplitude - rings[0].width/2, rings[0].height, NB_TRIANGLES_STRIP_RINGS)

	return vertices_tmp, normales_tmp, maxAxis()

def drawCibles (amplitude, width, height, nbCibles, H0):
	global vertices_tmp, normales_tmp
	vertices_tmp = []
	normales_tmp = []

	deltaAngle = 2 * math.pi / nbCibles
	if H0 == -1:
		H0 = 0
	i = 0
	while i < nbCibles:
		theta = i * deltaAngle 
		x = math.cos(theta) * amplitude
		y = math.sin(theta) * amplitude
		if i > 2 and i < 7:
			z = (height * (1 - H0)) + CONST_RISE_RING 
		else:
			z = (height * H0) + CONST_RISE_RING
		circle ([x, y, z], width, NB_TRIANGLES_TARGETS)
		i += 1
	circle ([0,0,0], 2, NB_TRIANGLES_TARGETS)

	return vertices_tmp, normales_tmp


def ring (radius1, radius2, height, nbSegments):
	pos = [0,0,0]
	i = 0
	while i <= nbSegments:
		theta1 = 2 * math.pi * (i%nbSegments) / nbSegments
		theta2 = 2 * math.pi * ((i+1)%nbSegments) / nbSegments
		vertice2 = verticeCompute(theta1, radius2, height, pos)
		vertice1 = verticeCompute(theta1, radius1, height, pos)
		vertice3 = verticeCompute(theta2, radius1, height, pos)

		fullList(vertice2, vertices_tmp, 3) #l'ordre est important !
		fullList(vertice1, vertices_tmp, 3)

		#n = normaleCompute(vertice1, vertice2, vertice3)
		fullList((N_FLAT, N_FLAT), normales_tmp, 2)
		
		i += 1

def ringAskew (radius1, radius2, height1, height2, nbSegments):
	pos = [0,0,0]
	i = 0
	while i <= nbSegments:
		theta1 = 2 * math.pi * (i%nbSegments) / nbSegments
		theta2 = 2 * math.pi * ((i+1)%nbSegments) / nbSegments
		vertice2 = verticeCompute(theta1, radius2, height2, pos)
		vertice1 = verticeCompute(theta1, radius1, height1, pos)
		vertice3 = verticeCompute(theta2, radius1, height1, pos)

		fullList(vertice2, vertices_tmp, 3) #l'ordre est important !
		fullList(vertice1, vertices_tmp, 3)

		n = normaleCompute(vertice1, vertice2, vertice3)
		fullList((n, n, n), normales_tmp, 2)

		i += 1

def circle (position, radius, nbSegments):
	i = 0
	height = position[2]
	while i < nbSegments:
		theta1 = 2 * math.pi * i / nbSegments
		theta2 = 2 * math.pi * ((i+1)%nbSegments) / nbSegments
		vertice1 = (position[0], position[1], position[2])
		vertice2 = verticeCompute(theta1, radius, 0, position)
		vertice3 = verticeCompute(theta2, radius, 0, position)

		fullList(vertice1, vertices_tmp, 3)
		fullList(vertice3, vertices_tmp, 3)
		fullList(vertice2, vertices_tmp, 3)

		#n = normaleCompute(vertice1, vertice2, vertice3)
		fullList((N_FLAT, N_FLAT, N_FLAT), normales_tmp, 3) 

		i += 1

def changeTargetsColor (nbCibles, numCible):
	newColor = []
	i = 0
	theta = numCible * 2*math.pi / nbCibles
	while i < nbCibles * 3 * NB_TRIANGLES_TARGETS:
		if (i >= numCible * NB_TRIANGLES_TARGETS * 3) and (i < (numCible+1) * NB_TRIANGLES_TARGETS * 3):
			newColor.append(COLOR_TARGET)
		else:
			newColor.append(COLOR_CIRCLE)
		i += 1
	return newColor

def initTargetsColor(nbCibles):
	newColor = []
	i = 0
	while i < (nbCibles+1) * 3 * NB_TRIANGLES_TARGETS:
		if i >= nbCibles * 3 * NB_TRIANGLES_TARGETS:
			newColor.append(COLOR_PAUSE)
		else:
			newColor.append(COLOR_CIRCLE)
		i += 1
	return newColor

def fullList(objectList, maList, n):
	global vertices_tmp, normales_tmp, xList, yList, zList
	maList.append(objectList[0])
	maList.append(objectList[1])
	if(n == 3):
		maList.append(objectList[2])
	if maList == vertices_tmp and numCurrentRing <= nbRingsIn:
		xList.append(objectList[0])
		yList.append(objectList[1])
		zList.append(objectList[2])

def v_sub (v1, v2):
	return [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]

def verticeCompute(theta, radius, height, position):
	x = (math.cos(theta) * radius)
	y = (math.sin(theta) * radius)
	z = height
	return(x+position[0], y+position[1], z+position[2])

def normaleCompute(v1, v2, v3):
	vecteur1 = matrix.v_normalize(v_sub(v2, v1))
	vecteur2 = matrix.v_normalize(v_sub(v3, v1))
	return matrix.v_normalize(matrix.v_cross(vecteur1, vecteur2))

#return Id
def fittsLaw_Id (A, W):
	return math.log2((A/W) + 1)

#return W
def fittsLaw_W (Id, A):
	return A  / (math.pow(2, Id) - 1)

#return height
def law_H (A, a, H):
	return a*H / A

def law_H_inv(A, a, H):
	return H -law_H(A,a,H)


#return amplitude
def law_a (A, nbRings, num):
	step = numpy.log(A) / (nbRings+1)
	a = numpy.exp(step * (num + 1))
	return a


def maxAxis():
	drawWidth = float(max(xList)) - float(min(xList))
	drawHeight = float(max(yList)) - float(min(yList))
	if(drawWidth > drawHeight):
		return drawWidth
	else:
		return drawHeight

def showRings(rings):
	i = 0
	while i < len(rings):
		tmp = rings[i]
		print("Ring :", i, "=>")
		print("Amplitude =", tmp.amplitude, "| Width =", tmp.width, "| Height =", tmp.height)
		i += 1











import numpy
import math
import re
import operator

from . import matrix


vertices_tmp = []
normales_tmp = []

xList = []
yList = []

plan = [1,1,0]

def drawExpe (verticesDrawing, normalesDrawing, center, amplitude, width, height, nbRings, H0):
	"""fonction qui à partir d'un anneau donné renvoie l'image d'expe associé"""
def ring (verticesDrawing, normalesDrawing, center, radius1, radius2, height, nbSegments):
	"""calcule les sommets de triangles pour faire des anneaux"""
def ringAskew (verticesDrawing, normalesDrawing, center, radius1, radius2, height1, height2, nbSegments):
	""""""
def fullList(objectList, maList):
	""""""
def fullMainList(mainTab, tmp):
	""""""
def v_sub (v1, v2):
	""""""
def verticeCompute(center, theta, radius, height):
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


def drawExpe (verticesDrawing, normalesDrawing, center, amplitude, width, height, nbRings, H0):
	
	rings = []
	Id = fittsLaw_Id(amplitude, width)
	step = amplitude / (nbRings+1)
	
	#determiner position en x (rayon) des différents cercles
	i = 0
	while i <= nbRings:
		rings.append(Ring(amplitude = law_a(amplitude, nbRings, i)))
		i += 1

	print("======")
	#en déduire largeur et hauteur
	i = 0
	alternance = H0
	while i < len(rings):
		amplitudeCurrent = rings[i].amplitude
		rings[i].width = fittsLaw_W(Id, amplitudeCurrent)
		rings[i].height = law_H(amplitude, amplitudeCurrent, height) * alternance
		alternance = 1 - alternance
		i += 1

	#showRings(rings)
	#calculer les sommets des anneaux et les sommets des anneaux oblique (cone coupé)
	i = 0
	while i < len(rings):
		radius1 = rings[i].amplitude - (rings[i].width / 2)
		radius2 = rings[i].amplitude + (rings[i].width / 2)
		height = rings[i].height
		ring (verticesDrawing, normalesDrawing, center, radius1, radius2, height, 50)

		#dessine les cones
		if (i < (len(rings) - 1)):
			radius1 = rings[i].amplitude + (rings[i].width / 2)
			radius2 = rings[i+1].amplitude - (rings[i+1].width / 2)
			height1 = rings[i].height
			height2 = rings[i+1].height
			ringAskew(verticesDrawing, normalesDrawing, center, radius1, radius2, height1, height2, 50)
		i += 1


	return maxAxis()


def ring (verticesDrawing, normalesDrawing, center, radius1, radius2, height, nbSegments):
	i = 0
	while i <= nbSegments:
		theta1 = 2 * math.pi * (i%nbSegments) / nbSegments
		theta2 = 2 * math.pi * ((i+1)%nbSegments) / nbSegments
		vertice2 = verticeCompute(center, theta1, radius2, height)
		vertice1 = verticeCompute(center, theta1, radius1, height)
		vertice3 = verticeCompute(center, theta2, radius1, height)

		fullList(vertice2, vertices_tmp) #l'ordre est important !
		fullList(vertice1, vertices_tmp)

		n = normaleCompute(vertice1, vertice2, vertice3)
		fullList((n, n), normales_tmp)
		
		i += 1

	fullMainList(verticesDrawing, vertices_tmp)
	fullMainList(normalesDrawing, normales_tmp)


def ringAskew (verticesDrawing, normalesDrawing, center, radius1, radius2, height1, height2, nbSegments):
	i = 0
	while i <= nbSegments:
		theta1 = 2 * math.pi * (i%nbSegments) / nbSegments
		theta2 = 2 * math.pi * ((i+1)%nbSegments) / nbSegments
		vertice2 = verticeCompute(center, theta1, radius2, height2)
		vertice1 = verticeCompute(center, theta1, radius1, height1)
		vertice3 = verticeCompute(center, theta2, radius1, height2)

		fullList(vertice2, vertices_tmp) #l'ordre est important !
		fullList(vertice1, vertices_tmp)

		n = normaleCompute(vertice1, vertice2, vertice3)
		fullList((n, n, n), normales_tmp)

		i += 1

	fullMainList(verticesDrawing, vertices_tmp)
	fullMainList(normalesDrawing, normales_tmp)


def fullList(objectList, maList):
	global vertices_tmp, normales_tmp, xList, yList
	maList.append(objectList[0])
	maList.append(objectList[1])
	if(maList == vertices_tmp):
		maList.append(objectList[2])
		xList.append(objectList[0])
		yList.append(objectList[1])

def fullMainList(mainTab, tmp):
	i = 0
	while(i < len(tmp)):
		mainTab.append(tmp[i])
		i += 1

def v_sub (v1, v2):
	return [v2[0] - v1[0], v2[1] - v1[1], v2[2] - v1[2]]

def verticeCompute(center, theta, radius, height):
	x = (math.cos(theta) * radius) + center[0]
	y = (math.sin(theta) * radius) + center[1]
	z = height + center[2]
	return(x, y, z)

def normaleCompute(v1, v2, v3):
	vecteur1 = v_sub(v2, v1)
	vecteur2 = v_sub(v3, v1)
	return matrix.v_normalize(matrix.v_cross(vecteur1, vecteur2))

#return Id
def fittsLaw_Id (A, W):
	return math.log2((W/A) + 1)

#return W
def fittsLaw_W (Id, A):
	return (math.pow(2, Id) - 1) * A

#return height
def law_H (A, a, H):
	return a*H / A

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











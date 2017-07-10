
import sys
import math

from . import drawExpe



center0 = [0, 0, 0]
nbTargets = 9

def isInTarget(thetaCible, thetaRotation, distance, rayonCible, xClic, yClic):
	"""True ou False selon si x y est dans la cible"""
def newRadius (oldRadius):
	"""calcule le rayon entre c1 et c5
	Fonction uniquement valable pour ISO"""



def isInTarget(thetaCible, thetaRotation, distance, rayonCible, pdp):

	newD = math.cos(thetaRotation) * distance
	xCenter = math.cos(thetaCible) * newD
	yCenter = math.sin(thetaCible) * newD
	xClic = pdp[0]
	yClic = pdp[1]

	if xClic >= xCenter - (rayonCible/2) and xClic <= xCenter + (rayonCible/2) and \
	   yClic >= yCenter - (rayonCible/2) and yClic <= yCenter + (rayonCible/2):
	   	return True
	else:
		return False

#!!! fonction valable dans un contexte ISO (pour 9 cibles)
def newRadius (oldRadius):
	theta = 8*math.pi / 9
	A = (abs(math.cos(theta)) * oldRadius) + oldRadius
	B = math.sin(theta) * oldRadius
	C = math.sqrt(A*A + B*B)
	return C / 2

def posTarget (theta, radius):
	return math.cos(theta)*radius, math.sin(theta)*radius




















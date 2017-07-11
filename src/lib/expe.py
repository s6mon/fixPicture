
import sys
import math
import numpy
import datetime

from . import drawExpe



center0 = [0, 0, 0]
nbTargets = 9

def isInTarget(thetaCible, thetaRotation, distance, rayonCible, pdp):
	"""True ou False selon si x y est dans la cible"""
def radius_InitToTarget (radius):
	"""calcule le rayon entre c1 et c5
	Fonction uniquement valable pour ISO"""
def posTarget (theta, radius):
	""""""
def mooveObject (tab, trans):
	""""""
def saveData(name, amplitude, largeur, hauteur, nbAnneaux, nbErreurClic, temps):
	""""""


def isInTarget(thetaCible, thetaRotation, distance, rayonCible, pdp):

	newD = math.cos(thetaRotation) * distance
	xCenter = math.cos(thetaCible) * newD
	yCenter = math.sin(thetaCible) * newD
	xClic = pdp[0]
	yClic = pdp[1]

	# print("Mouse :", xClic, yClic)
	# print("Target (x):", xCenter-(rayonCible/2), xCenter+(rayonCible/2))
	# print("Target (y):", yCenter-(rayonCible/2), yCenter+(rayonCible/2))


	if xClic >= xCenter - (rayonCible/2) and xClic <= xCenter + (rayonCible/2) and \
	   yClic >= yCenter - (rayonCible/2) and yClic <= yCenter + (rayonCible/2):
	   	return True
	else:
		return False

#!!! fonction valable dans un contexte ISO (pour 9 cibles)
#prend le rayon à l'état initial et renvoie le rayon entre deux cibles
def radius_InitToTarget (radius):
	theta = 8*math.pi / 9
	A = (abs(math.cos(theta)) * radius) + radius
	B = math.sin(theta) * radius
	C = math.sqrt(A*A + B*B)
	return C / 2

def radius_TargetToInit (radius):
	return radius * (1/radius_InitToTarget(1))

def posTarget (theta, radius):
	return math.cos(theta)*radius, math.sin(theta)*radius



def mooveObject (tab, trans):
	tabReturn = []
	i = 0
	while i < len(tab):
		tabReturn.append(tab[i]   + trans[0])
		tabReturn.append(tab[i+1] + trans[1])
		tabReturn.append(tab[i+2] + trans[2])
		i += 3
	# print("middle(x) :",(tab[0]+tab[12])/2)
	# print("middle(y) :",(tab[7]+tab[19])/2)
	tabReturn = numpy.array(tabReturn, dtype='float32')
	return tabReturn

def saveData(name, amplitude, largeur, hauteur, nbAnneaux, nbErreurClic, temps):
	filePath = "../resultats/"+name+".expe"
	id = drawExpe.fittsLaw_Id(amplitude, largeur)
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M:%S")
	lineToWrite = date+"\t"+str(round(id, 3))+"\t"+str(amplitude)+"\t\t"+str(largeur)+"\t\t"+str(hauteur)+"\t\t"+str(nbAnneaux)+"\t\t"+str(nbErreurClic)+"\t\t"+str(round(temps, 3))+"\n"
	try:
		dataFile = open(filePath, "r")
	except ValueError:
		print()
		print()
		print(ValueError)
		print()
	except:
		firstLine = ("Date :\t\t\tId:\tAmplitude\tLargeur:\tHauteur:\tNbAnneaux:\tNbErreurClic:\tTemps:\n")
		dataFile = open(filePath, "a")
		dataFile.write(firstLine)
	dataFile.close()
	try:
		dataFile = open(filePath, "a")
		dataFile.write(lineToWrite)
	except ValueError:
		print()
		print()
		print(ValueError)
		print()
		overall.stopApplication()
	dataFile.close
	print("Result files saved")











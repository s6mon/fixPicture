
import sys
import math
import numpy
import datetime
import random

from . import drawExpe
from . import overall

#IDX = [Amplitude, Width]
ID3 = [14, 2]
ID4 = [30, 2]
ID5 = [31, 1]

center0 = [0, 0, 0]
nbTargets = 9

def isInTarget(thetaCible, thetaRotation, distance, rayonCible, pdp):
	"""True ou False selon si x y est dans la cible"""
def isAtCenter(rayonCible, mouse):
	""""""
def radius_InitToTarget (radius):
	"""calcule le rayon entre c1 et c5
	Fonction uniquement valable pour ISO"""
def radius_TargetToInit (radius):
	""""""
def newRadius(radius):
	""""""
def thetaBis():
	""""""
def posTarget (theta, radius):
	""""""
def thetaTarget(numTarget):
	""""""
def mooveObject (tab, trans):
	""""""
def saveData(name, amplitude, largeur, hauteur, nbAnneaux, nbErreurClic, temps):
	""""""
def buildArrayExpe(tech):
	""""""
def saveArrayExpe(tab, tech):
	""""""
def loadArrayExpe(tech):
	""""""
def getTabExpe(tech):
	""""""



class ExpeCases:
	def __init__(self):
		self.tech = [0,1,2]
		self.id = [3, 4, 5]
		self.idCompo = [ID3, ID4, ID5]
		self.height = [10, 15, 20]
		self.symmetry = [1] #add -1 to make expe with 2 symmetry



def isInTarget(thetaCible, thetaRotation, distance, rayonCible, mouse):

	newD = math.cos(thetaRotation) * distance
	xCenter = math.cos(thetaCible) * newD
	yCenter = math.sin(thetaCible) * newD
	xClic = mouse[0]
	yClic = mouse[1]

	# print("Mouse :", xClic, yClic)
	# print("Target (x):", xCenter-(rayonCible), xCenter+(rayonCible))
	# print("Target (y):", yCenter-(rayonCible), yCenter+(rayonCible))

	if xClic >= xCenter - (rayonCible) and xClic <= xCenter + (rayonCible) and \
	   yClic >= yCenter - (rayonCible) and yClic <= yCenter + (rayonCible):
	   	return True
	else:
		return False


def isAtCenter(rayonCible, mouse):

	xClic = mouse[0]
	yClic = mouse[1]
	if xClic >= -(rayonCible/2) and xClic <= rayonCible/2 and \
	   yClic >= -(rayonCible/2) and yClic <= rayonCible/2:
	   	return True
	else:
		return False

def radius_InitToTarget (radius):
	theta = 8*math.pi / 9
	A = (abs(math.cos(theta)) * radius) + radius
	B = math.sin(theta) * radius
	C = math.sqrt(A*A + B*B)
	return C / 2

def radius_TargetToInit (radius):
	return radius * (1/radius_InitToTarget(1))

def newRadius(radius):
	return math.cos(math.pi - (8*math.pi/9)) * radius

def thetaBis():
	return math.asin(math.sin(8*math.pi/9)/2)

def posTarget (theta, radius):
	return math.cos(theta)*radius, math.sin(theta)*radius

def thetaTarget(numTarget):
	return numTarget * 2 * math.pi / 9


def mooveObject (tab, trans):
	tabReturn = []
	i = 0
	while i < len(tab):
		tabReturn.append(tab[i]   + trans[0])
		tabReturn.append(tab[i+1] + trans[1])
		tabReturn.append(tab[i+2] + trans[2])
		i += 3
	
	tabReturn = numpy.array(tabReturn, dtype='float32')
	return tabReturn

def saveData(name, tech, amplitude, largeur, hauteur, symetrie, nbErreurClic, temps):
	filePath = "../resultats/"+name+".expe"
	id = drawExpe.fittsLaw_Id(amplitude, largeur)
	now = datetime.datetime.now()
	date = now.strftime("%Y-%m-%d %H:%M:%S")
	lineToWrite = date+"\t\t"+name+"\t\t"+str(tech)+"\t\t"+str(round(id, 3))+"\t\t"+str(amplitude)+"\t\t\t"+str(largeur)+"\t\t\t"+str(hauteur)+"\t\t\t"+str(symetrie)+"\t\t\t"+str(nbErreurClic)+"\t\t\t\t"+str(round(temps, 3))+"\n"
	try:
		dataFile = open(filePath, "r")
	except ValueError:
		print()
		print()
		print(ValueError)
		print()
	except:
		firstLine = ("Date :\t\t\t\t\tName:\t\tTech\tID:\t\tAmplitude\tLargeur:\tHauteur:\tSymétrie:\tNbErreurClic:\tTemps:\n")
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
	#print("Result files saved")


def buildArrayTestExpe(tech):
	return [[tech, 3, 14, 2, 10, 1], [tech, 3, 14, 2, 20, 1], [tech, 5, 31, 1, 10, 1], [tech, 5, 31, 1, 20, 1]]

def buildArrayExpe(tech, nbRepet):

	tab = []
	expeCases = ExpeCases()
	i = len(expeCases.id) * len(expeCases.height) * len(expeCases.symmetry)
	t = tech
	idN = 0
	h = 0
	s = 0
	repetition = 0
	nbRepetition = nbRepet
	
	while i > 0:
		while idN < len(expeCases.id):
			h = 0
			while h < len(expeCases.height):
				s = 0
				while s < len(expeCases.symmetry):
					repetition = 0
					while repetition < nbRepetition:
						tab.append([expeCases.tech[t], expeCases.id[idN], expeCases.idCompo[idN][0], expeCases.idCompo[idN][1], expeCases.height[h], expeCases.symmetry[s]])
						i -= 1
						repetition += 1
					s += 1
				h += 1
			idN += 1

	return tab

def saveArrayExpe(tab, tech):
	pathTab = "../ressources/expe/"+tech

	try:
		numpy.save(pathTab, tab)
	except ValueError:
		print()
		print()
		print(ValueError)
		print()
		overall.stopApplication()
	print("Files saved")

def loadArrayExpe(tech):
	pathTab = "../ressources/expe/"+tech+".npy"

	try:
		tab = numpy.load(pathTab)
	except ValueError:
		print()
		print()
		print(ValueError)
		print()
		overall.stopApplication()
	except:
		print("Files doesn't loaded")
		return False, None
	print("Files loaded")
	return True, tab

def getTabExpe(tech, nbRepet, test):
	cond, tab = loadArrayExpe(tech)
	if not(cond):
		if tech == "T1" or tech == "T1_test":
			if test:
				tab = buildArrayTestExpe(0)
			else:
				tab = buildArrayExpe(0, nbRepet)

		elif tech == "T2" or tech == "T2_test":
			if test:
				tab = buildArrayTestExpe(1)
			else:
				tab = buildArrayExpe(1, nbRepet)

		elif tech == "T3" or tech == "T3_test":
			if test:
				tab = buildArrayTestExpe(2)
			else:
				tab = buildArrayExpe(2, nbRepet)
		else:
			print("Lib (expe.getTab): Argument tehc is wrong")
			overall.stopApplication()
		random.shuffle(tab)
		saveArrayExpe(tab, tech)
	return tab





		








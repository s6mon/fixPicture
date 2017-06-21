
import re
import numpy

from . import overall

vertic_picture = []

verticesTab = []
normaleTab = []

xMin, xMax, yMin, yMax, zMin, zMax = None, None, None, None, None, None


def parse(fileName):
	"""function to parse"""
def fullVertArray (s1, s2, s3):
	"""is not variable"""
def centre(x, y, z):
	"""calcule xMax xMin yMax yMin zMax zMin"""
def reCentre():
	"""change le tableau ou sont stocké les sommets à afficher => translate les sommets sur x y et z"""


#########################################
#           END OF DECLARATION          #
#########################################


def parse(fileName):
	nbBoucle = 0
	global vertic_picture, verticesTab, normaleTab
	print("Opening file to parse (", fileName,")")
	path = "../ressources/"+fileName
	try:
		fileIn = open(path, 'r')
	except IOError as e:
		print("I/O error({0}): {1}".format(e.errno, e.strerror))
		overall.stopApplication()
	print("Start of parsing")
	for ligne in fileIn:

	    match = re.search(r"(^[a-zA-Z]+) (((-?\d+.\d+) (-?\d+.\d+) (-?\d+.\d+))|((\d+)/\d*/(\d+) (\d+)/\d*/(\d+) (\d+)/\d*/(\d+) (\d+)/\d*/(\d+))|((\d+)/\d*/(\d+) (\d+)/\d*/(\d+) (\d+)/\d*/(\d+)))", ligne)

	    if match != None: 
	        if match.group(1) == 'v':
	            verticesTab.append([match.group(4), match.group(5), match.group(6)])
	            centre(match.group(4), match.group(5), match.group(6))

	        if match.group(1) == 'vn':
	            normaleTab.append(match.group(4))

	        if match.group(1) == 'f':
	        	if match.group(8) != None: #il y a plus de 3 sommets
	        		i = 6 #on initialise à 6 car on va aller récupérer le 8ème match de parse
	        		nbVert = 0
	        		s = 1
	        		while s != None:
	        			if nbVert > 2:
	        				nbVert = 0
	        				i = i - 2
	        			else:
	        				i += 2
	        				s = int(match.group(i)) - 1
	        				fullVertArray(verticesTab[s][0], verticesTab[s][1], verticesTab[s][2])
	        				s = match.group(i+2)
	        				nbVert += 1
	        		s0 = int(match.group(8)) - 1 #on relie le dernier sommet de la forme
	        		fullVertArray(verticesTab[s0][0], verticesTab[s0][1], verticesTab[s0][2])
	        	else : #il y a 3 sommets
	        		nbBoucle += 1
	        		i = 17
	        		while i <= 21:
	        			s = int(match.group(i)) - 1
	        			fullVertArray(verticesTab[s][0], verticesTab[s][1], verticesTab[s][2])
	        			i += 2

	vertic_picture = numpy.array(vertic_picture, dtype='float32')
	reCentre()
	fileIn.close()
	print("File closed")

	#TODO return normaleTab
	return vertic_picture

def fullVertArray(s1, s2, s3):
	global vertic_picture
	vertic_picture.append(s1)
	vertic_picture.append(s2)
	vertic_picture.append(s3)

def centre(x, y, z):
	global xMin, xMax, yMin, yMax, zMin, zMax

	#find xMin and xMax
	if (xMin == None and xMax == None):
		xMin = x
		xMax = x
	elif (x > xMax or x < xMin):
		if x < xMin:
			xMin = x
		else:
			xMax = x

	#find yMin and yMax
	if (yMin == None and yMax == None):
		yMin = y
		yMax = y
	elif (y > yMax or y < yMin):
		if y < yMin:
			yMin = y
		else:
			yMax = y

	#find zMin and zMax
	if (zMin == None and zMax == None):
		zMin = z
		zMax = z
	elif (z > zMax or z < zMin):
		if z < zMin:
			zMin = z
		else:
			zMax = z

def reCentre():
	global  vertic_picture

	arraySize = int(len(vertic_picture) / 3)

	xTrans = (float(xMax) + float(xMin)) / 2
	yTrans = (float(yMax) + float(yMin)) / 2
	zTrans = (float(zMax) + float(zMin)) / 2

	i = 0
	while i < arraySize:
		vertic_picture[i]   = vertic_picture[i]   - xTrans
		vertic_picture[i+1] = vertic_picture[i+1] - yTrans
		vertic_picture[i+2] = vertic_picture[i+2] - zTrans
		i += 3

	











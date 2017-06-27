
import re
import numpy
import operator

from . import overall

vertic_picture = []
norm_picture = []

verticesXTab = []
verticesYTab = []
verticesZTab = []

xList = []
yList = []
zList = []

normaleTab = []


def parse(fileName):
	"""function to parse"""
def fullVertArray (s1, s2, s3):
	"""is not variable"""
def reCentre():
	"""change le tableau ou sont stocké les sommets à afficher => translate les sommets sur x y et z"""


#########################################
#           END OF DECLARATION          #
#########################################


def parse(fileName):
	global vertic_picture, norm_picture, verticesTab, normaleTab
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
	            verticesXTab.append(match.group(4))
	            verticesYTab.append(match.group(5))
	            verticesZTab.append(match.group(6))

	        if match.group(1) == 'vn':
	            normaleTab.append([match.group(4), match.group(5), match.group(6)])

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
	        				fullVertArray(verticesXTab[s], verticesYTab[s], verticesZTab[s], vertic_picture)
	        				n = int(match.group(i+1)) - 1
	        				fullVertArray(normaleTab[n][0], normaleTab[n][1], normaleTab[n][2], norm_picture)

	        				s = match.group(i+2)
	        				nbVert += 1
	        		s0 = int(match.group(8)) - 1 #on relie le dernier sommet de la forme
	        		fullVertArray(verticesXTab[s0], verticesYTab[s0], verticesZTab[s0], vertic_picture)
	        		n0 = int(match.group(9)) - 1
	        		fullVertArray(normaleTab[n0][0], normaleTab[n0][1], normaleTab[n0][2], norm_picture)
	        	else : #il y a 3 sommets
	        		i = 17
	        		while i <= 21:
	        			s = int(match.group(i)) - 1

	        			fullVertArray(verticesXTab[s], verticesYTab[s], verticesZTab[s], vertic_picture)
	        			n = int(match.group(i+1)) - 1
	        			fullVertArray(normaleTab[n][0], normaleTab[n][1], normaleTab[n][2], norm_picture)

	        			i += 2

	vertic_picture = numpy.array(vertic_picture, dtype='float32')
	norm_picture = numpy.array(norm_picture, dtype='float32')
	reCentre()
	fileIn.close()
	print("File closed")

	return vertic_picture, norm_picture

def fullVertArray(sn1, sn2, sn3, arrayName):
	global vertic_picture, norm_picture
	global xList, yList, zList
	if(arrayName == vertic_picture):
		arrayName.append(sn1)
		arrayName.append(sn2)
		arrayName.append(sn3)
		xList.append(sn1)
		yList.append(sn2)
		zList.append(sn3)
	elif(arrayName == norm_picture):
		arrayName.append([sn1, sn2, sn3])

def reCentre():
	global  vertic_picture

	arraySize = int(len(vertic_picture))

	xTrans = (float(max(xList)) + float(min(xList))) / 2
	yTrans = (float(max(yList)) + float(min(yList))) / 2
	zTrans = (float(max(zList)) + float(min(zList))) / 2

	if yTrans > xTrans:
		scale = 1
	else:
		scale = xTrans
	i = 0
	while i < arraySize:
		vertic_picture[i] = vertic_picture[i] - xTrans #/ xTrans*2 #TODO changer la div pour tout voir ou jouer sur "m_persp_modelview[2][3] = -5" pour changer l'éloignement de la camera 
		vertic_picture[i] = vertic_picture[i] / scale

		vertic_picture[i+1] = vertic_picture[i+1] - yTrans #/ yTrans*2
		vertic_picture[i+1] = vertic_picture[i+1] / scale

		vertic_picture[i+2] = vertic_picture[i+2] - zTrans #/ zTrans*2
		vertic_picture[i+2] = vertic_picture[i+2] / scale
		i += 3











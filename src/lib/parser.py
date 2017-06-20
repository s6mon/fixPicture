import re
import numpy

vertic_picture = []

verticesTab = []
normaleTab = []


def parse(fileName):
	"""function to parse"""
def fullVertArray (s1, s2, s3):
	"""is not variable"""


#########################################
#           END OF DECLARATION          #
#########################################


def parse(fileName):
	global vertic_picture, verticesTab, normaleTab
	print("Opening file to parse")
	path = "../ressources/"+fileName
	fileIn = open(path, 'r')
	print("Start of parsing")
	for ligne in fileIn:

	    match = re.search(r"(^[a-zA-Z]+) (((-?\d+.\d+) (-?\d+.\d+) (-?\d+.\d+))|((\d+)/\d*/(\d+) (\d+)/\d*/(\d+) (\d+)/\d*/(\d+) (\d+)/\d*/(\d+))|((\d+)/\d*/(\d+) (\d+)/\d*/(\d+) (\d+)/\d*/(\d+)))", ligne)

	    if match != None: 
	        if match.group(1) == 'v':
	            verticesTab.append([match.group(4), match.group(5), match.group(6)])

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
	        		i = 17
	        		while i <= 21:
	        			s = int(match.group(i)) - 1
	        			fullVertArray(verticesTab[s][0], verticesTab[s][1], verticesTab[s][2])
	        			i += 2
	        			




	vertic_picture = numpy.array(vertic_picture, dtype='float32')
	fileIn.close()
	print("File closed")

	return vertic_picture

def fullVertArray(s1, s2, s3):
	global vertic_picture
	vertic_picture.append(s1)
	vertic_picture.append(s2)
	vertic_picture.append(s3)













import sys
import math



def stoApplication():
    """Function calling when application must be close"""
def isInTarget(thetaCible, thetaRotation, distance, rayonCible, xClic, yClic):
	"""True ou False selon si x y est dans la cible"""



def stopApplication():
    print("====> END")
    sys.exit(0)

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

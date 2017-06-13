#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 07/April/2017

import numpy
import math

def perspective(fov, aspect, near, far):
    
    d = 1/math.tan(fov/2.)
    mat = numpy.zeros((4,4))
    
    mat[0][0] = d/aspect
    mat[1][1] = d
    mat[2][2] = (near + far)/(near - far)
    mat[2][3] = 2*near*far/(near-far)
    mat[3][2] = -1
    
    return mat


def viewport(sx, sy, w, h, near, far):
    
    mat = numpy.identity(4)
    
    mat[0][0] = w/2.
    mat[0][3] = sx + w/2.
    mat[1][1] = h/2.
    mat[1][3] = sy + h/2.
    mat[2][2] = (far-near)/2.
    mat[2][3] = (far+near)/2.
    
    return mat


def orthographic(left, right, bottom, top, near, far):
    
    mat = numpy.identity(4)
    
    mat[0][0] = 2./(right-left)
    mat[0][3] = -(right+left)/(right-left)
    mat[1][1] = 2./(top-bottom)
    mat[1][3] = -(top+bottom)/(top-bottom)
    mat[2][2] = -2./(far-near)
    mat[2][3] = -(far+near)/(far-near)
    
    return mat

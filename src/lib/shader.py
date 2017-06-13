#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#Michael ORTEGA - 07/April/2017

try:
    from OpenGL.GL      import *
    from OpenGL.GL      import shaders
except:
    print ('''ERROR: PyOpenGL not installed properly.''')

def compile(path, type):
    try:
        shader = open(path, 'r').read()
    except:
        print('\n\n\t!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('\t!!! Cannot read', path, '!!!')
        print('\t!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        return None
    
    vs = glCreateShader(type)
    glShaderSource(vs, shader)
    
    glCompileShader(vs)
    log = glGetShaderInfoLog(vs)
    if log: 
        print('\n\n\t!!!!!!!!!!!!!!!!!!!!!!!!!')
        print('\t!!!Shader', path,': ', log)
        print('\t!!!!!!!!!!!!!!!!!!!!!!!!!\n')
        return None
    
    return vs


def create(vert_fname, geom_fname, frag_fname, attrib_indexes, attrib_names):
    
    #Reading Shaders
    if vert_fname:
        vs = compile(vert_fname, GL_VERTEX_SHADER)
        if not vs:
            sys.exit()
    
    if geom_fname:
        gs = compile(geom_fname, GL_GEOMETRY_SHADER)
        if not gs:
            sys.exit()
    
    if frag_fname:
        fs = compile(frag_fname, GL_FRAGMENT_SHADER)
        if not fs:
            sys.exit()
    
    sh = glCreateProgram()
    
    if vert_fname:
        glAttachShader(sh, vs)
    if geom_fname:
        glAttachShader(sh, gs)
    if frag_fname:
        glAttachShader(sh, fs)
    
    for i, n in zip(attrib_indexes, attrib_names):
        glBindAttribLocation(sh, i, n)
        
    glLinkProgram(sh)
    
    log = glGetProgramInfoLog(sh)
    if log : 
        print('After Linking the shader program:\n', log)
        return None
    
    log = glUseProgram(sh)
    if log :
        print('After using program:\n', log)
        return None
    
    return sh

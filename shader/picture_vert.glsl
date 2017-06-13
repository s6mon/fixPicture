#version 330 core
precision highp float;

uniform mat4 projection_mat;
uniform mat4 modelview_mat;

in vec3 position;

void main (){
	gl_Position = projection_mat * modelview_mat * vec4(position, 1.0);
}
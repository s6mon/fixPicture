#version 330 core
precision highp float;

uniform mat4 projection_mat;
uniform mat4 modelview_mat;
uniform mat4 view_mat;

in vec3 position;
//vec4 c_4 = inverse(view_mat)*vec4(0,0,0,1.0);


void main (){
	gl_Position = projection_mat * view_mat * modelview_mat * vec4(position, 1.0);
}
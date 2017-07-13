#version 330 core
precision highp float;

uniform mat4 projection_mat;
uniform mat4 modelview_mat;
uniform mat4 object_mat;

uniform vec3 light;

out float color_factor;
out vec4 t;

const vec3 oldLight = vec3(0, 0, 15);

vec3 l;

in vec3 position;
in vec3 normale;
in vec4 color;



void main (){
	//Projection * MV * Rotation/Translation
	gl_Position = projection_mat * modelview_mat * object_mat * vec4(position, 1.0);
	//calcul de la lumière a appliquer sur chaque sommets
	l = light - position;
	l = l / length(l);
	color_factor = clamp(dot(normale, l), 0, 1);
	t = color;
}
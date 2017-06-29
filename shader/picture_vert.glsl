#version 330 core
precision highp float;

uniform mat4 projection_mat;
uniform mat4 modelview_mat;
uniform mat4 object_mat;

out float color_factor;

const vec3 light = vec3(5, 0, 5);
const mat4 translate = mat4(vec4(1.0, 0.0, 0.0, 0.),
					   		vec4(0.0, 1.0, 0.0, 0.),
					    	vec4(0.0, 0.0, 1.0, 0.),
					    	vec4(0.0, 0.0, -0.5, 1.));
vec3 l;
in vec3 position;
in vec3 normale;

void main (){
	//Projection * MV * Rotation/Translation
	gl_Position = projection_mat * modelview_mat * object_mat * vec4(position, 1.0);
	//calcul de la lumière a appliquer sur chaque sommets
	l = light - position;
	l = l / length(l);
	color_factor = clamp(dot(normale, l), 0, 1);
}
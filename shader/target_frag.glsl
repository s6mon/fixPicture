#version 330 core
precision highp float; //High precision, critical !!!

out vec4 fragColor;

in float color_factor;
in vec3 t;


void main() {
    fragColor = vec4(t, 0.0) * color_factor;
}
#version 330 core
precision highp float; //High precision, critical !!!

out vec4 fragColor;

in float color_factor;
in vec4 t;


void main() {
    fragColor = t * color_factor;
}
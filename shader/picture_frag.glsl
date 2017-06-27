#version 330 core
precision highp float; //High precision, critical !!!

out vec4 fragColor;

in float color_factor;


void main() {
    fragColor = vec4(1,0,0,0.0) * color_factor;
    float t = color_factor;
}
#version 330 core
precision highp float; //High precision, critical !!!

out vec4 fragColor;

in float color_factor;


void main() {
    fragColor = vec4(vec3(1,1,1) * color_factor, 1.0);
}
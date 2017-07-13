#version 330 core
precision highp float; //High precision, critical !!!

out vec4 fragColor;

in float color_factor;


void main() {
<<<<<<< HEAD
    fragColor = vec4(1,1,1,1.0) * color_factor;
=======
    fragColor = vec4(1,0,0,0.0) * color_factor;
>>>>>>> 4190de08ba90299b7fad440a75651e4e1613ce0a
}
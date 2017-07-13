#version 330 core
precision highp float; //High precision, critical !!!

out vec4 fragColor;

in float color_factor;
<<<<<<< HEAD
in vec4 t;


void main() {
    fragColor = t * color_factor;
=======
in vec3 t;


void main() {
    fragColor = vec4(t, 0.0) * color_factor;
>>>>>>> 4190de08ba90299b7fad440a75651e4e1613ce0a
}
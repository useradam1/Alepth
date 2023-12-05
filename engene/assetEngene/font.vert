#version 130 

in vec2 v_texCoord;
in vec3 v_normal;

out vec2 texCoord;
out vec3 Normal;

void main() {
    gl_Position = gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex;
	texCoord = v_texCoord;
    Normal = v_normal;
}
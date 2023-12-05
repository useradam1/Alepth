#version 130 

in vec2 v_texCoord;
in vec3 v_normal;

out vec2 texCoord;
out vec3 Normal;
out vec2 ScreenSize;

uniform vec2 screenSize;

void main() {
    gl_Position = (gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex)*vec4(screenSize,1,1);

	texCoord = v_texCoord;

    Normal = v_normal;

	ScreenSize = screenSize;
}
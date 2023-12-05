#version 130 

in vec2 v_texCoord;
in vec3 v_normal;

out vec2 texCoord;
out vec3 Normal;
out float FarPlane;
out vec3 FragPos;

void main() {
    gl_Position = (gl_ProjectionMatrix * gl_ModelViewMatrix * gl_Vertex);

    FragPos = gl_Vertex.xyz;

	texCoord = v_texCoord;

    Normal = v_normal;

    FarPlane = gl_Position.z;
}
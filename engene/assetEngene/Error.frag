#version 130

in vec3 FragPos;
in vec2 texCoord;
in vec3 Normal;

uniform float time;
uniform vec3 v_Pos;
uniform vec3 v_Sca;
uniform mat3 v_Rot;
uniform vec3 CamPos;

void main(){
	vec3 fragPos = ((v_Rot*FragPos) * v_Sca) + v_Pos;
	vec3 normal = v_Rot * Normal;
	vec3 viewDir = normalize(CamPos-fragPos);

	float diff = 0.7 + max(0 , dot(normal,viewDir) ) * 0.3;

	gl_FragColor = vec4(

		vec3(
			1,
			vec2(sin(time)*0.5)
		) * diff
		
		,

		1

	);
}
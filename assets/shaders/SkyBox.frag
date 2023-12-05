#version 130
#define PI 			3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986

in vec2 texCoord;
in vec3 Normal;
in float FarPlane;
in vec3 FragPos;


uniform sampler2D SkyBox;
uniform vec2 ScreenSize;
uniform mat3 CamRot;
uniform float Fov;


void main(){
	float fov = (1.0/(Fov/100.0));
	vec2 uv = (2*gl_FragCoord.xy-ScreenSize)*pow(ScreenSize.y,-1);
	mat3 m = mat3(
		vec3(1,0,0),
		vec3(0,0,1),
		vec3(0,-1,0)
	);
	vec3 dir = normalize(m*(CamRot*vec3(uv,fov*0.98)));

	vec2 uvSky = vec2(atan(dir.x,dir.y), asin(dir.z)*2);
	uvSky/=PI;
	uvSky=uvSky*0.5+0.5;
	vec4 SkyColor = texture2D(SkyBox,uvSky);
	gl_FragColor = vec4( SkyColor.rgb , SkyColor.a );
}
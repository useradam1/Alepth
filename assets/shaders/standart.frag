#version 130
#define PI 			3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986

in vec2 texCoord;
in vec3 Normal;

in float FarPlane;
uniform float MaxFarPlaneCamera;
uniform vec3 CamPos;
uniform mat3 CamRot;
uniform float Fov;

in vec3 FragPos;
uniform vec3 v_Pos;
uniform vec3 v_Sca;
uniform mat3 v_Rot;

uniform vec4 Color;
uniform float Specular;
uniform bool useTexture;
uniform sampler2D Texture;
uniform bool useNormalTexture;
uniform sampler2D NormalTexture;
uniform vec2 scaleTex;
uniform vec2 shiftTex;

uniform sampler2D SkyBox;
uniform mat3 SunDirection;
uniform vec2 ScreenSize;

void main(){
	// SKYBOX
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
	//===================

	vec3 fragPos = ((v_Rot*FragPos) * v_Sca) + v_Pos;

	vec3 normal = v_Rot * Normal;
	vec3 normalTex = normal;
	if(useNormalTexture){
		vec3 nTex = normalize( (texture2D(NormalTexture,(texCoord*scaleTex)+shiftTex)).xyz * 2 - 1 );

		mat3 TBN = mat3(normalize(-dFdx(fragPos)), normalize(dFdy(fragPos)), normalTex);

		vec3 finalNormal = normalize(TBN * nTex);
		normalTex = normalize(mix(normalTex,finalNormal,0.75));
	}

	float diffusenormal = max(0 , dot(normal,SunDirection[2]) );

	// diffuse light
	float diffuse = max(0 , dot(normalTex,SunDirection[2]) ) * diffusenormal;

	// specular light
	vec3 viewDir = normalize(CamPos-fragPos);
	vec3 refl = reflect(-SunDirection[2],normalTex);
	float spec = pow(max(dot(viewDir,refl),0),50) * Specular * diffusenormal;	
	
	vec4 finColor;
	if(useTexture)finColor = Color * texture2D(Texture,(texCoord*scaleTex)+shiftTex);
	else finColor = Color;


	finColor = vec4(pow(finColor.rgb, vec3(2.2)),finColor.a);

	finColor = vec4(finColor.rgb * (0.5 + diffuse * 0.5) + vec3(1) * spec ,finColor.a);

	finColor = vec4(pow(finColor.rgb, 1 / vec3(2.2)),finColor.a);


    float Fog = clamp(1-(FarPlane/MaxFarPlaneCamera),0.0,1.0);

	finColor = vec4((( finColor.rgb * Fog ) + ( vec4(0.5) * (1 - Fog) ).rgb), finColor.a );


    Fog = clamp(1-(pow(FarPlane*0.001,4)/MaxFarPlaneCamera),0.0,1.0);

	finColor = vec4((( finColor.rgb * Fog ) + ( SkyColor * (1 - Fog) ).rgb), finColor.a );

	gl_FragColor = vec4( finColor.rgb , finColor.a );
}
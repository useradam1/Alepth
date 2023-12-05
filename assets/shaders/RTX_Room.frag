#version 130
#define PI 			3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986

#define CountPortal	2
#define CountSphere	3
#define CountPlane	9
#define CountCube	1
#define CountCloud	1
#define CountAtmosphere	1

mat3 mat3x3_y180 = mat3(
	-1,  0,  0,
	0, 1,  0,
	0, 0, -1
);
mat3 mat3x3_y90 = mat3(
	0,  0,  -1,
	0, 1,  0,
	1, 0, 0
);
mat3 mat3x3_y_90 = mat3(
	0,  0,  1,
	0, 1,  0,
	-1, 0, 0
);
mat3 mat3x3_x90 = mat3(
	1,  0,  0,
	0, 0,  1,
	0, -1, 0
);
mat3 mat3x3_x_90 = mat3(
	1,  0,  0,
	0, 0,  -1,
	0, 1, 0
);
mat3 mat3x3_z_90 = mat3(
	0,  -1,  0,
	1, 0,  0,
	0, 0, 1
);


in vec2 texCoord;
in vec3 Normal;
in vec2 ScreenSize;

uniform float FrameId;
uniform vec3 PosCam;
uniform mat3 MatCam;


uniform vec3 PortalPosition[CountPortal];
uniform vec3 PortalSize[CountPlane];
uniform mat3 PortalMatrix[CountPortal];
uniform vec4 PortalColor[CountPortal];


uniform vec4 Sphere[CountSphere];
uniform vec4 SphereColor[CountSphere];
uniform vec4 SphereLuminescence[CountSphere];
uniform vec3 SphereIntensity[CountSphere];
uniform vec3 SphereRoughness[CountSphere];
uniform float SphereDensity[CountSphere];
uniform bool SphereHollow[CountSphere];


uniform vec3 PlaneCenter[CountPlane];
uniform vec2 PlaneSize[CountPlane];
uniform mat3 PlaneRot[CountPlane];
uniform vec4 PlaneColor[CountPlane];
uniform sampler2D PlaneMainTexture[CountPlane];
uniform vec4 PlaneMainTexOffset[CountPlane];
uniform sampler2D PlaneNormalTexture[CountPlane];
uniform float PlaneNormalTexStreight[CountPlane];
uniform vec4 PlaneNormalTexOffset[CountPlane];
uniform sampler2D PlaneIntensityTexture[CountPlane];
uniform vec4 PlaneIntensityTexOffset[CountPlane];
uniform vec4 PlaneLuminescence[CountPlane];
uniform vec3 PlaneIntensity[CountPlane];
uniform vec3 PlaneRoughness[CountPlane];
uniform float PlaneDensity[CountPlane];


uniform vec3 CubeCenter[CountCube];
uniform vec3 CubeSize[CountCube];
uniform mat3 CubeRot[CountCube];
uniform vec4 CubeColor[CountCube];
uniform sampler2D CubeMainTexture[CountCube];
uniform vec4 CubeMainTexOffset[CountCube];
uniform sampler2D CubeNormalTexture[CountCube];
uniform float CubeNormalTexStreight[CountCube];
uniform vec4 CubeNormalTexOffset[CountCube];
uniform sampler2D CubeIntensityTexture[CountCube];
uniform vec4 CubeIntensityTexOffset[CountCube];
uniform vec4 CubeLuminescence[CountCube];
uniform vec3 CubeIntensity[CountCube];
uniform vec3 CubeRoughness[CountCube];
uniform float CubeDensity[CountCube];
uniform bool CubeHollow[CountCube];


uniform vec3 CloudCenter[CountCloud];
uniform vec3 CloudSize[CountCloud];
uniform mat3 CloudRot[CountCloud];
uniform vec4 CloudColor[CountCloud];
uniform vec4 CloudLuminescence[CountCloud];
uniform vec3 CloudIntensity[CountCloud];
uniform vec3 CloudRoughness[CountCloud];
uniform float CloudDensity[CountCloud];
uniform float CloudHollow[CountCloud];
uniform float CloudParticleSize[CountCloud];
uniform vec3 CloudOffsetScale[CountCloud];
uniform vec3 CloudOffsetPos[CountCloud];


uniform vec4 Atmosphere[CountAtmosphere];
uniform vec4 AtmosphereColor[CountAtmosphere];
uniform vec4 AtmosphereLuminescence[CountAtmosphere];
uniform vec3 AtmosphereIntensity[CountAtmosphere];
uniform vec3 AtmosphereRoughness[CountAtmosphere];
uniform float AtmosphereDensity[CountAtmosphere];
uniform float AtmosphereHollow[CountAtmosphere];
uniform float AtmosphereDistCenter[CountAtmosphere];
uniform float AtmosphereConcentration[CountAtmosphere];


vec2 uv;
int state;


struct RAY{vec3 ro,rd;};
struct OBJ{
	bool intersect; 
	vec3 norhit;
	vec3 poshit; 
	vec2 T; 
	vec4 color; 
	vec4 luminescence;
	vec3 intensity;
	vec3 roughness;
	float density; 
	int id;
	int ObjectCode;
	bool hollow;
	bool flip;
};

mat4 rotationAxisAngle(in vec3 v, in float angle )
{
    float s = sin( angle );
    float c = cos( angle );
    float ic = 1.0 - c;

    return mat4( v.x*v.x*ic + c,     v.y*v.x*ic - s*v.z, v.z*v.x*ic + s*v.y, 0.0,
                 v.x*v.y*ic + s*v.z, v.y*v.y*ic + c,     v.z*v.y*ic - s*v.x, 0.0,
                 v.x*v.z*ic - s*v.y, v.y*v.z*ic + s*v.x, v.z*v.z*ic + c,    0.0,
			     0.0,               0.0,               0.0,               1.0 );
}
mat4 translate(in float x, in float y, in float z )
{
    return mat4( 1.0, 0.0, 0.0, 0.0,
				 0.0, 1.0, 0.0, 0.0,
				 0.0, 0.0, 1.0, 0.0,
				 x,   y,   z,   1.0 );
}
mat4 inverse( in mat4 m )
{
	return mat4(
        m[0][0], m[1][0], m[2][0], 0.0,
        m[0][1], m[1][1], m[2][1], 0.0,
        m[0][2], m[1][2], m[2][2], 0.0,
        -dot(m[0].xyz,m[3].xyz),
        -dot(m[1].xyz,m[3].xyz),
        -dot(m[2].xyz,m[3].xyz),
        1.0 );
}
mat3 rotationAxisAngleMatrix3x3(vec3 axis, float angle){
	float x = axis.x;
	float y = axis.y;
	float z = axis.z;

	float Adeg = radians(-angle);
	float cos_angle = cos(Adeg);
	float sin_angle = sin(Adeg);
	float one_minus_cos = 1.0 - cos_angle;

	return mat3(
		vec3(cos_angle + x*x*one_minus_cos	,	x*y*one_minus_cos - z*sin_angle		,	x*z*one_minus_cos + y*sin_angle),

		vec3(y*x*one_minus_cos + z*sin_angle	,	 cos_angle + y*y*one_minus_cos	,	y*z*one_minus_cos - x*sin_angle),
		
		vec3(z*x*one_minus_cos - y*sin_angle	,	 z*y*one_minus_cos + x*sin_angle	,	 cos_angle + z*z*one_minus_cos)
	);
}
mat3 invertMatrix3x3(mat3 m) {
    mat3 result;

    result[0][0] = m[1][1] * m[2][2] - m[1][2] * m[2][1];
    result[1][0] = m[1][2] * m[2][0] - m[1][0] * m[2][2];
    result[2][0] = m[1][0] * m[2][1] - m[1][1] * m[2][0];

    result[0][1] = m[0][2] * m[2][1] - m[0][1] * m[2][2];
    result[1][1] = m[0][0] * m[2][2] - m[0][2] * m[2][0];
    result[2][1] = m[0][1] * m[2][0] - m[0][0] * m[2][1];

    result[0][2] = m[0][1] * m[1][2] - m[0][2] * m[1][1];
    result[1][2] = m[0][2] * m[1][0] - m[0][0] * m[1][2];
    result[2][2] = m[0][0] * m[1][1] - m[0][1] * m[1][0];

    float determinant = m[0][0] * result[0][0] + m[0][1] * result[1][0] + m[0][2] * result[2][0];

    // Check for nearly zero determinant to avoid division by small numbers
    if (abs(determinant) < 1e-6) {
        // Handle the case when determinant is close to zero (matrix is singular)
        return mat3(0.0);
    }

    float invDeterminant = 1.0 / determinant;

    // Multiply the result by the inverse determinant
    return result * invDeterminant;
}
vec3 spherical_to_cartesian(in float theta, in float phi) {
    float x = sin(theta) * cos(phi);
    float y = -sin(theta) * sin(phi);
    float z = cos(theta);
    return vec3(x, y, z);
}
vec3 generate_sphere_points(int index, float offset) {
    float inc = 2.39995687586;  // golden angle increment
    float y = float(index) * offset + (offset * 0.5);
    float phi = mod(float(index) * inc, 6.28319);
    float theta = acos(2.0 * y - 1.0);
    vec3 point = spherical_to_cartesian(theta, phi);
    return normalize(point);
}
float rand(vec2 co, float seed) {
    return fract(sin(dot(co.xy, vec2(12.9898, 78.233 + seed))) * 43758.5453123);
}
float RandomValue(inout int state){
	state = state * 747796405 + 2891336453;
	int result = ((state >> ((state >> 28) + 4)) ^ state) * 2778037373;
	result = (result >> 22) ^ result;
	return result / (4294967295.0);
}
vec3 random_unit_vector(vec3 base_vector) {
	float x = rand(uv+RandomValue(state),FrameId);
	float y = rand(uv+RandomValue(state),FrameId);
	float z = rand(uv+RandomValue(state),FrameId);
	vec3 vec = normalize(vec3(0.5-x,0.5-y,0.5-z)*2.0);
	if(length(vec)<=0.5) vec=base_vector;
    return vec;
}
float interpolate3(float a, float b, float c, float t) {
    // Линейная интерполяция между a и b
    float ab = mix(a, b, t);
    
    // Линейная интерполяция между b и c
    float bc = mix(b, c, t);
    
    // Итоговая линейная интерполяция между ab и bc
    return mix(ab, bc, t);
}

float mod289(float x){return x - floor(x * (1.0 / 289.0)) * 289.0;}
vec4 mod289(vec4 x){return x - floor(x * (1.0 / 289.0)) * 289.0;}
vec4 perm(vec4 x){return mod289(((x * 34.0) + 1.0) * x);}

float noise(vec3 p){
    vec3 a = floor(p);
    vec3 d = p - a;
    d = d * d * (3.0 - 2.0 * d);

    vec4 b = a.xxyy + vec4(0.0, 1.0, 0.0, 1.0);
    vec4 k1 = perm(b.xyxy);
    vec4 k2 = perm(k1.xyxy + b.zzww);

    vec4 c = k2 + a.zzzz;
    vec4 k3 = perm(c);
    vec4 k4 = perm(c + 1.0);

    vec4 o1 = fract(k3 * (1.0 / 41.0));
    vec4 o2 = fract(k4 * (1.0 / 41.0));

    vec4 o3 = o2 * d.z + o1 * (1.0 - d.z);
    vec2 o4 = o3.yw * d.x + o3.xz * (1.0 - d.x);

    return o4.y * d.y + o4.x * (1.0 - d.y);
}

#define INV_SQRT_OF_2PI 0.39894228040143267793994605993439  // 1.0/SQRT_OF_2PI
#define INV_PI 0.31830988618379067153776752674503

vec4 smartDeNoise(sampler2D tex, vec2 uv, float sigma, float kSigma, float threshold)
{
//  sampler2D tex     - sampler image / texture
//  vec2 uv           - actual fragment coord
//  float sigma  >  0 - sigma Standard Deviation
//  float kSigma >= 0 - sigma coefficient 
//      kSigma * sigma  -->  radius of the circular kernel
//  float threshold   - edge sharpening threshold 
    float radius = round(kSigma*sigma);
    float radQ = radius * radius;

    float invSigmaQx2 = .5 / (sigma * sigma);      // 1.0 / (sigma^2 * 2.0)
    float invSigmaQx2PI = INV_PI * invSigmaQx2;    // 1/(2 * PI * sigma^2)

    float invThresholdSqx2 = .5 / (threshold * threshold);     // 1.0 / (sigma^2 * 2.0)
    float invThresholdSqrt2PI = INV_SQRT_OF_2PI / threshold;   // 1.0 / (sqrt(2*PI) * sigma^2)

    vec4 centrPx = texture(tex,uv); 

    float zBuff = 0.0;
    vec4 aBuff = vec4(0.0);
    vec2 size = vec2(textureSize(tex, 0));

    vec2 d;
    for (d.x=-radius; d.x <= radius; d.x++) {
        float pt = sqrt(radQ-d.x*d.x);       // pt = yRadius: have circular trend
        for (d.y=-pt; d.y <= pt; d.y++) {
            float blurFactor = exp( -dot(d , d) * invSigmaQx2 ) * invSigmaQx2PI;

            vec4 walkPx =  texture(tex,uv+d/size);
            vec4 dC = walkPx-centrPx;
            float deltaFactor = exp( -dot(dC, dC) * invThresholdSqx2) * invThresholdSqrt2PI * blurFactor;

            zBuff += deltaFactor;
            aBuff += deltaFactor*walkPx;
        }
    }
    return aBuff/zBuff;
}




OBJ portal(RAY ray, int id) {

    vec3 planeOrigin = (ray.ro-PortalPosition[id])*PortalMatrix[id];
	vec3 dir = ray.rd*PortalMatrix[id];
    vec3 planeNormal = vec3(0,0,1);
	vec3 radius = PortalSize[id];

	float DotP = dot(planeNormal, dir);
    
    float t = dot(planeNormal,-planeOrigin) / DotP;

    if (t >= 0.0) {
        vec3 intersectionPoint = (planeOrigin + dir * t);
		intersectionPoint *= vec3(radius.xy,1.0);

        if (length(intersectionPoint)<=radius.z) {
			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?-((PortalMatrix[id])*planeNormal):((PortalMatrix[id])*planeNormal);
	
			return OBJ(
				true,
				normal,
				pos,
				vec2(t, t+0.01),
				PortalColor[id],
				vec4(0.0),
				vec3(0.0),
				vec3(0.0),
				0.0,
				id,
				0,
				false,
				false
			);
        }
    }




    return OBJ(
		false,
		vec3(0.0),
		vec3(0.0),
		vec2(-1.0),
		vec4(0.0),
		vec4(0.0),
		vec3(0.0),
        vec3(0.0),
		0.0,
		-1,
		-1,
		false,
		false
	);
}

OBJ sphere(RAY ray, int id) {

    vec4 sphere = Sphere[id];
    vec3 ce = sphere.xyz;
    float r = sphere.w;

    vec3 oc = ray.ro - ce;

    float b = 2.0 * dot(oc, ray.rd);
	float c = length(ray.ro-ce);

    float discriminant = b*b - 4.0*(c*c-r*r);
    if (discriminant > 0.0) {
		float s = sqrt(discriminant);
        float tNear = max(0,(-b - s) * 0.5);
        float tFar = max(0,(-b + s) * 0.5);
        if (tFar > 0.0) {

            vec3 pos;
			vec3 normal;
			if(tNear>0){
				pos = ray.ro + ray.rd * tNear;
				normal = normalize(pos - ce);
			}
			else{
				pos = ray.ro + ray.rd * tFar;
				normal = -normalize(pos - ce);
			}

			return OBJ(
				true,
				normal,
				pos,
				vec2(tNear, tFar),
				SphereColor[id],
				SphereLuminescence[id],
				SphereIntensity[id],
				SphereRoughness[id],
				SphereDensity[id],
				id,
				1,
				SphereHollow[id],
				!(tNear>0)
			);
        }
    }
    return OBJ(
		false,
		vec3(0.0),
		vec3(0.0),
		vec2(-1.0),
		vec4(0.0),
		vec4(0.0),
		vec3(0.0),
        vec3(0.0),
		0.0,
		-1,
		-1,
		false,
		false
	);
}

OBJ plane(RAY ray, int id) {
    vec3 planeOrigin = (ray.ro-PlaneCenter[id])*PlaneRot[id];
	vec3 dir = ray.rd*PlaneRot[id];
    vec3 planeNormal = vec3(0,0,1);
	vec2 planeSize = PlaneSize[id];

	float DotP = dot(planeNormal, dir);
    
    float t = dot(planeNormal,-planeOrigin) / DotP;

    if (t >= 0.0) {
        vec3 intersectionPoint = (planeOrigin + dir * t);

        if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?-(PlaneRot[id][2]):(PlaneRot[id][2]);
            // Точка пересечения находится внутри прямоугольника плоскости
			vec4 mainTex = texture2D(PlaneMainTexture[id],PlaneMainTexOffset[id].zw+vec2(0.5)+(PlaneMainTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0)));
			vec4 LightColor = texture2D(PlaneIntensityTexture[id],PlaneIntensityTexOffset[id].zw+vec2(0.5)+(PlaneIntensityTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0)));

			vec3 norm = normalize(texture2D(PlaneNormalTexture[id],PlaneNormalTexOffset[id].zw+vec2(0.5)+(PlaneNormalTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0))).xyz * 2.0 -1.0);
			if(DotP>0.0)norm.z*=-1.0;
			vec3 finalNormal = normalize(PlaneRot[id]*norm);
			finalNormal = normalize((normal*0.1)+(finalNormal*PlaneNormalTexStreight[id]));
            return OBJ(
				true, 
				finalNormal, 
				pos, 
				vec2(t, t+0.01),
				PlaneColor[id]*mainTex,
				PlaneLuminescence[id],
				PlaneIntensity[id]*LightColor.rgb, 
				PlaneRoughness[id], 
				PlaneDensity[id],
				id,
				2,
				true,
				DotP>0.0
			);
        }
    }

    return OBJ(
		false,
		vec3(0.0),
		vec3(0.0),
		vec2(-1.0),
		vec4(0.0),
		vec4(0.0),
		vec3(0.0),
        vec3(0.0),
		0.0,
		-1,
		-1,
		false,
		false
	);
}

OBJ cube(in RAY ray, in int id) {
	OBJ o = OBJ(
		false,
		vec3(0.0),
		vec3(0.0),
		vec2(-1.0),
		CubeColor[id],
		CubeLuminescence[id],
		CubeIntensity[id],
		CubeRoughness[id],
		CubeDensity[id],
		id,
		3,
		CubeHollow[id],
		false
	);

	vec3 calc_pos = vec3(0.0);
	vec3 calc_normal = vec3(0.0);
	bool calc_flip = false;

	float dist_near = -1.0;
	float dist_far = -1.0;

	mat3 PlaneRot = CubeRot[id];
	vec3 dir = ray.rd*PlaneRot;





	vec3 PlaneCenter = CubeCenter[id]+(PlaneRot*vec3(0.0,0.0,CubeSize[id].z));
	vec2 PlaneSize = CubeSize[id].xy;
	
	vec3 planeOrigin = (ray.ro-PlaneCenter)*PlaneRot;
    vec3 planeNormal = vec3(0.0,0.0,1.0);
	vec2 planeSize = PlaneSize;

	float DotP = dot(planeNormal, dir);
    
    float t = dot(planeNormal,-planeOrigin) / DotP;
	
    if (t >= 0.0) {
        vec3 intersectionPoint = (planeOrigin + dir * t);

        if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			intersectionPoint.x*=-1;

			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?-(PlaneRot[2]):(PlaneRot[2]);
			
			vec4 mainTex = texture2D(CubeMainTexture[id],CubeMainTexOffset[id].zw+vec2(0.5)+(CubeMainTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0)));
			vec4 LightColor = texture2D(CubeIntensityTexture[id],CubeIntensityTexOffset[id].zw+vec2(0.5)+(CubeIntensityTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0)));

			vec3 norm = normalize(texture2D(CubeNormalTexture[id],CubeNormalTexOffset[id].zw+vec2(0.5)+(CubeNormalTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0))).xyz * 2.0 -1.0);
			if(DotP>0.0)norm.z*=-1.0;
			vec3 finalNormal = normalize(PlaneRot*norm);
			finalNormal = normalize((normal*0.1)+(finalNormal*CubeNormalTexStreight[id]));

			if(dist_near>t || dist_near==-1.0){
				o.intersect = true;
				o.color = CubeColor[id]*mainTex;
				o.intensity = CubeIntensity[id]*LightColor.rgb;
				calc_pos = pos;
				calc_normal = finalNormal;
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
        }
    }



	PlaneCenter = CubeCenter[id]+(PlaneRot*vec3(0.0,0.0,-CubeSize[id].z));
	PlaneSize = CubeSize[id].xy;
	
	planeOrigin = (ray.ro-PlaneCenter)*PlaneRot;
    planeNormal = vec3(0.0,0.0,-1.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
    
    t = dot(planeNormal,-planeOrigin) / DotP;

    if (t >= 0.0) {
        vec3 intersectionPoint = -(planeOrigin + dir * t);

        if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			intersectionPoint.x*=-1;

			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?(PlaneRot[2]):-(PlaneRot[2]);
			
			vec4 mainTex = texture2D(CubeMainTexture[id],CubeMainTexOffset[id].zw+vec2(0.5)+(CubeMainTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0)));
			vec4 LightColor = texture2D(CubeIntensityTexture[id],CubeIntensityTexOffset[id].zw+vec2(0.5)+(CubeIntensityTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0)));

			vec3 norm = normalize(texture2D(CubeNormalTexture[id],CubeNormalTexOffset[id].zw+vec2(0.5)+(CubeNormalTexOffset[id].xy*intersectionPoint.xy/(planeSize*2.0))).xyz * 2.0 -1.0);
			if(DotP>0.0)norm.z*=-1.0;
			vec3 finalNormal = normalize(PlaneRot*(-norm));
			finalNormal = normalize((normal*0.1)+(finalNormal*CubeNormalTexStreight[id]));

			if(dist_near>t || dist_near==-1.0){
				o.intersect = true;
				o.color = CubeColor[id]*mainTex;
				o.intensity = CubeIntensity[id]*LightColor.rgb;
				calc_pos = pos;
				calc_normal = finalNormal;
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
        }
    }



	PlaneCenter = CubeCenter[id]+(PlaneRot*vec3(0.0,CubeSize[id].y,0.0));
	PlaneSize = CubeSize[id].xz;
	
	planeOrigin = (ray.ro-PlaneCenter)*PlaneRot;
    planeNormal = vec3(0.0,1.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
    
    t = dot(planeNormal,-planeOrigin) / DotP;

    if (t >= 0.0) {
        vec3 intersectionPoint = (planeOrigin + dir * t);

        if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.z) <= planeSize.y) {
			intersectionPoint*=-1;

			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?-(PlaneRot[1]):(PlaneRot[1]);
			
			vec4 mainTex = texture2D(CubeMainTexture[id],CubeMainTexOffset[id].zw+vec2(0.5)+(CubeMainTexOffset[id].xy*intersectionPoint.xz/(planeSize*2.0)));
			vec4 LightColor = texture2D(CubeIntensityTexture[id],CubeIntensityTexOffset[id].zw+vec2(0.5)+(CubeIntensityTexOffset[id].xy*intersectionPoint.xz/(planeSize*2.0)));

			vec3 norm = normalize(texture2D(CubeNormalTexture[id],CubeNormalTexOffset[id].zw+vec2(0.5)+(CubeNormalTexOffset[id].xy*intersectionPoint.xz/(planeSize*2.0))).xyz * 2.0 -1.0);
			if(DotP>0.0)norm.z*=-1.0;
			vec3 finalNormal = normalize(PlaneRot*(mat3x3_x_90*norm));
			finalNormal = normalize((normal*0.1)+(finalNormal*CubeNormalTexStreight[id]));

			if(dist_near>t || dist_near==-1.0){
				o.intersect = true;
				o.color = CubeColor[id]*mainTex;
				o.intensity = CubeIntensity[id]*LightColor.rgb;
				calc_pos = pos;
				calc_normal = finalNormal;
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
        }
    }



	PlaneCenter = CubeCenter[id]+(PlaneRot*vec3(0.0,-CubeSize[id].y,0.0));
	PlaneSize = CubeSize[id].xz;
	
	planeOrigin = (ray.ro-PlaneCenter)*PlaneRot;
    planeNormal = vec3(0.0,-1.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
    
    t = dot(planeNormal,-planeOrigin) / DotP;

    if (t >= 0.0) {
        vec3 intersectionPoint = -(planeOrigin + dir * t);

        if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.z) <= planeSize.y) {
			intersectionPoint*=-1;

			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?(PlaneRot[1]):-(PlaneRot[1]);
			
			vec4 mainTex = texture2D(CubeMainTexture[id],CubeMainTexOffset[id].zw+vec2(0.5)+(CubeMainTexOffset[id].xy*intersectionPoint.xz/(planeSize*2.0)));
			vec4 LightColor = texture2D(CubeIntensityTexture[id],CubeIntensityTexOffset[id].zw+vec2(0.5)+(CubeIntensityTexOffset[id].xy*intersectionPoint.xz/(planeSize*2.0)));

			vec3 norm = normalize(texture2D(CubeNormalTexture[id],CubeNormalTexOffset[id].zw+vec2(0.5)+(CubeNormalTexOffset[id].xy*intersectionPoint.xz/(planeSize*2.0))).xyz * 2.0 -1.0);
			if(DotP>0.0)norm.z*=-1.0;
			norm.x*=-1.0;
			vec3 finalNormal = normalize(PlaneRot*(mat3x3_x90*norm));
			finalNormal = normalize((normal*0.1)+(finalNormal*CubeNormalTexStreight[id]));

			if(dist_near>t || dist_near==-1.0){
				o.intersect = true;
				o.color = CubeColor[id]*mainTex;
				o.intensity = CubeIntensity[id]*LightColor.rgb;
				calc_pos = pos;
				calc_normal = finalNormal;
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
        }
    }


	
	PlaneCenter = CubeCenter[id]+(PlaneRot*vec3(CubeSize[id].x,0.0,0.0));
	PlaneSize = CubeSize[id].zy;
	
	planeOrigin = (ray.ro-PlaneCenter)*PlaneRot;
    planeNormal = vec3(1.0,0.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
    
    t = dot(planeNormal,-planeOrigin) / DotP;

    if (t >= 0.0) {
        vec3 intersectionPoint = (planeOrigin + dir * t);

        if (abs(intersectionPoint.z) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {

			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?-(PlaneRot[0]):(PlaneRot[0]);
			
			vec4 mainTex = texture2D(CubeMainTexture[id],CubeMainTexOffset[id].zw+vec2(0.5)+(CubeMainTexOffset[id].xy*intersectionPoint.zy/(planeSize*2.0)));
			vec4 LightColor = texture2D(CubeIntensityTexture[id],CubeIntensityTexOffset[id].zw+vec2(0.5)+(CubeIntensityTexOffset[id].xy*intersectionPoint.zy/(planeSize*2.0)));

			vec3 norm = normalize(texture2D(CubeNormalTexture[id],CubeNormalTexOffset[id].zw+vec2(0.5)+(CubeNormalTexOffset[id].xy*intersectionPoint.zy/(planeSize*2.0))).xyz * 2.0 -1.0);
			if(DotP>0.0)norm.z*=-1.0;
			vec3 finalNormal = normalize(PlaneRot*(mat3x3_y90*norm));
			finalNormal = normalize((normal*0.1)+(finalNormal*CubeNormalTexStreight[id]));

			if(dist_near>t || dist_near==-1.0){
				o.intersect = true;
				o.color = CubeColor[id]*mainTex;
				o.intensity = CubeIntensity[id]*LightColor.rgb;
				calc_pos = pos;
				calc_normal = finalNormal;
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
        }
    }


	
	PlaneCenter = CubeCenter[id]+(PlaneRot*vec3(-CubeSize[id].x,0.0,0.0));
	PlaneSize = CubeSize[id].zy;
	
	planeOrigin = (ray.ro-PlaneCenter)*PlaneRot;
    planeNormal = vec3(-1.0,0.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
    
    t = dot(planeNormal,-planeOrigin) / DotP;

    if (t >= 0.0) {
        vec3 intersectionPoint = -(planeOrigin + dir * t);

        if (abs(intersectionPoint.z) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			intersectionPoint.y*=-1.0;

			vec3 pos = ray.ro + ray.rd * t;
			vec3 normal = DotP>0.0?(PlaneRot[0]):-(PlaneRot[0]);
			
			vec4 mainTex = texture2D(CubeMainTexture[id],CubeMainTexOffset[id].zw+vec2(0.5)+(CubeMainTexOffset[id].xy*intersectionPoint.zy/(planeSize*2.0)));
			vec4 LightColor = texture2D(CubeIntensityTexture[id],CubeIntensityTexOffset[id].zw+vec2(0.5)+(CubeIntensityTexOffset[id].xy*intersectionPoint.zy/(planeSize*2.0)));

			vec3 norm = normalize(texture2D(CubeNormalTexture[id],CubeNormalTexOffset[id].zw+vec2(0.5)+(CubeNormalTexOffset[id].xy*intersectionPoint.zy/(planeSize*2.0))).xyz * 2.0 -1.0);
			if(DotP>0.0)norm.z*=-1.0;
			vec3 finalNormal = normalize(PlaneRot*(mat3x3_y_90*norm));
			finalNormal = normalize((normal*0.1)+(finalNormal*CubeNormalTexStreight[id]));

			if(dist_near>t || dist_near==-1.0){
				o.intersect = true;
				o.color = CubeColor[id]*mainTex;
				o.intensity = CubeIntensity[id]*LightColor.rgb;
				calc_pos = pos;
				calc_normal = finalNormal;
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
        }
    }
	if(calc_flip) dist_near = -1.0;

	o.norhit = calc_normal;
	o.poshit = calc_pos;
	o.flip = calc_flip;
	o.T.x = dist_near;
	o.T.y = dist_far;

	return o;
}

OBJ cloud(RAY ray, int id) {

	OBJ o = OBJ(
		false,
		vec3(0.0),
		vec3(0.0),
		vec2(-1.0),
		CloudColor[id],
		CloudLuminescence[id],
		CloudIntensity[id],
		CloudRoughness[id],
		CloudDensity[id],
		id,
		4,
		true,
		false
	);

	bool calc_flip = false;
	float dist_near = -1.0;
	float dist_far = -1.0;

	mat3 Rotation = CloudRot[id];
	vec3 PlaneCenter = CloudCenter[id]+(Rotation*vec3(0.0,0.0,CloudSize[id].z));
	vec2 PlaneSize = CloudSize[id].xy;
	
	vec3 planeOrigin = (ray.ro-PlaneCenter)*Rotation;
	vec3 dir = ray.rd*Rotation;
	vec3 planeNormal = vec3(0.0,0.0,1.0);
	vec2 planeSize = PlaneSize;

	float DotP = dot(planeNormal, dir);
	
	float t = dot(planeNormal,-planeOrigin) / DotP;

	if (t >= 0.0) {
		vec3 intersectionPoint = (planeOrigin + dir * t);

		if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			if(dist_near>t || dist_near==-1.0){
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
		}
	}



	PlaneCenter = CloudCenter[id]+(Rotation*vec3(0.0,0.0,-CloudSize[id].z));
	PlaneSize = CloudSize[id].xy;
	
	planeOrigin = (ray.ro-PlaneCenter)*Rotation;
	planeNormal = vec3(0.0,0.0,-1.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
	
	t = dot(planeNormal,-planeOrigin) / DotP;

	if (t >= 0.0) {
		vec3 intersectionPoint = (planeOrigin + dir * t);

		if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			if(dist_near>t || dist_near==-1.0){
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
		}
	}



	PlaneCenter = CloudCenter[id]+(Rotation*vec3(0.0,CloudSize[id].y,0.0));
	PlaneSize = CloudSize[id].xz;
	
	planeOrigin = (ray.ro-PlaneCenter)*Rotation;
	planeNormal = vec3(0.0,1.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
	
	t = dot(planeNormal,-planeOrigin) / DotP;

	if (t >= 0.0) {
		vec3 intersectionPoint = (planeOrigin + dir * t);

		if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.z) <= planeSize.y) {
			if(dist_near>t || dist_near==-1.0){
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
		}
	}



	PlaneCenter = CloudCenter[id]+(Rotation*vec3(0.0,-CloudSize[id].y,0.0));
	PlaneSize = CloudSize[id].xz;
	
	planeOrigin = (ray.ro-PlaneCenter)*Rotation;
	planeNormal = vec3(0.0,-1.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
	
	t = dot(planeNormal,-planeOrigin) / DotP;

	if (t >= 0.0) {
		vec3 intersectionPoint = (planeOrigin + dir * t);

		if (abs(intersectionPoint.x) <= planeSize.x && abs(intersectionPoint.z) <= planeSize.y) {
			if(dist_near>t || dist_near==-1.0){
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
		}
	}



	PlaneCenter = CloudCenter[id]+(Rotation*vec3(CloudSize[id].x,0.0,0.0));
	PlaneSize = CloudSize[id].zy;
	
	planeOrigin = (ray.ro-PlaneCenter)*Rotation;
	planeNormal = vec3(1.0,0.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
	
	t = dot(planeNormal,-planeOrigin) / DotP;

	if (t >= 0.0) {
		vec3 intersectionPoint = (planeOrigin + dir * t);

		if (abs(intersectionPoint.z) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			if(dist_near>t || dist_near==-1.0){
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
		}
	}



	PlaneCenter = CloudCenter[id]+(Rotation*vec3(-CloudSize[id].x,0.0,0.0));
	PlaneSize = CloudSize[id].zy;
	
	planeOrigin = (ray.ro-PlaneCenter)*Rotation;
	planeNormal = vec3(-1.0,0.0,0.0);
	planeSize = PlaneSize;

	DotP = dot(planeNormal, dir);
	
	t = dot(planeNormal,-planeOrigin) / DotP;

	if (t >= 0.0) {
		vec3 intersectionPoint = (planeOrigin + dir * t);

		if (abs(intersectionPoint.z) <= planeSize.x && abs(intersectionPoint.y) <= planeSize.y) {
			if(dist_near>t || dist_near==-1.0){
				calc_flip = DotP>0.0;
				dist_near = t;
			}
			if(dist_far<t || dist_far==-1.0){
				dist_far = t;
			}
		}
	}



	if(calc_flip) dist_near = 0.0;
	

	if(dist_far!=-1.0){
		float distCalc = -1.0;
		float fixed_dist = (dist_far)-(dist_near);
		vec3 p = ray.ro + ray.rd * dist_near;
		
		for(int i = 0; i < int(CloudHollow[id]); i++) {
			vec3 ce = p+ray.rd*(fixed_dist*rand(uv+RandomValue(state),FrameId));
			float r = CloudParticleSize[id]*noise(ce*CloudOffsetScale[id]+CloudOffsetPos[id]);
			r *= rand(uv+RandomValue(state),FrameId);
			if(r>=0.01){
				vec3 oc = ray.ro - ce;

				float b = 2.0 * dot(oc, ray.rd);
				float c = length(ray.ro - ce);

				float discriminant = b * b - 4.0 * (c * c - r * r);
				if(discriminant > 0.0) {
					float s = sqrt(discriminant);
					float tNear = max(0, (-b - s) * 0.5);
					float tFar = max(0, (-b + s) * 0.5);
					if(tFar > 0.0) {

						vec3 pos;
						if(tNear > 0) {
							pos = ray.ro + ray.rd * tNear;
						} else {
							pos = ray.ro + ray.rd * tFar;
						}
						if(distCalc==-1.0 || (tNear>0?tNear<distCalc:tFar<distCalc)){
							
							mat3 invrotMat = invertMatrix3x3(Rotation);
							//pint in the box
							vec3 point = invrotMat*(pos-CloudCenter[id]);
							if(
								rand(uv+RandomValue(state),FrameId) < (CloudSize[id].x-abs(point.x)) && 
								rand(uv+RandomValue(state),FrameId) < (CloudSize[id].y-abs(point.y)) && 
								rand(uv+RandomValue(state),FrameId) < (CloudSize[id].z-abs(point.z))
							){

								distCalc=tNear>0?tNear:tFar;
								o.intersect = true;
								o.poshit = pos;
								o.T = vec2(tNear,tFar);
								o.flip = !(tNear > 0);

								vec3 normal = normalize((pos-CloudCenter[id])/CloudSize[id]);
								float minValueNoise = -1.0;
								for(int i = 0; i < 4; i++) {
									vec3 randVec = random_unit_vector(pos);
									vec3 center = pos-randVec*r;
									float radius = CloudParticleSize[id]*noise(center*CloudOffsetScale[id]+CloudOffsetPos[id]);
									point = invrotMat*(center-CloudCenter[id]);
									bool nul = !(
										rand(uv+RandomValue(state),FrameId) < (CloudSize[id].x-abs(point.x)) && 
										rand(uv+RandomValue(state),FrameId) < (CloudSize[id].y-abs(point.y)) && 
										rand(uv+RandomValue(state),FrameId) < (CloudSize[id].z-abs(point.z))
									);
									if(!nul && (minValueNoise<=-1.0 || minValueNoise>radius)){
										minValueNoise=radius;
										normal=-randVec;
									}
									if(radius<=0.0)break;
								}
								o.norhit = normal;
							}
						}
					}
				}
			}
		}
	}

	return o;
}

OBJ atmosphere(RAY ray, int id) {

	OBJ o = OBJ(
		false,
		vec3(0.0),
		vec3(0.0),
		vec2(-1.0),
		AtmosphereColor[id],
		AtmosphereLuminescence[id],
		AtmosphereIntensity[id],
		AtmosphereRoughness[id],
		AtmosphereDensity[id],
		id,
		5,
		true,
		false
	);

    vec4 sphere = Atmosphere[id];
    vec3 ce = sphere.xyz;

    vec3 oc = ray.ro - ce;

    float b = 2.0 * dot(oc, ray.rd);
	float c = length(ray.ro-ce);


	float distCalc = -1.0;
	for(int i = 0; i < int(AtmosphereHollow[id]); i++) {
    	float r = AtmosphereDistCenter[id]+(sphere.w*pow(rand(uv+RandomValue(state),FrameId),AtmosphereConcentration[id]));
		float discriminant = b*b - 4.0*(c*c-r*r);
		if (discriminant > 0.0) {
			float s = sqrt(discriminant);
			float tNear = max(0,(-b - s) * 0.5);
			float tFar = max(0,(-b + s) * 0.5);
			if (tFar > 0.0) {

				vec3 pos;
				vec3 normal;
				if(tNear>0){
					pos = ray.ro + ray.rd * tNear;
					normal = normalize(pos - ce);
				}
				else{
					pos = ray.ro + ray.rd * tFar;
					normal = -normalize(pos - ce);
				}
				if(distCalc==-1.0 || (tNear>0?tNear<distCalc:tFar<distCalc)){
					distCalc=tNear>0?tNear:tFar;
					o.intersect = true;
					o.norhit = normal;
					o.poshit = pos;
					o.T = vec2(tNear,tFar);
					o.flip = !(tNear > 0);
				}
			}
		}
		
	}
    return o;
}

OBJ CloserObj(RAY ray){
    OBJ o = OBJ(
		false,
		vec3(0.0),
		vec3(0.0),
		vec2(-1.0),
		vec4(0.0),
		vec4(0.0),
		vec3(0.0),
        vec3(0.0),
		0.0,
		-1,
		-1,
		false,
		false
	);
    float dist=-1.0;
    for(int i = 0; i < CountPortal; i++) {
        OBJ newO=portal(ray,i);
        if(newO.intersect && ((newO.T.x>0?newO.T.x<dist:newO.T.y<dist) || dist==-1.0)){
            dist=newO.T.x>0?newO.T.x:newO.T.y;
            o=newO;
        }
    }
    for(int i = 0; i < CountSphere; i++) {
        OBJ newO=sphere(ray,i);
        if(newO.intersect && ((newO.T.x>0?newO.T.x<dist:newO.T.y<dist) || dist==-1.0)){
			dist=newO.T.x>0?newO.T.x:newO.T.y;
			o=newO;
        }
    }
   	for(int i = 0; i < CountPlane; i++) {
        OBJ newO=plane(ray,i);
        if(newO.intersect && ((newO.T.x>0?newO.T.x<dist:newO.T.y<dist) || dist==-1.0)){
			dist=newO.T.x>0?newO.T.x:newO.T.y;
			o=newO;
        }
    }
	for(int i = 0; i < CountCube; i++) {
        OBJ newO=cube(ray,i);
        if(newO.intersect && ((newO.T.x>0?newO.T.x<dist:newO.T.y<dist) || dist==-1.0)){
            dist=newO.T.x>0?newO.T.x:newO.T.y;
            o=newO;
        }
    }
    /*for(int i = 0; i < CountCloud; i++) {
        OBJ newO=cloud(ray,i);
        if(newO.intersect && ((newO.T.x>0?newO.T.x<dist:newO.T.y<dist) || dist==-1.0)){
			dist=newO.T.x>0?newO.T.x:newO.T.y;
			o=newO;
        }
    }*/
    /*for(int i = 0; i < CountAtmosphere; i++) {
        OBJ newO=atmosphere(ray,i);
        if(newO.intersect && ((newO.T.x>0?newO.T.x<dist:newO.T.y<dist) || dist==-1.0)){
			dist=newO.T.x>0?newO.T.x:newO.T.y;
			o=newO;
        }
    }*/
    return o;
}






/////////////param////////////
const float fow = 1.3333;
const float camerSize = 0.0;
uniform float farPlane;
uniform float aperture;
const bool dispersion = true;

const int NumRaysPerPixel = 2;
const int SphereMap = 1000;
const float offsetSphereMap = pow(SphereMap,-1);

const int bounsing = 6;
const float brightness = pow(float(NumRaysPerPixel),-1);
//////////////////////////////

uniform sampler2D BufferTexture;
uniform bool Render;

const float wavelengths = 1.0;
const vec4 Dispersion[16] = vec4[16](
    vec4(1.0, 0.0, 0.0, pow(7.4*wavelengths,-1.0)),    // Красный
    vec4(1.0, 0.0, 0.0, pow(7.4*wavelengths,-1.0)),    // Красный
    vec4(1.0, 0.5, 0.0, pow(6.8*wavelengths,-1.0)),    // Оранжевый
    vec4(1.0, 0.5, 0.0, pow(6.8*wavelengths,-1.0)),    // Оранжевый
    vec4(1.0, 1.0, 0.0, pow(6.2*wavelengths,-1.0)),    // Желтый
    vec4(1.0, 1.0, 0.0, pow(6.2*wavelengths,-1.0)),    // Желтый
    vec4(0.0, 1.0, 0.0, pow(6.0*wavelengths,-1.0)),    // Зеленый
    vec4(0.0, 1.0, 0.0, pow(6.0*wavelengths,-1.0)),    // Зеленый
    vec4(0.0, 1.0, 1.0, pow(5.3*wavelengths,-1.0)),    // Голубой
    vec4(0.0, 1.0, 1.0, pow(5.3*wavelengths,-1.0)),    // Голубой
    vec4(0.0, 0.0, 1.0, pow(5.1*wavelengths,-1.0)),    // Синий
    vec4(0.0, 0.0, 1.0, pow(5.1*wavelengths,-1.0)),    // Синий
    vec4(0.5, 0.0, 1.0, pow(4.8*wavelengths,-1.0)),    // Фиолетовый
    vec4(0.5, 0.0, 1.0, pow(4.8*wavelengths,-1.0)),    // Фиолетовый
    vec4(0.0, 0.0, 0.0, pow(4.05*wavelengths,-1.0)),    // None
    vec4(0.0, 0.0, 0.0, pow(7.4*wavelengths,-1.0))     // None
);
const int countColorDisp = Dispersion.length();


void DefaultCalculation(inout vec3 p, inout vec3 d, int id, OBJ hit, inout float eDensity, float uDensity){

	//Random Direction
	//vec3 randVec = random_unit_vector(d);
	float r = float(id)/float(NumRaysPerPixel);
	vec3 randVec = generate_sphere_points((int(float(SphereMap)*(r+(FrameId*0.01))))%SphereMap,offsetSphereMap);
	vec3 dirAxis = cross(hit.norhit,vec3(0,0,1));
	if(length(dirAxis)<=0.5) dirAxis = hit.norhit;
	else dirAxis = normalize(dirAxis);
	float dotProduct = dot(hit.norhit, vec3(0,0,1));
	float angleRadians = acos(dotProduct);

	randVec = normalize(rotationAxisAngleMatrix3x3(dirAxis,angleRadians*180.0)*randVec);
	randVec = normalize(rotationAxisAngleMatrix3x3(hit.norhit,rand(uv+RandomValue(state),FrameId)*360.0)*randVec);

	randVec = normalize(rotationAxisAngleMatrix3x3(random_unit_vector(d),rand(uv+RandomValue(state),FrameId)*360.0)*randVec);
	//=======================================================



	//calculating the probability of reflection or refraction
	float n2 = hit.density;
	if(hit.T.x<=0.0 && !hit.hollow)eDensity=n2;
	float n1 = eDensity;
	float a = (-dot(d, hit.norhit));

	float i1 = acos(a);
	float i2 = asin((n1 - n2) / (n1 + n2)) * i1;

	float Fresnel = pow(
		(n1 * cos(i1) - n2 * cos(i2)) 
		/ 
		(n1 * cos(i1) + n2 * cos(i2)), 
	2);

	bool Snellius = ( rand(uv+RandomValue(state),FrameId) < hit.color.a+Fresnel );
	//=======================================================



	vec3 spec = vec3(0);
	if(Snellius){
		spec=reflect(d,hit.norhit);
		p=hit.poshit+hit.norhit*0.001;
		if(dot(hit.norhit,randVec)<0.0)randVec*=-1.0;
	}
	else{
		spec=refract(d,hit.norhit,1.0-pow((n1-n2)/(n1+n2),2.0));
		p=hit.poshit-hit.norhit*0.001;
		if(hit.T.x<=0.0)eDensity=uDensity;
		if(dot(hit.norhit,randVec)>0.0)randVec*=-1.0;
	}
	if(hit.ObjectCode==5){
		float lenWave = 1.0-((uDensity)/(1.0+Dispersion[0].w));
		d=normalize(
			mix(
				spec,
				randVec,
				min(max(interpolate3(
					hit.roughness.x,
					hit.roughness.y,
					hit.roughness.z,
					lenWave*lenWave
				),0.0),1.0)
			)
		);
	}
	else{
		hit.roughness.x = max(min(0.999,hit.roughness.x),0.001);
		hit.roughness.y = max(min(0.999,hit.roughness.y),0.001);
		d=normalize(
			mix(
				spec,
				randVec,
				(
					Snellius?
					(rand(uv+RandomValue(state),FrameId)<hit.roughness.z)
					:
					false
				)?
					min(hit.roughness.y*(dispersion?pow((1.0-Dispersion[0].w)+(uDensity-1.0),n2):1.0),1.0)
					:
					min(hit.roughness.x*(dispersion?pow((1.0-Dispersion[0].w)+(uDensity-1.0),n2):1.0),1.0)
			)
		);
	}
}
void PortalCalculation(inout vec3 p, inout vec3 d, OBJ hit){
	vec3 thisPos = PortalPosition[hit.id];
	vec3 thisSca = PortalSize[hit.id];
	mat3 thisRot = PortalMatrix[hit.id];

	vec3 otherPos = PortalPosition[hit.id%2==0?hit.id+1:hit.id-1];
	vec3 otherSca = PortalSize[hit.id%2==0?hit.id+1:hit.id-1];
	mat3 otherRot = PortalMatrix[hit.id%2==0?hit.id+1:hit.id-1]*mat3x3_y180;

	mat3 thisinvrot = invertMatrix3x3(thisRot);
	float scale = otherSca.z/thisSca.z;
	vec3 posRayThisPortal = (thisinvrot*(thisPos-hit.poshit))*scale;
	vec3 dirRayThisPortal = thisinvrot*d;

	vec3 dir = otherRot*dirRayThisPortal;

	p = otherPos-(otherRot*(posRayThisPortal/vec3(otherSca.xy/thisSca.xy,1.0)))+dir*0.001;
	//d = dir;
	
	float rad = length(
		(thisPos-hit.poshit)*(thisRot*vec3(thisSca.xy,1.0))
	)/thisSca.z;

	d = refract(dir,otherRot[2],1.0-pow(rad,20.0));
}
vec3 renderUFA(RAY ray, int id, OBJ hit, vec3 rayColor, float environmentalDensity){
	vec3 color=vec3(0);
	vec3 p = ray.ro;
	vec3 d = ray.rd;

	float unionEnvironmentalDensity = environmentalDensity;

	
	for(int i = 0; i <= bounsing; i++) {
		if(rayColor.r<=0.0 && rayColor.g<=0.0 && rayColor.b<=0.0) return color;
		if(hit.intersect){
			if(hit.ObjectCode == 0){
				if(
					length(
						(PortalPosition[hit.id].xyz-hit.poshit)*(PortalMatrix[hit.id]*vec3(PortalSize[hit.id].xy,1.0))
					)>PortalSize[hit.id].z*(1.0-pow(rand(uv+RandomValue(state),FrameId),10.0)*0.1)
				){
					color += hit.color.rgb*rayColor;
					if(hit.ObjectCode!=5)rayColor*=hit.color.rgb;
				}
			}
			else{
				color += hit.color.rgb*hit.intensity*rayColor;
				rayColor *= clamp(hit.color.rgb,vec3(0.0),vec3(1.0));
			}
		}
		else {
			return color;
		}

		if(hit.ObjectCode == 0)PortalCalculation(p,d,hit);
		else DefaultCalculation(p,d,id,hit,environmentalDensity,unionEnvironmentalDensity);
		hit = CloserObj(RAY(p,d));
	}

	return color;
}
vec3 render(RAY ray, int id, OBJ hit, vec3 rayColor, float environmentalDensity){
	//return hit.norhit*0.5;
	//return hit.color.rgb*0.5*brightness;
	vec3 color=vec3(0);
	vec3 p = ray.ro;
	vec3 d = ray.rd;

	float unionEnvironmentalDensity = environmentalDensity;

	
	for(int i = 0; i <= bounsing; i++) {
		if(rayColor.r<=0.0 && rayColor.g<=0.0 && rayColor.b<=0.0) return color;
		if(hit.intersect){
			if(hit.ObjectCode == 0){
				if(
					length(
						(PortalPosition[hit.id].xyz-hit.poshit)*(PortalMatrix[hit.id]*vec3(PortalSize[hit.id].xy,1.0))
					)>PortalSize[hit.id].z*(1.0-pow(rand(uv+RandomValue(state),FrameId),10.0)*0.1)
				){
					color += hit.color.rgb*rayColor;
					rayColor*=hit.color.rgb;
				}
			}
			else{
				color += hit.color.rgb*hit.intensity*rayColor;
				vec3 luminescence = vec3(0.0);
				if(length(hit.luminescence.rgb*hit.luminescence.w)>0.01){
					float e = environmentalDensity;
					float ufa = (length(vec3(0.0,0.0,1.0)-renderUFA(RAY(p,d),id,hit,rayColor,e)));
					luminescence = (hit.luminescence.rgb*hit.luminescence.w) * (1.0-pow(clamp(ufa,0.0,1.0),0.5));
				}
				color += luminescence;
				rayColor *= clamp(hit.color.rgb + luminescence,vec3(0.0),vec3(1.0));
			}
		}
		else {
			return color;
		}
		if(
			FrameId<=1.0 && 
			(hit.ObjectCode!=0?
				true
				:
				length(
					(PortalPosition[hit.id].xyz-hit.poshit)*(PortalMatrix[hit.id]*vec3(PortalSize[hit.id].xy,1.0))
				)>PortalSize[hit.id].z*0.9)
		){
			vec3 randVec = random_unit_vector(d);

			float n2 = hit.density;
			float n1 = unionEnvironmentalDensity;
			float a = (-dot(d, hit.norhit));

			float i1 = acos(a);
			float i2 = asin((n1 - n2) / (n1 + n2)) * i1;

			float Fresnel = pow(
				(n1 * cos(i1) - n2 * cos(i2)) 
				/ 
				(n1 * cos(i1) + n2 * cos(i2)), 
			2);

			bool Snellius = ( rand(uv+RandomValue(state),FrameId) < hit.color.a+Fresnel );

			vec3 spec = vec3(0);
			if(Snellius){
				spec=reflect(d,hit.norhit);
				p=hit.poshit+hit.norhit*0.001;
				if(dot(hit.norhit,randVec)<0.0)randVec*=-1.0;
			}
			else{
				spec=refract(d,hit.norhit,1.0-pow((n1-n2)/(n1+n2),2.0));
				p=hit.poshit-hit.norhit*0.001;
				if(dot(hit.norhit,randVec)>0.0)randVec*=-1.0;
			}


			vec3 dir = normalize(
				mix(
					spec,
					randVec,
					(
						Snellius?
						(rand(uv+RandomValue(state),FrameId)<hit.roughness.z)
						:
						false
					)?
						min(hit.roughness.y*(dispersion?pow((1.0-Dispersion[0].w)+(unionEnvironmentalDensity-1.0),n2):1.0),1.0)
						:
						min(hit.roughness.x*(dispersion?pow((1.0-Dispersion[0].w)+(unionEnvironmentalDensity-1.0),n2):1.0),1.0)
				)
			);
			if( Snellius && (dot(dir,spec)<0.99) || hit.ObjectCode==0 || hit.ObjectCode==4 ){
				if(!Snellius){
					OBJ h = CloserObj(RAY(p,d));
					if(h.intersect && length(h.intensity)>0.0){
						return h.color.rgb*0.5;
					}
					else return hit.color.rgb*0.5;
				}
				else return hit.color.rgb*0.5;
			}
		}

		if(hit.ObjectCode == 0)PortalCalculation(p,d,hit);
		else DefaultCalculation(p,d,id,hit,environmentalDensity,unionEnvironmentalDensity);
		hit = CloserObj(RAY(p,d));
	}

	return color;
}


vec3 DispersionRay(RAY ray, int id, OBJ hit){
	if(FrameId<=1.0){
		return render(
			ray,
			id,
			hit,
			vec3(1.0),
			1.0);
	}
	int idraycolor = int(FrameId*0.5)+id;
	float weightraycolor = ((FrameId*0.5)+float(id))-float(idraycolor);
	idraycolor %= countColorDisp;
	vec4 raycolor = mix(Dispersion[idraycolor],Dispersion[min(idraycolor+1,countColorDisp-1)],weightraycolor);
	return render(
		ray,
		id,
		hit,
		raycolor.xyz,
		1.0+raycolor.w);
}



uniform float Chunk;
uniform float CountOfChunkRender;

void main(){
    uv = (2*gl_FragCoord.xy - ScreenSize) * pow(ScreenSize.y, -1);
    vec2 pixCoord = uv * ScreenSize;
	vec3 texColor = texture2D(BufferTexture, (texCoord*ScreenSize)+vec2(0.5)).xyz;

	float size = pow(CountOfChunkRender,-1.0);
	float chunkFullSize = ((ScreenSize.x*(ScreenSize.x/ScreenSize.y))-1.0)*2.0;
	float curentPixel = (pixCoord.x+chunkFullSize*0.5);
	if(
		!(
			( (curentPixel) > ((chunkFullSize*size*Chunk) ) ) &&
			( (curentPixel) < ((chunkFullSize*(size*Chunk+size)) ) )
		) &&
		Chunk>=0.0
	){
		gl_FragColor = vec4(texColor, 1.0 );
		return;
	}


	int pixelIndex = int(pixCoord.y * ScreenSize.x + pixCoord.x);
	state = pixelIndex + int(FrameId*75215454);



	if(Render){

		vec3 color=vec3(0);
		RAY ray;
		OBJ hit;

		for(int i = 1; i <= (FrameId<=1.0?1:NumRaysPerPixel); i++) {
			vec2 rUV = vec2(
				(0.5-rand(uv+RandomValue(state),FrameId))*2.0,
				(0.5-rand(uv+RandomValue(state),FrameId))*2.0
			);
			rUV = normalize(rUV)*rand(uv+RandomValue(state),FrameId);
			//rUV = clamp(rUV, -normalize(rUV), normalize(rUV));
			//rUV = normalize(rUV);

			vec3 posOfPixel = PosCam + (MatCam * vec3((uv*camerSize)+(rUV*(aperture)),0));
			vec3 posOfMat = PosCam + (MatCam * vec3((uv*camerSize)+(uv*farPlane)+(rUV*0.005),farPlane*fow));

			ray = RAY(
				posOfPixel,
				normalize(posOfMat-posOfPixel)
			);

			hit = CloserObj(ray);
			if(hit.intersect){
				if(dispersion) color += DispersionRay(ray, i,hit)*brightness;
				else color += render(ray,i,hit,vec3(1,1,1),1.0)*brightness;
			}
		}

		color = clamp(color,vec3(0),vec3(1))*NumRaysPerPixel*2.0;
		//color = clamp(color,vec3(0),vec3(1));

		float streight = 1.0/FrameId;

		vec3 FinColor = mix(texColor,color,streight);
		FinColor = clamp(FinColor,vec3(0),vec3(1));

		gl_FragColor = vec4(FinColor, 1.0 );
	}
	else{
		gl_FragColor = vec4(texColor, 1.0 );
		/*if(FrameId>=1000){
			vec4 denoise = smartDeNoise(BufferTexture,((texCoord*ScreenSize)+vec2(0.5)),1,1,1);
			gl_FragColor = vec4(denoise.rgb, 1.0 );
		}
		else{
			gl_FragColor = vec4(texColor, 1.0 );
		}*/
		/*if(FrameId>=1000){
			vec3 smothColor = vec3(0);
			for(int x = -1; x <= 1; x++) {
				for(int y = -1; y <= 1; y++) {
					smothColor += texture2D(BufferTexture, (texCoord*ScreenSize)+vec2(0.5)+(vec2(x,y)/ScreenSize)).xyz;
				}
			}
			smothColor/=9;
			gl_FragColor = vec4(mix(smothColor,texColor,0.1),1.0);
		}
		else{
			gl_FragColor = vec4(texColor, 1.0 );
		}*/
	}
}
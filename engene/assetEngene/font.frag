#version 130

in vec2 texCoord;
in vec3 Normal;

uniform sampler2D Texture;
uniform vec2 texScale;
uniform vec2 CharScale;
uniform vec2 CharPos;
uniform vec4 Color;

void main(){
	vec2 chraScale = 1.0/CharScale;
	vec2 p = CharPos * chraScale;
	vec2 border = (1.0/texScale) + vec2(1,1);

	vec2 scaleebel = texCoord*chraScale*0.9  +  vec2(		p.x	,	(1-chraScale.y) - p.y		) + border;
	
	gl_FragColor = texture2D(Texture,scaleebel)*Color;
}
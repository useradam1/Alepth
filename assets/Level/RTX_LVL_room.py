from engene.openGL_atrib import *

class Level:
	def __init__(self, MainForm : Form) -> None:
		self.mainForm : Form = MainForm
	
	def LoadLevel(self) -> None:
	#_____________________________________________________________Camera
		self.CameraMove : bool = False
		self.swith : bool = False

		self.Player = GameObject(
			transform = Transform(
				pos = vec3f( -7 , -7 , 9.5 ),
				sca = vec3f( 1 , 1 , 1 ),
				rot = Rotation().Ly(180-40)
			)
		)
		self.MainCamera = GameObject(
			transform = Transform(
				pos = vec3f( 0 , 0 , 0 ),
				sca = vec3f( 1 , 1 , 1 ),
				rot = Rotation().Lx(10)
			),
			parent = self.Player
		)
		self.camera = Camera(
			form = self.mainForm,
			gameObject = self.MainCamera,
			near = 0.75,
			far = 20_000,
			fov = 75.0,
			renderLayer = [
				'default',
			]
		)
		##############################################################



		#_____________________________________________________________Shader
		self.RTX_Shader = Shader(
			form = self.mainForm,
			PathToShaders = (
				"assets/shaders/RTX_Room.frag",
				"assets/shaders/RTX.vert"
			))
		##############################################################



		#_____________________________________________________________Texture
		self.BufferTexture = Texture(self.mainForm,self.mainForm.size,vec4f())
		#=============================================================
		self.WhiteTex = Texture(self.mainForm,vec2i(1,1),vec4f(1,1,1,1))
		#=============================================================
		self.NormalTex = Texture(self.mainForm,vec2i(1,1),vec4f(0.5,0.5,1,1))
		#=============================================================
		self.arrowTex = Texture(
			form = self.mainForm,
			path = "assets/image/arrow.bmp"
		)
		#=============================================================
		self.PortalFlorTex = Texture(
			form = self.mainForm,
			path = "assets/image/portalPanel.jpg"
		)
		#=============================================================
		self.PortalFlorNormalTex = Texture(
			form = self.mainForm,
			path = "assets/image/portalPanelNormal.png"
		)
		#=============================================================
		self.concreteFlorTex = Texture(
			form = self.mainForm,
			path = "assets/image/construct_concrete_floor.png"
		)
		#=============================================================
		self.concreteFlorNormalTex = Texture(
			form = self.mainForm,
			path = "assets/image/floorNormalMap.png"
		)
		#=============================================================
		self.BrickWallTex = Texture(
			form = self.mainForm,
			path = "assets/image/brickwall003a.png"
		)
		#=============================================================
		self.BrickWallNormalTex = Texture(
			form = self.mainForm,
			path = "assets/image/brickwallNormalMap.png"
		)
		#=============================================================
		self.roof_templateTex = Texture(
			form = self.mainForm,
			path = "assets/image/roof_template001a.png"
		)
		#=============================================================
		self.roof_templateNormalTex = Texture(
			form = self.mainForm,
			path = "assets/image/roofNormal.png"
		)
		#=============================================================
		self.RGBTex = Texture(
			form = self.mainForm,
			path = "assets/image/rgb.jpg"
		)
		#=============================================================
		self.chamber13 = Texture(
			form = self.mainForm,
			path = "assets/image/chamber13.jpg"
		)
		#=============================================================
		self.CubeTex = Texture(
			form = self.mainForm,
			path = "assets/image/portalCubeTex.bmp"
		)
		#=============================================================
		self.CubeTexLight = Texture(
			form = self.mainForm,
			path = "assets/image/portalCubeTexLight.bmp"
		)
		#=============================================================
		self.NormalMapTex = Texture(
			form = self.mainForm,
			path = "assets/image/NormalMap.png"
		)
		##############################################################



		#_____________________________________________________________Material
		self.DefaultMaterial = Material(
			shader = self.RTX_Shader,
			attributes = {
			},
			uniforms = {
				"screenSize" : self.mainForm.size,
				"BufferTexture" : self.BufferTexture,
			}
		)
		##############################################################



#_____________________________________________________________SkyBox
		self.SkyBox = SkyBox(
			camera = self.camera,
			material = self.DefaultMaterial,
			renderLayer = 'default',
			renderSide = 'Front'
		)
##############################################################

#_____________________________________________________________Game_Objects
		self.Portals : Dict[str,Dict[Literal['G_O','Color'],Union[GameObject,vec4f]]] = {
			'p1':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( -5 , -7 , -9.99 ),
						sca = vec3f( 1.8 , 1 , 3 ),
						rot = Rotation().Ly(0)
					)),
				'Color' : vec4f( vec3f( 0.1 , 0.5 , 1 ) , 1 ),
				#'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
			},
			'p2':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 9.99 , -7 , 5 ),
						sca = vec3f( 1.8 , 1 , 3 ),
						rot = Rotation().Ly(-90)
					)),
				'Color' : vec4f( vec3f( 1 , 0.5 , 0.1 ) , 1 ),
				#'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
			},
		}
#=============================================================
		self.Planes : Dict[str,Dict[Literal['G_O','Color','MainTex','TexOffset','Luminescence','Intensity','Roughness','Density'],Union[GameObject,vec4f,Texture,vec3f,float]]] = {
			'wallbackward':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , 0 , -10 ),
						sca = vec3f( 10 , 10 ),
						rot = Rotation()
					)),
				'Color' : vec4f( vec3f( 0.75 , 1 , 0.75 ) , 1 ),
				
				'MainTex' : self.PortalFlorTex,
				'MainTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.PortalFlorNormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0.05 ) ,
				'Density' : 1 
			},
			'wallforward':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , 0 , 10 ),
						sca = vec3f( 10 , 10 ),
						rot = Rotation()
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 )*0.75 , 1 ),
				
				'MainTex' : self.PortalFlorTex,
				'MainTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.PortalFlorNormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0.05 ) ,
				'Density' : 1 
			},
			'wallL':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 10 , 0 , 0 ),
						sca = vec3f( 10 , 10 ),
						rot = Rotation().Ly(90)
					)),
				'Color' : vec4f( vec3f( 0.75 , 0.75 , 1 ) , 1 ),
				
				'MainTex' : self.PortalFlorTex,
				'MainTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.PortalFlorNormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0.05 ) ,
				'Density' : 1
			},
			'wallR':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( -10 , 0 , 0 ),
						sca = vec3f( 10 , 10 ),
						rot = Rotation().Ly(90)
					)),
				'Color' : vec4f( vec3f( 1 , 0.75 , 0.75 ) , 1 ),
				
				'MainTex' : self.PortalFlorTex,
				'MainTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.PortalFlorNormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0.05 ) ,
				'Density' : 1
			},
			'flor':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , -10 , 0 ),
						sca = vec3f( 10 , 10 ),
						rot = Rotation().Lx(90)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				
				'MainTex' : self.PortalFlorTex,
				'MainTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.PortalFlorNormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0.05 ) ,
				'Density' : 1 
			},
			'chell':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , 10 , 0 ),
						sca = vec3f( 10 , 10 ),
						rot = Rotation().Lx(90)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),

				'MainTex' : self.PortalFlorTex,
				'MainTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.PortalFlorNormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),

				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0.05 ) ,
				'Density' : 1 
			},
			'plane':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , 0 , -5 ),
						sca = vec3f( 10 , 5 ),
						rot = Rotation().Lx(90)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),

				'MainTex' : self.PortalFlorTex,
				'MainTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.PortalFlorNormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 10 , 10 ) , vec2f( 0 , 0 ) ),

				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0.05 ) ,
				'Density' : 1 
			},
			'glassWall':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 5 , -5 , 0 ),
						sca = vec3f( 5 , 5 ),
						rot = Rotation().Lz(180)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 0 ),
				
				'MainTex' : self.WhiteTex,
				'MainTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.roof_templateNormalTex,
				'NormalTexStreight' : 0.9,
				'NormalTexOffset' : vec4f( vec2f( 2 , 2 ) , vec2f( 0 , 0 ) ),
				
				'Intensity' : vec3f( 0.5 , 0.75 , 1 )*0.0 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 0 , 0 , 0 ) ,
				'Density' : 2 
			},
			'light1':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , 9.99 , 5 ),
						sca = vec3f( 1 , 1 )*3,
						rot = Rotation().Lx(90)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),

				'MainTex' : self.WhiteTex,
				'MainTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.NormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Intensity' : vec3f( 1 , 1 , 1 )*1 ,
				'IntensityTex' : self.WhiteTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0 ) ,
				'Density' : 1 
			},
			'light':{
				'G_O' : GameObject(
					transform = Transform(
						#pos = vec3f( 9.9 , 1.5 , 5 ),
						pos = vec3f( 9.9 , -4.5 , -5 ),
						sca = vec3f( 1 , 1.5 )*3,
						rot = Rotation().Ly(90)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),

				'MainTex' : self.chamber13,
				'MainTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.NormalTex,
				'NormalTexStreight' : 0.5,
				'NormalTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Intensity' : vec3f( 1 , 1 , 1 )*0.25 ,
				'IntensityTex' : self.chamber13,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Roughness' : vec3f( 1 , 0 , 0 ) ,
				'Density' : 1 
			},
		}
#=============================================================
		self.Cubes : Dict[str,Dict[Literal['G_O','Color','Luminescence','Intensity','Roughness','Density','Hollow'],Union[GameObject,vec4f,vec3f,float,bool]]] = {
			'cube':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0.1 , -7.99 , 5 ),
						sca = vec3f( 1 , 1 , 1 )*2,
						rot = Rotation().Lx(0).Ly(15)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 0 ),

				'MainTex' : self.arrowTex,
				'MainTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),
				
				'NormalTex' : self.NormalMapTex,
				'NormalTexStreight' : 0.9,
				'NormalTexOffset' : vec4f( vec2f( 1 , 1 )*0.5 , vec2f( 0 , 0 ) ),

				'Intensity' : vec3f( 0.5 , 0.75 , 1 )*0.0 ,
				'IntensityTex' : self.RGBTex,
				'IntensityTexOffset' : vec4f( vec2f( 1 , 1 ) , vec2f( 0 , 0 ) ),

				'Luminescence' : vec4f( vec3f( 0 , 1 , 0 ) , 0 ),
				'Roughness' : vec3f( 0 , 0 , 0 ) ,
				'Density' : 1.5 ,
				'Hollow' : True
			},
		}
#=============================================================
		self.Clouds : Dict[str,Dict[Literal['G_O','Color','Luminescence','Intensity','Roughness','Density','Hollow'],Union[GameObject,vec4f,vec3f,float,int]]] = {
			'cloud':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 5 , 0 , 5 ),
						sca = vec3f( 5 , 1.5 , 5 ),
						rot = Rotation().Lx(0).Ly(0)
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 0 ),
				'Luminescence' : vec4f( vec3f( 0 , 1 , 0 ) , 0 ),
				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'Roughness' : vec3f( 1 , 0 , 0 ) ,
				'Density' : 1 ,
				'Hollow' : 10 ,
				'Particle_Size' : 0.03 ,
				'OffsetPos' : vec3f( 0 , 0 , 0 ) ,
				'OffsetScale' : vec3f( 1 , 1 , 1 )*0.5 ,
			},
		}
#=============================================================
		self.Atmospheres : Dict[str,Dict[Literal['G_O','Color','Luminescence','Intensity','Roughness','Density','Hollow'],Union[GameObject,vec4f,vec3f,float,int]]] = {
			'atmosphere':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , -100_010 , 0 ) - vec3f(0,10,0),
						sca = vec3f( 100_000*0.5 ),
						rot = Rotation()
					)),
				'Color' : vec4f( vec3f( 0.75 , 0.9 , 1 ) , 0.0 ),
				'Luminescence' : vec4f( vec3f( 0.75 , 0.9 , 1 ) , 0 ),
				'Intensity' : vec3f( 1 , 1 , 1 )*0.1 ,
				'Roughness' : vec3f( 0 , 750 , 1000 ) ,
				'Density' : 1.0 ,
				'Hollow' : 1 ,
				'DistCenter' : 90_000 ,
				'Concentration' : 4.0 ,
			},
		}
#=============================================================
		self.Spheres : Dict[str,Dict[Literal['G_O','Color','Luminescence','Intensity','Roughness','Density','Hollow'],Union[GameObject,vec4f,vec3f,float,bool]]] = {
			'companion':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( -5 , -8.99 , -5 ),
						sca = vec3f( 1 ),
						rot = Rotation()
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				'Luminescence' : vec4f( vec3f( 0 , 1 , 1 ) , 0 ),
				'Intensity' : vec3f( 1 , 1 , 0.5 )*0 ,
				'Roughness' : vec3f( 0 , 0 , 0 ) ,
				'Density' : 2.0 ,
				'Hollow' : False
			},
			'chell':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , 100_010*10 , 0 ),
						sca = vec3f( 100_000 ),
						rot = Rotation()
					)),
				'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Intensity' : vec3f( 1 , 1 , 1 )*1.0 ,
				'Roughness' : vec3f( 1 , 0 , 0 ) ,
				'Density' : 1 ,
				'Hollow' : False
			},
			'flor':{
				'G_O' : GameObject(
					transform = Transform(
						pos = vec3f( 0 , -100_010.01 , 0 ),
						sca = vec3f( 100_000 ),
						rot = Rotation()
					)),
				#'Color' : vec4f( vec3f( 1 , 0.9 , 0.5 ) , 1 ),
				'Color' : vec4f( vec3f( 0.8 , 1 , 0.8 )*0.75 , 1 ),
				#'Color' : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				'Luminescence' : vec4f( vec3f( 0 , 0 , 0 ) , 0 ),
				'Intensity' : vec3f( 1 , 1 , 1 )*0 ,
				'Roughness' : vec3f( 1 , 0 , 0 ) ,
				'Density' : 1 ,
				'Hollow' : False
			},
		}
##############################################################
		
		#print(round(Rotation().Lz(-90).m,decimals=0))

		self.farPlane : float = 2.0
		self.aperture : float = 0.0
		self.Text = Text(
			camera = self.camera,
			color = vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
			text = "Rendered",
			pos = vec2f(-0.9,0.9),
			sca = vec2f(1,1)*0.5,
			rot = Rotation(),
			align = 'right',
			offset = 1,
			renderLayer = 'none',
			renderSide = 'Front'
		)

		self.FrameId : float = 1.0
		self.RenderComplete : bool = False
		self.RenderID : int = 0

		self.Chunk : int = 0
		self.CountOfChunkRender : int = 4


		self.DefaultMaterial.uniforms["farPlane"] = self.farPlane
		self.DefaultMaterial.uniforms["aperture"] = self.aperture
		self.DefaultMaterial.uniforms["PosCam"] = self.camera.gameObject.transform.position
		self.DefaultMaterial.uniforms["MatCam"] = self.camera.gameObject.transform.rotation
		self.PushData()



	def Update(self, dt : float) -> None:

		self.DefaultMaterial.uniforms["CountOfChunkRender"] = self.CountOfChunkRender
		self.DefaultMaterial.uniforms["Chunk"] = self.Chunk
		self.CameraControl(dt)
		self.DefaultMaterial.uniforms["FrameId"] = self.FrameId


		#self.Planes['glassWall']['G_O'].L_transform.rotation.Ly(0.1)

		#'''
		glPushMatrix()

		self.DefaultMaterial.uniforms["Render"] = False
		self.render(self.camera)

		if(self.FrameId>1000):
			if(not self.RenderComplete):
				self.Text.renderLayer='default'
				framebuffer = glGenFramebuffers(1)
				glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)  # Ensure you're still binding the framebuffer
				glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.BufferTexture.target, 0)

				width, height = self.BufferTexture.scale.arr  # Get the dimensions of the framebuffer
				image_data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)

				from numpy import frombuffer
				image_data = frombuffer(image_data, dtype=uint8).reshape(height, width, 4)
				image_data = image_data.reshape(height, width, -1)[::-1,:,:]

				# Create a Pillow image from the NumPy array
				image = Image.fromarray(image_data)

				# Save the image in PNG format
				image.save(f'RTX_RENDER/{self.RenderID}.png', format='PNG')
				image.close()
				glDeleteFramebuffers(1, [framebuffer])
				del framebuffer, width, height, image_data, image
				
				self.RenderComplete = True
				self.RenderID+=1
				#self.Chunk=0
				#self.FrameId = 1.0
				#self.PushData()

		else:
			self.Text.renderLayer='none'

			framebuffer = glGenFramebuffers(1)
			glBindFramebuffer(GL_FRAMEBUFFER,framebuffer)
			glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.BufferTexture.target, 0)

			self.DefaultMaterial.uniforms["Render"] = True
			self.render(self.camera)

			glDeleteFramebuffers(1, [framebuffer])
			del framebuffer
			self.RenderComplete = False
			self.Chunk=(self.Chunk+1)%self.CountOfChunkRender
			if(self.Chunk>=self.CountOfChunkRender-1):self.FrameId+=0.1

			pg.display.set_caption(f'Progress Render is = {((self.FrameId/1000)*100):.1f}% | {self.RenderID} frame | render slow down by a factor of {self.CountOfChunkRender} | FPS is = {self.mainForm.physics.fps:.0f}')
		glPopMatrix()#'''



	def PushData(self)->None:


		self.DefaultMaterial.uniforms["PortalPosition[0]"] = [self.Portals[i]['G_O'].transform.position for i in self.Portals]
		self.DefaultMaterial.uniforms["PortalSize[0]"] = [self.Portals[i]['G_O'].transform.scale for i in self.Portals]
		self.DefaultMaterial.uniforms["PortalMatrix[0]"] = [self.Portals[i]['G_O'].transform.rotation for i in self.Portals]
		self.DefaultMaterial.uniforms["PortalColor[0]"] = [self.Portals[i]['Color'] for i in self.Portals]


		self.DefaultMaterial.uniforms["Sphere[0]"] = [vec4f(self.Spheres[i]['G_O'].transform.position,(self.Spheres[i]['G_O'].transform.scale).magnitude) for i in self.Spheres]
		self.DefaultMaterial.uniforms["SphereColor[0]"] = [self.Spheres[i]['Color'] for i in self.Spheres]
		self.DefaultMaterial.uniforms["SphereLuminescence[0]"] = [self.Spheres[i]['Luminescence'] for i in self.Spheres]
		self.DefaultMaterial.uniforms["SphereIntensity[0]"] = [self.Spheres[i]['Intensity'] for i in self.Spheres]
		self.DefaultMaterial.uniforms["SphereRoughness[0]"] = [self.Spheres[i]['Roughness'] for i in self.Spheres]
		self.DefaultMaterial.uniforms["SphereDensity[0]"] = [self.Spheres[i]['Density'] for i in self.Spheres]
		self.DefaultMaterial.uniforms["SphereHollow[0]"] = [self.Spheres[i]['Hollow'] for i in self.Spheres]


		self.DefaultMaterial.uniforms["PlaneCenter[0]"] = [self.Planes[i]['G_O'].transform.position for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneSize[0]"] = [self.Planes[i]['G_O'].transform.scale.xy for i in self.Planes]		
		self.DefaultMaterial.uniforms["PlaneRot[0]"] = [self.Planes[i]['G_O'].transform.rotation for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneColor[0]"] = [self.Planes[i]['Color'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneMainTexture[0]"] = [self.Planes[i]['MainTex'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneMainTexOffset[0]"] = [self.Planes[i]['MainTexOffset'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneNormalTexture[0]"] = [self.Planes[i]['NormalTex'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneNormalTexStreight[0]"] = [self.Planes[i]['NormalTexStreight'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneNormalTexOffset[0]"] = [self.Planes[i]['NormalTexOffset'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneIntensityTexture[0]"] = [self.Planes[i]['IntensityTex'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneIntensityTexOffset[0]"] = [self.Planes[i]['IntensityTexOffset'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneLuminescence[0]"] = [self.Planes[i]['Luminescence'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneIntensity[0]"] = [self.Planes[i]['Intensity'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneRoughness[0]"] = [self.Planes[i]['Roughness'] for i in self.Planes]
		self.DefaultMaterial.uniforms["PlaneDensity[0]"] = [self.Planes[i]['Density'] for i in self.Planes]


		self.DefaultMaterial.uniforms["CubeCenter[0]"] = [self.Cubes[i]['G_O'].transform.position for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeSize[0]"] = [self.Cubes[i]['G_O'].transform.scale for i in self.Cubes]		
		self.DefaultMaterial.uniforms["CubeRot[0]"] = [self.Cubes[i]['G_O'].transform.rotation for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeColor[0]"] = [self.Cubes[i]['Color'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeMainTexture[0]"] = [self.Cubes[i]['MainTex'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeMainTexOffset[0]"] = [self.Cubes[i]['MainTexOffset'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeNormalTexture[0]"] = [self.Cubes[i]['NormalTex'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeNormalTexStreight[0]"] = [self.Cubes[i]['NormalTexStreight'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeNormalTexOffset[0]"] = [self.Cubes[i]['NormalTexOffset'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeIntensityTexture[0]"] = [self.Cubes[i]['IntensityTex'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeIntensityTexOffset[0]"] = [self.Cubes[i]['IntensityTexOffset'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeLuminescence[0]"] = [self.Cubes[i]['Luminescence'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeIntensity[0]"] = [self.Cubes[i]['Intensity'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeRoughness[0]"] = [self.Cubes[i]['Roughness'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeDensity[0]"] = [self.Cubes[i]['Density'] for i in self.Cubes]
		self.DefaultMaterial.uniforms["CubeHollow[0]"] = [self.Cubes[i]['Hollow'] for i in self.Cubes]


		self.DefaultMaterial.uniforms["CloudCenter[0]"] = [self.Clouds[i]['G_O'].transform.position for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudSize[0]"] = [self.Clouds[i]['G_O'].transform.scale for i in self.Clouds]		
		self.DefaultMaterial.uniforms["CloudRot[0]"] = [self.Clouds[i]['G_O'].transform.rotation for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudColor[0]"] = [self.Clouds[i]['Color'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudLuminescence[0]"] = [self.Clouds[i]['Luminescence'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudIntensity[0]"] = [self.Clouds[i]['Intensity'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudRoughness[0]"] = [self.Clouds[i]['Roughness'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudDensity[0]"] = [self.Clouds[i]['Density'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudHollow[0]"] = [self.Clouds[i]['Hollow'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudParticleSize[0]"] = [self.Clouds[i]['Particle_Size'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudOffsetScale[0]"] = [self.Clouds[i]['OffsetScale'] for i in self.Clouds]
		self.DefaultMaterial.uniforms["CloudOffsetPos[0]"] = [self.Clouds[i]['OffsetPos'] for i in self.Clouds]


		self.DefaultMaterial.uniforms["Atmosphere[0]"] = [vec4f(self.Atmospheres[i]['G_O'].transform.position,(self.Atmospheres[i]['G_O'].transform.scale).magnitude) for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereColor[0]"] = [self.Atmospheres[i]['Color'] for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereLuminescence[0]"] = [self.Atmospheres[i]['Luminescence'] for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereIntensity[0]"] = [self.Atmospheres[i]['Intensity'] for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereRoughness[0]"] = [self.Atmospheres[i]['Roughness'] for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereDensity[0]"] = [self.Atmospheres[i]['Density'] for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereHollow[0]"] = [self.Atmospheres[i]['Hollow'] for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereDistCenter[0]"] = [self.Atmospheres[i]['DistCenter'] for i in self.Atmospheres]
		self.DefaultMaterial.uniforms["AtmosphereConcentration[0]"] = [self.Atmospheres[i]['Concentration'] for i in self.Atmospheres]

	def render(self, camera:Camera) -> None:
		glClear(GL_DEPTH_BUFFER_BIT)
		glDepthMask(False)
		for i in camera.SkyBoxes:
			if(i.renderLayer in camera.renderLayer):
				i.Draw()

		for i in camera.Texts:
			if(i.renderLayer in camera.renderLayer):
				i.Draw()

	def CameraControl(self, dt : float)->None:

#=============================================================




		if(self.mainForm.keys[pg.K_UP]): self.farPlane=min(20,self.farPlane+0.01)
		if(self.mainForm.keys[pg.K_DOWN]): self.farPlane=max(0.1,self.farPlane-0.01)
		if(self.mainForm.keys[pg.K_LEFT]): self.aperture=max(0.0,self.aperture-0.001)
		if(self.mainForm.keys[pg.K_RIGHT]): self.aperture=min(1.0,self.aperture+0.001)

		tab : bool = self.mainForm.keys[pg.K_TAB]
		if(not self.swith and tab):
			self.swith = True
		if(self.swith and not tab):
			self.swith = False
			self.CameraMove = not self.CameraMove
			pg.mouse.set_visible(not self.CameraMove)
		del tab

		if(self.CameraMove):
			self.FrameId = 1.0
			self.Chunk = 0
			self.DefaultMaterial.uniforms["farPlane"] = self.farPlane
			self.DefaultMaterial.uniforms["aperture"] = self.aperture
			self.DefaultMaterial.uniforms["PosCam"] = self.camera.gameObject.transform.position
			self.DefaultMaterial.uniforms["MatCam"] = self.camera.gameObject.transform.rotation
			self.DefaultMaterial.uniforms["CountOfChunkRender"] = 0
			self.DefaultMaterial.uniforms["Chunk"] = -1

			moveSpeed : float = 2.5 * dt * (10 if(self.mainForm.keys[pg.K_LSHIFT]) else 1)
			q : bool = self.mainForm.keys[pg.K_q]
			e : bool = self.mainForm.keys[pg.K_e]
			w : bool = self.mainForm.keys[pg.K_w]
			a : bool = self.mainForm.keys[pg.K_a]
			s : bool = self.mainForm.keys[pg.K_s]
			d : bool = self.mainForm.keys[pg.K_d]

			if(q): self.Player.L_transform.position += self.MainCamera.transform.up * moveSpeed * -1
			if(e): self.Player.L_transform.position += self.MainCamera.transform.up * moveSpeed
			if(w): self.Player.L_transform.position += self.MainCamera.transform.forward * moveSpeed
			if(a): self.Player.L_transform.Move_right(-moveSpeed)
			if(s): self.Player.L_transform.position += self.MainCamera.transform.forward * moveSpeed * -1
			if(d): self.Player.L_transform.Move_right(moveSpeed)

			del q,e,w,a,s,d

			moveSpeed = 10 * dt
			mousePos : vec2i = self.mainForm.get_posMouse()

			self.Player.L_transform.rotation.Ly(mousePos.x * moveSpeed)
			self.MainCamera.L_transform.rotation.Lx(mousePos.y * moveSpeed)

			if(mousePos != 0):
				pg.mouse.set_pos(self.mainForm.Half_size.arr)

			del moveSpeed,mousePos
#=============================================================
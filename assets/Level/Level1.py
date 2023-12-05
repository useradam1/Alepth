from engene.openGL_atrib import *
import ast

class Level:
	def __init__(self, MainForm : Form) -> None:
		self.mainForm : Form = MainForm
	
	def LoadLevel(self) -> None:
		#_____________________________________________________________Camera
		self.CameraMove : bool = False
		self.swith : bool = False

		self.Player = GameObject(
			transform = Transform(
				pos = vec3f( -8 , -1 , 0 ),
				sca = vec3f( 1 , 1 , 1 ),
				rot = Rotation().Ly(90)
			)
		)
		self.MainCamera = GameObject(
			transform = Transform(
				pos = vec3f( 0 , 0 , 0 ),
				sca = vec3f( 1 , 1 , 1 ),
				rot = Rotation().Lx(0)
			),
			parent = self.Player,
			attributes = {
			}
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
		self.DefaultShader = Shader(
			form = self.mainForm,
			PathToShaders = (
				"assets/shaders/standart.frag",
				"assets/shaders/standart.vert"
			))
		#=============================================================
		self.SkyBoxShader = Shader(
			form = self.mainForm,
			PathToShaders = (
				"assets/shaders/SkyBox.frag",
				"assets/shaders/SkyBox.vert"
			))
		#=============================================================
		self.BlurShader = Shader(
			form = self.mainForm,
			PathToShaders = (
				"assets/shaders/Blur.frag",
				"assets/shaders/RTX.vert"
			))
		##############################################################



		#_____________________________________________________________Texture
		self.arrowTex = Texture(
			form = self.mainForm,
			path = "assets/image/arrow.bmp"
		)
		#=============================================================
		self.SkyBoxTex = Texture(
			form = self.mainForm,
			path = "assets/image/SkyBox1.jpg"
		)
		#=============================================================
		self.City_RGBA = Texture(
			form = self.mainForm,
			path = "assets/image/City-RGBA.png"
		)
		#=============================================================
		self.NormalMapCity = Texture(
			form = self.mainForm,
			path = "assets/image/NormalMapCity.png"
		)
		##############################################################



		#_____________________________________________________________SunDirection
		self.SunDirection = Rotation().Ly(180-45).Lx(-45)
		##############################################################



		#_____________________________________________________________Material
		self.SkyBoxMaterial = Material(
			shader = self.SkyBoxShader,
			attributes = {
			},
			uniforms = {
				"SkyBox" : self.SkyBoxTex,
			}
		)
		#=============================================================
		self.ArrowMaterial = Material(
			shader = self.DefaultShader,
			attributes = {
			},
			uniforms = {
				"Color" : vec4f( vec3f( 1 , 1 , 1 ) , 0.5 ),
				"Specular" : 10,
				"useTexture" : True,
				"Texture" : self.arrowTex,
				"useNormalTexture" : False,
				#"NormalTexture" : ,
				"scaleTex" : vec2f( 1 , 1 ),
				"shiftTex" : vec2f( 0 , 0 ),
				"SkyBox" : self.SkyBoxTex,
				"SunDirection" : self.SunDirection,
			}
		)
		self.DefaultMaterial = Material(
			shader = self.DefaultShader,
			attributes = {
			},
			uniforms = {
				"Color" : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				"Specular" : 0.5,
				"useTexture" : False,
				#"Texture" : self.arrowTex,
				"useNormalTexture" : False,
				#"NormalTexture" : ,
				"scaleTex" : vec2f( 1 , 1 ),
				"shiftTex" : vec2f( 0 , 0 ),
				"SkyBox" : self.SkyBoxTex,
				"SunDirection" : self.SunDirection,
			}
		)
		#=============================================================
		self.CityMaterial = Material(
			shader = self.DefaultShader,
			attributes = {
			},
			uniforms = {
				"Color" : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				"Specular" : 0.5,
				"useTexture" : True,
				"Texture" : self.City_RGBA,
				"useNormalTexture" : True,
				"NormalTexture" : self.NormalMapCity,
				"scaleTex" : vec2f( 1 , 1 ),
				"shiftTex" : vec2f( 0 , 0 ),
				"SkyBox" : self.SkyBoxTex,
				"SunDirection" : self.SunDirection,
			}
		)
		#=============================================================



		#_____________________________________________________________SkyBox
		self.SkyBox = SkyBox(
			camera = self.camera,
			material = self.SkyBoxMaterial,
			renderLayer = 'default',
			renderSide = 'All'
		)
		##############################################################



		#_____________________________________________________________Text
		self.Text = Text(
			camera = self.camera,
			color = vec4f(1,1,1,1),
			text = "[TAB] for move",
			pos = vec2f(0,-0.6),
			sca = vec2f(1,1),
			rot = Rotation(),
			align = 'chenter',
			offset = 1,
			renderLayer = 'none',
			renderSide = 'All'
		)
		##############################################################






		#_____________________________________________________________MeshFilter
		self.cube__MeshFilter = MeshFilter(self.mainForm, 0)
		self.city__MeshFilter = MeshFilter(self.mainForm, 0)
		#=============================================================
		self.mainForm.loader.LoadMeshes((
			(self.cube__MeshFilter, "assets/Obj/cube.obj", -1),
			#(self.city__MeshFilter, "assets/Obj/gm_construct.obj", 5),
			(self.city__MeshFilter, "assets/Obj/City.obj", -1),
		))
		##############################################################



		#_____________________________________________________________GameObject
		self.Cube__GameObject = GameObject(
			transform = Transform(
				pos = vec3f( 0 , 1 , 0 ),
				sca = vec3f( 1 , 1 , 1 ),
				rot = Rotation()
			),
			attributes = {
				'MeshRender' : MeshRender(
					form = self.mainForm,
					gameObject = None,
					meshFilter = self.cube__MeshFilter,
					material = self.ArrowMaterial,
					renderLayer = 'default',
					renderSide = 'Front'
				)
			}
		)
		#self.Cube__GameObject.Del()
		#=============================================================
		#'''
		self.City__GameObject = GameObject(
			transform = Transform(
				#pos = vec3f( 0 , 0 , 0 ),
				pos = vec3f( 0 , -40 , 0 ),
				#sca = vec3f( 1 , 1 , 1 ),
				sca = vec3f( 1 , 1 , 1 )*0.01,
				rot = Rotation()
			),
			attributes = {
				'MeshRender' : MeshRender(
					form = self.mainForm,
					gameObject = None,
					meshFilter = self.city__MeshFilter,
					material = self.CityMaterial,
					renderLayer = 'default',
					renderSide = 'Front'
				)
			}
		)#'''
		##############################################################
		#self.LoadCity()


	
	def Update(self, dt : float) -> None:
		self.Cube__GameObject.L_transform.rotation.Lx(50*dt).Ly(50*dt).Lz(50*dt)

		self.CameraControl(dt)

		self.camera.render()

	def LoadCity(self) -> None:
		
		construct_concrete_floor = Texture(
			form = self.mainForm,
			path = "assets/image/construct_concrete_floor.png"
		)
		grass = Texture(
			form = self.mainForm,
			path = "assets/image/grass.jpg"
		)
		roof_template001a = Texture(
			form = self.mainForm,
			path = "assets/image/roof_template001a.png"
		)
		brickwall003a = Texture(
			form = self.mainForm,
			path = "assets/image/brickwall003a.png"
		)
		construct_concrete_floorMat = Material(
			shader = self.DefaultShader,
			attributes = {
			},
			uniforms = {
				"Color" : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				"Specular" : 0.5,
				"useTexture" : True,
				"Texture" : construct_concrete_floor,
				"useNormalTexture" : False,
				#"NormalTexture" : self.NormalMapCity,
				"scaleTex" : vec2f( 1 , 1 ),
				"shiftTex" : vec2f( 0 , 0 ),
				"SkyBox" : self.SkyBoxTex,
				"SunDirection" : self.SunDirection,
			}
		)
		grassMat = Material(
			shader = self.DefaultShader,
			attributes = {
			},
			uniforms = {
				"Color" : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				"Specular" : 0.5,
				"useTexture" : True,
				"Texture" : grass,
				"useNormalTexture" : False,
				#"NormalTexture" : self.NormalMapCity,
				"scaleTex" : vec2f( 1 , 1 ),
				"shiftTex" : vec2f( 0 , 0 ),
				"SkyBox" : self.SkyBoxTex,
				"SunDirection" : self.SunDirection,
			}
		)
		roof_template001aMat = Material(
			shader = self.DefaultShader,
			attributes = {
			},
			uniforms = {
				"Color" : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				"Specular" : 0.5,
				"useTexture" : True,
				"Texture" : roof_template001a,
				"useNormalTexture" : False,
				#"NormalTexture" : self.NormalMapCity,
				"scaleTex" : vec2f( 1 , 1 ),
				"shiftTex" : vec2f( 0 , 0 ),
				"SkyBox" : self.SkyBoxTex,
				"SunDirection" : self.SunDirection,
			}
		)
		brickwall003aMat = Material(
			shader = self.DefaultShader,
			attributes = {
			},
			uniforms = {
				"Color" : vec4f( vec3f( 1 , 1 , 1 ) , 1 ),
				"Specular" : 0.5,
				"useTexture" : True,
				"Texture" : brickwall003a,
				"useNormalTexture" : False,
				#"NormalTexture" : self.NormalMapCity,
				"scaleTex" : vec2f( 1 , 1 ),
				"shiftTex" : vec2f( 0 , 0 ),
				"SkyBox" : self.SkyBoxTex,
				"SunDirection" : self.SunDirection,
			}
		)

		meshes = Get_Model("assets/Obj/gm_construct.obj","Fragment")
		filters : List[MeshFilter] = []
		for i in meshes:
			filters.append(MeshFilter(self.mainForm,i))


		City__GameObject = GameObject(
			transform = Transform(
				pos = vec3f( 0 , 0 , 0 ),
				#pos = vec3f( 0 , -40 , 0 ),
				sca = vec3f( 1 , 1 , 1 ),
				#sca = vec3f( 1 , 1 , 1 )*0.01,
				rot = Rotation()
			),
			attributes = {
			}
		)
		for i in filters:
			s = i.basename
			try:
				parts = s.split('+')[1]
				parts = ast.literal_eval(parts)
				parts = parts[1]
			except:parts = s.split('+')[0]

			City__GameObject.add_attribute(f"MeshFilter{i.basename}",
				MeshRender(
					form = self.mainForm,
					gameObject = City__GameObject,
					meshFilter = i,
					material = grassMat if(parts=='gm_construct.obj') else construct_concrete_floorMat if(parts=='func_illusionary_8348') else brickwall003aMat if(parts=='gross') else self.DefaultMaterial,
					renderLayer = 'default',
					renderSide = 'Front'
				)
			)

	def CameraControl(self, dt : float) -> None:
		#=============================================================
		tab : bool = self.mainForm.keys[pg.K_TAB]

		if(not self.swith and tab):
			self.swith = True
		if(self.swith and not tab):
			self.swith = False
			self.CameraMove = not self.CameraMove
			pg.mouse.set_visible(not self.CameraMove)
		del tab

		if(self.CameraMove):
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

			moveSpeed : float = 10 * dt
			mousePos : vec2i = self.mainForm.get_posMouse()

			self.Player.L_transform.rotation.Ly(mousePos.x * moveSpeed)
			self.MainCamera.L_transform.rotation.Lx(mousePos.y * moveSpeed)

			if(mousePos != 0):
				pg.mouse.set_pos(self.mainForm.Half_size.arr)
			
			del moveSpeed,mousePos
		#=============================================================
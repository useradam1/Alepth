from engene.model_shader_exporter import *
from engene.Obj_3D import *


from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame as pg

from engene.physics.physics import *

class Rigidbody(GameObjectInterface):
	def __init__(self,
		physics : 'Physics',
		gameObject : GameObject,
		transform : Transform,
		collider : Literal['sphere','cube'],
		static : bool,
		istrigger : bool
	) -> None:
		self.physics : Physics = physics
		super().__init__(gameObject)
		self.transform : Transform = transform
		self.collider : Literal['sphere','cube'] = collider
		self.static : bool = static
		self.istrigger : bool = istrigger
		self.physics.List_RigidBody.append(self)
		self.velocity : vec3f = vec3f(0,0,0)
		self.DeleateMethod = self.Del

	def Del(self) -> None:
		self.physics.List_RigidBody.remove(self)

	def Update(self) -> None:
		self.velocity += self.physics.gravity * 0.0001
		curentTransform : Transform = self.gameObject.transform.copy()
		curentTransform.position+=self.transform.position
		curentTransform.scale*=self.transform.scale
		curentTransform.rotation*=self.transform.rotation
		for i in self.physics.List_RigidBody:
			if(i!=self):
				data = do_cubes_intersect(curentTransform,i.gameObject.transform,self.velocity)
				if(data):
					self.velocity *= 0

		if(self.gameObject.parent != None):
			self.gameObject.L_transform.position += self.gameObject.parent.transform.rotation * (self.velocity)
		else:
			self.gameObject.L_transform.position += self.velocity
		del curentTransform

class Physics:
	def __init__(self, FPS : int = 60, gravity : vec3f = vec3f( 0 , -9.87 , 0 )) -> None:
		self.deltaT: float = 0
		self.time: float = 0
		self.fps: float = 0
		self.FPS_Limit : int = FPS
		self.gravity : vec3f = gravity
		self.clock = pg.time.Clock()
		self.List_RigidBody : List['Rigidbody'] = []

	def Update(self) -> None:
		self.deltaT = self.clock.tick(self.FPS_Limit)*0.001
		self.fps = self.clock.get_fps()
		self.time = pg.time.get_ticks() * 0.001
		[i.Update() for i in self.List_RigidBody if(not i.static)]










def get_shader_variables(Shader) -> Dict[Literal['attributes','uniforms'],dict]:
	attributes = {}
	uniforms = {}
	attrib_count = glGetProgramiv(Shader, GL_ACTIVE_ATTRIBUTES)
	uniform_count = glGetProgramiv(Shader, GL_ACTIVE_UNIFORMS)
	for i in range(attrib_count):
		name, size, Type = glGetActiveAttrib(Shader, i)
		location = glGetAttribLocation(Shader, name)
		if location != -1:
			attributes[name.decode("utf-8")]=(size,location,get_type_name(Type))
	for i in range(uniform_count):
		name, size, Type = glGetActiveUniform(Shader, i)
		location = glGetUniformLocation(Shader, name)
		if location != -1:
			uniforms[name.decode("utf-8")]=(size,location,get_type_name(Type))
	return {'attributes': attributes, 'uniforms': uniforms}

def get_type_name(type_enum):
	if type_enum == GL_BOOL:
		return bool
	elif type_enum == GL_INT:
		return int
	elif type_enum == GL_FLOAT:
		return float
	elif type_enum == GL_FLOAT_VEC2:
		return vec2f
	elif type_enum == GL_FLOAT_VEC3:
		return vec3f
	elif type_enum == GL_FLOAT_VEC4:
		return vec4f
	elif type_enum == GL_INT_VEC2:
		return vec2i
	elif type_enum == GL_INT_VEC3:
		return vec3i
	elif type_enum == GL_INT_VEC4:
		return vec4i
	elif type_enum == GL_FLOAT_MAT2:
		return mat2f
	elif type_enum == GL_FLOAT_MAT3:
		return mat3f
	elif type_enum == GL_FLOAT_MAT4:
		return mat4f
	elif type_enum == GL_SAMPLER_2D:
		return Texture
	else:
		return 'unknown'


class Texture:
	def __init__(self,
		form : 'Form',
		path : str | vec2i,
		color : vec4f = vec4f(1.0, 1.0, 1.0, 1.0)
	) -> None:
		self.form : 'Form' = form
		self.path = path
		self.color : vec4f = color
		self.baseName : str = str(path)
		self.form.Textures.append(self)

		image : Image = 0
		image_data : ndarray[uint8] = []
		width, height = (1,1)

		print(f'Load Texture {self.baseName} start')
		if(isinstance(path,str)):
			image_data, width, height = LoadTextureData(filePath=path)
		elif(isinstance(path,vec2i)):
			width, height = path.arr
			image_data = ones((height, width, 4), dtype=uint8) * 255

		if self.color != vec4f(1.0, 1.0, 1.0, 1.0):
			image_data[:, :, 0:4] = (image_data[:, :, 0:4] * self.color.arr).astype(uint8)

		target = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, target)

		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
			GL_RGBA, GL_UNSIGNED_BYTE, image_data)

		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

		glGenerateMipmap(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, 0)
		self.target : uintc = target
		self.scale = vec2i(width,height)
		del image_data, image, width, height, target
		print(f'Load Texture {self.baseName} end')

	def Del(self) -> None:
		glDeleteTextures(1, array([int(self.target)]))
		self.form.Remove_GPU_Buffer(self)
		print(f'deleated Texture from GPU memory {self.baseName}')
		del self.form, self.path, self.color, self.baseName, self.target, self.scale

class Shader:
	def __init__(self, form : 'Form', PathToShaders : Tuple[str]) -> None:
		self.form : 'Form' = form
		self.PathToShaders = PathToShaders
		print(f"Load Shader {self.PathToShaders} start")
		self.ShaderProg=extract_Shader(self.PathToShaders)
		self.form.ShaderBuffer.append(self)
		self.ParamsShader = get_shader_variables(self.ShaderProg)
		print(f"Load Shader {self.PathToShaders} end")

	def Del(self):
		glDeleteProgram(self.ShaderProg)
		self.form.Remove_GPU_Buffer(self)
		print(f"deleated Shader {self.PathToShaders}")
		del self.form, self.ShaderProg, self.ParamsShader

matrix2x2 = eye(2)
matrix3x3 = eye(3)
matrix4x4 = eye(4)

class Material:
	def __init__(self, shader : Shader,
		attributes : Dict[
				str , Union[
						'bool',
						'int',
						'float',
						'vec2f',
						'vec3f',
						'vec4f',

						Union[List['bool'],Tuple['bool']],
						Union[List['int'],Tuple['int']],
						Union[List['float'],Tuple['float']],
						Union[List['vec2f'],Tuple['vec2f']],
						Union[List['vec3f'],Tuple['vec3f']],
						Union[List['vec4f'],Tuple['vec4f']],
							]
			],
		uniforms : Dict[
				str , Union[
						'bool',
						'int',
						'float',
						'vec2f',
						'vec3f',
						'vec4f',
						'vec2i',
						'vec3i',
						'vec4i',
						'mat2f',
						'mat3f',
						'mat4f',
						'Texture',

						Union[List['bool'],Tuple['bool']],
						Union[List['int'],Tuple['int']],
						Union[List['float'],Tuple['float']],
						Union[List['vec2f'],Tuple['vec2f']],
						Union[List['vec3f'],Tuple['vec3f']],
						Union[List['vec4f'],Tuple['vec4f']],
						Union[List['vec2i'],Tuple['vec2i']],
						Union[List['vec3i'],Tuple['vec3i']],
						Union[List['vec4i'],Tuple['vec4i']],
						Union[List['mat2f'],Tuple['mat2f']],
						Union[List['mat3f'],Tuple['mat3f']],
						Union[List['mat4f'],Tuple['mat4f']],
						Union[List['Texture'],Tuple['Texture']],
							]
		]

	) -> None:
		self.shader : Shader = shader
		self.attributes = attributes
		self.uniforms = uniforms

	@property
	def UseShader(self) -> None:
		if(self.shader==0):
			glUseProgram(0)
			glColor3f(1,0,1)
			return
		glUseProgram(self.shader.ShaderProg)
		texID : int = 0

		atr = self.shader.ParamsShader['attributes']
		for name in atr:
			location : intc = atr[name][1]
			size : int = atr[name][0]
			Type : type = atr[name][2]
			if(name in self.attributes):
				data = self.uniforms[name]
				if isinstance(data, (list, tuple)):
					if(all(isinstance(item, (bool, float, int)) for item in data) and (Type in (bool, float, int))):
						glVertexAttrib1fv(location, size, data)
					elif(all(isinstance(item, (vec2f, vec2i)) for item in data) and (Type in (vec2f, vec2i))):
						glVertexAttrib2fv(location, size, [(j.x,j.y) for j in data])
					elif(all(isinstance(item, (vec3f, vec3i)) for item in data) and (Type in (vec3f, vec3i))):
						glVertexAttrib3fv(location, size, [(j.x,j.y,j.z) for j in data])
					elif(all(isinstance(item, (vec4f, vec4i)) for item in data) and (Type in (vec4f, vec4i))):
						glVertexAttrib4fv(location, size, [(j.x,j.y,j.z,j.w) for j in data])
					else:self.NullData(size,location,Type,'attributes',texID)
				else:
					if(isinstance(data , (bool, float, int)) and (Type in (bool, float, int))):
						glVertexAttrib1f(location, data)
					elif(isinstance(data , (vec2f, vec2i)) and (Type in (vec2f, vec2i))):
						glVertexAttrib2f(location, data.x, data.y)
					elif(isinstance(data , (vec3f, vec3i)) and (Type in (vec3f, vec3i))):
						glVertexAttrib3f(location, data.x, data.y, data.z)
					elif(isinstance(data , (vec4f, vec4i)) and (Type in (vec4f, vec4i))):
						glVertexAttrib4f(location, data.x, data.y, data.z, data.w)
					else:self.NullData(size,location,Type,'attributes',texID)
			else:self.NullData(size,location,Type,'attributes',texID)

		atr = self.shader.ParamsShader['uniforms']
		for name in atr:
			location : intc = atr[name][1]
			size : int = atr[name][0]
			Type : type = atr[name][2]
			if(name in self.uniforms):
				data = self.uniforms[name]
				if isinstance(data, (list, tuple)):
					if(all(isinstance(item, (bool, float, int)) for item in data) and (Type in (bool, float, int))):
						glUniform1fv(location, size, data)
					elif(all(isinstance(item, (vec2f, vec2i)) for item in data) and (Type in (vec2f, vec2i))):
						glUniform2fv(location, size, [(j.x,j.y) for j in data])
					elif(all(isinstance(item, (vec3f, vec3i)) for item in data) and (Type in (vec3f, vec3i))):
						glUniform3fv(location, size, [(j.x,j.y,j.z) for j in data])
					elif(all(isinstance(item, (vec4f, vec4i)) for item in data) and (Type in (vec4f, vec4i))):
						glUniform4fv(location, size, [(j.x,j.y,j.z,j.w) for j in data])
					elif(all(isinstance(item, (mat2f,)) for item in data) and (Type in (mat2f,))):
						glUniformMatrix2fv(location, size, GL_FALSE, [value for array in data for value in array.m.flatten()])
					elif(all(isinstance(item, (mat3f,)) for item in data) and (Type in (mat3f,))):
						glUniformMatrix3fv(location, size, GL_FALSE, [value for array in data for value in array.m.flatten()])
					elif(all(isinstance(item, (mat4f,)) for item in data) and (Type in (mat4f,))):
						glUniformMatrix4fv(location, size, GL_FALSE, [value for array in data for value in array.m.flatten()])
					elif(all(isinstance(item, (Texture,)) for item in data) and (Type in (Texture,))):
						lastsTexId : float = texID
						for tex in range(size):
							if(len(data)>tex):
								glActiveTexture(GL_TEXTURE0+texID)
								glBindTexture(GL_TEXTURE_2D, data[tex].target)
							else:
								glActiveTexture(GL_TEXTURE0+texID)
								glBindTexture(GL_TEXTURE_2D, 1)
							texID += 1
						textures = [i+lastsTexId for i in range(size)]
						glUniform1iv(location, size, textures)
					else:self.NullData(size,location,Type,'uniforms',texID)
				else:
					if(isinstance(data , (bool, float, int)) and (Type in (bool, float, int))):
						glUniform1f(location, data)
					elif(isinstance(data , (vec2f, vec2i)) and (Type in (vec2f, vec2i))):
						glUniform2f(location, data.x, data.y)
					elif(isinstance(data , (vec3f, vec3i)) and (Type in (vec3f, vec3i))):
						glUniform3f(location, data.x, data.y, data.z)
					elif(isinstance(data , (vec4f, vec4i)) and (Type in (vec4f, vec4i))):
						glUniform4f(location, data.x, data.y, data.z, data.w)
					elif(isinstance(data , (mat2f,)) and (Type in (mat2f,))):
						glUniformMatrix2fv(location, size, GL_FALSE, data.m)
					elif(isinstance(data , (mat3f,)) and (Type in (mat3f,))):
						glUniformMatrix3fv(location, size, GL_FALSE, data.m)
					elif(isinstance(data , (mat4f,)) and (Type in (mat4f,))):
						glUniformMatrix4fv(location, size, GL_FALSE, data.m)
					elif(isinstance(data , (Texture,)) and (Type in (Texture,))):
						glActiveTexture(GL_TEXTURE0+texID)
						glBindTexture(GL_TEXTURE_2D, data.target)
						glUniform1i(location, texID)
						texID += 1
					else:self.NullData(size,location,Type,'uniforms',texID)
			else:self.NullData(size,location,Type,'uniforms',texID)

	def NullData(self, size:int, location, Type, atr:str, texID:int) -> None:
		if(atr == 'attributes'):
			if(size == 1):
				if(Type in (int, float, bool)):
					glVertexAttrib1f(location, 0)
				elif(Type in (vec2f, vec2i)):
					glVertexAttrib2f(location, 0, 0)
				elif(Type in (vec3f, vec3i)):
					glVertexAttrib3f(location, 0, 0, 0)
				elif(Type in (vec4f, vec4i)):
					glVertexAttrib4f(location, 0, 0, 0, 0)
			else:
				if(Type in (int, float, bool)):
					glVertexAttrib1fv(location, size, [0,])
				elif(Type in (vec2f, vec2i)):
					glVertexAttrib2fv(location, size, [0,])
				elif(Type in (vec3f, vec3i)):
					glVertexAttrib3fv(location, size, [0,])
				elif(Type in (vec4f, vec4i)):
					glVertexAttrib4fv(location, size, [0,])
		elif(atr=='uniforms'):
			if(size==1):
				if(Type in (int, float, bool)):
					glUniform1f(location, 0)
				elif(Type in (vec2f, vec2i)):
					glUniform2f(location, 0,0)
				elif(Type in (vec3f, vec3i)):
					glUniform3f(location, 0,0,0)
				elif(Type in (vec4f, vec4i)):
					glUniform4f(location, 0,0,0,0)
				elif(Type == mat2f):
					glUniformMatrix2fv(location, size, GL_FALSE, matrix2x2)
				elif(Type == mat3f):
					glUniformMatrix3fv(location, size, GL_FALSE, matrix3x3)
				elif(Type == mat4f):
					glUniformMatrix4fv(location, size, GL_FALSE, matrix4x4)
				elif(Type == Texture):
					glActiveTexture(GL_TEXTURE0+texID)
					glBindTexture(GL_TEXTURE_2D, 1)
					glUniform1i(location, texID)
					texID += 1
			else:
				if(Type in (int, float, bool)):
					glUniform1fv(location, size, [0,])
				elif(Type in (vec2f, vec2i)):
					glUniform2fv(location, size, [0,])
				elif(Type in (vec3f, vec3i)):
					glUniform3fv(location, size, [0,])
				elif(Type in (vec4f, vec4i)):
					glUniform4fv(location, size, [0,])
				elif(Type == mat2f):
					glUniformMatrix2fv(location, size, GL_FALSE, matrix2x2)
				elif(Type == mat3f):
					glUniformMatrix3fv(location, size, GL_FALSE, matrix3x3)
				elif(Type == mat4f):
					glUniformMatrix4fv(location, size, GL_FALSE, matrix4x4)
				elif(Type == Texture):
					lastsTexId : float = texID
					for _ in range(size):
						glActiveTexture(GL_TEXTURE0+texID)
						glBindTexture(GL_TEXTURE_2D, 1)
						texID += 1
					textures = [i+lastsTexId for i in range(size)]
					glUniform1iv(location, size, textures)

class MeshFilter:
	def __init__(self,
		form : 'Form',
		mesh : Mesh | int = 0
	) -> None:

		self.form : Form = form
		self.loaded : bool = False
		self.form.MeshFilters.append(self)

		if(mesh!=0):
			self.LoadMesh(mesh)

	def LoadMesh(self, mesh : Mesh = 0) -> None:

		if(mesh==0):return

		self.GPU_Del

		self.basename : str = mesh.baseName
		print(f'Load Mesh {self.basename} start')

		# VAO
		self.VAO = glGenVertexArrays(1)
		glBindVertexArray(self.VAO)

		# VBO
		self.vertexVBO = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.vertexVBO)
		glBufferData(GL_ARRAY_BUFFER, mesh.Vertices.nbytes, mesh.Vertices, GL_STATIC_DRAW)
		glVertexAttribPointer(0, 3, GL_FLOAT, False, 0, None)
		glEnableVertexAttribArray(0)

		self.UVSbool : bool = len(mesh.Uvs)==len(mesh.Vertices)
		# uvsVBO
		if(self.UVSbool):
			self.uvsVBO = glGenBuffers(1)
			glBindBuffer(GL_ARRAY_BUFFER, self.uvsVBO)
			glBufferData(GL_ARRAY_BUFFER, mesh.Uvs.nbytes, mesh.Uvs, GL_STATIC_DRAW)
			glVertexAttribPointer(1, 2, GL_FLOAT, False, 0, None)
			glEnableVertexAttribArray(1)
		else:
			print(F'!Warning! Mesh no have UVS!!! {self.basename}')

		# NBO
		self.normalNBO = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, self.normalNBO)
		glBufferData(GL_ARRAY_BUFFER, mesh.Normals.nbytes, mesh.Normals, GL_STATIC_DRAW)
		glVertexAttribPointer(2, 3, GL_FLOAT, False, 0, None)
		glEnableVertexAttribArray(2)

		# EBO
		self.indexEBO = glGenBuffers(1)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indexEBO)
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, mesh.Faces.nbytes, mesh.Faces, GL_STATIC_DRAW)

		glBindVertexArray(0)
		glBindBuffer(GL_ARRAY_BUFFER, 0)
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
		self.lenT = len(mesh.Faces) * 3

		print(f'Load MeshFilter {self.basename} end')
		self.loaded = True
		del mesh

	def Draw(self):
		glBindVertexArray(self.VAO)
		glDrawElements(GL_TRIANGLES, self.lenT, GL_UNSIGNED_INT, None)
		glBindVertexArray(0)

	@property
	def GPU_Del(self) -> None:
		if(self.loaded):
			self.loaded = False
			glDeleteBuffers(1, array([self.vertexVBO], dtype=float32))
			if(self.UVSbool):
				glDeleteBuffers(1, array([self.uvsVBO], dtype=float32))
			glDeleteBuffers(1, array([self.normalNBO], dtype=float32))
			glDeleteBuffers(1, array([self.indexEBO], dtype=int32))
			glDeleteVertexArrays(1, array([self.VAO], dtype=int32))
			print(f"deleated MeshFilter from GPU memory {self.basename}")

	def Del(self) -> None:
		self.GPU_Del
		self.form.Remove_GPU_Buffer(self)
		del self.form, self.loaded

RENDER_LAYER = Literal['default','none']

class MeshRender(GameObjectInterface):
	def __init__(self,
		form : 'Form',
		gameObject : GameObject,
		meshFilter : MeshFilter,
		material : Material | int = 0,
		renderLayer : RENDER_LAYER = 'default',
		renderSide : Literal['Front','Back','All'] = 'Front'
	) -> None:
		self.form : Form = form
		super().__init__(gameObject)
		self.meshFilter : MeshFilter = meshFilter
		self.material : Material = material
		self.renderLayer : RENDER_LAYER = renderLayer
		self.renderSide : Literal['Front','Back','All'] = renderSide
		self.DeleateMethod = self.Del
		self.form.MeshRenders.append(self)

	def Draw(self, camera : 'Camera') -> None:
		if(self.renderSide=='Back'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_FRONT)
		elif(self.renderSide=='Front'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_BACK)
		elif(self.renderSide=='All'):
			glDisable(GL_CULL_FACE)

		#Shader
		if(not self.meshFilter.UVSbool or self.material==0):
			glUseProgram(0)
			glColor3f(1,0,1)
		elif(self.meshFilter.basename == "__ERROR__.obj"):
			glUseProgram(self.form._ERROR_SHADER.ShaderProg)
			atr = self.form._ERROR_SHADER.ParamsShader['uniforms']
			for j in atr:
				location = atr[j][1]
				size = atr[j][0]
				if(j == 'time'):
					glUniform1f(location, self.form.physics.time*20)
				elif(j == 'v_Pos'):
					glUniform3f(location,
						self.gameObject.transform.position.x,
						self.gameObject.transform.position.y,
						self.gameObject.transform.position.z
					)
				elif(j == 'v_Sca'):
					glUniform3f(location,
						self.gameObject.transform.scale.x,
						self.gameObject.transform.scale.y,
						self.gameObject.transform.scale.z
					)
				elif(j == 'v_Rot'):
					glUniformMatrix3fv(location, size, GL_FALSE, self.gameObject.transform.rotation.m)
				elif(j == 'CamPos'):
					pca = camera.gameObject.transform.position
					glUniform3f(location, pca.x, pca.y, pca.z)
					del pca
		else:
			self.material.uniforms['CamPos']=camera.gameObject.transform.position
			self.material.uniforms['CamRot']=camera.gameObject.transform.rotation
			self.material.uniforms['MaxFarPlaneCamera']=camera.far
			self.material.uniforms['Fov']=camera.fov
			self.material.uniforms['ScreenSize']=self.form.size
			self.material.uniforms['v_Pos']=self.gameObject.transform.position
			self.material.uniforms['v_Sca']=self.gameObject.transform.scale
			self.material.uniforms['v_Rot']=self.gameObject.transform.rotation
			self.material.UseShader

		glPushMatrix()
		glTranslatef(
			self.gameObject.transform.position.x,
			self.gameObject.transform.position.y,
			self.gameObject.transform.position.z)
		view_matrix = eye(4)
		view_matrix[:3, :3] = self.gameObject.transform.rotation.m
		glMultMatrixf(view_matrix)
		del view_matrix
		glScalef(
			self.gameObject.transform.scale.x,
			self.gameObject.transform.scale.y,
			self.gameObject.transform.scale.z)
		self.meshFilter.Draw()
		glPopMatrix()
		glDisable(GL_CULL_FACE)

	def Del(self) -> None:
		self.form.Remove_GPU_Buffer(self)



class Camera(GameObjectInterface):
	def __init__(self,
			form : 'Form',
			gameObject : GameObject,
			near : float = 0.1,
			far : float = 20_000,
			fov : float = 75.0,
			renderLayer : List[RENDER_LAYER] = ['default',]) -> None:
		self.form : Form = form
		super().__init__(gameObject)
		self.near : float = near
		self.far : float = far
		self.fov : float = fov
		self.aspectRatio : float = (self.form.size.x/self.form.size.y)
		self.renderLayer : List[RENDER_LAYER] = renderLayer
		self.SkyBoxes : List[SkyBox] = []
		self.Rectangles : List[Rectangle] = []
		self.Texts : List[Text] = []

	def perspective(self) -> None:
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		gluPerspective(self.fov,self.aspectRatio,self.near,self.far)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		glScalef(
			-50*self.gameObject.transform.scale.x,
			50*self.gameObject.transform.scale.y,
			50*self.gameObject.transform.scale.z
		)
		glRotatef(180,0,1,0)

	def ortogonal(self) -> None:
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(-1,1,-1,1,-1,self.far*2)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def ClearColor(self) -> None:
		glClearColor(
			self.form.color.x,
			self.form.color.y,
			self.form.color.z,
			self.form.color.w,
		)
		glClear(GL_COLOR_BUFFER_BIT)

	def render(self) -> None:
		glClear(GL_DEPTH_BUFFER_BIT)
		glDepthMask(False)
		for i in self.SkyBoxes:
			if(i.renderLayer in self.renderLayer):
				i.Draw()
		glDepthMask(True)
		for i in self.Rectangles:
			if(i.renderLayer in self.renderLayer):
				i.Draw()

		glPushMatrix()
		self.perspective()

		view_matrix = eye(4)
		view_matrix[:3, :3] = self.gameObject.transform.rotation.inv_get_nparray
		glMultMatrixf(view_matrix)
		del view_matrix

		glTranslatef(
		-self.gameObject.transform.position.x,
		-self.gameObject.transform.position.y,
		-self.gameObject.transform.position.z)

		#'''
		glEnable(GL_ALPHA_TEST)

		glDepthMask(True)
		glAlphaFunc(GL_GREATER,0.99)
		for i in self.form.MeshRenders:
			if(i.meshFilter.loaded and i.renderLayer in self.renderLayer):
				i.Draw(self)

		glDepthMask(False)
		glAlphaFunc(GL_LEQUAL,0.99)
		for i in self.form.MeshRenders:
			if(i.meshFilter.loaded and i.renderLayer in self.renderLayer):
				i.Draw(self)

		glDisable(GL_ALPHA_TEST)
		#'''

		glDepthMask(True)
		for i in self.form.MeshRenders:
			if(i.meshFilter.loaded and i.renderLayer in self.renderLayer):
				i.Draw(self)
		glPopMatrix()

		for i in self.Texts:
			if(i.renderLayer in self.renderLayer):
				i.Draw()



class Rectangle:
	def __init__(self,
			camera : Camera,
			material : Material,
			pos : vec3f = vec3f(0,0,0),
			sca : vec2f = vec2f(1,1),
			rot : float = 0,
			renderLayer : RENDER_LAYER = 'default',
			renderSide : Literal['Front','Back','All'] = 'All'
		) -> None:
		self.camera = camera
		self.material = material
		self.pos : vec3f = pos
		self.sca : vec2f = sca
		self.rot : float = rot
		self.camera.Rectangles.append(self)
		self.renderLayer : RENDER_LAYER = renderLayer
		self.renderSide : Literal['Front','Back','All'] = renderSide
	@property
	def Del(self):
		self.camera.Rectangles.remove(self)
	def Draw(self):
		if(self.renderSide=='Front'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_FRONT)
		elif(self.renderSide=='Back'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_BACK)
		elif(self.renderSide=='All'):
			glDisable(GL_CULL_FACE)
		glPushMatrix()
		self.camera.perspective()
		glTranslatef(self.pos.x,self.pos.y,self.pos.z)
		glScalef(self.sca.x,self.sca.y,1)
		glRotatef(self.rot, 0,0,1)
		self.material.UseShader
		self.camera.form._RECTANGLE_MESH_FILTER.Draw()
		glPopMatrix()
		glDisable(GL_CULL_FACE)

class SkyBox:
	def __init__(self,
			camera : Camera,
			material : Material,
			renderLayer : RENDER_LAYER = 'default',
			renderSide : Literal['Front','Back','All'] = 'All'
		) -> None:
		self.camera = camera
		self.material = material
		self.camera.SkyBoxes.append(self)
		self.renderLayer : RENDER_LAYER = renderLayer
		self.renderSide : Literal['Front','Back','All'] = renderSide
	@property
	def Del(self):
		self.camera.SkyBoxes.remove(self)
	def Draw(self):
		if(self.renderSide=='Front'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_FRONT)
		elif(self.renderSide=='Back'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_BACK)
		elif(self.renderSide=='All'):
			glDisable(GL_CULL_FACE)
		glPushMatrix()
		glDisable(GL_DEPTH_TEST)
		self.camera.ortogonal()
		glTranslatef(0,0,-1)
		glScalef(1,1,1)
		self.material.uniforms["CamRot"] = self.camera.gameObject.transform.rotation
		self.material.uniforms['Fov']=self.camera.fov
		self.material.uniforms['ScreenSize']=self.camera.form.size
		self.material.UseShader
		self.camera.form._RECTANGLE_MESH_FILTER.Draw()
		glEnable(GL_DEPTH_TEST)
		glPopMatrix()
		glDisable(GL_CULL_FACE)

class Text:
	def __init__(self,
			camera : Camera,
			color : vec4f,
			text : str,
			pos : vec2f,
			sca : vec2f,
			rot : Rotation,
			align : Literal['chenter','right','left'],
			offset : float,
			renderLayer : RENDER_LAYER = 'default',
			renderSide : Literal['Front','Back','All'] = 'All'
	) -> None:
		self.camera = camera
		self.color = color
		self.text = text
		self.pos = pos
		self.sca = sca
		self.rot = rot
		self.align = align
		self.offset = offset
		self._COUNT_OF_ALL_CHAR : vec2i = vec2i(256,256)
		self.renderLayer : RENDER_LAYER = renderLayer
		self.renderSide : Literal['Front','Back','All'] = renderSide
		self.material = Material(
			shader = self.camera.form._FONT_SHADER, attributes = {},
			uniforms = {
				"Texture":self.camera.form._FONT_TEXTURE,
				"texScale":self.camera.form._FONT_TEXTURE.scale,
				"CharScale":self._COUNT_OF_ALL_CHAR,
				"Color":self.color,
			})
		self.camera.Texts.append(self)
	@property
	def Del(self):
		self.camera.Texts.remove(self)
	def Draw(self):
		glClear(GL_DEPTH_BUFFER_BIT)
		if(self.renderSide=='Front'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_FRONT)
		elif(self.renderSide=='Back'):
			glEnable(GL_CULL_FACE)
			glCullFace(GL_BACK)
		elif(self.renderSide=='All'):
			glDisable(GL_CULL_FACE)
		glPushMatrix()
		glDisable(GL_DEPTH_TEST)
		self.camera.ortogonal()
		glTranslatef(self.pos.x,self.pos.y,0)
		for id, char in enumerate(self.text):
			x = ord(char) & (self._COUNT_OF_ALL_CHAR.x-1)
			y = ord(char) // self._COUNT_OF_ALL_CHAR.x
			self.material.uniforms["CharPos"] = vec2f(x,y)
			self.material.UseShader
			lenText = len(self.text)-1
			glPushMatrix()
			if(self.align == 'chenter'):
				self.rot.Push
				self.rot.m[1]*=(self.camera.form.size.x/self.camera.form.size.y)
				point = self.rot*vec3f((-((lenText*0.5)-(id)) ) * (self.sca.x*(0.05)) * self.offset)
				self.rot.Pop
				glTranslatef(point.x,point.y,point.z)
			elif(self.align == 'right'):
				self.rot.Push
				self.rot.m[1]*=(self.camera.form.size.x/self.camera.form.size.y)
				point = self.rot*vec3f((-((lenText*0)-(id))) * (self.sca.x*(0.05)) * self.offset)
				self.rot.Pop
				glTranslatef(point.x,point.y,point.z)
			elif(self.align == 'left'):
				self.rot.Push
				self.rot.m[1]*=(self.camera.form.size.x/self.camera.form.size.y)
				point = self.rot*vec3f((-((lenText)-(id))) * (self.sca.x*(0.05)) * self.offset)
				self.rot.Pop
				glTranslatef(point.x,point.y,point.z)
			glScalef(self.sca.x*(0.05),self.sca.y*(0.05*(self.camera.form.size.x/self.camera.form.size.y)),1)
			view_matrix = eye(4)
			view_matrix[:3, :3] = self.rot.inv_get_nparray
			glMultMatrixf(view_matrix)
			del view_matrix
			self.camera.form._RECTANGLE_MESH_FILTER.Draw()
			glPopMatrix()
		glEnable(GL_DEPTH_TEST)
		glPopMatrix()
		glDisable(GL_CULL_FACE)




from io import BytesIO
from base64 import b64decode
def get_icon():
	return BytesIO(b64decode('''iVBORw0KGgoAAAANSUhEUgAAABIAAAASAQMAAAB
sABwUAAAABlBMVEUAAAD///+l2Z/dAAAAAnRST
lP5Al3j9uAAAAAJcEhZcwAADsQAAA7EAZUrDhsA
AAAtdEVYdFNvZnR3YXJlAENyZWF0ZWQgYnkgZk
NvZGVyIEdyYXBoaWNzIFByb2Nlc3Nvcn/D7V8AA
ABASURBVHjaY/j//wDD9/cQ/Pn5AYbfnw8w/Px
5gOHP1wMMv8qBfPMDDJ+nA/F5KP4OlAeq+QFS8/
cAw0egfqAZAIMgLlWRNdO/AAAAAElFTkSuQmCC'''))



class Form:
	def __init__(self,
			size : vec2i = vec2i(500,500),
			title : str = "New",
			color : vec4f = vec4f(0,0,0,1),
			physics : Physics = Physics()
		) -> None:


		self.MeshFilters : List[MeshFilter] = []
		self.ShaderBuffer : List[Shader] = []
		self.MeshRenders : List[MeshRender] = []
		self.Textures : List[Texture] = []

		self.size : vec2i = size
		self.Half_size : vec2i = self.size * 0.5
		self.title : str = title
		self.color : vec4f = color
		self.physics : Physics = physics
		self.loader : Loader = Loader()

		pg.init()

		pg.display.set_caption("Loading")
		pg.display.set_icon(pg.image.load(get_icon()))



		#_____________________________OPEN_GL_CONTEXT___________________________
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION,3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,pg.GL_CONTEXT_PROFILE_CORE)
		pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)
		pg.display.set_mode(self.size.arr, flags=pg.DOUBLEBUF|pg.OPENGL)

		glEnable(GL_DEPTH_TEST)
		glEnable(GL_BLEND)
		glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
		glDisable(GL_CULL_FACE)
		############################################################################


		#_______________________SHADER___________________
		self._ERROR_SHADER = Shader(form = self,
			PathToShaders = (
			'engene/assetEngene/Error.frag',
			'engene/assetEngene/Error.vert',
		))
		self._FONT_SHADER = Shader(form = self,
			PathToShaders = (
			"engene/assetEngene/font.frag",
			"engene/assetEngene/font.vert"
		))
		self.Remove_GPU_Buffer(self._ERROR_SHADER)
		self.Remove_GPU_Buffer(self._FONT_SHADER)
		#################################################


		#____________________MeshFilter__________________
		self._RECTANGLE_MESH_FILTER = MeshFilter(form=self,
			mesh = Get_Model('engene/assetEngene/__fontPlane__.obj',"All")[0]
		)
		self.Remove_GPU_Buffer(self._RECTANGLE_MESH_FILTER)
		#################################################


		#_______________________TEXTURE________________
		self.__PINK_PUNK_TEXTURE = Texture(form = self , path="engene/assetEngene/pink_Punk.bmp")
		self._FONT_TEXTURE = Texture(form = self , path="engene/assetEngene/font.png")
		self.Remove_GPU_Buffer(self.__PINK_PUNK_TEXTURE)
		self.Remove_GPU_Buffer(self._FONT_TEXTURE)
		###############################################
		print("\n\n\n")

		self.keys = pg.key.get_pressed()
		self.mousePos : vec2i = vec2i()

		self.Exist : bool = True

	def Remove_GPU_Buffer(self, __value : MeshFilter | Shader | MeshRender | Texture | Rectangle) -> None:
		try:
			if(isinstance(__value, MeshFilter)):
				self.MeshFilters.remove(__value)
			elif(isinstance(__value, Shader)):
				self.ShaderBuffer.remove(__value)
			elif(isinstance(__value, MeshRender)):
				self.MeshRenders.remove(__value)
			elif(isinstance(__value, Texture)):
				self.Textures.remove(__value)
		except Exception as err:print(err)

	def ClearMemory(self) -> None:
		arr = self.MeshFilters[:]
		for i in arr: i.Del()
		arr = self.ShaderBuffer[:]
		for i in arr: i.Del()
		arr = self.MeshRenders[:]
		for i in arr: i.Del()
		arr = self.Textures[:]
		for i in arr: i.Del()

	def Exit(self) -> None:
		print("\n\n\n")
		self._ERROR_SHADER.Del
		self._FONT_SHADER.Del
		self._RECTANGLE_MESH_FILTER.Del
		self.__PINK_PUNK_TEXTURE.Del
		self._FONT_TEXTURE.Del
		print("\n\n\n")
		self.ClearMemory()
		self.Exist=False
		pg.quit()

	def run(self) -> None:
		self.keys = pg.key.get_pressed()

		#pg.display.set_caption(f'{self.title} {self.physics.fps:.0f}')
		self.physics.Update()

		pg.display.flip()

		[self.Exit() for i in pg.event.get() if i.type==pg.QUIT]


	def get_posMouse(self) -> vec2i:
		x,y = pg.mouse.get_pos()-self.Half_size.arr
		if(
			(-(self.Half_size.x-1)<x<(self.Half_size.x-1))
			and
			(-(self.Half_size.y-1)<y<(self.Half_size.y-1))
		):
			self.mousePos.x = x
			self.mousePos.y = y
		else:
			self.mousePos*=0
		del x, y
		return self.mousePos


from threading import Thread

class Loader:
	def __init__(self) -> None:

		self.__WHETHER_LOAD_MESH : bool = False
		self.__ListOfLoadedMeshFilter : List[bool] = []
		self.__countOfLoadedMeshFilter : int = 0
		self.__BUFFER_OF_MESH : Tuple[
			Tuple[
				Tuple['MeshFilter',str,int]
			],
			Dict[str,List[Mesh]]
		] = None



	def ThreadLoadMesh(self, name : str, mod : int) -> None:
		self.__BUFFER_OF_MESH[1][name] = Get_Model(name,"All" if(mod==-1) else "Fragment")

	def LoadMeshes(self,
		data :
		Tuple[
			Tuple['MeshFilter',str,int]
		]) -> None:


		self.__BUFFER_OF_MESH = (data,{})

		threads = []

		for value in data:
			self.__ListOfLoadedMeshFilter.append(False)
			thread = Thread(target=self.ThreadLoadMesh, args=(value[1],value[2]))
			thread.start()
			threads.append(thread)
		self.__countOfLoadedMeshFilter = len(self.__ListOfLoadedMeshFilter)
		self.__WHETHER_LOAD_MESH = True

	def MeshesHasLoaded(self) -> bool:
		if(self.__WHETHER_LOAD_MESH):
			if(self.__BUFFER_OF_MESH):
				for index, i in enumerate(self.__BUFFER_OF_MESH[0]):
					if(not self.__ListOfLoadedMeshFilter[index] and (i[1] in self.__BUFFER_OF_MESH[1])):
						model = self.__BUFFER_OF_MESH[1][i[1]]
						#if(isinstance(model , Mesh)): model.baseName = i[1]
						i[0].LoadMesh(
							model if(isinstance(model , (Mesh,int))) else model[i[2]]
						)
						self.__countOfLoadedMeshFilter-=1
						self.__ListOfLoadedMeshFilter[index] = True
						del model
			if(self.__countOfLoadedMeshFilter<=0): self.__WHETHER_LOAD_MESH = False
		return self.__WHETHER_LOAD_MESH

	def ClearMeshLoadData(self) -> None:
		self.__WHETHER_LOAD_MESH = False
		self.__ListOfLoadedMeshFilter.clear()
		self.__countOfLoadedMeshFilter = 0
		self.__BUFFER_OF_MESH = None
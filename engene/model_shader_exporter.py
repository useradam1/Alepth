from engene.MathF import *
from OpenGL.GL import *
from OpenGL.GLU import *
from os import path as PathOs, remove as DeleteFile
from tqdm import tqdm
from PIL import Image
from pickle import load as PickleLoad, dump as PickleDump
from io import BufferedReader, BufferedWriter



def tryGet_cache(filePath : str, mod : str = "") -> Tuple[Union[BufferedReader,BufferedWriter],bool]:
	basename = PathOs.basename(filePath)
	try:
		file_path = f'engene/Buffer/{basename}+{mod}.vpk'
		if(PathOs.getatime(file_path) < PathOs.getatime(filePath)):
			file_obj = open(file_path, 'wb')
			del file_path
			return (file_obj,False)		
		else:
			file_obj = open(file_path, 'rb')
			del file_path
			return (file_obj,True)
	except FileNotFoundError:
		return (open(f'engene/Buffer/{basename}+{mod}.vpk', 'wb'),False)



def LoadTextureData(filePath : str) -> Tuple[ndarray[uint8],int,int]:
	fileBuffer=tryGet_cache(filePath)
	if(fileBuffer[1]):
		data=PickleLoad(fileBuffer[0])
		fileBuffer[0].close()
		del fileBuffer
		return data
	else:
		image = Image.open(filePath).convert('RGBA')
		image_data = array(list(image.getdata()), uint8)
		width, height = image.size
		image.close()
		image_data = image_data.reshape(height, width, -1)[::-1,:,:]
		image_data = image_data.reshape(-1, image_data.shape[-1])
		PickleDump((image_data, width, height),fileBuffer[0])
		fileBuffer[0].close()
		del image, fileBuffer
		return (image_data, width, height)



def extract_Shader(PathToShaders : Tuple[str]):
	try:

		shaders=[]

		for PathToShader in PathToShaders:
			shaders.append(LS(PathToShader))

		prog = glCreateProgram()
		for s in shaders:
			if s!=0:
				glAttachShader(prog,s)
			else:
				for s in shaders:
					glDeleteShader(s)
				return 0
		glLinkProgram(prog)

		#err check
		ok=glGetProgramiv(prog,GL_LINK_STATUS)
		if(not ok):
			logg=glGetProgramInfoLog(prog)
			print('!!!!!!!!!!!!!!')
			print('error link')
			print(logg)
			print('!!!!!!!!!!!!!!')
			for s in shaders:
				glDeleteShader(s)
			return 0
		#--------

		for s in shaders:
			glDeleteShader(s)

		del shaders, PathToShaders, PathToShader, ok

		return prog
	except Exception as err:
		print(err)
		return 0



def LS(PathToShader:str):
	
	extension = PathToShader.split(".")[-1]

	ShaderType = 0
	text : bytes = 0

	if(extension=='frag'):ShaderType=GL_FRAGMENT_SHADER
	elif(extension=='vert'):ShaderType=GL_VERTEX_SHADER
	else:
		print('!!!!!!!!!!!!!!')
		print('error type file')
		print(PathToShader)
		print('!!!!!!!!!!!!!!')
		return 0

	with open(PathToShader, 'rb') as f:
		text = f.read()
	f.close()

	shader=glCreateShader(ShaderType)
	glShaderSource(shader,text)
	glCompileShader(shader)

	#err check
	ok=glGetShaderiv(shader,GL_COMPILE_STATUS)
	if(not ok):
		logg=glGetShaderInfoLog(shader)
		print('!!!!!!!!!!!!!!')
		print('error compile')
		print(PathToShader)
		print(logg)
		print('!!!!!!!!!!!!!!')
		return 0
	#--------

	del extension, PathToShader, ShaderType, text, ok

	return shader



def NormalPoligon(vertices : Tuple[ndarray[float],ndarray[float],ndarray[float]]) -> ndarray[float]:
	p1, p2, p3 = vertices
	v1 = p2 - p1
	v2 = p3 - p1
	del p1, p2, p3
	return cross(v1, v2)

class Mesh:
	def __init__(self, 
	    	baseName : str, 
			Vertices : List[ndarray[float]], 
			Uvs : List[ndarray[float]], 
			Normals : List[ndarray[float]], 
			Faces : List[
						Dict[
							Literal["v","vt","vn"],
							Tuple[int]
						]]
		) -> None:

		self.baseName : str = baseName
		self.Vertices : ndarray[float32] = Vertices
		self.Uvs : ndarray[float32] = Uvs
		self.Normals : ndarray[float32] = Normals
		self.Faces : ndarray[int32] = Faces
	
	@property
	def triangulation(self) -> 'Mesh':
		V : List[ndarray[float]] = []
		VT : List[ndarray[float]] = []
		VN : List[ndarray[float]] = []

		iterator : int = 0

		F : List[ndarray[int]] = []

		for face in tqdm(self.Faces, desc=f"{self.baseName} = Triangulate"):
			count : int = len(face['v'])

			if ( count == 3 ):

				for j in face['v']:
					V.append(self.Vertices[j])

				for j in face['vt']:
					VT.append(self.Uvs[j])

				for j in face['vn']:
					VN.append(self.Normals[j])

				F.append(array((iterator,iterator+1,iterator+2),dtype=int))
				iterator+=3

			elif ( count == 4 ):

				if(len(face['v'])>=3 and len(self.Vertices) >= 3):
					for j in range(3):
						V.append(self.Vertices[face['v'][j]])
					V.append(self.Vertices[face['v'][3]])
					V.append(self.Vertices[face['v'][0]])
					V.append(self.Vertices[face['v'][2]])

				if(len(face['vt'])>=3 and len(self.Uvs) >= 3):
					for j in range(3):
						VT.append(self.Uvs[face['vt'][j]])
					VT.append(self.Uvs[face['vt'][3]])
					VT.append(self.Uvs[face['vt'][0]])
					VT.append(self.Uvs[face['vt'][2]])

				if(len(face['vn'])>=3 and len(self.Normals) >= 3):
					for j in range(3):
						VN.append(self.Normals[face['vn'][j]])
					VN.append(self.Normals[face['vn'][3]])
					VN.append(self.Normals[face['vn'][0]])
					VN.append(self.Normals[face['vn'][2]])

				F.append(array((iterator,iterator+1,iterator+2),dtype=int))
				F.append(array((iterator+3,iterator+4,iterator+5),dtype=int))
				iterator+=6
		
		iterator = len(V)
		if(len(VN)<iterator):
			VN.clear()
			for face in tqdm(range(0,iterator,3), desc=f"{self.baseName} = CalculateNormals"):
				n = NormalPoligon((V[face],V[face+1],V[face+2]))
				VN.append(n)
				VN.append(n)
				VN.append(n)

		self.Vertices = array([(i[0],i[1],i[2]) for i in tqdm(V, desc=f"{self.baseName} = Decode vertex")], dtype=float32)
		self.Uvs = array([(i[0],i[1]) for i in tqdm(VT, desc=f"{self.baseName} = Decode uvs")], dtype=float32)
		self.Normals = array([(i[0],i[1],i[2]) for i in tqdm(VN, desc=f"{self.baseName} = Decode normals")], dtype=float32)
		self.Faces = array([(i[0],i[1],i[2]) for i in tqdm(F, desc=f"{self.baseName} = Decode faces")], dtype=int32)

		del V, VT, VN, iterator, F

		return self
	
	@property
	def Del(self) -> None:
		print(f'deleted Mesh {self.baseName}')
		del self.baseName, self.Vertices, self.Uvs, self.Normals, self.Faces

ERROR_MODEL : Mesh = 0 

def Get_Model(filePath : str, mod : Literal["All","Fragment"]) -> List[Mesh]:
	baseName : str = PathOs.basename(filePath)
	fileBuffer=tryGet_cache(filePath,mod)
	try:
		if(fileBuffer[1]):
			data=PickleLoad(fileBuffer[0])
			fileBuffer[0].close()
			del fileBuffer
			return data
		else:
			meshes: List[Mesh] = []
			elements : List[str] = []
			V : List[ndarray[float]] = []
			VT : List[ndarray[float]] = []
			VN : List[ndarray[float]] = []
			F : List[
				Dict[
					Literal["v","vt","vn"],
					Tuple[int]
				]] = []

			with open(filePath, 'r') as file:
				for line in tqdm(file, desc=f"{filePath} = Reading"):
					elements = line.split()
					if not elements:
						continue
					if elements[0] == 'v':
						V.append(array(elements[1:4], dtype=float)*array([-1,1,1], dtype=float))
					elif elements[0] == 'vt':
						VT.append(array(elements[1:3], dtype=float))
					elif elements[0] == 'vn':
						VN.append(array(elements[1:4], dtype=float)*array([-1,1,1], dtype=float))
					elif elements[0] == 'f':
						F.append( 
							{
								'v': tuple(int(pol_.split('/')[0]) - 1 for pol_ in elements[1:]),
								'vt': tuple(int(pol_.split('/')[1]) - 1 for pol_ in elements[1:] if len(pol_.split('/')) > 1),
								'vn': tuple(int(pol_.split('/')[2]) - 1 for pol_ in elements[1:] if len(pol_.split('/')) > 2),
							}
						)
					
					elif (elements[0] == 'o' and mod=="Fragment"):
						# Create a new mesh when encountering a new group
						try:
							if V:
								meshes.append(Mesh(f'{baseName} + {elements[:]}', V.copy(), VT.copy(), VN.copy(), F.copy()))
							# Clear the current data for the new group
							#V.clear()
							#VT.clear()
							#VN.clear()
							F.clear()
						except Exception as err: print(f'{baseName} + {elements[:]} == {err}')

				# Add the last mesh after the loop ends (if any)
				if V:
					meshes.append(Mesh(baseName, V.copy(), VT.copy(), VN.copy(), F.copy()))

			for i in meshes:
				i.triangulation

			del V, VT, VN, F, baseName, elements

			PickleDump(meshes,fileBuffer[0])
			fileBuffer[0].close()
			del fileBuffer
			return meshes

	except Exception as err:
		fileBuffer[0].close()
		del fileBuffer
		DeleteFile(f'engene/Buffer/{baseName}+{mod}.vpk')
		print(f"Load Error {filePath} ===== {err}")
		return ERROR_MODEL

ERROR_MODEL = Get_Model('engene/assetEngene/__ERROR__.obj',"All")[0]
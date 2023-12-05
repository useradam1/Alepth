from engene.MathF import *

class Rotation(mat3f):
	def __init__(self) -> None:
		super().__init__()
		self._cache : mat3f = mat3f()

	def copy(self) -> 'Rotation':
		return copy.deepcopy(self)

	def R(self, axis : Tuple[float,float,float], angle : float) -> 'Rotation':

		# Получаем компоненты оси вращения
		x, y, z = axis

		# Вычисляем тригонометрические значения угла
		Adeg = radians(-angle)
		cos_angle = cos(Adeg)
		sin_angle = sin(Adeg)
		one_minus_cos = 1 - cos_angle

		# Строим матрицу вращения
		self.m=dot(self.m,array((
			(cos_angle + x*x*one_minus_cos	,	x*y*one_minus_cos - z*sin_angle		,	x*z*one_minus_cos + y*sin_angle),

			(y*x*one_minus_cos + z*sin_angle	,	 cos_angle + y*y*one_minus_cos	,	y*z*one_minus_cos - x*sin_angle),
			
			(z*x*one_minus_cos - y*sin_angle	,	 z*y*one_minus_cos + x*sin_angle	,	 cos_angle + z*z*one_minus_cos)
		), dtype=float))
		return self

	def Gx(self, angle : float) -> 'Rotation':
		return self.R( (1.0 , 0.0 , 0.0) , angle)

	def Gy(self, angle : float) -> 'Rotation':
		return self.R( (0.0 , 1.0 , 0.0) , angle)

	def Gz(self, angle : float) -> 'Rotation':
		return self.R( (0.0 , 0.0 , 1.0) , angle)

	def Lx(self, angle : float) -> 'Rotation':
		return self.R( self.i.normalize.arr , angle)

	def Ly(self, angle : float) -> 'Rotation':
		return self.R( self.j.normalize.arr , angle)

	def Lz(self, angle : float) -> 'Rotation':
		return self.R( self.k.normalize.arr , angle)
	
	@property
	def Push(self) -> 'Rotation':
		self._cache.m=copy.deepcopy(self.m)
		return self
	
	@property
	def Pop(self) -> 'Rotation':
		self.m=copy.deepcopy(self._cache.m)
		return self



class Transform:
	def __init__(self,
		pos : vec3f = vec3f(0.0 , 0.0 , 0.0),
		sca : vec3f = vec3f(1.0 , 1.0 , 1.0),
		rot : Rotation = Rotation()
	) -> None:
		self.position : vec3f = pos
		self.scale : vec3f = sca
		self.rotation : Rotation = rot

	def copy(self) -> 'Transform':
		return Transform(
			self.position.copy(),
			self.scale.copy(),
			self.rotation.copy())

	@property
	def right(self) -> vec3f:
		return self.rotation.i
	@property
	def up(self) -> vec3f:
		return self.rotation.j
	@property
	def forward(self) -> vec3f:
		return self.rotation.k

	def Move_right(self, __value : float) -> None:
		self.position+=self.right*__value
	def Move_up(self, __value : float) -> None:
		self.position+=self.up*__value
	def Move_forward(self, __value : float) -> None:
		self.position+=self.forward*__value



class GameObjectInterface:
	def __init__(self, _gameObject:'GameObject') -> None:
		self.gameObject:'GameObject' = _gameObject
		self.DeleateMethod = None

	def Deleate(self) -> None:
		self.DeleateMethod()

class GameObject:
	def __init__(self,
			transform : Transform,
			parent : 'GameObject' = None,
			attributes : Dict[str,GameObjectInterface] = {}
		) -> None:

		self.L_transform : Transform = transform
		self.parent : GameObject = parent
		self.attributes : Dict[str,GameObjectInterface] = attributes

		for obj in self.attributes.values():
			obj.gameObject = self

		self.__t : Transform = Transform().copy()
		self.__obsolete : List[Transform] = [
			Transform().copy(),
			Transform().copy()
		]

	def add_attribute(self, __name : str, __value : GameObjectInterface) -> None:
		__value.gameObject = self
		self.attributes[__name] = __value

	def remove_attribute(self, __name : str) -> None:
		self.attributes.get(__name).gameObject = GameObject(Transform.copy())
		self.attributes.pop(__name)

	def Del(self) -> None:
		for i in self.attributes.values():
			try:
				i.Deleate()
			except Exception as err: print(err)

	@property
	def transform(self) -> Transform:
		if(self.parent == None):
			return self.L_transform
		else:
			if(
				self.__obsolete[0].position != self.L_transform.position or
				self.__obsolete[1].position != self.parent.transform.position or
				self.__obsolete[0].rotation != self.L_transform.rotation or
				self.__obsolete[1].rotation != self.parent.transform.rotation
			):
				self.__obsolete[0].position = self.L_transform.position.xyz
				self.__obsolete[1].position = self.parent.transform.position.xyz
				self.__t.position = self.parent.transform.position + (self.parent.transform.rotation.inv_get * (self.parent.transform.scale * self.L_transform.position))
			if(
				self.__obsolete[0].scale != self.L_transform.scale or
				self.__obsolete[1].scale != self.parent.transform.scale
			):
				self.__obsolete[0].scale = self.L_transform.scale.xyz
				self.__obsolete[1].scale = self.parent.transform.scale.xyz
				self.__t.scale = self.parent.transform.scale * self.L_transform.scale
			if(
				self.__obsolete[0].rotation != self.L_transform.rotation or
				self.__obsolete[1].rotation != self.parent.transform.rotation
			):
				self.__obsolete[0].rotation.m = self.L_transform.rotation.m.copy()
				self.__obsolete[1].rotation.m = self.parent.transform.rotation.m.copy()
				self.__t.rotation.m = (self.parent.transform.rotation.inv_get * self.L_transform.rotation.inv_get).inv_get_nparray

			return self.__t
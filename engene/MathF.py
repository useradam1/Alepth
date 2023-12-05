from typing import Union, List, Tuple, Dict, Literal
from numpy import array, ndarray, dot, cross, inf, array_equal, trace, transpose, eye, ones, float32, int32, uint8, sin, cos, radians, intc, uintc, round
from numpy.linalg import inv, det, matrix_power, matrix_rank, norm
import copy

class vec2f:
	def __init__(self,
		x:Union[float, int, 'vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i']=0.0,
		y:float=0.0) -> None:
		if(isinstance(x, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i))):
			self._x:float=float(x._x)
			self._y:float=float(x._y)
		else:
			self._x:float=float(x)
			self._y:float=float(y)
		self.__obsolete : bool = False
		self.__npArr : ndarray[float] = array([self._x,self._y], dtype=float)
		self.__obsolete_norm : bool = True
		self.__normV : vec2f = 0

	def __str__(self) -> str:
		return f"({self._x:.1f} , {self._y:.1f})"
	
	def __repr__(self) -> str:
		return f"({self._x} , {self._y})"

	def copy(self) -> 'vec2f':
		return copy.deepcopy(self)

	@property
	def x(self) -> float:
		return self._x

	@x.setter
	def x(self, __value : float) -> None:
		self._x = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def y(self) -> float:
		return self._y

	@y.setter
	def y(self, __value : float) -> None:
		self._y = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property 
	def xy(self) -> 'vec2f': return vec2f(self._x,self._y)
	@property
	def yx(self) -> 'vec2f': return vec2f(self._y,self._x)


	def __eq__(self, __value : Union['vec2f', 'vec2i', float, int]) -> bool:

		if isinstance(__value, (vec2f,)):
			return (self._x==__value._x and 
					self._y==__value._y)

		elif isinstance(__value, (vec2i,)):
			return (self._x==float(__value._x) and 
					self._y==float(__value._y))

		elif isinstance(__value, (float,)):
			return (self._x==__value and 
					self._y==__value)

		elif isinstance(__value, (int,)):
			return (self._x==float(__value) and 
					self._y==float(__value))

		#raise TypeError("Unsupported operand type for ==: 'vec2f and '{}'".format(type(__value)))
	def __ne__(self, __value : Union['vec2f', 'vec2i', float, int]) -> bool:
		return not self.__eq__(__value)



	def __pow__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':

		if isinstance(__value, (float, int)):
			return vec2f(self._x ** __value, self._y ** __value)

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec2f(self._x ** __value._x, self._y ** __value._y)

		#raise TypeError("Unsupported operand type for +: 'vec2f' and '{}'".format(type(__value)))
	def __ipow__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x **= __value
			self._y **= __value
			return self

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x **= __value._x
			self._y **= __value._y
			return self

		#raise TypeError("Unsupported operand type for +: 'vec2f' and '{}'".format(type(__value)))



	def __add__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':

		if isinstance(__value, (float, int)):
			return vec2f(self._x + __value, self._y + __value)

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec2f(self._x + __value._x, self._y + __value._y)

		#raise TypeError("Unsupported operand type for +: 'vec2f' and '{}'".format(type(__value)))
	def __iadd__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x += __value
			self._y += __value
			return self

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x += __value._x
			self._y += __value._y
			return self

		#raise TypeError("Unsupported operand type for +: 'vec2f' and '{}'".format(type(__value)))



	def __sub__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':

		if isinstance(__value, (float, int)):
			return vec2f(self._x - __value, self._y - __value)

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec2f(self._x - __value._x, self._y - __value._y)

		#raise TypeError("Unsupported operand type for -: 'vec2f' and '{}'".format(type(__value)))
	def __isub__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x -= __value
			self._y -= __value
			return self

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x -= __value._x
			self._y -= __value._y
			return self

		#raise TypeError("Unsupported operand type for -: 'vec2f' and '{}'".format(type(__value)))



	def __mul__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':

		if isinstance(__value, (float, int)):
			return vec2f(self._x * __value, self._y * __value)

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec2f(self._x * __value._x, self._y * __value._y)

		#raise TypeError("Unsupported operand type for *: 'vec2f' and '{}'".format(type(__value)))
	def __imul__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x *= __value
			self._y *= __value
			return self

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x *= __value._x
			self._y *= __value._y
			return self

		#raise TypeError("Unsupported operand type for *: 'vec2f' and '{}'".format(type(__value)))



	def __truediv__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':

		if isinstance(__value, (float, int)):
			if(__value==0): 
				return vec2f(
					(inf if(self._x>=0) else -inf),
					(inf if(self._y>=0) else -inf)
				)
			return vec2f(self._x / __value, self._y / __value)

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec2f(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			)

		#raise TypeError("Unsupported operand type for /: 'vec2f' and '{}'".format(type(__value)))
	def __itruediv__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec2f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			if(__value==0): 
				self._x = (inf if(self._x>=0) else -inf)
				self._y = (inf if(self._y>=0) else -inf)
				return self
			self._x /= __value
			self._y /= __value
			return self

		#if isinstance(__value, (vec2f, vec2i, vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x = ((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = ((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			return self

		#raise TypeError("Unsupported operand type for /: 'vec2f' and '{}'".format(type(__value)))



	@property
	def magnitude(self) -> float:
		return (self._x*self._x + self._y*self._y) ** 0.5

	@property
	def normalize(self) -> 'vec2f':
		if(self.__obsolete_norm):
			self.__obsolete_norm = False
			self.__normV = self/self.magnitude
			return self.__normV
		else: return self.__normV

	@property
	def arr(self) -> ndarray[float]:
		if(self.__obsolete):
			self.__npArr[0]=self._x
			self.__npArr[1]=self._y
			self.__obsolete = False
		return self.__npArr


####################################################################################################################################################


class vec2i:
	def __init__(self,
		x:Union[int, float, 'vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f']=0,
		y:int=0) -> None:
		if(isinstance(x, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f))):
			self._x:int=int(x._x)
			self._y:int=int(x._y)
		else:
			self._x:int=int(x)
			self._y:int=int(y)
		self.__obsolete : bool = False
		self.__npArr : ndarray[int] = array([self._x,self._y], dtype=int)
		self.__obsolete_norm : bool = True
		self.__normV : vec2i = 0

	def __str__(self) -> str:
		return f"({self._x} , {self._y})"
	
	def __repr__(self) -> str:
		return f"({self._x} , {self._y})"

	def copy(self) -> 'vec2i':
		return copy.deepcopy(self)

	@property
	def x(self) -> int:
		return self._x

	@x.setter
	def x(self, __value : int) -> None:
		self._x = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def y(self) -> int:
		return self._y

	@y.setter
	def y(self, __value : int) -> None:
		self._y = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def xy(self) -> 'vec2i': return vec2i(self._x,self._y)
	@property
	def yx(self) -> 'vec2i': return vec2i(self._y,self._x)


	def __eq__(self, __value : Union['vec2i', int]) -> bool:

		if isinstance(__value, (vec2i,)):
			return (self._x==__value._x and 
					self._y==__value._y)

		elif isinstance(__value, (int,)):
			return (self._x==__value and 
					self._y==__value)

		#raise TypeError("Unsupported operand type for ==: 'vec2i and '{}'".format(type(__value)))
	def __ne__(self, __value : Union['vec2i', int]) -> bool:
		return not self.__eq__(__value)



	def __pow__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':
		
		if isinstance(__value, (int, float)):
			return vec2i(self._x ** __value, self._y ** __value)

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec2i(self._x ** __value._x, self._y ** __value._y)

		#raise TypeError("Unsupported operand type for +: 'vec2i' and '{}'".format(type(__value)))
	def __ipow__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':
		self.__obsolete = True
		self.__obsolete_norm = True
		
		if isinstance(__value, (int, float)):
			self._x **= int(__value)
			self._y **= int(__value)
			return self

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x **= int(__value._x)
			self._y **= int(__value._y)
			return self

		#raise TypeError("Unsupported operand type for +: 'vec2i' and '{}'".format(type(__value)))



	def __add__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':
		
		if isinstance(__value, (int, float)):
			return vec2i(self._x + __value, self._y + __value)

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec2i(self._x + __value._x, self._y + __value._y)

		#raise TypeError("Unsupported operand type for +: 'vec2i' and '{}'".format(type(__value)))
	def __iadd__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':
		self.__obsolete = True
		self.__obsolete_norm = True
		
		if isinstance(__value, (int, float)):
			self._x += int(__value)
			self._y += int(__value)
			return self

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x += int(__value._x)
			self._y += int(__value._y)
			return self

		#raise TypeError("Unsupported operand type for +: 'vec2i' and '{}'".format(type(__value)))



	def __sub__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':

		if isinstance(__value, (int, float)):
			return vec2i(self._x - __value, self._y - __value)

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec2i(self._x - __value._x, self._y - __value._y)

		#raise TypeError("Unsupported operand type for -: 'vec2i' and '{}'".format(type(__value)))
	def __isub__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x -= int(__value)
			self._y -= int(__value)
			return self

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x -= int(__value._x)
			self._y -= int(__value._y)
			return self

		#raise TypeError("Unsupported operand type for -: 'vec2i' and '{}'".format(type(__value)))



	def __mul__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':

		if isinstance(__value, (int, float)):
			return vec2i(self._x * __value, self._y * __value)

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec2i(self._x * __value._x, self._y * __value._y)

		#raise TypeError("Unsupported operand type for *: 'vec2i' and '{}'".format(type(__value)))
	def __imul__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x *= int(__value)
			self._y *= int(__value)
			return self

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x *= int(__value._x)
			self._y *= int(__value._y)
			return self

		#raise TypeError("Unsupported operand type for *: 'vec2i' and '{}'".format(type(__value)))



	def __truediv__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':

		if isinstance(__value, (int, float)):
			if(__value==0): 
				return vec2i(
					(inf if(self._x>=0) else -inf),
					(inf if(self._y>=0) else -inf)
				)
			return vec2i(self._x / __value, self._y / __value)

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec2i(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			)

		#raise TypeError("Unsupported operand type for /: 'vec2i' and '{}'".format(type(__value)))
	def __itruediv__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec2i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			if(__value==0): 
				self._x = int(inf if(self._x>=0) else -inf)
				self._y = int(inf if(self._y>=0) else -inf)
				return self
			self._x = int(self._x / __value)
			self._y = int(self._y / __value)
			return self

		#if isinstance(__value, (vec2i, vec2f, vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x = int((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = int((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			return self

		#raise TypeError("Unsupported operand type for /: 'vec2i' and '{}'".format(type(__value)))



	@property
	def magnitude(self) -> float:
		return (self._x*self._x + self._y*self._y) ** 0.5

	@property
	def normalize(self) -> 'vec2i':
		if(self.__obsolete_norm):
			self.__obsolete_norm = False
			self.__normV = self/self.magnitude
			return self.__normV
		else: return self.__normV

	@property
	def arr(self) -> ndarray[int]:
		if(self.__obsolete):
			self.__npArr[0] = self._x
			self.__npArr[1] = self._y
			self.__obsolete = False
		return self.__npArr



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################



class vec3f:
	def __init__(self,
		x:Union[float, int, 'vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i']=0.0,
		y:Union[float, int, 'vec2f', 'vec2i']=0.0,
		z:float=0.0) -> None:
		if(isinstance(x, (vec2f, vec2i))):
			self._x:float=float(x._x)
			self._y:float=float(x._y)
			self._z:float=float(y)
		elif(isinstance(y, (vec2f, vec2i))):
			self._x:float=float(x)
			self._y:float=float(y._x)
			self._z:float=float(y._y)
		elif(isinstance(x, (vec3f, vec3i, vec4f, vec4i))):
			self._x:float=float(x._x)
			self._y:float=float(x._y)
			self._z:float=float(x._z)
		else:
			self._x:float=float(x)
			self._y:float=float(y)
			self._z:float=float(z)
		self.__obsolete : bool = False
		self.__npArr : ndarray[float] = array([self._x,self._y,self._z], dtype=float)
		self.__obsolete_norm : bool = True
		self.__normV : vec3f = 0

	def __str__(self) -> str:
		return f"({self._x:.1f} , {self._y:.1f} , {self._z:.1f})"
	
	def __repr__(self) -> str:
		return f"({self._x} , {self._y} , {self._z})"

	def copy(self) -> 'vec3f':
		return copy.deepcopy(self)

	@property
	def x(self) -> float:
		return self._x

	@x.setter
	def x(self, __value : float) -> None:
		self._x = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def y(self) -> float:
		return self._y

	@y.setter
	def y(self, __value : float) -> None:
		self._y = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def z(self) -> float:
		return self._z

	@z.setter
	def z(self, __value : float) -> None:
		self._z = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def xy(self) -> 'vec2f': return vec2f(self._x, self._y)
	@property
	def xz(self) -> 'vec2f': return vec2f(self._x, self._z)
	@property
	def yx(self) -> 'vec2f': return vec2f(self._y, self._x)
	@property
	def yz(self) -> 'vec2f': return vec2f(self._y, self._z)
	@property
	def zx(self) -> 'vec2f': return vec2f(self._z, self._x)
	@property
	def zy(self) -> 'vec2f': return vec2f(self._z, self._y)
	@property
	def xyz(self) -> 'vec3f': return vec3f(self._x, self._y, self._z)
	@property
	def yxz(self) -> 'vec3f': return vec3f(self._y, self._x, self._z)
	@property
	def xzy(self) -> 'vec3f': return vec3f(self._x, self._z, self._y)
	@property
	def zxy(self) -> 'vec3f': return vec3f(self._z, self._x, self._y)
	@property
	def yzx(self) -> 'vec3f': return vec3f(self._y, self._z, self._x)
	@property
	def zyx(self) -> 'vec3f': return vec3f(self._z, self._y, self._x)


	def __eq__(self, __value : Union['vec3f', 'vec3i', float, int]) -> bool:

		if isinstance(__value, (vec3f,)):
			return (self._x==__value._x and 
					self._y==__value._y and 
					self._z==__value._z)

		elif isinstance(__value, (vec3i,)):
			return (self._x==float(__value._x) and 
					self._y==float(__value._y) and 
					self._z==float(__value._z))

		elif isinstance(__value, (float,)):
			return (self._x==__value and 
					self._y==__value and 
					self._z==__value)

		elif isinstance(__value, (int,)):
			return (self._x==float(__value) and 
					self._y==float(__value) and 
					self._z==float(__value))

		#raise TypeError("Unsupported operand type for ==: 'vec3f and '{}'".format(type(__value)))
	def __ne__(self, __value : Union['vec3f', 'vec3i', float, int]) -> bool:
		return not self.__eq__(__value)



	def __pow__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':

		if isinstance(__value, (float, int)):
			return vec3f(self._x ** __value, self._y ** __value, self._z ** __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec3f(self._x ** __value._x, self._y ** __value._y, self._z)

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec3f(self._x ** __value._x, self._y ** __value._y, self._z ** __value._z)

		#raise TypeError("Unsupported operand type for +: 'vec3f' and '{}'".format(type(__value)))
	def __ipow__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x **= __value
			self._y **= __value
			self._z **= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x **= __value._x
			self._y **= __value._y
			return self

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x **= __value._x
			self._y **= __value._y
			self._z **= __value._z
			return self

		#raise TypeError("Unsupported operand type for +: 'vec3f' and '{}'".format(type(__value)))



	def __add__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':

		if isinstance(__value, (float, int)):
			return vec3f(self._x + __value, self._y + __value, self._z + __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec3f(self._x + __value._x, self._y + __value._y, self._z)

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec3f(self._x + __value._x, self._y + __value._y, self._z + __value._z)

		#raise TypeError("Unsupported operand type for +: 'vec3f' and '{}'".format(type(__value)))
	def __iadd__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x += __value
			self._y += __value
			self._z += __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x += __value._x
			self._y += __value._y
			return self

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x += __value._x
			self._y += __value._y
			self._z += __value._z
			return self

		#raise TypeError("Unsupported operand type for +: 'vec3f' and '{}'".format(type(__value)))



	def __sub__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':

		if isinstance(__value, (float, int)):
			return vec3f(self._x - __value, self._y - __value, self._z - __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec3f(self._x - __value._x, self._y - __value._y, self._z)

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec3f(self._x - __value._x, self._y - __value._y, self._z - __value._z)

		#raise TypeError("Unsupported operand type for -: 'vec3f' and '{}'".format(type(__value)))
	def __isub__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x -= __value
			self._y -= __value
			self._z -= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x -= __value._x
			self._y -= __value._y
			return self

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x -= __value._x
			self._y -= __value._y
			self._z -= __value._z
			return self

		#raise TypeError("Unsupported operand type for -: 'vec3f' and '{}'".format(type(__value)))




	def __mul__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':

		if isinstance(__value, (float, int)):
			return vec3f(self._x * __value, self._y * __value, self._z * __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec3f(self._x * __value._x, self._y * __value._y, self._z)

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec3f(self._x * __value._x, self._y * __value._y, self._z * __value._z)

		#raise TypeError("Unsupported operand type for *: 'vec3f' and '{}'".format(type(__value)))
	def __imul__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x *= __value
			self._y *= __value
			self._z *= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x *= __value._x
			self._y *= __value._y
			return self

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x *= __value._x
			self._y *= __value._y
			self._z *= __value._z
			return self

		#raise TypeError("Unsupported operand type for *: 'vec3f' and '{}'".format(type(__value)))



	def __truediv__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':

		if isinstance(__value, (float, int)):
			if(__value==0): 
				return vec3f(
					(inf if(self._x>=0) else -inf),
					(inf if(self._y>=0) else -inf),
					(inf if(self._z>=0) else -inf)
				)
			return vec3f(self._x / __value, self._y / __value, self._z / __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec3f(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)), 
				self._z
			)

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			return vec3f(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)), 
				((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			)

		#raise TypeError("Unsupported operand type for /: 'vec3f' and '{}'".format(type(__value)))
	def __itruediv__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec3f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			if(__value==0): 
				self._x = (inf if(self._x>=0) else -inf)
				self._y = (inf if(self._y>=0) else -inf)
				self._z = (inf if(self._z>=0) else -inf)
				return self
			self._x /= __value
			self._y /= __value
			self._z /= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x = ((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = ((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			return self

		#elif isinstance(__value, (vec3f, vec3i, vec4f, vec4i)):
		else:
			self._x = ((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = ((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			self._z = ((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			return self

		#raise TypeError("Unsupported operand type for /: 'vec3f' and '{}'".format(type(__value)))



	@property
	def magnitude(self) -> float:
		return (self._x*self._x + self._y*self._y + self._z*self._z) ** 0.5

	@property
	def normalize(self) -> 'vec3f':
		if(self.__obsolete_norm):
			self.__obsolete_norm = False
			self.__normV = self/self.magnitude
			return self.__normV
		else: return self.__normV

	@property
	def arr(self) -> ndarray[float]:
		if(self.__obsolete):
			self.__npArr[0] = self._x
			self.__npArr[1] = self._y
			self.__npArr[2] = self._z
			self.__obsolete = False
		return self.__npArr


####################################################################################################################################################


class vec3i:
	def __init__(self,
		x:Union[int, float, 'vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f']=0,
		y:Union[int, float, 'vec2i', 'vec2f']=0,
		z:int=0) -> None:
		if(isinstance(x, (vec2i, vec2f))):
			self._x:int=int(x._x)
			self._y:int=int(x._y)
			self._z:int=int(y)
		elif(isinstance(y, (vec2i, vec2f))):
			self._x:int=int(x)
			self._y:int=int(y._x)
			self._z:int=int(y._y)
		elif(isinstance(x, (vec3i, vec3f, vec4i, vec4f))):
			self._x:int=int(x._x)
			self._y:int=int(x._y)
			self._z:int=int(x._z)
		else:
			self._x:int=int(x)
			self._y:int=int(y)
			self._z:int=int(z)
		self.__obsolete : bool = False
		self.__npArr : ndarray[int] = array([self._x,self._y,self._z], dtype=int)
		self.__obsolete_norm : bool = True
		self.__normV : vec3i = 0

	def __str__(self) -> str:
		return f"({self._x} , {self._y} , {self._z})"
	
	def __repr__(self) -> str:
		return f"({self._x} , {self._y} , {self._z})"

	def copy(self) -> 'vec3i':
		return copy.deepcopy(self)

	@property
	def x(self) -> int:
		return self._x

	@x.setter
	def x(self, __value : int) -> None:
		self._x = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def y(self) -> int:
		return self._y

	@y.setter
	def y(self, __value : int) -> None:
		self._y = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def z(self) -> int:
		return self._z

	@z.setter
	def z(self, __value : int) -> None:
		self._z = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def xy(self) -> 'vec2i': return vec2i(self._x, self._y)
	@property
	def xz(self) -> 'vec2i': return vec2i(self._x, self._z)
	@property
	def yx(self) -> 'vec2i': return vec2i(self._y, self._x)
	@property
	def yz(self) -> 'vec2i': return vec2i(self._y, self._z)
	@property
	def zx(self) -> 'vec2i': return vec2i(self._z, self._x)
	@property
	def zy(self) -> 'vec2i': return vec2i(self._z, self._y)
	@property
	def xyz(self) -> 'vec3i': return vec3i(self._x, self._y, self._z)
	@property
	def yxz(self) -> 'vec3i': return vec3i(self._y, self._x, self._z)
	@property
	def xzy(self) -> 'vec3i': return vec3i(self._x, self._z, self._y)
	@property
	def zxy(self) -> 'vec3i': return vec3i(self._z, self._x, self._y)
	@property
	def yzx(self) -> 'vec3i': return vec3i(self._y, self._z, self._x)
	@property
	def zyx(self) -> 'vec3i': return vec3i(self._z, self._y, self._x)


	def __eq__(self, __value : Union['vec3i', int]) -> bool:

		if isinstance(__value, (vec3i,)):
			return (self._x==__value._x and 
					self._y==__value._y and 
					self._z==__value._z)

		elif isinstance(__value, (int,)):
			return (self._x==__value and 
					self._y==__value and 
					self._z==__value)

		#raise TypeError("Unsupported operand type for ==: 'vec3i and '{}'".format(type(__value)))
	def __ne__(self, __value : Union['vec3i', int]) -> bool:
		return not self.__eq__(__value)



	def __pow__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':

		if isinstance(__value, (int, float)):
			return vec3i(self._x ** __value, self._y ** __value, self._z ** __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec3i(self._x ** __value._x, self._y ** __value._y, self._z)

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec3i(self._x ** __value._x, self._y ** __value._y, self._z ** __value._z)

		#raise TypeError("Unsupported operand type for +: 'vec3i' and '{}'".format(type(__value)))
	def __ipow__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x **= int(__value)
			self._y **= int(__value)
			self._z **= int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x **= int(__value._x)
			self._y **= int(__value._y)
			return self

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x **= int(__value._x)
			self._y **= int(__value._y)
			self._z **= int(__value._z)
			return self

		#raise TypeError("Unsupported operand type for +: 'vec3i' and '{}'".format(type(__value)))



	def __add__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':

		if isinstance(__value, (int, float)):
			return vec3i(self._x + __value, self._y + __value, self._z + __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec3i(self._x + __value._x, self._y + __value._y, self._z)

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec3i(self._x + __value._x, self._y + __value._y, self._z + __value._z)

		#raise TypeError("Unsupported operand type for +: 'vec3i' and '{}'".format(type(__value)))
	def __iadd__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x += int(__value)
			self._y += int(__value)
			self._z += int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x += int(__value._x)
			self._y += int(__value._y)
			return self

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x += int(__value._x)
			self._y += int(__value._y)
			self._z += int(__value._z)
			return self

		#raise TypeError("Unsupported operand type for +: 'vec3i' and '{}'".format(type(__value)))



	def __sub__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':

		if isinstance(__value, (int, float)):
			return vec3i(self._x - __value, self._y - __value, self._z - __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec3i(self._x - __value._x, self._y - __value._y, self._z)

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec3i(self._x - __value._x, self._y - __value._y, self._z - __value._z)

		#raise TypeError("Unsupported operand type for -: 'vec3i' and '{}'".format(type(__value)))
	def __isub__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x -= int(__value)
			self._y -= int(__value)
			self._z -= int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x -= int(__value._x)
			self._y -= int(__value._y)
			return self

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x -= int(__value._x)
			self._y -= int(__value._y)
			self._z -= int(__value._z)
			return self

		#raise TypeError("Unsupported operand type for -: 'vec3i' and '{}'".format(type(__value)))



	def __mul__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':

		if isinstance(__value, (int, float)):
			return vec3i(self._x * __value, self._y * __value, self._z * __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec3i(self._x * __value._x, self._y * __value._y, self._z)

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec3i(self._x * __value._x, self._y * __value._y, self._z * __value._z)

		#raise TypeError("Unsupported operand type for *: 'vec3i' and '{}'".format(type(__value)))
	def __imul__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x *= int(__value)
			self._y *= int(__value)
			self._z *= int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x *= int(__value._x)
			self._y *= int(__value._y)
			return self

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x *= int(__value._x)
			self._y *= int(__value._y)
			self._z *= int(__value._z)
			return self

		#raise TypeError("Unsupported operand type for *: 'vec3i' and '{}'".format(type(__value)))



	def __truediv__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':

		if isinstance(__value, (int, float)):
			if(__value==0): 
				return vec3i(
					(inf if(self._x>=0) else -inf),
					(inf if(self._y>=0) else -inf),
					(inf if(self._z>=0) else -inf)
				)
			return vec3i(self._x / __value, self._y / __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec3i(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)), 
				self._z
			)

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			return vec3i(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)), 
				((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			)

		#raise TypeError("Unsupported operand type for /: 'vec3i' and '{}'".format(type(__value)))
	def __itruediv__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec3i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			if(__value==0): 
				self._x = int(inf if(self._x>=0) else -inf)
				self._y = int(inf if(self._y>=0) else -inf)
				self._z = int(inf if(self._z>=0) else -inf)
				return self
			self._x = int(self._x / __value)
			self._y = int(self._y / __value)
			self._z = int(self._z / __value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x = int((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = int((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			return self

		#elif isinstance(__value, (vec3i, vec3f, vec4i, vec4f)):
		else:
			self._x = int((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = int((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			self._z = int((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			return self

		#raise TypeError("Unsupported operand type for /: 'vec3i' and '{}'".format(type(__value)))



	@property
	def magnitude(self) -> float:
		return (self._x*self._x + self._y*self._y + self._z*self._z) ** 0.5

	@property
	def normalize(self) -> 'vec3i':
		if(self.__obsolete_norm):
			self.__obsolete_norm = False
			self.__normV = self/self.magnitude
			return self.__normV
		else: return self.__normV

	@property
	def arr(self) -> ndarray[int]:
		if(self.__obsolete):
			self.__npArr[0] = self._x
			self.__npArr[1] = self._y
			self.__npArr[2] = self._z
			self.__obsolete = False
		return self.__npArr



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################



class vec4f:
	def __init__(self,
		x:Union[float, int, 'vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i']=0.0,
		y:Union[float, int, 'vec2f', 'vec2i', 'vec3f', 'vec3i']=0.0,
		z:Union[float, int, 'vec2f', 'vec2i']=0.0,
		w:float=0.0) -> None:
		if(isinstance(x,(vec2f,vec2i)) and isinstance(y,(vec2f,vec2i))):
			self._x:float=float(x._x)
			self._y:float=float(x._y)
			self._z:float=float(y._x)
			self._w:float=float(y._y)
		elif(isinstance(x,(vec2f,vec2i))):
			self._x:float=float(x._x)
			self._y:float=float(x._y)
			self._z:float=float(y)
			self._w:float=float(z)
		elif(isinstance(y,(vec2f,vec2i))):
			self._x:float=float(x)
			self._y:float=float(y._x)
			self._z:float=float(y._y)
			self._w:float=float(z)
		elif(isinstance(z,(vec2f,vec2i))):
			self._x:float=float(x)
			self._y:float=float(y)
			self._z:float=float(z._x)
			self._w:float=float(z._y)
		elif(isinstance(x,(vec3f,vec3i))):
			self._x:float=float(x._x)
			self._y:float=float(x._y)
			self._z:float=float(x._z)
			self._w:float=float(y)
		elif(isinstance(y,(vec3f,vec3i))):
			self._x:float=float(x)
			self._y:float=float(y._x)
			self._z:float=float(y._y)
			self._w:float=float(y._z)
		elif(isinstance(x,(vec4f,vec4i))):
			self._x:float=float(x._x)
			self._y:float=float(x._y)
			self._z:float=float(x._z)
			self._w:float=float(x._w)
		else:
			self._x:float=float(x)
			self._y:float=float(y)
			self._z:float=float(z)
			self._w:float=float(w)
		self.__obsolete : bool = False
		self.__npArr : ndarray[float] = array([self._x,self._y,self._z,self._w], dtype=float)
		self.__obsolete_norm : bool = True
		self.__normV : vec4f = 0

	def __str__(self) -> str:
		return f"({self._x:.1f} , {self._y:.1f} , {self._z:.1f} , {self._w:.1f})"
	
	def __repr__(self) -> str:
		return f"({self._x} , {self._y} , {self._z} , {self._w})"

	def copy(self) -> 'vec4f':
		return copy.deepcopy(self)

	@property
	def x(self) -> float:
		return self._x

	@x.setter
	def x(self, __value : float) -> None:
		self._x = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def y(self) -> float:
		return self._y

	@y.setter
	def y(self, __value : float) -> None:
		self._y = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def z(self) -> float:
		return self._z

	@z.setter
	def z(self, __value : float) -> None:
		self._z = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def w(self) -> float:
		return self._w

	@w.setter
	def w(self, __value : float) -> None:
		self._w = float(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def xy(self) -> 'vec2f': return vec2f(self._x, self._y)
	@property
	def xz(self) -> 'vec2f': return vec2f(self._x, self._z)
	@property
	def xw(self) -> 'vec2f': return vec2f(self._x, self._w)
	@property
	def yx(self) -> 'vec2f': return vec2f(self._y, self._x)
	@property
	def yz(self) -> 'vec2f': return vec2f(self._y, self._z)
	@property
	def yw(self) -> 'vec2f': return vec2f(self._y, self._w)
	@property
	def zx(self) -> 'vec2f': return vec2f(self._z, self._x)
	@property
	def zy(self) -> 'vec2f': return vec2f(self._z, self._y)
	@property
	def zw(self) -> 'vec2f': return vec2f(self._z, self._w)
	@property
	def wx(self) -> 'vec2f': return vec2f(self._w, self._x)
	@property
	def wy(self) -> 'vec2f': return vec2f(self._w, self._y)
	@property
	def wz(self) -> 'vec2f': return vec2f(self._w, self._z)
	@property
	def xyz(self) -> 'vec3f': return vec3f(self._x, self._y, self._z)
	@property
	def xyw(self) -> 'vec3f': return vec3f(self._x, self._y, self._w)
	@property
	def xzy(self) -> 'vec3f': return vec3f(self._x, self._z, self._y)
	@property
	def xzw(self) -> 'vec3f': return vec3f(self._x, self._z, self._w)
	@property
	def xwy(self) -> 'vec3f': return vec3f(self._x, self._w, self._y)
	@property
	def xwz(self) -> 'vec3f': return vec3f(self._x, self._w, self._z)
	@property
	def yxz(self) -> 'vec3f': return vec3f(self._y, self._x, self._z)
	@property
	def yxw(self) -> 'vec3f': return vec3f(self._y, self._x, self._w)
	@property
	def yzx(self) -> 'vec3f': return vec3f(self._y, self._z, self._x)
	@property
	def yzw(self) -> 'vec3f': return vec3f(self._y, self._z, self._w)
	@property
	def ywx(self) -> 'vec3f': return vec3f(self._y, self._w, self._x)
	@property
	def ywz(self) -> 'vec3f': return vec3f(self._y, self._w, self._z)
	@property
	def zxy(self) -> 'vec3f': return vec3f(self._z, self._x, self._y)
	@property
	def zxw(self) -> 'vec3f': return vec3f(self._z, self._x, self._w)
	@property
	def zyx(self) -> 'vec3f': return vec3f(self._z, self._y, self._x)
	@property
	def zyw(self) -> 'vec3f': return vec3f(self._z, self._y, self._w)
	@property
	def zwx(self) -> 'vec3f': return vec3f(self._z, self._w, self._x)
	@property
	def zwy(self) -> 'vec3f': return vec3f(self._z, self._w, self._y)
	@property
	def wxy(self) -> 'vec3f': return vec3f(self._w, self._x, self._y)
	@property
	def wxz(self) -> 'vec3f': return vec3f(self._w, self._x, self._z)
	@property
	def wyx(self) -> 'vec3f': return vec3f(self._w, self._y, self._x)
	@property
	def wyz(self) -> 'vec3f': return vec3f(self._w, self._y, self._z)
	@property
	def wzx(self) -> 'vec3f': return vec3f(self._w, self._z, self._x)
	@property
	def wzy(self) -> 'vec3f': return vec3f(self._w, self._z, self._y)
	@property
	def xyzw(self) -> 'vec4f': return vec4f(self._x, self._y, self._z, self._w)
	@property
	def xywz(self) -> 'vec4f': return vec4f(self._x, self._y, self._w, self._z)
	@property
	def xzyw(self) -> 'vec4f': return vec4f(self._x, self._z, self._y, self._w)
	@property
	def xzwy(self) -> 'vec4f': return vec4f(self._x, self._z, self._w, self._y)
	@property
	def xwyz(self) -> 'vec4f': return vec4f(self._x, self._w, self._y, self._z)
	@property
	def xwzy(self) -> 'vec4f': return vec4f(self._x, self._w, self._z, self._y)
	@property
	def yxzw(self) -> 'vec4f': return vec4f(self._y, self._x, self._z, self._w)
	@property
	def yxwz(self) -> 'vec4f': return vec4f(self._y, self._x, self._w, self._z)
	@property
	def yzxw(self) -> 'vec4f': return vec4f(self._y, self._z, self._x, self._w)
	@property
	def yzwx(self) -> 'vec4f': return vec4f(self._y, self._z, self._w, self._x)
	@property
	def ywxz(self) -> 'vec4f': return vec4f(self._y, self._w, self._x, self._z)
	@property
	def ywzx(self) -> 'vec4f': return vec4f(self._y, self._w, self._z, self._x)
	@property
	def zxyw(self) -> 'vec4f': return vec4f(self._z, self._x, self._y, self._w)
	@property
	def zxwy(self) -> 'vec4f': return vec4f(self._z, self._x, self._w, self._y)
	@property
	def zyxw(self) -> 'vec4f': return vec4f(self._z, self._y, self._x, self._w)
	@property
	def zywx(self) -> 'vec4f': return vec4f(self._z, self._y, self._w, self._x)
	@property
	def zwxy(self) -> 'vec4f': return vec4f(self._z, self._w, self._x, self._y)
	@property
	def zwyx(self) -> 'vec4f': return vec4f(self._z, self._w, self._y, self._x)
	@property
	def wxyz(self) -> 'vec4f': return vec4f(self._w, self._x, self._y, self._z)
	@property
	def wxzy(self) -> 'vec4f': return vec4f(self._w, self._x, self._z, self._y)
	@property
	def wyxz(self) -> 'vec4f': return vec4f(self._w, self._y, self._x, self._z)
	@property
	def wyzx(self) -> 'vec4f': return vec4f(self._w, self._y, self._z, self._x)
	@property
	def wzxy(self) -> 'vec4f': return vec4f(self._w, self._z, self._x, self._y)
	@property
	def wzyx(self) -> 'vec4f': return vec4f(self._w, self._z, self._y, self._x)


	def __eq__(self, __value : Union['vec4f', 'vec4i', float, int]) -> bool:

		if isinstance(__value, (vec4f,)):
			return (self._x==__value._x and 
					self._y==__value._y and 
					self._z==__value._z and 
					self._w==__value._w)

		elif isinstance(__value, (vec4i,)):
			return (self._x==float(__value._x) and 
					self._y==float(__value._y) and 
					self._z==float(__value._z) and 
					self._w==float(__value._w))

		elif isinstance(__value, (float,)):
			return (self._x==__value and 
					self._y==__value and 
					self._z==__value and 
					self._w==__value)

		elif isinstance(__value, (int,)):
			return (self._x==float(__value) and 
					self._y==float(__value) and 
					self._z==float(__value) and 
					self._w==float(__value))

		#raise TypeError("Unsupported operand type for ==: 'vec4f and '{}'".format(type(__value)))
	def __ne__(self, __value : Union['vec4f', 'vec4i', float, int]) -> bool:
		return not self.__eq__(__value)



	def __pow__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':

		if isinstance(__value, (float, int)):
			return vec4f(self._x ** __value, self._y ** __value, self._z ** __value, self._w ** __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec4f(self._x ** __value._x, self._y ** __value._y, self._z, self._w)

		elif isinstance(__value, (vec3f, vec3i)):
			return vec4f(self._x ** __value._x, self._y ** __value._y, self._z ** __value._z, self._w)

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			return vec4f(self._x ** __value._x, self._y ** __value._y, self._z ** __value._z, self._w ** __value._w)

		#raise TypeError("Unsupported operand type for +: 'vec4f' and '{}'".format(type(__value)))
	def __ipow__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x **= __value
			self._y **= __value
			self._z **= __value
			self._w **= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x **= __value._x
			self._y **= __value._y
			return self

		elif isinstance(__value, (vec3f, vec3i)):
			self._x **= __value._x
			self._y **= __value._y
			self._z **= __value._z
			return self

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			self._x **= __value._x
			self._y **= __value._y
			self._z **= __value._z
			self._w **= __value._w
			return self

		#raise TypeError("Unsupported operand type for +: 'vec4f' and '{}'".format(type(__value)))



	def __add__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':

		if isinstance(__value, (float, int)):
			return vec4f(self._x + __value, self._y + __value, self._z + __value, self._w + __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec4f(self._x + __value._x, self._y + __value._y, self._z, self._w)

		elif isinstance(__value, (vec3f, vec3i)):
			return vec4f(self._x + __value._x, self._y + __value._y, self._z + __value._z, self._w)

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			return vec4f(self._x + __value._x, self._y + __value._y, self._z + __value._z, self._w + __value._w)

		#raise TypeError("Unsupported operand type for +: 'vec4f' and '{}'".format(type(__value)))
	def __iadd__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x += __value
			self._y += __value
			self._z += __value
			self._w += __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x += __value._x
			self._y += __value._y
			return self

		elif isinstance(__value, (vec3f, vec3i)):
			self._x += __value._x
			self._y += __value._y
			self._z += __value._z
			return self

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			self._x += __value._x
			self._y += __value._y
			self._z += __value._z
			self._w += __value._w
			return self

		#raise TypeError("Unsupported operand type for +: 'vec4f' and '{}'".format(type(__value)))



	def __sub__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':

		if isinstance(__value, (float, int)):
			return vec4f(self._x - __value, self._y - __value, self._z - __value, self._w - __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec4f(self._x - __value._x, self._y - __value._y, self._z, self._w)

		elif isinstance(__value, (vec3f, vec3i)):
			return vec4f(self._x - __value._x, self._y - __value._y, self._z - __value._z, self._w)

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			return vec4f(self._x - __value._x, self._y - __value._y, self._z - __value._z, self._w - __value._w)

		#raise TypeError("Unsupported operand type for -: 'vec4f' and '{}'".format(type(__value)))
	def __isub__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x -= __value
			self._y -= __value
			self._z -= __value
			self._w -= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x -= __value._x
			self._y -= __value._y
			return self

		elif isinstance(__value, (vec3f, vec3i)):
			self._x -= __value._x
			self._y -= __value._y
			self._z -= __value._z
			return self

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			self._x -= __value._x
			self._y -= __value._y
			self._z -= __value._z
			self._w -= __value._w
			return self

		#raise TypeError("Unsupported operand type for -: 'vec4f' and '{}'".format(type(__value)))



	def __mul__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':

		if isinstance(__value, (float, int)):
			return vec4f(self._x * __value, self._y * __value, self._z * __value, self._w * __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec4f(self._x * __value._x, self._y * __value._y, self._z, self._w)

		elif isinstance(__value, (vec3f, vec3i)):
			return vec4f(self._x * __value._x, self._y * __value._y, self._z * __value._z, self._w)

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			return vec4f(self._x * __value._x, self._y * __value._y, self._z * __value._z, self._w * __value._w)

		#raise TypeError("Unsupported operand type for *: 'vec4f' and '{}'".format(type(__value)))
	def __imul__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			self._x *= __value
			self._y *= __value
			self._z *= __value
			self._w *= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x *= __value._x
			self._y *= __value._y
			return self

		elif isinstance(__value, (vec3f, vec3i)):
			self._x *= __value._x
			self._y *= __value._y
			self._z *= __value._z
			return self

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			self._x *= __value._x
			self._y *= __value._y
			self._z *= __value._z
			self._w *= __value._w
			return self

		#raise TypeError("Unsupported operand type for *: 'vec4f' and '{}'".format(type(__value)))



	def __truediv__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':

		if isinstance(__value, (float, int)):
			if(__value==0): 
				return vec4f(
					(inf if(self._x>=0) else -inf),
					(inf if(self._y>=0) else -inf),
					(inf if(self._z>=0) else -inf),
					(inf if(self._w>=0) else -inf)
				)
			return vec4f(self._x / __value, self._y / __value, self._z / __value, self._w / __value)

		elif isinstance(__value, (vec2f, vec2i)):
			return vec4f(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)), 
				self._z, 
				self._w
			)

		elif isinstance(__value, (vec3f, vec3i)):
			return vec4f(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)),
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)),
				((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf)),
				self._w
			)

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			return vec4f(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)),
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)),
				((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf)),
				((self._w / __value._w) if(__value._w!=0) else (inf if(self._w>=0) else -inf)),
			)

		#raise TypeError("Unsupported operand type for /: 'vec4f' and '{}'".format(type(__value)))
	def __itruediv__(self, __value : Union['vec2f', 'vec2i', 'vec3f', 'vec3i', 'vec4f', 'vec4i', float, int]) -> 'vec4f':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (float, int)):
			if(__value==0): 
				self._x = (inf if(self._x>=0) else -inf)
				self._y = (inf if(self._y>=0) else -inf)
				self._z = (inf if(self._z>=0) else -inf)
				self._w = (inf if(self._w>=0) else -inf)
				return self
			self._x /= __value
			self._y /= __value
			self._z /= __value
			self._w /= __value
			return self

		elif isinstance(__value, (vec2f, vec2i)):
			self._x = ((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = ((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			return self

		elif isinstance(__value, (vec3f, vec3i)):
			self._x = ((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = ((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			self._z = ((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			return self

		#elif isinstance(__value, (vec4f, vec4i)):
		else:
			self._x = ((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = ((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			self._z = ((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			self._w = ((self._w / __value._w) if(__value._w!=0) else (inf if(self._w>=0) else -inf))
			return self

		#raise TypeError("Unsupported operand type for /: 'vec4f' and '{}'".format(type(__value)))



	@property
	def magnitude(self) -> float:
		return (self._x*self._x + self._y*self._y + self._z*self._z + self._w*self._w) ** 0.5

	@property
	def normalize(self) -> 'vec4f':
		if(self.__obsolete_norm):
			self.__obsolete_norm = False
			self.__normV = self/self.magnitude
			return self.__normV
		else: return self.__normV

	@property
	def arr(self) -> ndarray[float]:
		if(self.__obsolete):
			self.__npArr[0] = self._x
			self.__npArr[1] = self._y
			self.__npArr[2] = self._z
			self.__npArr[3] = self._w
			self.__obsolete = False
		return self.__npArr



####################################################################################################################################################



class vec4i:
	def __init__(self,
		x:Union[int, float, 'vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f']=0,
		y:Union[int, float, 'vec2i', 'vec2f', 'vec3i', 'vec3f']=0,
		z:Union[int, float, 'vec2i']=0,
		w:int=0) -> None:
		if(isinstance(x,(vec2i,vec2f)) and isinstance(y,(vec2i,vec2f))):
			self._x:int=int(x._x)
			self._y:int=int(x._y)
			self._z:int=int(y._x)
			self._w:int=int(y._y)
		elif(isinstance(x,(vec2i,vec2f))):
			self._x:int=int(x._x)
			self._y:int=int(x._y)
			self._z:int=int(y)
			self._w:int=int(z)
		elif(isinstance(y,(vec2i,vec2f))):
			self._x:int=int(x)
			self._y:int=int(y._x)
			self._z:int=int(y._y)
			self._w:int=int(z)
		elif(isinstance(z,(vec2i,vec2f))):
			self._x:int=int(x)
			self._y:int=int(y)
			self._z:int=int(z._x)
			self._w:int=int(z._y)
		elif(isinstance(x,(vec3i,vec3f))):
			self._x:int=int(x._x)
			self._y:int=int(x._y)
			self._z:int=int(x._z)
			self._w:int=int(y)
		elif(isinstance(y,(vec3i,vec3f))):
			self._x:int=int(x)
			self._y:int=int(y._x)
			self._z:int=int(y._y)
			self._w:int=int(y._z)
		elif(isinstance(x,(vec4i,vec4f))):
			self._x:int=int(x._x)
			self._y:int=int(x._y)
			self._z:int=int(x._z)
			self._w:int=int(x._w)
		else:
			self._x:int=int(x)
			self._y:int=int(y)
			self._z:int=int(z)
			self._w:int=int(w)
		self.__obsolete : bool = False
		self.__npArr : ndarray[int] = array([self._x,self._y,self._z,self._w], dtype=int)
		self.__obsolete_norm : bool = True
		self.__normV : vec4i = 0

	def __str__(self) -> str:
		return f"({self._x} , {self._y} , {self._z} , {self._w})"
	
	def __repr__(self) -> str:
		return f"({self._x} , {self._y} , {self._z} , {self._w})"

	def copy(self) -> 'vec4i':
		return copy.deepcopy(self)

	@property
	def x(self) -> int:
		return self._x

	@x.setter
	def x(self, __value : int) -> None:
		self._x = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def y(self) -> int:
		return self._y

	@y.setter
	def y(self, __value : int) -> None:
		self._y = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def z(self) -> int:
		return self._z

	@z.setter
	def z(self, __value : int) -> None:
		self._z = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def w(self) -> int:
		return self._w

	@w.setter
	def w(self, __value : int) -> None:
		self._w = int(__value)
		self.__obsolete = True
		self.__obsolete_norm = True

	@property
	def xy(self) -> 'vec2i': return vec2i(self._x, self._y)
	@property
	def xz(self) -> 'vec2i': return vec2i(self._x, self._z)
	@property
	def xw(self) -> 'vec2i': return vec2i(self._x, self._w)
	@property
	def yx(self) -> 'vec2i': return vec2i(self._y, self._x)
	@property
	def yz(self) -> 'vec2i': return vec2i(self._y, self._z)
	@property
	def yw(self) -> 'vec2i': return vec2i(self._y, self._w)
	@property
	def zx(self) -> 'vec2i': return vec2i(self._z, self._x)
	@property
	def zy(self) -> 'vec2i': return vec2i(self._z, self._y)
	@property
	def zw(self) -> 'vec2i': return vec2i(self._z, self._w)
	@property
	def wx(self) -> 'vec2i': return vec2i(self._w, self._x)
	@property
	def wy(self) -> 'vec2i': return vec2i(self._w, self._y)
	@property
	def wz(self) -> 'vec2i': return vec2i(self._w, self._z)
	@property
	def xyz(self) -> 'vec3i': return vec3i(self._x, self._y, self._z)
	@property
	def xyw(self) -> 'vec3i': return vec3i(self._x, self._y, self._w)
	@property
	def xzy(self) -> 'vec3i': return vec3i(self._x, self._z, self._y)
	@property
	def xzw(self) -> 'vec3i': return vec3i(self._x, self._z, self._w)
	@property
	def xwy(self) -> 'vec3i': return vec3i(self._x, self._w, self._y)
	@property
	def xwz(self) -> 'vec3i': return vec3i(self._x, self._w, self._z)
	@property
	def yxz(self) -> 'vec3i': return vec3i(self._y, self._x, self._z)
	@property
	def yxw(self) -> 'vec3i': return vec3i(self._y, self._x, self._w)
	@property
	def yzx(self) -> 'vec3i': return vec3i(self._y, self._z, self._x)
	@property
	def yzw(self) -> 'vec3i': return vec3i(self._y, self._z, self._w)
	@property
	def ywx(self) -> 'vec3i': return vec3i(self._y, self._w, self._x)
	@property
	def ywz(self) -> 'vec3i': return vec3i(self._y, self._w, self._z)
	@property
	def zxy(self) -> 'vec3i': return vec3i(self._z, self._x, self._y)
	@property
	def zxw(self) -> 'vec3i': return vec3i(self._z, self._x, self._w)
	@property
	def zyx(self) -> 'vec3i': return vec3i(self._z, self._y, self._x)
	@property
	def zyw(self) -> 'vec3i': return vec3i(self._z, self._y, self._w)
	@property
	def zwx(self) -> 'vec3i': return vec3i(self._z, self._w, self._x)
	@property
	def zwy(self) -> 'vec3i': return vec3i(self._z, self._w, self._y)
	@property
	def wxy(self) -> 'vec3i': return vec3i(self._w, self._x, self._y)
	@property
	def wxz(self) -> 'vec3i': return vec3i(self._w, self._x, self._z)
	@property
	def wyx(self) -> 'vec3i': return vec3i(self._w, self._y, self._x)
	@property
	def wyz(self) -> 'vec3i': return vec3i(self._w, self._y, self._z)
	@property
	def wzx(self) -> 'vec3i': return vec3i(self._w, self._z, self._x)
	@property
	def wzy(self) -> 'vec3i': return vec3i(self._w, self._z, self._y)
	@property
	def xyzw(self) -> 'vec4i': return vec4i(self._x, self._y, self._z, self._w)
	@property
	def xywz(self) -> 'vec4i': return vec4i(self._x, self._y, self._w, self._z)
	@property
	def xzyw(self) -> 'vec4i': return vec4i(self._x, self._z, self._y, self._w)
	@property
	def xzwy(self) -> 'vec4i': return vec4i(self._x, self._z, self._w, self._y)
	@property
	def xwyz(self) -> 'vec4i': return vec4i(self._x, self._w, self._y, self._z)
	@property
	def xwzy(self) -> 'vec4i': return vec4i(self._x, self._w, self._z, self._y)
	@property
	def yxzw(self) -> 'vec4i': return vec4i(self._y, self._x, self._z, self._w)
	@property
	def yxwz(self) -> 'vec4i': return vec4i(self._y, self._x, self._w, self._z)
	@property
	def yzxw(self) -> 'vec4i': return vec4i(self._y, self._z, self._x, self._w)
	@property
	def yzwx(self) -> 'vec4i': return vec4i(self._y, self._z, self._w, self._x)
	@property
	def ywxz(self) -> 'vec4i': return vec4i(self._y, self._w, self._x, self._z)
	@property
	def ywzx(self) -> 'vec4i': return vec4i(self._y, self._w, self._z, self._x)
	@property
	def zxyw(self) -> 'vec4i': return vec4i(self._z, self._x, self._y, self._w)
	@property
	def zxwy(self) -> 'vec4i': return vec4i(self._z, self._x, self._w, self._y)
	@property
	def zyxw(self) -> 'vec4i': return vec4i(self._z, self._y, self._x, self._w)
	@property
	def zywx(self) -> 'vec4i': return vec4i(self._z, self._y, self._w, self._x)
	@property
	def zwxy(self) -> 'vec4i': return vec4i(self._z, self._w, self._x, self._y)
	@property
	def zwyx(self) -> 'vec4i': return vec4i(self._z, self._w, self._y, self._x)
	@property
	def wxyz(self) -> 'vec4i': return vec4i(self._w, self._x, self._y, self._z)
	@property
	def wxzy(self) -> 'vec4i': return vec4i(self._w, self._x, self._z, self._y)
	@property
	def wyxz(self) -> 'vec4i': return vec4i(self._w, self._y, self._x, self._z)
	@property
	def wyzx(self) -> 'vec4i': return vec4i(self._w, self._y, self._z, self._x)
	@property
	def wzxy(self) -> 'vec4i': return vec4i(self._w, self._z, self._x, self._y)
	@property
	def wzyx(self) -> 'vec4i': return vec4i(self._w, self._z, self._y, self._x)


	def __eq__(self, __value : Union['vec4i', int]) -> bool:

		if isinstance(__value, (vec4i,)):
			return (self._x==__value._x and 
					self._y==__value._y and 
					self._z==__value._z and 
					self._w==__value._w)

		elif isinstance(__value, (int,)):
			return (self._x==__value and 
					self._y==__value and 
					self._z==__value and 
					self._w==__value)

		#raise TypeError("Unsupported operand type for ==: 'vec4i and '{}'".format(type(__value)))
	def __ne__(self, __value : Union['vec4i', int]) -> bool:
		return not self.__eq__(__value)



	def __pow__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':

		if isinstance(__value, (int, float)):
			return vec4i(self._x ** __value, self._y ** __value, self._z ** __value, self._w ** __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec4i(self._x ** __value._x, self._y ** __value._y, self._z, self._w)

		elif isinstance(__value, (vec3i, vec3f)):
			return vec4i(self._x ** __value._x, self._y ** __value._y, self._z ** __value._z, self._w)

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			return vec4i(self._x ** __value._x, self._y ** __value._y, self._z ** __value._z, self._w ** __value._w)

		#raise TypeError("Unsupported operand type for +: 'vec4i' and '{}'".format(type(__value)))
	def __ipow__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x **= int(__value)
			self._y **= int(__value)
			self._z **= int(__value)
			self._w **= int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x **= int(__value._x)
			self._y **= int(__value._y)
			return self

		elif isinstance(__value, (vec3i, vec3f)):
			self._x **= int(__value._x)
			self._y **= int(__value._y)
			self._z **= int(__value._z)
			return self

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			self._x **= int(__value._x)
			self._y **= int(__value._y)
			self._z **= int(__value._z)
			self._w **= int(__value._w)
			return self

		#raise TypeError("Unsupported operand type for +: 'vec4i' and '{}'".format(type(__value)))



	def __add__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':

		if isinstance(__value, (int, float)):
			return vec4i(self._x + __value, self._y + __value, self._z + __value, self._w + __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec4i(self._x + __value._x, self._y + __value._y, self._z, self._w)

		elif isinstance(__value, (vec3i, vec3f)):
			return vec4i(self._x + __value._x, self._y + __value._y, self._z + __value._z, self._w)

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			return vec4i(self._x + __value._x, self._y + __value._y, self._z + __value._z, self._w + __value._w)

		#raise TypeError("Unsupported operand type for +: 'vec4i' and '{}'".format(type(__value)))
	def __iadd__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x += int(__value)
			self._y += int(__value)
			self._z += int(__value)
			self._w += int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x += int(__value._x)
			self._y += int(__value._y)
			return self

		elif isinstance(__value, (vec3i, vec3f)):
			self._x += int(__value._x)
			self._y += int(__value._y)
			self._z += int(__value._z)
			return self

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			self._x += int(__value._x)
			self._y += int(__value._y)
			self._z += int(__value._z)
			self._w += int(__value._w)
			return self

		#raise TypeError("Unsupported operand type for +: 'vec4i' and '{}'".format(type(__value)))



	def __sub__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':

		if isinstance(__value, (int, float)):
			return vec4i(self._x - __value, self._y - __value, self._z - __value, self._w - __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec4i(self._x - __value._x, self._y - __value._y, self._z, self._w)

		elif isinstance(__value, (vec3i, vec3f)):
			return vec4i(self._x - __value._x, self._y - __value._y, self._z - __value._z, self._w)

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			return vec4i(self._x - __value._x, self._y - __value._y, self._z - __value._z, self._w - __value._w)

		#raise TypeError("Unsupported operand type for -: 'vec4i' and '{}'".format(type(__value)))
	def __isub__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x -= int(__value)
			self._y -= int(__value)
			self._z -= int(__value)
			self._w -= int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x -= int(__value._x)
			self._y -= int(__value._y)
			return self

		elif isinstance(__value, (vec3i, vec3f)):
			self._x -= int(__value._x)
			self._y -= int(__value._y)
			self._z -= int(__value._z)
			return self

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			self._x -= int(__value._x)
			self._y -= int(__value._y)
			self._z -= int(__value._z)
			self._w -= int(__value._w)
			return self

		#raise TypeError("Unsupported operand type for -: 'vec4i' and '{}'".format(type(__value)))



	def __mul__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':

		if isinstance(__value, (int, float)):
			return vec4i(self._x * __value, self._y * __value, self._z * __value, self._w * __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec4i(self._x * __value._x, self._y * __value._y, self._z, self._w)

		elif isinstance(__value, (vec3i, vec3f)):
			return vec4i(self._x * __value._x, self._y * __value._y, self._z * __value._z, self._w)

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			return vec4i(self._x * __value._x, self._y * __value._y, self._z * __value._z, self._w * __value._w)

		#raise TypeError("Unsupported operand type for *: 'vec4i' and '{}'".format(type(__value)))
	def __imul__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			self._x *= int(__value)
			self._y *= int(__value)
			self._z *= int(__value)
			self._w *= int(__value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x *= int(__value._x)
			self._y *= int(__value._y)
			return self

		elif isinstance(__value, (vec3i, vec3f)):
			self._x *= int(__value._x)
			self._y *= int(__value._y)
			self._z *= int(__value._z)
			return self

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			self._x *= int(__value._x)
			self._y *= int(__value._y)
			self._z *= int(__value._z)
			self._w *= int(__value._w)
			return self

		#raise TypeError("Unsupported operand type for *: 'vec4i' and '{}'".format(type(__value)))



	def __truediv__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':

		if isinstance(__value, (int, float)):
			if(__value==0): 
				return vec4i(
					(inf if(self._x>=0) else -inf),
					(inf if(self._y>=0) else -inf),
					(inf if(self._z>=0) else -inf),
					(inf if(self._w>=0) else -inf)
				)
			return vec4i(self._x / __value, self._y / __value, self._z / __value, self._w / __value)

		elif isinstance(__value, (vec2i, vec2f)):
			return vec4i(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)), 
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)), 
				self._z, 
				self._w
			)

		elif isinstance(__value, (vec3i, vec3f)):
			return vec4i(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)),
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)),
				((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf)),
				self._w
			)

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			return vec4i(
				((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf)),
				((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf)),
				((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf)),
				((self._w / __value._w) if(__value._w!=0) else (inf if(self._w>=0) else -inf)),
			)

		#raise TypeError("Unsupported operand type for /: 'vec4i' and '{}'".format(type(__value)))
	def __itruediv__(self, __value : Union['vec2i', 'vec2f', 'vec3i', 'vec3f', 'vec4i', 'vec4f', int, float]) -> 'vec4i':
		self.__obsolete = True
		self.__obsolete_norm = True

		if isinstance(__value, (int, float)):
			if(__value==0): 
				self._x = int(inf if(self._x>=0) else -inf)
				self._y = int(inf if(self._y>=0) else -inf)
				self._z = int(inf if(self._z>=0) else -inf)
				self._w = int(inf if(self._w>=0) else -inf)
				return self
			self._x = int(self._x / __value)
			self._y = int(self._x / __value)
			self._z = int(self._x / __value)
			self._w = int(self._x / __value)
			return self

		elif isinstance(__value, (vec2i, vec2f)):
			self._x = int((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = int((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			return self

		elif isinstance(__value, (vec3i, vec3f)):
			self._x = int((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = int((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			self._z = int((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			return self

		#elif isinstance(__value, (vec4i, vec4f)):
		else:
			self._x = int((self._x / __value._x) if(__value._x!=0) else (inf if(self._x>=0) else -inf))
			self._y = int((self._y / __value._y) if(__value._y!=0) else (inf if(self._y>=0) else -inf))
			self._z = int((self._z / __value._z) if(__value._z!=0) else (inf if(self._z>=0) else -inf))
			self._w = int((self._w / __value._w) if(__value._w!=0) else (inf if(self._w>=0) else -inf))
			return self

		#raise TypeError("Unsupported operand type for /: 'vec4i' and '{}'".format(type(__value)))



	@property
	def magnitude(self) -> float:
		return (self._x*self._x + self._y*self._y + self._z*self._z + self._w*self._w) ** 0.5

	@property
	def normalize(self) -> 'vec4i':
		if(self.__obsolete_norm):
			self.__obsolete_norm = False
			self.__normV = self/self.magnitude
			return self.__normV
		else: return self.__normV

	@property
	def arr(self) -> ndarray[int]:
		if(self.__obsolete):
			self.__npArr[0] = self._x
			self.__npArr[1] = self._y
			self.__npArr[2] = self._z
			self.__npArr[3] = self._w
			self.__obsolete = False
		return self.__npArr



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################



def DotP(
	a:Union[vec2f,vec2i,vec3f,vec3i,vec4f,vec4i],
	b:Union[vec2f,vec2i,vec3f,vec3i,vec4f,vec4i]
	) -> float:
	if(type(a)==type(b)):
		return dot(a.arr,b.arr)

def Cross(
	a:Union[vec2f,vec2i,vec3f,vec3i],
	b:Union[vec2f,vec2i,vec3f,vec3i]
	) -> Union[float, vec3f]:
	res = 0
	if(type(a)==type(b)):
		res = cross(a.arr,b.arr)
		if(res.size==1): res = float(res)
		elif(res.size==3): res = vec3f(res[0],res[1],res[2])
	return res



####################################################################################################################################################
####################################################################################################################################################
####################################################################################################################################################



class mat2f:
	def __init__(self,
	    m :
		Tuple[
			Union[Tuple[float, float], List[float], ndarray[float]],
			Union[Tuple[float, float], List[float], ndarray[float]],
			Union[Tuple[float, float], List[float], ndarray[float]]
		]
		=
		(
			(1.0 , 0.0) ,
			(0.0 , 1.0)
		)
	) -> None:
		self._m : ndarray[float] = array(m, dtype=float)
		self.__obsolete : List[bool] = [True,True,True]
		self.__i : vec2f = vec2f()
		self.__j : vec2f = vec2f()
		self.__inv_np : ndarray[float] = eye(2)

	@property
	def m(self) -> ndarray[float]:
		return self._m

	@m.setter
	def m(self, __value : ndarray[float]) -> None:
		self._m = __value
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True

	@property
	def identity(self) -> 'mat2f':
		self._m[0][0] = 1.0
		self._m[0][1] = 0.0
		self._m[1][0] = 0.0
		self._m[1][1] = 1.0
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		return self

	@property
	def i(self) -> 'vec2f':
		if(self.__obsolete[0]):
			self.__i.x = self._m[0][0]
			self.__i.y = self._m[0][1]
			self.__obsolete[0] = False
		return self.__i
	@property
	def j(self) -> 'vec2f':
		if(self.__obsolete[1]):
			self.__j.x = self._m[1][0]
			self.__j.y = self._m[1][1]
			self.__obsolete[1] = False
		return self.__j

	def __str__(self) -> str:
		return f'{self._m}'

	def copy(self) -> 'mat2f':
		return copy.deepcopy(self)



	def __eq__(self, other: 'mat2f') -> bool:
		return array_equal(self._m, other._m)

	def __ne__(self, other: 'mat2f') -> bool:
		return not self.__eq__(other)



	def __add__(self, __value : 'mat2f') -> 'mat2f':
		return mat2f(self._m+__value._m)

	def __iadd__(self, __value : 'mat2f') -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self._m+__value._m
		return self



	def __sub__(self, __value : 'mat2f') -> 'mat2f':
		return mat2f(self._m-__value._m)

	def __isub__(self, __value : 'mat2f') -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self._m-__value._m
		return self



	def __mul__(self, __value : Union[int, float, 'vec2f', 'vec2i', 'mat2f']) -> Union['vec2f','mat2f']:
		if(isinstance(__value, mat2f)):
			return mat2f(dot(self._m, __value._m))
		elif(isinstance(__value, (vec2f, vec2i))):
			m=self._m*__value.arr
			return vec2f(
				m[0][0]+m[0][1],
				m[1][0]+m[1][1]
			)
		elif(isinstance(__value, (int, float))):
			return mat2f(self._m*__value)

	def __imul__(self, __value : Union[int, float, 'mat2f']) -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		if(isinstance(__value, mat2f)):
			self._m=dot(self._m, __value._m)
			return self
		elif(isinstance(__value, (int, float))):
			self._m=self._m*__value
			return self



	def __truediv__(self, __value : Union[int, float, 'mat2f']) -> 'mat2f':
		if(isinstance(__value, mat2f)):
			return mat2f(dot(self._m,__value.inv_get._m))
		elif(isinstance(__value, (int, float))):
			return mat2f(self._m/__value)

	def __itruediv__(self, __value : Union[int, float, 'mat2f']) -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		if(isinstance(__value, mat2f)):
			self._m=dot(self._m,__value.inv_get._m)
			return self
		elif(isinstance(__value, (int, float))):
			self._m=self._m/__value
			return self


	@property
	def T_get(self) -> 'mat2f':
		return mat2f(self._m.T)

	@property
	def T_set(self) -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self._m=self._m.T
		return self


	@property
	def determinant(self) -> float:
		return det(self._m)


	@property
	def inv_get(self) -> 'mat2f':
		if(self.__obsolete[2]):
			if self.determinant == 0:
				raise ValueError("Matrix is not invertible")
			self.__obsolete[2] = False
			self.__inv_np = inv(self._m)
		return mat2f(self.__inv_np)
	
	@property
	def inv_get_nparray(self) -> ndarray[float]:
		if(self.__obsolete[2]):
			if self.determinant == 0:
				raise ValueError("Matrix is not invertible")
			self.__obsolete[2] = False
			self.__inv_np = inv(self._m)
		return self.__inv_np

	@property
	def inv_set(self) -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		if self.determinant == 0:
			raise ValueError("Matrix is not invertible")
		self._m=inv(self._m)
		return self
	
	@property
	def Trans_get(self) -> 'mat2f':
		return mat4f(transpose(self._m))
	
	@property
	def Trans_set(self) -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self._m = transpose(self._m)
		return self

	@property
	def rank(self) -> int:
		return matrix_rank(self._m)


	@property
	def Trace(self) -> float:
		return trace(self._m)

	@property
	def frobenius_norm(self) -> float:
		return norm(self._m, 'fro')


	@property
	def max_abs_row_sum_norm(self) -> float:
		return norm(self._m, inf)


	def pow_get(self, n: int) -> 'mat2f':
		return mat2f(matrix_power(self._m, n))

	def pow_set(self, n: int) -> 'mat2f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self._m=matrix_power(self._m, n)
		return self


####################################################################################################################################################


class mat3f:
	def __init__(self,
	    m :
		Tuple[
			Union[Tuple[float, float, float], List[float], ndarray[float]],
			Union[Tuple[float, float, float], List[float], ndarray[float]],
			Union[Tuple[float, float, float], List[float], ndarray[float]]
		]
		=
		(
			(1.0 , 0.0 , 0.0) ,
			(0.0 , 1.0 , 0.0) ,
			(0.0 , 0.0 , 1.0)
		)
	) -> None:
		self._m : ndarray[float] = array(m, dtype=float)
		self.__obsolete : List[bool] = [True,True,True,True]
		self.__i : vec3f = vec3f()
		self.__j : vec3f = vec3f()
		self.__k : vec3f = vec3f()
		self.__inv_np : ndarray[float] = eye(3)

	@property
	def m(self) -> ndarray[float]:
		return self._m

	@m.setter
	def m(self, __value : ndarray[float]) -> None:
		self._m = __value
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True

	@property
	def identity(self) -> 'mat3f':
		self._m[0][0] = 1.0
		self._m[0][1] = 0.0
		self._m[0][2] = 0.0

		self._m[1][0] = 0.0
		self._m[1][1] = 1.0
		self._m[1][2] = 0.0

		self._m[2][0] = 0.0
		self._m[2][1] = 0.0
		self._m[2][2] = 1.0

		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		return self

	@property
	def i(self) -> 'vec3f':
		if(self.__obsolete[0]):
			self.__i.x=self._m[0][0]
			self.__i.y=self._m[0][1]
			self.__i.z=self._m[0][2]
			self.__obsolete[0] = False
		return self.__i
	@property
	def j(self) -> 'vec3f':
		if(self.__obsolete[1]):
			self.__j.x=self._m[1][0]
			self.__j.y=self._m[1][1]
			self.__j.z=self._m[1][2]
			self.__obsolete[1] = False
		return self.__j
	@property
	def k(self) -> 'vec3f':
		if(self.__obsolete[2]):
			self.__k.x=self._m[2][0]
			self.__k.y=self._m[2][1]
			self.__k.z=self._m[2][2]
			self.__obsolete[2] = False
		return self.__k

	def __str__(self) -> str:
		return f'{self._m}'

	def copy(self) -> 'mat3f':
		return copy.deepcopy(self)



	def __eq__(self, other: 'mat3f') -> bool:
		return array_equal(self._m, other._m)

	def __ne__(self, other: 'mat3f') -> bool:
		return not self.__eq__(other)



	def __add__(self, __value : 'mat3f') -> 'mat3f':
		return mat3f(self._m+__value._m)

	def __iadd__(self, __value : 'mat3f') -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self._m+__value._m
		return self



	def __sub__(self, __value : 'mat3f') -> 'mat3f':
		return mat3f(self._m-__value._m)

	def __isub__(self, __value : 'mat3f') -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self._m-__value._m
		return self



	def __mul__(self, __value : Union[int, float, 'vec3f', 'vec3i', 'mat3f']) -> Union['vec3f','mat3f']:
		if(isinstance(__value, mat3f)):
			return mat3f(dot(self._m, __value._m))
		elif(isinstance(__value, (vec3f, vec3i))):
			m=self._m*__value.arr
			return vec3f(
				m[0][0]+m[0][1]+m[0][2],
				m[1][0]+m[1][1]+m[1][2],
				m[2][0]+m[2][1]+m[2][2]
			)
		elif(isinstance(__value, (int, float))):
			return mat3f(self._m*__value)

	def __imul__(self, __value : Union[int, float, 'mat3f']) -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		if(isinstance(__value, mat3f)):
			self._m=dot(self._m, __value._m)
			return self
		elif(isinstance(__value, (int, float))):
			self._m=self._m*__value
			return self



	def __truediv__(self, __value : Union[int, float, 'mat3f']) -> 'mat3f':
		if(isinstance(__value, mat3f)):
			return mat3f(dot(self._m,__value.inv_get._m))
		elif(isinstance(__value, (int, float))):
			return mat3f(self._m/__value)

	def __itruediv__(self, __value : Union[int, float, 'mat3f']) -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		if(isinstance(__value, mat3f)):
			self._m=dot(self._m,__value.inv_get._m)
			return self
		elif(isinstance(__value, (int, float))):
			self._m=self._m/__value
			return self


	@property
	def T_get(self) -> 'mat3f':
		return mat3f(self._m.T)

	@property
	def T_set(self) -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self._m=self._m.T
		return self


	@property
	def determinant(self) -> float:
		return det(self._m)


	@property
	def inv_get(self) -> 'mat3f':
		if(self.__obsolete[3]):
			if self.determinant == 0:
				raise ValueError("Matrix is not invertible")
			self.__obsolete[3] = False
			self.__inv_np = inv(self._m)
		return mat3f(self.__inv_np)
	
	@property
	def inv_get_nparray(self) -> ndarray[float]:
		if(self.__obsolete[3]):
			if self.determinant == 0:
				raise ValueError("Matrix is not invertible")
			self.__obsolete[3] = False
			self.__inv_np = inv(self._m)
		return self.__inv_np

	@property
	def inv_set(self) -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		if self.determinant == 0:
			raise ValueError("Matrix is not invertible")
		self._m=inv(self._m)
		return self
	
	@property
	def Trans_get(self) -> 'mat3f':
		return mat3f(transpose(self._m))
	
	@property
	def Trans_set(self) -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self._m = transpose(self._m)
		return self

	@property
	def rank(self) -> int:
		return matrix_rank(self._m)


	@property
	def Trace(self) -> float:
		return trace(self._m)

	@property
	def frobenius_norm(self) -> float:
		return norm(self._m, 'fro')


	@property
	def max_abs_row_sum_norm(self) -> float:
		return norm(self._m, inf)


	def pow_get(self, n: int) -> 'mat3f':
		return mat3f(matrix_power(self._m, n))

	def pow_set(self, n: int) -> 'mat3f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self._m=matrix_power(self._m, n)
		return self


####################################################################################################################################################


class mat4f:
	def __init__(self,
	    m :
		Tuple[
			Union[Tuple[float, float, float, float], List[float], ndarray[float]],
			Union[Tuple[float, float, float, float], List[float], ndarray[float]],
			Union[Tuple[float, float, float, float], List[float], ndarray[float]],
			Union[Tuple[float, float, float, float], List[float], ndarray[float]]
		]
		=
		(
			(1.0 , 0.0 , 0.0 , 0.0) ,
			(0.0 , 1.0 , 0.0 , 0.0) ,
			(0.0 , 0.0 , 1.0 , 0.0) ,
			(0.0 , 0.0 , 0.0 , 1.0)
		)
	) -> None:
		self._m : ndarray[float] = array(m, dtype=float)
		self.__obsolete : List[bool] = [True,True,True,True,True]
		self.__i : vec4f = vec4f()
		self.__j : vec4f = vec4f()
		self.__k : vec4f = vec4f()
		self.__l : vec4f = vec4f()
		self.__inv_np : ndarray[float] = eye(4)

	@property
	def m(self) -> ndarray[float]:
		return self._m

	@m.setter
	def m(self, __value : ndarray[float]) -> None:
		self._m = __value
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True

	@property
	def identity(self) -> 'mat4f':
		self._m[0][0] = 1.0
		self._m[0][1] = 0.0
		self._m[0][2] = 0.0
		self._m[0][3] = 0.0

		self._m[1][0] = 0.0
		self._m[1][1] = 1.0
		self._m[1][2] = 0.0
		self._m[1][3] = 0.0

		self._m[2][0] = 0.0
		self._m[2][1] = 0.0
		self._m[2][2] = 1.0
		self._m[2][3] = 0.0

		self._m[3][0] = 0.0
		self._m[3][1] = 0.0
		self._m[3][2] = 0.0
		self._m[3][3] = 1.0

		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		return self

	@property
	def i(self) -> 'vec4f':
		if(self.__obsolete[0]):
			self.__i.x=self._m[0][0]
			self.__i.y=self._m[0][1]
			self.__i.z=self._m[0][2]
			self.__i.w=self._m[0][3]
			self.__obsolete[0] = False
		return self.__i
	@property
	def j(self) -> 'vec4f':
		if(self.__obsolete[1]):
			self.__j.x=self._m[1][0]
			self.__j.y=self._m[1][1]
			self.__j.z=self._m[1][2]
			self.__j.w=self._m[1][3]
			self.__obsolete[0] = False
		return self.__j
	@property
	def k(self) -> 'vec4f':
		if(self.__obsolete[2]):
			self.__k.x=self._m[2][0]
			self.__k.y=self._m[2][1]
			self.__k.z=self._m[2][2]
			self.__k.w=self._m[2][3]
			self.__obsolete[0] = False
		return self.__k
	@property
	def l(self) -> 'vec4f':
		if(self.__obsolete[3]):
			self.__l.x=self._m[3][0]
			self.__l.y=self._m[3][1]
			self.__l.z=self._m[3][2]
			self.__l.w=self._m[3][3]
			self.__obsolete[0] = False
		return self.__l

	def __str__(self) -> str:
		return f'{self._m}'

	def copy(self) -> 'mat4f':
		return copy.deepcopy(self)



	def __eq__(self, other: 'mat4f') -> bool:
		return array_equal(self._m, other._m)

	def __ne__(self, other: 'mat4f') -> bool:
		return not self.__eq__(other)



	def __add__(self, __value : 'mat4f') -> 'mat4f':
		return mat4f(self._m+__value._m)

	def __iadd__(self, __value : 'mat4f') -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		self._m+__value._m
		return self



	def __sub__(self, __value : 'mat4f') -> 'mat4f':
		return mat4f(self._m-__value._m)

	def __isub__(self, __value : 'mat4f') -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		self._m-__value._m
		return self



	def __mul__(self, __value : Union[int, float, 'vec4f', 'vec4i', 'mat4f']) -> Union['vec4f','mat4f']:
		if(isinstance(__value, mat4f)):
			return mat4f(dot(self._m, __value._m))
		elif(isinstance(__value, (vec4f, vec4i))):
			m=self._m*__value.arr
			return vec4f(
				m[0][0]+m[0][1]+m[0][2]+m[0][3],
				m[1][0]+m[1][1]+m[1][2]+m[1][3],
				m[2][0]+m[2][1]+m[2][2]+m[2][3],
				m[3][0]+m[3][1]+m[3][2]+m[3][3]
			)
		elif(isinstance(__value, (int, float))):
			return mat4f(self._m*__value)

	def __imul__(self, __value : Union[int, float, 'mat4f']) -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		if(isinstance(__value, mat4f)):
			self._m=dot(self._m, __value._m)
			return self
		elif(isinstance(__value, (int, float))):
			self._m=self._m*__value
			return self



	def __truediv__(self, __value : Union[int, float, 'mat4f']) -> 'mat4f':
		if(isinstance(__value, mat4f)):
			return mat4f(dot(self._m,__value.inv_get._m))
		elif(isinstance(__value, (int, float))):
			return mat4f(self._m/__value)

	def __itruediv__(self, __value : Union[int, float, 'mat4f']) -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		if(isinstance(__value, mat4f)):
			self._m=dot(self._m,__value.inv_get._m)
			return self
		elif(isinstance(__value, (int, float))):
			self._m=self._m/__value
			return self


	@property
	def T_get(self) -> 'mat4f':
		return mat4f(self._m.T)

	@property
	def T_set(self) -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		self._m=self._m.T
		return self


	@property
	def determinant(self) -> float:
		return det(self._m)


	@property
	def inv_get(self) -> 'mat4f':
		if(self.__obsolete[4]):
			if self.determinant == 0:
				raise ValueError("Matrix is not invertible")
			self.__obsolete[4] = False
			self.__inv_np = inv(self._m)
		return mat4f(self.__inv_np)
	
	@property
	def inv_get_nparray(self) -> ndarray[float]:
		if(self.__obsolete[4]):
			if self.determinant == 0:
				raise ValueError("Matrix is not invertible")
			self.__obsolete[4] = False
			self.__inv_np = inv(self._m)
		return self.__inv_np

	@property
	def inv_set(self) -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		if self.determinant == 0:
			raise ValueError("Matrix is not invertible")
		self._m=inv(self._m)
		return self
	
	@property
	def Trans_get(self) -> 'mat4f':
		return mat4f(transpose(self._m))
	
	@property
	def Trans_set(self) -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		self._m = transpose(self._m)
		return self

	@property
	def rank(self) -> int:
		return matrix_rank(self._m)


	@property
	def Trace(self) -> float:
		return trace(self._m)

	@property
	def frobenius_norm(self) -> float:
		return norm(self._m, 'fro')


	@property
	def max_abs_row_sum_norm(self) -> float:
		return norm(self._m, inf)


	def pow_get(self, n: int) -> 'mat4f':
		return mat4f(matrix_power(self._m, n))

	def pow_set(self, n: int) -> 'mat4f':
		self.__obsolete[0] = True
		self.__obsolete[1] = True
		self.__obsolete[2] = True
		self.__obsolete[3] = True
		self.__obsolete[4] = True
		self._m=matrix_power(self._m, n)
		return self


####################################################################################################################################################
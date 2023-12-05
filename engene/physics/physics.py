from engene.Obj_3D import *
from numpy import mean



def do_cubes_intersect(Cube1: Transform, Cube2: Transform, velocity: vec3f) -> bool:

	cubeMat1 : List[vec3f] = [
		(Cube1.rotation*(Cube1.scale*vec3f(-0.5,-0.5,-0.5)))+Cube1.position,
		(Cube1.rotation*(Cube1.scale*vec3f(0.5,-0.5,-0.5)))+Cube1.position,
		(Cube1.rotation*(Cube1.scale*vec3f(0.5,0.5,-0.5)))+Cube1.position,
		(Cube1.rotation*(Cube1.scale*vec3f(-0.5,0.5,-0.5)))+Cube1.position,

		(Cube1.rotation*(Cube1.scale*vec3f(-0.5,-0.5,0.5)))+Cube1.position,
		(Cube1.rotation*(Cube1.scale*vec3f(0.5,-0.5,0.5)))+Cube1.position,
		(Cube1.rotation*(Cube1.scale*vec3f(0.5,0.5,0.5)))+Cube1.position,
		(Cube1.rotation*(Cube1.scale*vec3f(-0.5,0.5,0.5)))+Cube1.position
	]
	cubeMat2 : List[vec3f] = [
		(Cube2.rotation*(Cube2.scale*vec3f(-0.5,-0.5,-0.5)))+Cube2.position,
		(Cube2.rotation*(Cube2.scale*vec3f(0.5,-0.5,-0.5)))+Cube2.position,
		(Cube2.rotation*(Cube2.scale*vec3f(0.5,0.5,-0.5)))+Cube2.position,
		(Cube2.rotation*(Cube2.scale*vec3f(-0.5,0.5,-0.5)))+Cube2.position,

		(Cube2.rotation*(Cube2.scale*vec3f(-0.5,-0.5,0.5)))+Cube2.position,
		(Cube2.rotation*(Cube2.scale*vec3f(0.5,-0.5,0.5)))+Cube2.position,
		(Cube2.rotation*(Cube2.scale*vec3f(0.5,0.5,0.5)))+Cube2.position,
		(Cube2.rotation*(Cube2.scale*vec3f(-0.5,0.5,0.5)))+Cube2.position
	]
	
	differenceVectors : List[ndarray[float]] = []

	#===========================================================
	for vertex2 in cubeMat2:
		for vertex1 in cubeMat1:
			differenceVectors.append((vertex2-vertex1).arr)
	del vertex2, vertex1, cubeMat2, cubeMat1
	differenceVectors : ndarray[float] = array(differenceVectors,dtype=float)
	#===========================================================
	
	#'''#===========================================================
	meanV = mean([vertex.arr for vertex in differenceVectors],axis=0)
	#===========================================================

	#===========================================================
	for vector in differenceVectors:
		dotp : float = dot((vector-velocity).arr,meanV)
		if(dotp<=0.0):
			del differenceVectors, dotp, vector, meanV
			return True
	del vector, dotp
	del differenceVectors, meanV
	#==========================================================='''

	return False
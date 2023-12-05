from engene.openGL_atrib import *
from sys import exit


MainForm = Form(
    size = vec2i(1920,1080)*0.5,
    #size = vec2i(1000,1000)*0.75,
    title = "Alepth",
    color = vec4f( vec3f( 1 , 2 , 3 ).normalize , 1 ),
	physics = Physics(
		FPS = 300,
		gravity = vec3f( 0 , -0.97 , 0 )
	)
)

defaultCamera = Camera(
	form = MainForm,
	gameObject = GameObject(
		transform = Transform(
			pos = vec3f( 0 , 0 , 0 ),
			sca = vec3f( 1 , 1 , 1 ),
			rot = Rotation(),
		),
		parent = None
	),
	near = 0,
	far = 1,
	fov = 75.0,
	renderLayer = [
		'default',
	]
)
LoadText = Text(
	camera = defaultCamera,
	color = vec4f(1,1,1,1),
	text = "Loading",
	pos = vec2f(-0.5,-0.75),
	sca = vec2f(1,1),
	rot = Rotation(),
	align = 'left',
	offset = 1,
	renderLayer = 'default',
	renderSide = 'Front'
)
LoadIcoText = Text(
	camera = defaultCamera,
	color = vec4f(1,1,1,1),
	text = "◌",
	pos = LoadText.pos+vec2f(0.1,0),
	sca = vec2f(1,1),
	rot = Rotation(),
	align = 'chenter',
	offset = 1,
	renderLayer = 'default',
	renderSide = 'Front'
)

#'''
from assets.Level.RTX_LVL_room import Level
lvl = Level(MainForm = MainForm)
lvl.LoadLevel()
#'''

if (__name__ == '__main__'):
	
	while MainForm.Exist:
		dt = MainForm.physics.deltaT

		if(not MainForm.loader.MeshesHasLoaded()):
			#pg.display.set_caption(f'{MainForm.title} {MainForm.physics.fps:.0f}')

			#___________________


			lvl.Update(dt)


			#___________________
			pass

		else:
			pg.display.set_caption(f'Loading {MainForm.physics.fps:.0f}')
			defaultCamera.ClearColor()
			LoadText.Draw()
			LoadIcoText.Draw()
			LoadIcoText.rot.Lz(1)

		MainForm.run()

	exit()
from ursina import *

class CubeDisplay(Entity):  # A CubeDisplay osztály öröklődik az Entity osztályból
    def __init__(self):
        super().__init__()  # Hívja meg az Entity konstruktorát
        window.borderless = False
        window.fullscreen = False
        window.exit_button.visible = False
        window.fps_counter.enabled = True
        self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
        
        # A háttér létrehozása
        Entity(model='quad', scale=60, texture='white_cube', rotation_x=90, y=-5, color=color.light_gray)
        # Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)
        
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.load_game()
        
    def load_game(self):
         self.create_cube_positions()
         self.CUBES = []
         self.initial_positions = {}
         self.PARENT = Entity(model='cube', color=color.black)
         for idx, pos in enumerate(self.SIDE_POSITIONS):
             cube = Entity(parent=self.PARENT,model=self.cube_model, texture=self.cube_texture, position=pos)
             cube.id = idx
             self.CUBES.append(cube)
             self.initial_positions[idx] = pos

         
         
         self.rotation_axes = {'LEFT': 'x','RIGHT':'x','TOP': 'y' , 'BOTTOM': 'y', 'FACE': 'z', 'BACK': 'z'}
         self.cubes_side_positions = {'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.RIGHT, 'FACE': self.FACE, 'BACK': self.BACK, 'TOP': self.TOP }
        #  'LEFT': self.LEFT, 'BOTTOM': self.BOTTOM, 'RIGHT': self.FACE,
        #  'FACE': self.FACE, 'BACK': self.BACK, 'TOP': self.TOP
         self.animation_time = 0.1

    def rotate_side(self, side_name):
        cube_positions = self.cubes_side_positions[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        # print(cube_positions, rotation_axis)
        for cube in self.CUBES:
            coordinates=cube.position.x,cube.position.y,cube.position.z
            if coordinates in cube_positions:
                cube.parent = self.PARENT
                
                if rotation_axis == 'x':
                    self.PARENT.animate_rotation_x(90, duration=self.animation_time)
                elif rotation_axis == 'y':
                    self.PARENT.animate_rotation_y(90, duration=self.animation_time)
                elif rotation_axis == 'z':
                    self.PARENT.animate_rotation_z(90, duration=self.animation_time)
                

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        size=5
        self.LEFT = {(-1, y, z) for y in range(-1, size) for z in range(-1, size)}
        self.BOTTOM = {(x, -1, z) for x in range(-1, size) for z in range(-1, size)}
        self.FACE = {(x, y, -1) for x in range(-1, size) for y in range(-1, size)}
        self.BACK = {(x, y, size-1) for x in range(-1, size) for y in range(-1, size)}
        self.RIGHT = {(size-1, y, z) for y in range(-1, size) for z in range(-1, size)}
        self.TOP = {(x, size-1, z) for x in range(-1, size) for z in range(-1, size)}
        self.SIDE_POSITIONS = self.LEFT | self.BOTTOM  | self.FACE | self.BACK | self.RIGHT | self.TOP
        
    def is_solved(self):
        for cube in self.CUBES:
            if cube.position != self.initial_positions[cube.id]:
                return False
        return True

    def input(self, key):
        # print(key)
        if key=='a':
            self.rotate_side('LEFT')
        if key=='d':
            self.rotate_side('RIGHT')
        if key=='w':
            self.rotate_side('TOP')
        if key=='s':
            self.rotate_side('BOTTOM')
        if key=='q':
            self.rotate_side('FACE')
        if key=='e':
            self.rotate_side('BACK')

if __name__ == '__main__':
    app = Ursina()
    game = CubeDisplay()
    app.run()

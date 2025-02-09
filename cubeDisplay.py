from ursina import *
import cubeModel


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
        self.PARENT = Entity(model=self.cube_model,texture=self.cube_texture)
        self.CUBES=[]
        self.animation_time = 0.1
        self.create_cube_positions()
        

        

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
        size=3
        index=0
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    model=cubeModel.CubeModel(Entity( position=(i, j, k),parent=self.PARENT,model=self.cube_model, texture=self.cube_texture),index)
                    self.CUBES.append(model)
                    index+=1
        

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

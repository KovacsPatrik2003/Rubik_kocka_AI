# from ursina import *
# import cubeModel


# class CubeDisplay(Entity):  # A CubeDisplay osztály öröklődik az Entity osztályból
#     def __init__(self):
#         super().__init__()  # Hívja meg az Entity konstruktorát
#         window.borderless = False
#         window.fullscreen = False
#         window.exit_button.visible = False
#         window.fps_counter.enabled = True
#         self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'

#         # A háttér létrehozása
#         Entity(model='quad', scale=60, texture='white_cube', rotation_x=90, y=-5, color=color.light_gray)
#         # Entity(model='sphere', scale=100, texture='textures/sky0', double_sided=True)

#         EditorCamera()
#         camera.world_position = (0, 0, -15)
#         self.load_game()

#     def load_game(self):
#         self.PARENT = Entity(model=self.cube_model,texture=self.cube_texture)
#         proba=Entity(position=(10, 10, 10), color=color.black, parent=self.PARENT)
#         self.CUBES=[]
#         self.animation_time = 0.1
#         # self.cubes_side_positions = {'X': self.XSide, 'Y': self.YSide,   'Z': self.ZSide}
#         self.create_cube_positions()
#         self.cubes_axes = {'X': self.XSide, 'Y': self.YSide,   'Z': self.ZSide}
#         last_Index=self.CUBES[-1].Id
#         # model=cubeModel.CubeModel(self.PARENT,last_Index+1)
#         # self.CUBES.append(model)
        




#     def rotate_side(self, side_name, line_number=1):
#         # # cube_positions = self.cubes_side_positions[side_name]
#         # cube_positions = [(lineNumber, i, j) for i in range(3) for j in range(3)]
#         # rotation_axis = self.cubes_axes[side_name]
#         # rotation_axis='X'
#         # self.reparent_to_scene()
#         # for cube in self.CUBES:
#         #     coordinates=cube.Entity.position.x,cube.Entity.position.y,cube.Entity.position.z
#         #     if coordinates in cube_positions:
#         #         cube.Entity.parent = self.PARENT
                
#         #         if rotation_axis == 'X':
#         #             self.PARENT.animate_rotation_x(90, duration=self.animation_time)
#         #         elif rotation_axis == 'Z':
#         #             self.PARENT.animate_rotation_y(90, duration=self.animation_time)
#         #         elif rotation_axis == 'Z':
#         #             self.PARENT.animate_rotation_z(90, duration=self.animation_time)


#         rotation_axis = self.cubes_axes[side_name]
#         self.reparent_to_scene()
        
#         affected_cubes = []
#         for cube in self.CUBES:
#             x, y, z = cube.Entity.position
#             if (side_name == 'X' and x == line_number) or \
#                (side_name == 'Y' and y == line_number) or \
#                (side_name == 'Z' and z == line_number):
#                 affected_cubes.append(cube)
#                 cube.Entity.parent = self.PARENT

#         if rotation_axis == 'X':
#             self.PARENT.animate_rotation_x(90, duration=self.animation_time)
#         elif rotation_axis == 'Y':
#             self.PARENT.animate_rotation_y(90, duration=self.animation_time)
#         elif rotation_axis == 'Z':
#             self.PARENT.animate_rotation_z(90, duration=self.animation_time)

#         invoke(self.reparent_to_scene, delay=self.animation_time)


        
        


#     def reparent_to_scene(self):
#         for cube in self.CUBES:
#             if cube.Entity.parent == self.PARENT:
#                 world_pos, world_rot = round(cube.Entity.world_position, 1), cube.Entity.world_rotation
#                 cube.Entity.parent = scene
#                 cube.Entity.position, cube.Entity.rotation = world_pos, world_rot
#         self.PARENT.rotation = 0

#     def create_cube_positions(self):
#         size=3
#         index=0
#         for i in range(size):
#             for j in range(size):
#                 for k in range(size):
#                     # , texture=self.cube_texture
#                     # color=color.black
#                     model=cubeModel.CubeModel(Entity( position=(i, j, k),parent=self.PARENT,model=self.cube_model, texture=self.cube_texture),index)
#                     self.CUBES.append(model)
#                     index+=1
#         # self.X='X'
#         # self.Y='Y'
#         # self.Z='Z'
#         self.XSide='X'
#         self.YSide='Y'
#         self.ZSide='Z'
#         self.SIDE_POSITIONS = [self.XSide, self.YSide, self.ZSide]
#         #for debug only
#         # for i in self.CUBES:
#         #     if  i.Entity.position.x==1 and i.Entity.position.y==2 and i.Entity.position.z==0:
                
#         #         i.Entity.color=color.white


#     def input(self, key):
#         # print(key)
#         if key=='a':
#             self.rotate_side('Z',0)
#         if key=='d':
#             self.rotate_side('Z',0)
#         if key=='w':
#             self.rotate_side('Z',0)
#         if key=='s':
#             self.rotate_side('Z',0)
#         if key=='q':
#             self.rotate_side('Z',0)
#         if key=='e':
#             self.rotate_side('Z',0)

# if __name__ == '__main__':
#     app = Ursina()
#     game = CubeDisplay()
#     app.run()


#sajat de ugyan ugy mukodik mint a gpt kod
from ursina import *
import cubeModel
import copy

class CubeDisplay(Entity):
    def __init__(self):
        super().__init__()
        window.borderless = False
        window.fullscreen = False
        window.exit_button.visible = False
        window.fps_counter.enabled = True
        self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
        self.OrginalCoordinates=[]
        self.affected_cubes = []
        Entity(model='quad', scale=60, texture='white_cube', rotation_x=90, y=-5, color=color.light_gray)
        
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.load_game()

    def load_game(self):
        self.PARENT = Entity(model=self.cube_model,color=color.black)
        self.CUBES = []
        self.animation_time = 0.1
        self.create_cube_positions()
        self.cubes_axes = {'X': 'X', 'Y': 'Y', 'Z': 'Z'}

    def rotate_side(self, side_name, line_number):
        # rotation_axis = self.cubes_axes[side_name]
        
        # self.reparent_to_scene()
        # self.affected_cubes = []
        # self.OrginalCoordinates=[]
        # for cube in self.CUBES:
        #     x, y, z = cube.Entity.position
        #     if (side_name == 'X' and round(x, 1) == line_number) or \
        #         (side_name == 'Y' and round(y, 1) == line_number) or \
        #         (side_name == 'Z' and round(z, 1) == line_number):
        #         # if rotation_axis == 'X':
        #         #     cube.Entity.rotation_x += 90  # Itt közvetlenül frissítjük a rotációt
        #         # elif rotation_axis == 'Y':
        #         #     cube.Entity.rotation_y += 90
        #         # elif rotation_axis == 'Z':
        #         #     cube.Entity.rotation_z += 90

        #         # # Frissítjük a világpozíciót és világrotációt
        #         # cube.Entity.position = round(cube.Entity.world_position, 1)
        #         # cube.Entity.rotation = cube.Entity.world_rotation
        #         self.affected_cubes.append(cube)
                
            
        # for c in self.affected_cubes:
        #     print(c.Id,c.Entity.position)
        # self.PARENT.position = (line_number, 1, 1)
        # for cube in self.affected_cubes:
        #     cube.Entity.parent = self.PARENT
        
        # # self.PARENT.animate_rotation_x(90, duration=self.animation_time)
        # self.PARENT.rotation_x += 90







        # rotation_axis = self.cubes_axes[side_name]
        
        # self.reparent_to_scene()
        # self.affected_cubes = []
        # for cube in self.CUBES:
        #     x, y, z = cube.Entity.position
        #     if (side_name == 'X' and round(x, 1) == line_number) or \
        #     (side_name == 'Y' and round(y, 1) == line_number) or \
        #     (side_name == 'Z' and round(z, 1) == line_number):
        #         self.affected_cubes.append(cube)
        
        # self.PARENT.position = (line_number, line_number, line_number)
        # for cube in self.affected_cubes:
        #     cube.Entity.parent = self.PARENT
        
        # if rotation_axis == 'X':
        #     self.PARENT.animate_rotation_x(90, duration=self.animation_time)
        # elif rotation_axis == 'Y':
        #     self.PARENT.animate_rotation_y(90, duration=self.animation_time)
        # elif rotation_axis == 'Z':
        #     self.PARENT.animate_rotation_z(90, duration=self.animation_time)




        rotation_axis = self.cubes_axes[side_name]
    
        self.reparent_to_scene()
        self.affected_cubes = []
        
        # Calculate the center position for rotation
        center_pos = {'X': (line_number, 1, 1),
                    'Y': (1, line_number, 1),
                    'Z': (1, 1, line_number)}
        
        # Find affected cubes
        for cube in self.CUBES:
            x, y, z = cube.Entity.position
            if (side_name == 'X' and round(x, 1) == line_number) or \
            (side_name == 'Y' and round(y, 1) == line_number) or \
            (side_name == 'Z' and round(z, 1) == line_number):
                self.affected_cubes.append(cube)
        
        # Set the parent's position to the center of rotation
        self.PARENT.position = center_pos[side_name]
        
        # Parent the affected cubes before rotation
        for cube in self.affected_cubes:
            # Store original world position
            original_pos = cube.Entity.world_position
            cube.Entity.parent = self.PARENT
            # Maintain world position after parenting
            cube.Entity.world_position = original_pos
        
        # Perform rotation animation
        if rotation_axis == 'X':
            self.PARENT.animate_rotation_x(90, duration=self.animation_time)
        elif rotation_axis == 'Y':
            self.PARENT.animate_rotation_y(90, duration=self.animation_time)
        elif rotation_axis == 'Z':
            self.PARENT.animate_rotation_z(90, duration=self.animation_time)
        
        # After animation completes, update positions
        invoke(self.reparent_to_scene, delay=self.animation_time + 0.1)


    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.Entity.parent == self.PARENT:
                # Store the world position and rotation
                world_pos = cube.Entity.world_position
                world_rot = cube.Entity.world_rotation
                
                # Reparent to scene
                cube.Entity.parent = scene
                
                # Restore world position and rotation
                cube.Entity.world_position = world_pos
                cube.Entity.world_rotation = world_rot
                
                # Round positions to prevent floating point errors
                cube.Entity.position = Vec3(
                    round(cube.Entity.position.x, 1),
                    round(cube.Entity.position.y, 1),
                    round(cube.Entity.position.z, 1)
                )
        
        # Reset parent rotation
        self.PARENT.rotation = (0, 0, 0)

    def create_cube_positions(self):
        size = 5
        index = 0
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    model = cubeModel.CubeModel(Entity(position=(i, j, k), 
                                                       model=self.cube_model, texture=self.cube_texture), index)
                    self.CUBES.append(model)
                    index += 1

    def input(self, key):
        if key == 'a':
            self.rotate_side('X', 0)
        elif key == 'd':
            self.rotate_side('X', 2)
        elif key == 'w':
            self.rotate_side('Y', 0)
        elif key == 's':
            self.rotate_side('Y', 2)
        elif key == 'q':
            self.rotate_side('Z', 0)
        elif key == 'e':
            self.rotate_side('Z', 2)
        


if __name__ == '__main__':
    app = Ursina()
    game = CubeDisplay()
    app.run()


































#gpt kod
# from ursina import *
# import cubeModel

# class CubeDisplay(Entity):
#     def __init__(self):
#         super().__init__()
#         window.borderless = False
#         window.fullscreen = False
#         window.exit_button.visible = False
#         window.fps_counter.enabled = True
#         self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'

#         Entity(model='quad', scale=60, texture='white_cube', rotation_x=90, y=-5, color=color.light_gray)
        
#         EditorCamera()
#         camera.world_position = (0, 0, -15)
#         self.load_game()

#     def load_game(self):
#         self.PARENT = Entity(model=self.cube_model, color=color.black)
#         self.CUBES = []
#         self.animation_time = 0.1
#         self.create_cube_positions()
#         self.cubes_axes = {'X': 'X', 'Y': 'Y', 'Z': 'Z'}

#     def get_side_center(self, side_name, line_number):
#         """ A PARENT objektum középpontját adja vissza a megfelelő tengelyhez. """
#         if side_name == 'X':
#             return (line_number, 1, 1)
#         elif side_name == 'Y':
#             return (1, line_number, 1)
#         elif side_name == 'Z':
#             return (1, 1, line_number)

#     def rotate_side(self, side_name, line_number):
#         rotation_axis = self.cubes_axes[side_name]

#         # self.reparent_to_scene()  # Biztosítjuk, hogy minden kocka alapállapotban van
#         affected_cubes = []

#         for cube in self.CUBES:
#             x, y, z = cube.Entity.position
#             if (side_name == 'X' and round(x, 1) == line_number) or \
#             (side_name == 'Y' and round(y, 1) == line_number) or \
#             (side_name == 'Z' and round(z, 1) == line_number):
#                 affected_cubes.append(cube)

#         # 📌 A PARENT pontos középpontja
#         self.PARENT.position = Vec3(line_number if side_name == 'X' else 1, 
#                                     line_number if side_name == 'Y' else 1, 
#                                     line_number if side_name == 'Z' else 1)

#         # 📍 A kiválasztott kockák a PARENT alá kerülnek
#         for cube in affected_cubes:
#             cube.Entity.parent = self.PARENT

#         # 🔄 Közvetlen forgatás animáció nélkül
#         if rotation_axis == 'X':
#             self.PARENT.rotation_x += 90
#         elif rotation_axis == 'Y':
#             self.PARENT.rotation_y += 90
#         elif rotation_axis == 'Z':
#             self.PARENT.rotation_z += 90

#         # 🔥 Fontos: Visszaállítjuk a kockák globális helyzetét és leválasztjuk őket a PARENT-ről
#         invoke(self.reparent_to_scene, delay=0.05)


#     def reparent_to_scene(self):
#         """ A kockák visszakerülnek a fő jelenetbe, pontos világpozícióval. """
#         for cube in self.CUBES:
#             if cube.Entity.parent == self.PARENT:
#                 world_pos, world_rot = cube.Entity.world_position, cube.Entity.world_rotation
#                 cube.Entity.parent = scene
#                 cube.Entity.position = Vec3(round(world_pos.x, 1), round(world_pos.y, 1), round(world_pos.z, 1))
#                 cube.Entity.rotation = world_rot
#         self.PARENT.rotation = 0

#     def create_cube_positions(self):
#         """ A 3x3x3 Rubik-kocka létrehozása. """
#         size = 3
#         index = 0
#         for i in range(size):
#             for j in range(size):
#                 for k in range(size):
#                     model = cubeModel.CubeModel(Entity(position=(i, j, k), 
#                                                        model=self.cube_model, texture=self.cube_texture), index)
#                     self.CUBES.append(model)
#                     index += 1

#     def input(self, key):
#         """ Billentyűzetes vezérlés a rétegek forgatására. """
#         if key == 'a':
#             self.rotate_side('X', 0)
#         elif key == 'd':
#             self.rotate_side('X', 2)
#         elif key == 'w':
#             self.rotate_side('Y', 0)
#         elif key == 's':
#             self.rotate_side('Y', 2)
#         elif key == 'q':
#             self.rotate_side('Z', 0)
#         elif key == 'e':
#             self.rotate_side('Z', 2)

# if __name__ == '__main__':
#     app = Ursina()
#     game = CubeDisplay()
#     app.run()


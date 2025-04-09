

#majdnem mukodik

from ursina import *
import numpy as np
import copy

class RubiksCube(Entity):
    def __init__(self, size=3):
        super().__init__()
        # Use the custom model and texture
        self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
        self.size = size
        self.cube_size = 0.95  # Size of each individual cube
        self.spacing = 0  # Space between cubes
        self.cubes = []
        self.rotating = False
        self.rotation_duration = 0.3
        
        # Create parent entity for rotations
        self.rotater = Entity()
        
        # Create the cube
        self.create_cube()
        
        # Track the current layer for rotation
        self.current_layer = 0
        
        # Create UI
        self.create_ui()
        
        # Debug mode
        self.debug = False
    
    def create_ui(self):
        # Layer indicator
        self.layer_text = Text(text=f"Layer: {self.current_layer}", position=(-0.7, 0.45))
        
        # Instructions
        instructions = [
            "Controls:",
            "1-9: Select layer",
            "X: Rotate X-axis",
            "Y: Rotate Y-axis",
            "Z: Rotate Z-axis",
            "Hold Shift: Rotate counter-clockwise",
            "D: Toggle debug mode"
        ]
        # Text(text="\n".join(instructions), position=(-0.7, 0.35), scale=1.5, color=color.light_gray)
    
    def create_cube(self):
        # Create cubes
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    # Only create cubes on the outside for optimization
                    if x == 0 or x == self.size-1 or y == 0 or y == self.size-1 or z == 0 or z == self.size-1:
                        # Create cube with custom model and texture
                        cube = Entity(
                            model=self.cube_model,
                            texture=self.cube_texture,
                            position=(x-(self.size-1)/2, y-(self.size-1)/2, z-(self.size-1)/2),
                            scale=self.cube_size
                        )
                        
                        # Store cube with its grid position
                        self.cubes.append({
                            'entity': cube,
                            'grid': (x, y, z)
                        })
    
    def get_layer_cubes(self, axis, layer_index):
        """Get all cubes in a specific layer."""
        layer_cubes = []
        for cube_data in self.cubes:
            grid_pos = cube_data['grid']
            
            if axis == 'x' and grid_pos[0] == layer_index:
                layer_cubes.append(cube_data)
            elif axis == 'y' and grid_pos[1] == layer_index:
                layer_cubes.append(cube_data)
            elif axis == 'z' and grid_pos[2] == layer_index:
                layer_cubes.append(cube_data)
        
        return layer_cubes
    
    def rotate_layer(self, axis, layer_index, clockwise=True):
        """Rotate a specific layer around an axis."""
        if self.rotating:
            return
        
        self.rotating = True
        cube_data_list = self.get_layer_cubes(axis, layer_index)
        
        if not cube_data_list:
            self.rotating = False
            return
        
        # Reset rotater
        self.rotater.position = (0, 0, 0)
        self.rotater.rotation = (0, 0, 0)
        
        # Parent cubes to rotater
        for cube_data in cube_data_list:
            cube = cube_data['entity']
            # Store world position before parenting
            world_pos = cube.world_position
            # Parent to rotater
            cube.parent = self.rotater
            # Restore world position
            cube.world_position = world_pos
        
        # Set rotation direction
        direction = 1 if clockwise else -1
        
        # # Perform rotation animation
        if axis == 'x':
            self.rotater.animate_rotation_x(90 * direction, duration=self.rotation_duration, curve=curve.linear)
        elif axis == 'y':
            self.rotater.animate_rotation_y(90 * direction, duration=self.rotation_duration, curve=curve.linear)
        elif axis == 'z':
            self.rotater.animate_rotation_z(90 * direction, duration=self.rotation_duration, curve=curve.linear)
        
        # After animation completes, update grid positions and reparent
        invoke(lambda: self.finish_rotation(axis, layer_index, cube_data_list, clockwise), 
               delay=self.rotation_duration + 0.1)
    
    def finish_rotation(self, axis, layer_index, cube_data_list, clockwise):
        """Finish rotation by updating grid positions and reparenting cubes."""
        # Create a temporary list to store new grid positions
        new_grid_positions = {} 
        
        # Calculate new grid positions based on rotation
        for cube_data in cube_data_list:
            entity = cube_data['entity']
            x, y, z = cube_data['grid']
            
            # Calculate new grid position based on rotation
            new_x, new_y, new_z = x, y, z  # Default: no change
            
            if axis == 'x':
                # X-axis rotation (around the YZ plane)
                if clockwise:
                    new_y, new_z = z, self.size - 1 - y
                else:
                    new_y, new_z = self.size - 1 - z, y
            
            elif axis == 'y':
                # Y-axis rotation (around the XZ plane)
                if clockwise:
                    new_x, new_z = self.size - 1 - z, x
                else:
                    new_x, new_z = z, self.size - 1 - x
            
            elif axis == 'z':
                # Z-axis rotation (around the XY plane)
                if clockwise:
                    new_x, new_y = y, self.size - 1 - x
                else:
                    new_x, new_y = self.size - 1 - y, x
            
            # Store the new grid position
            new_grid_positions[entity] = (new_x, new_y, new_z)
            
            if self.debug:
                print(f"Cube at {(x,y,z)} moved to {(new_x, new_y, new_z)}")
        
        # Update grid positions and reparent cubes
        for cube_data in cube_data_list:
            entity = cube_data['entity']
            
            # Update grid position
            if entity in new_grid_positions:
                cube_data['grid'] = new_grid_positions[entity]
            
            # Get updated grid position
            x, y, z = cube_data['grid']
            
            # Calculate new position based on grid
            new_pos = Vec3(
                x - (self.size-1)/2,
                y - (self.size-1)/2,
                z - (self.size-1)/2
            )
            
            # Store world rotation
            world_rot = entity.world_rotation
            
            # Reparent to scene
            entity.parent = scene
            
            # Set position and restore rotation
            entity.position = new_pos
            entity.rotation = world_rot
        
        # Reset rotater
        self.rotater.rotation = (0, 0, 0)
        
        # Allow new rotations
        self.rotating = False
    
    def rotate_x(self, layer, clockwise=True):
        """Rotate a layer around the X axis."""
        self.rotate_layer('x', layer, clockwise)
    
    def rotate_y(self, layer, clockwise=True):
        """Rotate a layer around the Y axis."""
        self.rotate_layer('y', layer, clockwise)
    
    def rotate_z(self, layer, clockwise=True):
        """Rotate a layer around the Z axis."""
        self.rotate_layer('z', layer, clockwise)
    
    def update_layer(self, layer):
        """Update the current layer."""
        if layer >= 0 and layer < self.size:
            self.current_layer = layer
            self.layer_text.text = f"Layer: {self.current_layer}"
    
    def input(self, key):
        """Handle input."""
        # Layer selection (1-9)
        if key.isdigit() and 1 <= int(key) <= 9:
            layer = int(key) - 1
            if layer < self.size:
                self.update_layer(layer)
        
        # Rotation keys
        elif key == 'x':
            self.rotate_x(self.current_layer, not held_keys['shift'])
        elif key == 'y':
            self.rotate_y(self.current_layer, not held_keys['shift'])
        elif key == 'z':
            self.rotate_z(self.current_layer, not held_keys['shift'])
        
        # Debug mode
        elif key == 'd':
            self.debug = not self.debug
            print(f"Debug mode: {'ON' if self.debug else 'OFF'}")

# Main application
if __name__ == '__main__':
    app = Ursina()
    
    # Set up window
    window.title = "Rubik's Cube"
    window.borderless = False
    window.fullscreen = False
    window.exit_button.visible = True
    window.fps_counter.enabled = True
    
    # Create ground
    Entity(model='plane', scale=20, color=color.dark_gray, y=-5)
    
    # Set up camera
    camera_entity = EditorCamera()
    camera.position = (5, 5, -10)
    camera.look_at(Vec3(0, 0, 0))
    
    # Create cube (change size parameter for different cube dimensions)
    cube = RubiksCube(size=6)
    
    app.run()



from ursina import *
import numpy as np
import time

class RubiksCube(Entity):
    def __init__(self, size=3):
        super().__init__()
        # Use the custom model and texture
        self.cube_model, self.cube_texture = 'models/custom_cube', 'textures/rubik_texture'
        self.size = size
        self.cube_size = 0.95  # Size of each individual cube
        self.spacing = 0.05    # Space between cubes
        self.cubes = []
        self.rotating = False
        self.rotation_duration = 0.5
        
        # Create the cube
        self.create_cube()
        
        # Track the current layer for rotation
        self.current_layer = 0
        
        # Create UI
        self.create_ui()
        
        # Debug mode
        self.debug = True  # Set to True to help debug
        
        # Auto-rotation variables
        self.auto_rotating = False
        self.rotations_count = 0
        self.total_rotations = 100  # Number of rotations to perform when 'g' is pressed
    
    def create_ui(self):
        # Layer indicator
        self.layer_text = Text(text=f"Layer: {self.current_layer}", position=(-0.7, 0.45))
        
        # Auto-rotation counter
        self.rotation_counter = Text(text="", position=(-0.7, 0.4))
        
        # Instructions
        instructions = [
            "Controls:",
            "1-9: Select layer",
            "X: Rotate X-axis",
            "Y: Rotate Y-axis",
            "Z: Rotate Z-axis",
            "Hold Shift: Rotate counter-clockwise",
            "G: Auto-rotate 100 times",
            "D: Toggle debug mode"
        ]
        # Text(text="\n".join(instructions), position=(-0.7, 0.35), scale=1.5, color=color.light_gray)
    
    def create_cube(self, for_Is_Solved=False, size=2):
        # Create cubes
        id=0
        if for_Is_Solved:
            result=[]
            for x in range(size):
                for y in range(size):
                    for z in range(size):
                        # Only create cubes on the outside for optimization
                        if x == 0 or x == size-1 or y == 0 or y == size-1 or z == 0 or z == size-1:
                            # Create cube with custom model and texture
                            cube = Entity(
                                model='models/custom_cube',
                                texture='textures/rubik_texture',
                                position=(x-(size-1)/2, y-(size-1)/2, z-(size-1)/2),
                                scale=size
                            )
                            
                            # Store cube with its grid position
                            result.append({
                                'entity': cube,
                                'grid': (x, y, z),
                                'id': id
                            })
                            id+=1
            return result
        else:
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
                                'grid': (x, y, z),
                                'id': id
                            })
                            id+=1
        
    
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
    
    def rotate_layer(self, axis, layer_index, clockwise=True, visualize=True):
        """Rotate a specific layer around an axis."""
        if self.rotating:
            if self.debug:
                print("Already rotating, ignoring rotation request")
            return
        
        self.rotating = True
        if self.debug:
            print(f"Starting rotation: axis={axis}, layer={layer_index}, clockwise={clockwise}")
        
        cube_data_list = self.get_layer_cubes(axis, layer_index)
        
        if not cube_data_list:
            if self.debug:
                print(f"No cubes found in layer {layer_index} for axis {axis}")
            self.rotating = False
            self.check_continue_auto_rotation()
            return
        
        # Create a parent entity for rotation
        rotater = Entity()
        
        # Parent cubes to rotater
        for cube_data in cube_data_list:
            cube = cube_data['entity']
            # Store world position before parenting
            world_pos = Vec3(cube.world_position.x, cube.world_position.y, cube.world_position.z)
            # Parent to rotater
            cube.parent = rotater
            # Restore world position
            cube.world_position = world_pos
        
        # Set rotation direction
        direction = 1 if clockwise else -1
        
        # Perform rotation
        if axis == 'x' and visualize:
            rotater.animate_rotation_x(90 * direction, duration=self.rotation_duration)
            print('belepett ide')
        elif axis == 'y' and visualize:
            rotater.animate_rotation_y(90 * direction, duration=self.rotation_duration)
        elif axis == 'z' and visualize:
            rotater.animate_rotation_z(90 * direction, duration=self.rotation_duration)
        
        # After animation completes, update grid positions
        if visualize:
            invoke(lambda: self.finish_rotation(axis, layer_index, cube_data_list, rotater, clockwise), 
               delay=self.rotation_duration + 0.1)
        else:
            self.finish_rotation(axis, layer_index, cube_data_list, rotater, clockwise)
    
    def finish_rotation(self, axis, layer_index, cube_data_list, rotater, clockwise):
        """Finish rotation by updating grid positions."""
        if self.debug:
            print(f"Finishing rotation: axis={axis}, layer={layer_index}")
            
        # Create a temporary dictionary to store new grid positions
        new_grid_positions = {}
        
        # First pass: calculate new grid positions
        for cube_data in cube_data_list:
            entity = cube_data['entity']
            x, y, z = cube_data['grid']
            
            # Calculate new grid position based on rotation
            if axis == 'x':
                # X-axis rotation (around the x-axis) - FIXED
                if clockwise:  # Clockwise looking from positive x towards origin
                    new_grid_positions[entity] = (x, self.size-1-z, y)
                else:  # Counter-clockwise
                    new_grid_positions[entity] = (x, z, self.size-1-y)
            
            elif axis == 'y':
                # Y-axis rotation (around the y-axis)
                if clockwise:  # Clockwise looking from positive y towards origin (top view)
                    new_grid_positions[entity] = (z, y, self.size-1-x)
                else:  # Counter-clockwise
                    new_grid_positions[entity] = (self.size-1-z, y, x)
            
            elif axis == 'z':
                # Z-axis rotation (around the z-axis)
                if clockwise:  # Clockwise looking from positive z towards origin
                    new_grid_positions[entity] = (y, self.size-1-x, z)
                else:  # Counter-clockwise
                    new_grid_positions[entity] = (self.size-1-y, x, z)
        
        # Second pass: update grid positions and reparent cubes
        for cube_data in cube_data_list:
            entity = cube_data['entity']
            
            # Store original grid for debugging
            original_grid = cube_data['grid']
            
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
            
            # Get the current world rotation after the animation
            world_rot = Vec3(entity.world_rotation.x, entity.world_rotation.y, entity.world_rotation.z)
            
            # Reparent to scene
            entity.parent = scene
            
            # Set position
            entity.position = new_pos
            
            # Preserve the rotation that was applied during the animation
            entity.rotation = world_rot
            
            if self.debug:
                print(f"Axis: {axis}, Direction: {'CW' if clockwise else 'CCW'}")
                print(f"Cube moved from {original_grid} to {cube_data['grid']}")
        
        # Destroy the rotater entity
        destroy(rotater)
        
        # Allow new rotations
        self.rotating = False
        if self.debug:
            print("Rotation completed, ready for next rotation")
        
        # If we're auto-rotating, continue with the next rotation
        self.check_continue_auto_rotation()
    
    def check_continue_auto_rotation(self):
        """Check if we should continue with auto-rotation."""
        if self.auto_rotating:
            self.rotations_count += 1
            self.rotation_counter.text = f"Auto-rotations: {self.rotations_count}/{self.total_rotations}"
            
            if self.rotations_count < self.total_rotations:
                # Schedule the next rotation with a small delay
                invoke(self.random_rotation, delay=0.1)
            else:
                # We've completed all rotations
                self.auto_rotating = False
                self.rotations_count = 0
                self.rotation_counter.text = "Auto-rotation complete!"
                invoke(lambda: setattr(self.rotation_counter, 'text', ''), delay=2)
    
    def rotate_x(self, layer, clockwise=True, visualize=True):
        """Rotate a layer around the X axis."""
        self.rotate_layer('x', layer, clockwise, visualize)
    
    def rotate_y(self, layer, clockwise=True, visualize=True):
        """Rotate a layer around the Y axis."""
        self.rotate_layer('y', layer, clockwise, visualize)
    
    def rotate_z(self, layer, clockwise=True, visualize=True):
        """Rotate a layer around the Z axis."""
        self.rotate_layer('z', layer, clockwise, visualize)
    
    def update_layer(self, layer):
        """Update the current layer."""
        if layer >= 0 and layer < self.size:
            self.current_layer = layer
            self.layer_text.text = f"Layer: {self.current_layer}"
    
    def random_rotation(self):
        """Perform a random rotation."""
        if self.rotating:
            if self.debug:
                print("Already rotating, skipping random rotation")
            return
            
        randAxis = np.random.randint(0, 3)
        randLayer = np.random.randint(0, self.size)
        randClockwise = bool(np.random.randint(0, 2))
        
        if self.debug:
            print(f"Random rotation: axis={randAxis}, layer={randLayer}, clockwise={randClockwise}")
            
        if randAxis == 0:
            self.rotate_x(randLayer, randClockwise)
        elif randAxis == 1:
            self.rotate_y(randLayer, randClockwise)
        else:
            self.rotate_z(randLayer, randClockwise)
    
    def start_auto_rotation(self):
        """Start auto-rotating the cube."""
        if self.auto_rotating:
            # Already auto-rotating, do nothing
            return
            
        self.auto_rotating = True
        self.rotations_count = 0
        self.rotation_counter.text = f"Auto-rotations: {self.rotations_count}/{self.total_rotations}"
        
        # Start the first random rotation
        self.random_rotation()
    
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
        elif key == 'g':
            self.start_auto_rotation()

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
    camera.position = (0, 0, 0)
    camera.look_at(Vec3(0, 0, 0))
    
    # Create cube (change size parameter for different cube dimensions)
    cube = RubiksCube(size=10)
    
    app.run()
import os
from ursina import *
import time
import numpy as np

class RubiksCubeEnv:
    """A Gym-like environment for the Rubik's Cube."""
    
    def __init__(self, size=3, headless=False):
        self.size = size
        self.headless = headless
        self.app = None
        self.cube = None
        
        # Define action space
        # Actions: (axis, layer, direction)
        # axis: 0=x, 1=y, 2=z
        # layer: 0 to size-1
        # direction: 0=clockwise, 1=counterclockwise
        self.action_space_size = 3 * size * 2
        
        # For tracking steps
        self.steps = 0
        self.max_steps = 200  # Increased from 100 to give more time to solve
        
        # Color mapping
        self.color_map = {
            0: 'red',     # Front face
            1: 'orange',  # Back face
            2: 'blue',    # Left face
            3: 'green',   # Right face
            4: 'white',   # Top face
            5: 'yellow'   # Bottom face
        }
        
        self.initialize_environment()
    
    def initialize_environment(self):
        """Initialize the Ursina environment and Rubik's Cube."""
        if self.app is None:
            # Set headless mode BEFORE creating the Ursina app
            if self.headless:
                # Configure Ursina for headless mode
                from ursina import application
                application.development_mode = False
                application.headless = True
            
            # Now create the Ursina app
            self.app = Ursina(borderless=False, fullscreen=False)
        
        if self.cube is None:
            from main import RubiksCube
            self.cube = RubiksCube(size=self.size)
            # Disable input handling from the original cube
            self.cube.input = lambda key: None
    
    def reset(self):
        """Reset the environment to a new episode."""
        # Destroy existing cube if any
        if self.cube:
            destroy(self.cube)
        
        # Create a new cube
        from main import RubiksCube
        self.cube = RubiksCube(size=self.size)
        self.cube.input = lambda key: None  # Disable input handling
        
        # Scramble the cube with random moves
        self.scramble(20)  # Apply 20 random moves
        
        # Reset step counter
        self.steps = 0
        
        # Return the initial state
        return self.get_state()
    
    def scramble(self, num_moves):
        """Scramble the cube with random moves."""
        if num_moves <= 0:
            return
            
        print(f"Scrambling cube with {num_moves} random moves...")
        
        # Store initial state to verify scrambling worked
        initial_state = self.get_state().copy()
        
        # Track the moves we've made
        moves_made = []
        
        for i in range(num_moves):
            # Choose a random move
            axis_idx = np.random.randint(0, 3)  # 0=x, 1=y, 2=z
            layer = np.random.randint(0, self.size)
            clockwise = np.random.choice([True, False])
            
            axis = ['x', 'y', 'z'][axis_idx]
            
            # Apply the move
            if axis == 'x':
                self.cube.rotate_x(layer, clockwise, False)
            elif axis == 'y':
                self.cube.rotate_y(layer, clockwise, False)
            else:
                self.cube.rotate_z(layer, clockwise, False)
            
            # Record the move
            moves_made.append((axis, layer, clockwise))
            
            # Wait for rotation to complete
            while self.cube.rotating:
                if not self.headless:
                    time.dt = 1/60  # Simulate time passing
                    self.app.step()
                else:
                    # In headless mode, just update the cube's state without rendering
                    self.cube.rotating = False  # Force rotation to complete immediately
        
        # Verify scrambling worked
        new_state = self.get_state()
        state_changed = not np.array_equal(initial_state, new_state)
        
        if not state_changed and num_moves > 0:
            print("WARNING: Cube appears to still be in same state after scrambling!")
            print("This suggests an issue with state representation or scrambling.")
            print(f"Moves made: {moves_made}")
    
    def step(self, action):
        """Take a step in the environment by applying an action."""
        # Decode action
        axis_idx = action // (self.size * 2)
        remaining = action % (self.size * 2)
        layer = remaining // 2
        clockwise = remaining % 2 == 0
        
        axis = ['x', 'y', 'z'][axis_idx]
        
        # Apply the action
        if axis == 'x':
            self.cube.rotate_x(layer, clockwise, False)
        elif axis == 'y':
            self.cube.rotate_y(layer, clockwise, False)
        else:
            self.cube.rotate_z(layer, clockwise, False)
        
        # Wait for rotation to complete
        while self.cube.rotating:
            if not self.headless:
                time.dt = 1/60  # Simulate time passing
                self.app.step()
            else:
                # In headless mode, just update the cube's state without rendering
                self.cube.rotating = False  # Force rotation to complete immediately
        
        # Increment step counter
        self.steps += 1
        
        # Get new state
        new_state = self.get_state()
        
        # Check if solved
        solved = self.is_solved()
        
        # Calculate reward
        reward = self.calculate_reward(solved)
        
        # Check if episode is done
        done = solved or self.steps >= self.max_steps
        
        # Additional info
        info = {
            'solved': solved,
            'steps': self.steps
        }
        
        return new_state, reward, done, info
    
    def get_face_colors(self, face_idx):
        """Get the colors of all stickers on a specific face."""
        # Map face index to face name and coordinates
        face_map = {
            0: ('z', self.size-1),  # Front face (z = size-1)
            1: ('z', 0),            # Back face (z = 0)
            2: ('x', 0),            # Left face (x = 0)
            3: ('x', self.size-1),  # Right face (x = size-1)
            4: ('y', self.size-1),  # Top face (y = size-1)
            5: ('y', 0)             # Bottom face (y = 0)
        }
        
        axis, value = face_map[face_idx]
        
        # Get all cubes on this face
        face_cubes = []
        for cube_data in self.cube.cubes:
            grid_pos = cube_data['grid']
            
            if axis == 'x' and grid_pos[0] == value:
                face_cubes.append(cube_data)
            elif axis == 'y' and grid_pos[1] == value:
                face_cubes.append(cube_data)
            elif axis == 'z' and grid_pos[2] == value:
                face_cubes.append(cube_data)
        
        # Initialize color grid
        colors = np.zeros((self.size, self.size), dtype=int)
        
        # Fill in colors based on cube orientations
        for cube_data in face_cubes:
            entity = cube_data['entity']
            grid_pos = cube_data['grid']
            
            # Determine position on the face
            if axis == 'x':
                i, j = grid_pos[1], grid_pos[2]
                if value == 0:  # Left face
                    color_idx = self.get_color_from_rotation(entity, 2)  # Left face color
                else:  # Right face
                    color_idx = self.get_color_from_rotation(entity, 3)  # Right face color
            elif axis == 'y':
                i, j = grid_pos[0], grid_pos[2]
                if value == 0:  # Bottom face
                    color_idx = self.get_color_from_rotation(entity, 5)  # Bottom face color
                else:  # Top face
                    color_idx = self.get_color_from_rotation(entity, 4)  # Top face color
            else:  # axis == 'z'
                i, j = grid_pos[0], grid_pos[1]
                if value == 0:  # Back face
                    color_idx = self.get_color_from_rotation(entity, 1)  # Back face color
                else:  # Front face
                    color_idx = self.get_color_from_rotation(entity, 0)  # Front face color
            
            # Normalize i, j to be within [0, size-1]
            i = min(max(i, 0), self.size-1)
            j = min(max(j, 0), self.size-1)
            
            colors[i, j] = color_idx
        
        return colors
    
    def get_color_from_rotation(self, entity, face_idx):
        """Determine the color of a face based on the cube's rotation."""
        # This is a simplified approach - in a real implementation, you would need to
        # calculate the actual face color based on the entity's rotation matrix
        
        # For simplicity, we'll use the face_idx directly as the color index
        # In a real implementation, you would compute this based on the entity's rotation
        return face_idx
    

    def get_state(self):
        """Convert the cube state to a format suitable for the neural network using cube IDs."""
        # For an NxNxN cube, we track which cubie ID is at each position
        
        # Calculate the number of cubies on the outside of the cube
        # For a 2x2x2 cube, this is 8 cubies
        # For a 3x3x3 cube, this is 26 cubies (all except the center)
        num_positions = 0
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    if x == 0 or x == self.size-1 or y == 0 or y == self.size-1 or z == 0 or z == self.size-1:
                        num_positions += 1
        
        # Initialize state array - one position for each possible cube position
        state = np.zeros(num_positions)
        
        # Create a mapping from grid position to index in the state array
        grid_to_index = {}
        index = 0
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    if x == 0 or x == self.size-1 or y == 0 or y == self.size-1 or z == 0 or z == self.size-1:
                        grid_to_index[(x, y, z)] = index
                        index += 1
        
        # For each cubie, record its ID at its current position
        for cube_data in self.cube.cubes:
            # Get the cubie's ID
            cubie_id = cube_data['id']
            
            # Get its current position in the grid
            entity = cube_data['entity']
            current_grid_pos = self.get_current_grid_position(entity)
            
            # Get the index in our state array for this grid position
            pos_index = grid_to_index[current_grid_pos]
            
            # Store the cubie ID at this position
            state[pos_index] = cubie_id
        
        
    
        return state
    
    def get_current_grid_position(self, entity):
        """Convert entity position to grid position."""
        # Calculate grid position based on entity position
        # Adjust these calculations based on your specific implementation
        
        # Convert from world coordinates to grid coordinates
        x = round(entity.x + (self.size-1)/2)
        y = round(entity.y + (self.size-1)/2)
        z = round(entity.z + (self.size-1)/2)
        
        # Ensure values are within valid range
        x = max(0, min(x, self.size - 1))
        y = max(0, min(y, self.size - 1))
        z = max(0, min(z, self.size - 1))
        
        return (x, y, z)
    
    def is_solved(self):
        """Check if the cube is solved."""
        # A cube is solved when each face has a single color
        
        # For each face
        from main import RubiksCube
        base_cube= RubiksCube.create_cube(True,self.size)

        for i in base_cube:
            matching_cubes = [s for s in self.cube.cubes if s['id'] == i['id']]

            if not matching_cubes or matching_cubes[0]['grid'] != i['grid']:
                
                return False
            
        return True
        
    
    def calculate_reward(self, solved):
        """Calculate the reward for the current state."""
        # Base reward
        if solved:
            return 100.0  # Large positive reward for solving
        
        # Calculate how many stickers are in the correct position
        correct_stickers = 0
        total_stickers = 6 * self.size * self.size
        
        # For each face
        for face_idx in range(6):
            face_colors = self.get_face_colors(face_idx)
            
            # Get the center color (or any reference color if size < 3)
            if self.size >= 3:
                center_color = face_colors[self.size//2, self.size//2]
            else:
                center_color = face_colors[0, 0]
            
            # Count correct stickers
            for i in range(self.size):
                for j in range(self.size):
                    if face_colors[i, j] == center_color:
                        correct_stickers += 1
        
        # Calculate progress reward (normalized between 0 and 1)
        progress_reward = correct_stickers / total_stickers
        
        # Penalty for each step to encourage efficiency
        step_penalty = -0.1
        
        return step_penalty + progress_reward * 10  # Scale up the progress reward
    
    def close(self):
        """Close the environment."""
        if self.app:
            try:
                # Try different methods to close Ursina
                if hasattr(self.app, 'quit'):
                    self.app.quit()
                elif hasattr(self.app, 'destroy'):
                    self.app.destroy()
                elif hasattr(self.app, 'exit'):
                    self.app.exit()
                else:
                    # If no direct method exists, try to access the application module
                    from ursina import application
                    application.quit()
            except Exception as e:
                print(f"Warning: Could not properly close Ursina application: {e}")
                print("This is not critical and training has completed successfully.")
        
        self.app = None

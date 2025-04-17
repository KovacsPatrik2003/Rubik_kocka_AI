import numpy as np
from main import RubiksCube, Ursina
from ursina import application, time, destroy

class RubiksCubeEnv:
    """A Gym-like environment for the Rubik's Cube."""
    
    def __init__(self, size=3, headless=False):
        self.size = size
        self.headless = headless
        self.app = None
        self.cube = None
        self.initialize_environment()
        
        # Define action space
        # Actions: (axis, layer, direction)
        # axis: 0=x, 1=y, 2=z
        # layer: 0 to size-1
        # direction: 0=clockwise, 1=counterclockwise
        self.action_space_size = 3 * size * 2
        
        # For tracking steps
        self.steps = 0
        self.max_steps = 100  # Maximum steps before episode terminates
    
    def initialize_environment(self):
        """Initialize the Ursina environment and Rubik's Cube."""
        if self.app is None:
            self.app = Ursina(borderless=False, fullscreen=False)
            if self.headless:
                application.headless = True
        
        if self.cube is None:
            self.cube = RubiksCube(size=self.size)
            # Disable input handling from the original cube
            self.cube.input = lambda key: None
    
    def reset(self):
        """Reset the environment to a new episode."""
        # Destroy existing cube if any
        if self.cube:
            destroy(self.cube)
        
        # Create a new cube
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
        for _ in range(num_moves):
            axis = np.random.choice(['x', 'y', 'z'])
            layer = np.random.randint(0, self.size)
            clockwise = np.random.choice([True, False])
            
            if axis == 'x':
                self.cube.rotate_x(layer, clockwise)
            elif axis == 'y':
                self.cube.rotate_y(layer, clockwise)
            else:
                self.cube.rotate_z(layer, clockwise)
            
            # Wait for rotation to complete
            while self.cube.rotating:
                time.dt = 1/60  # Simulate time passing
                self.app.step()
    
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
            self.cube.rotate_x(layer, clockwise)
        elif axis == 'y':
            self.cube.rotate_y(layer, clockwise)
        else:
            self.cube.rotate_z(layer, clockwise)
        
        # Wait for rotation to complete
        while self.cube.rotating:
            time.dt = 1/60  # Simulate time passing
            self.app.step()
        
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
    
    def get_state(self):
        """Convert the cube state to a format suitable for the neural network."""
        # Create a state representation based on the colors of each face
        # This is a simplified representation - you might want to enhance this
        
        # Initialize state array
        # For each cube, we'll store its grid position and a one-hot encoding of its orientation
        state = np.zeros((len(self.cube.cubes), 6))
        
        for i, cube_data in enumerate(self.cube.cubes):
            # Get grid position
            x, y, z = cube_data['grid']
            
            # Normalize grid positions to [0, 1]
            state[i, 0] = x / (self.size - 1)
            state[i, 1] = y / (self.size - 1)
            state[i, 2] = z / (self.size - 1)
            
            # Get entity rotation (simplified)
            entity = cube_data['entity']
            rx, ry, rz = entity.rotation.x % 360, entity.rotation.y % 360, entity.rotation.z % 360
            
            # Normalize rotations to [0, 1]
            state[i, 3] = rx / 360
            state[i, 4] = ry / 360
            state[i, 5] = rz / 360
        
        # Flatten the state
        return state.flatten()
    
    def is_solved(self):
        """Check if the cube is solved."""
        # A cube is solved when all faces have the same color
        # This is a simplified check - you might want to enhance this
        
        # For each face (x=0, x=size-1, y=0, y=size-1, z=0, z=size-1)
        # Check if all cubes on that face have the same orientation
        
        # Get all cubes on each face
        faces = [
            [(x, y, z) for x, y, z in [cube_data['grid'] for cube_data in self.cube.cubes] if x == 0],
            [(x, y, z) for x, y, z in [cube_data['grid'] for cube_data in self.cube.cubes] if x == self.size-1],
            [(x, y, z) for x, y, z in [cube_data['grid'] for cube_data in self.cube.cubes] if y == 0],
            [(x, y, z) for x, y, z in [cube_data['grid'] for cube_data in self.cube.cubes] if y == self.size-1],
            [(x, y, z) for x, y, z in [cube_data['grid'] for cube_data in self.cube.cubes] if z == 0],
            [(x, y, z) for x, y, z in [cube_data['grid'] for cube_data in self.cube.cubes] if z == self.size-1]
        ]
        
        # Check if each face has cubes with the same orientation
        for face in faces:
            # Get entities for this face
            face_entities = [next(cube_data['entity'] for cube_data in self.cube.cubes 
                                if cube_data['grid'] == pos) for pos in face]
            
            # Check if all rotations are the same (simplified)
            rotations = [(e.rotation.x % 360, e.rotation.y % 360, e.rotation.z % 360) for e in face_entities]
            if len(set(rotations)) > 1:  # If there's more than one unique rotation
                return False
        
        return True
    
    def calculate_reward(self, solved):
        """Calculate the reward for the current state."""
        # Base reward
        if solved:
            return 100.0  # Large positive reward for solving
        
        # Penalty for each step to encourage efficiency
        step_penalty = -0.1
        
        # Calculate how "close" the cube is to being solved
        # This is a simplified heuristic - you might want to enhance this
        
        # Count how many cubes are in their correct orientation
        correct_orientations = 0
        total_cubes = len(self.cube.cubes)
        
        # Define "correct" orientations for each face
        # This is a simplified approach - you might need to adjust based on your cube implementation
        for cube_data in self.cube.cubes:
            entity = cube_data['entity']
            x, y, z = cube_data['grid']
            
            # Check if rotation is aligned with axes (0, 90, 180, 270 degrees)
            rx, ry, rz = entity.rotation.x % 90, entity.rotation.y % 90, entity.rotation.z % 90
            if rx < 1 and ry < 1 and rz < 1:  # Allow small floating point errors
                correct_orientations += 1
        
        # Calculate progress reward
        progress_reward = 0.5 * (correct_orientations / total_cubes)
        
        return step_penalty + progress_reward
    
    def close(self):
        """Close the environment."""
        if self.app:
            self.app.quit()
            self.app = None
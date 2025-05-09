import numpy as np
import tensorflow as tf
from rubiks_env import RubiksCubeEnv
from agent import DQNAgent
import time
import argparse

def visualize(model_path, scramble_moves=20, max_steps=100, delay=0.5):
    # Initialize environment
    env = RubiksCubeEnv(size=3, headless=False)
    
    # Get state size
    state = env.reset()
    state_size = len(state)
    
    # Get action size
    action_size = env.action_space_size
    
    # Initialize agent
    agent = DQNAgent(state_size, action_size)
    
    # Load trained model
    agent.load(model_path)
    
    # Set epsilon to minimum for visualization (mostly exploitation)
    agent.epsilon = agent.epsilon_min
    
    # Reset environment
    state = env.reset()
    
    print(f"Scrambling cube with {scramble_moves} random moves...")
    env.scramble(scramble_moves)
    
    print("Starting solution...")
    
    # Initialize variables
    done = False
    step = 0
    
    # Start time
    start_time = time.time()
    
    while not done and step < max_steps:
        # Choose action
        action = agent.act(state, training=False)
        
        # Take action
        next_state, reward, done, info = env.step(action)
        
        # Update state
        state = next_state
        
        step += 1
        
        # Print progress
        print(f"Step: {step}, Reward: {reward:.2f}, Solved: {info['solved']}")
        
        # Add delay for better visualization
        time.sleep(delay)
    
    # End time
    end_time = time.time()
    solution_time = end_time - start_time
    
    # Print summary
    if info['solved']:
        print(f"\nCube solved in {step} steps and {solution_time:.2f} seconds!")
    else:
        print(f"\nFailed to solve cube in {max_steps} steps.")
    
    # Keep the visualization window open
    input("Press Enter to close...")
    
    # Close environment
    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visualize Rubik\'s Cube Solver')
    parser.add_argument('--model', type=str, required=True, help='Path to the trained model')
    parser.add_argument('--scramble', type=int, default=20, help='Number of scramble moves')
    parser.add_argument('--max-steps', type=int, default=100, help='Maximum solution steps')
    parser.add_argument('--delay', type=float, default=0.5, help='Delay between moves (seconds)')
    
    args = parser.parse_args()
    
    # Ensure model path has the correct extension
    model_path = args.model
    if not model_path.endswith('.weights.h5') and model_path.endswith('.h5'):
        model_path = model_path.replace('.h5', '.weights.h5')
    
    visualize(model_path, args.scramble, args.max_steps, args.delay)

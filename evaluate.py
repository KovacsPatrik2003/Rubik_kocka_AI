import numpy as np
import tensorflow as tf
from rubiks_env import RubiksCubeEnv
from agent import DQNAgent
import time
import argparse

def evaluate(model_path, num_episodes=10, headless=False):
    # Initialize environment
    env = RubiksCubeEnv(size=3, headless=headless)
    
    # Get state size
    state = env.reset()
    state_size = len(state)
    
    # Get action size
    action_size = env.action_space_size
    
    # Initialize agent
    agent = DQNAgent(state_size, action_size)
    
    # Load trained model
    agent.load(model_path)
    
    # Set epsilon to minimum for evaluation (mostly exploitation)
    agent.epsilon = agent.epsilon_min
    
    # Evaluation metrics
    success_count = 0
    total_steps = 0
    total_time = 0
    
    # Evaluation loop
    for e in range(num_episodes):
        # Reset environment
        state = env.reset()
        
        # Initialize variables for this episode
        done = False
        step = 0
        
        # Episode start time
        start_time = time.time()
        
        while not done:
            # Choose action
            action = agent.act(state, training=False)
            
            # Take action
            next_state, reward, done, info = env.step(action)
            
            # Update state
            state = next_state
            
            step += 1
            
            # Print progress
            print(f"\rEpisode: {e+1}/{num_episodes}, Step: {step}", end="")
            
            # Limit steps to prevent infinite loops
            if step >= 100:
                done = True
        
        # Episode end time
        end_time = time.time()
        episode_time = end_time - start_time
        
        # Update metrics
        if info['solved']:
            success_count += 1
        total_steps += step
        total_time += episode_time
        
        # Print episode summary
        print(f"\rEpisode: {e+1}/{num_episodes}, Steps: {step}, Time: {episode_time:.2f}s, Solved: {info['solved']}")
    
    # Print overall metrics
    print(f"\nEvaluation Results:")
    print(f"Success Rate: {success_count/num_episodes:.2%}")
    print(f"Average Steps: {total_steps/num_episodes:.2f}")
    print(f"Average Time: {total_time/num_episodes:.2f}s")
    
    # Close environment
    env.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate Rubik\'s Cube Solver')
    parser.add_argument('--model', type=str, required=True, help='Path to the trained model')
    parser.add_argument('--episodes', type=int, default=10, help='Number of evaluation episodes')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    evaluate(args.model, args.episodes, args.headless)
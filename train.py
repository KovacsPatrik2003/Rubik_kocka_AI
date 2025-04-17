import numpy as np
import tensorflow as tf
from rubiks_env import RubiksCubeEnv
from agent import DQNAgent
import time
import os

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# Training parameters
EPISODES = 1000
BATCH_SIZE = 32
CUBE_SIZE = 3  # 3x3x3 cube
HEADLESS = False  # Set to True for faster training without visualization

# Create log directory
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

def train():
    # Initialize environment
    env = RubiksCubeEnv(size=CUBE_SIZE, headless=HEADLESS)
    
    # Get state size
    state = env.reset()
    state_size = len(state)
    
    # Get action size
    action_size = env.action_space_size
    
    # Initialize agent
    agent = DQNAgent(state_size, action_size)
    
    # Training metrics
    scores = []
    epsilon_history = []
    
    # Training loop
    for e in range(EPISODES):
        # Reset environment
        state = env.reset()
        
        # Initialize variables for this episode
        score = 0
        done = False
        step = 0
        
        # Episode start time
        start_time = time.time()
        
        while not done:
            # Choose action
            action = agent.act(state)
            
            # Take action
            next_state, reward, done, info = env.step(action)
            
            # Remember experience
            agent.remember(state, action, reward, next_state, done)
            
            # Update state
            state = next_state
            
            # Update score
            score += reward
            
            # Train agent
            if len(agent.memory) > BATCH_SIZE:
                agent.replay(BATCH_SIZE)
            
            # Update target model periodically
            if step % agent.update_target_frequency == 0:
                agent.update_target_model()
            
            step += 1
            
            # Print progress
            if step % 10 == 0:
                print(f"\rEpisode: {e+1}/{EPISODES}, Step: {step}, Score: {score:.2f}, Epsilon: {agent.epsilon:.4f}", end="")
        
        # Episode end time
        end_time = time.time()
        episode_time = end_time - start_time
        
        # Save score and epsilon
        scores.append(score)
        epsilon_history.append(agent.epsilon)
        
        # Print episode summary
        print(f"\rEpisode: {e+1}/{EPISODES}, Steps: {step}, Score: {score:.2f}, Epsilon: {agent.epsilon:.4f}, Time: {episode_time:.2f}s, Solved: {info['solved']}")
        
        # Save model every 100 episodes
        if (e + 1) % 100 == 0:
            agent.save(f"{log_dir}/rubiks_dqn_model_{e+1}.h5")
            
            # Save training metrics
            np.save(f"{log_dir}/scores.npy", np.array(scores))
            np.save(f"{log_dir}/epsilon_history.npy", np.array(epsilon_history))
    
    # Save final model
    agent.save(f"{log_dir}/rubiks_dqn_model_final.h5")
    
    # Close environment
    env.close()

if __name__ == "__main__":
    train()
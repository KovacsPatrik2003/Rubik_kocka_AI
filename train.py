import numpy as np
import tensorflow as tf
from rubiks_env import RubiksCubeEnv
from agent import DQNAgent
import time
import os
import gc

tf.keras.backend.clear_session()


np.random.seed(42)
tf.random.set_seed(42)


EPISODES = 10000 
BATCH_SIZE = 128  
CUBE_SIZE = 2     
HEADLESS = True   
MEMORY_LIMIT = 0.8  


log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

def train():
    env = RubiksCubeEnv(size=CUBE_SIZE, headless=HEADLESS)
    
    state = env.reset()
    state_size = len(state)
    
    action_size = env.action_space_size
    
    print(f"State size: {state_size}, Action size: {action_size}")
    
    agent = DQNAgent(state_size, action_size)
    
    scores = []
    epsilon_history = []
    solved_episodes = 0
    
    for e in range(EPISODES):
        state = env.reset()
        
        score = 0
        done = False
        step = 0
        
        start_time = time.time()
        
        while not done:
            action = agent.act(state)
            
            next_state, reward, done, info = env.step(action)
            
            agent.remember(state, action, reward, next_state, done)
            
            state = next_state
            
            score += reward
            
            if len(agent.memory) > BATCH_SIZE:
                agent.replay(BATCH_SIZE)
            
            if step % agent.update_target_frequency == 0:
                agent.update_target_model()
            
            step += 1
            
            if step % 10 == 0:
                print(f"\rEpisode: {e+1}/{EPISODES}, Step: {step}, Score: {score:.2f}, Epsilon: {agent.epsilon:.4f}", end="")
                
                gc.collect()
        
        end_time = time.time()
        episode_time = end_time - start_time
        
        if info['solved']:
            solved_episodes += 1
        
        scores.append(score)
        epsilon_history.append(agent.epsilon)
        
        print(f"\rEpisode: {e+1}/{EPISODES}, Steps: {step}, Score: {score:.2f}, Epsilon: {agent.epsilon:.4f}, Time: {episode_time:.2f}s, Solved: {info['solved']}")
        print(f"Solved episodes so far: {solved_episodes}/{e+1} ({solved_episodes/(e+1):.2%})")
        
        if (e + 1) % 10 == 0:
            model_path = f"{log_dir}/rubiks_dqn_model_{e+1}.weights.h5"
            agent.save(model_path)
            
            np.save(f"{log_dir}/scores.npy", np.array(scores))
            np.save(f"{log_dir}/epsilon_history.npy", np.array(epsilon_history))
            
            gc.collect()
    
    final_model_path = f"{log_dir}/rubiks_dqn_model_final.weights.h5"
    agent.save(final_model_path)
    
    env.close()

if __name__ == "__main__":
    train()

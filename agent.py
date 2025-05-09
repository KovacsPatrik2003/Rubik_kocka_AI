import numpy as np
import tensorflow as tf
from tensorflow import keras
from collections import deque
import random

# Configure TensorFlow to use memory growth instead of pre-allocating all GPU memory
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    try:
        for device in physical_devices:
            tf.config.experimental.set_memory_growth(device, True)
        print("Memory growth enabled for GPUs")
    except Exception as e:
        print(f"Error setting memory growth: {e}")

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        
        # Hyperparameters
        self.gamma = 0.99  # Increased discount rate for better long-term planning
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.9995  # Slower decay for more exploration
        self.learning_rate = 0.0005  # Lower learning rate for stability
        self.update_target_frequency = 5  # Update target network more frequently
        
        # Memory for experience replay
        self.memory = deque(maxlen=10000)
        
        # Main model (trained every step)
        self.model = self._build_model()
        
        # Target model (periodically updated)
        self.target_model = self._build_model()
        self.update_target_model()
    
    def _build_model(self):
        """Build a neural network model for deep Q-learning."""
        # More complex model with batch normalization for better training
        model = keras.Sequential([
            keras.layers.Dense(512, input_dim=self.state_size, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dense(512, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dense(256, activation='relu'),
            keras.layers.BatchNormalization(),
            keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model
    
    def update_target_model(self):
        """Update the target model with weights from the main model."""
        self.target_model.set_weights(self.model.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory for replay."""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state, training=True):
        """Choose an action based on the current state."""
        if training and np.random.rand() <= self.epsilon:
            # Exploration: choose a random action
            return random.randrange(self.action_size)
        
        # Exploitation: choose best action based on Q-values
        act_values = self.model.predict(np.array([state]), verbose=0)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size):
        """Train the model using experience replay."""
        if len(self.memory) < batch_size:
            return
        
        # Sample a batch of experiences from memory
        minibatch = random.sample(self.memory, batch_size)
        
        # Extract data from minibatch
        states = np.array([experience[0] for experience in minibatch])
        actions = np.array([experience[1] for experience in minibatch])
        rewards = np.array([experience[2] for experience in minibatch])
        next_states = np.array([experience[3] for experience in minibatch])
        dones = np.array([experience[4] for experience in minibatch])
        
        # Calculate target Q-values
        target = self.model.predict(states, verbose=0)
        target_next = self.target_model.predict(next_states, verbose=0)
        
        for i in range(batch_size):
            if dones[i]:
                target[i][actions[i]] = rewards[i]
            else:
                target[i][actions[i]] = rewards[i] + self.gamma * np.amax(target_next[i])
        
        # Train the model
        self.model.fit(states, target, epochs=1, verbose=0, batch_size=32)
        
        # Decay epsilon for less exploration over time
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def load(self, name):
        """Load model weights from file."""
        try:
            # Try the new format first
            if not name.endswith('.weights.h5'):
                name = name.replace('.h5', '.weights.h5')
            self.model.load_weights(name)
        except (IOError, ValueError) as e:
            # If that fails, try the old format
            original_name = name.replace('.weights.h5', '.h5')
            print(f"Could not load weights with new format, trying original format: {original_name}")
            self.model.load_weights(original_name)
        
        self.update_target_model()
    
    def save(self, name):
        """Save model weights to file."""
        # Ensure the filename ends with .weights.h5 for newer Keras versions
        if not name.endswith('.weights.h5'):
            name = name.replace('.h5', '.weights.h5')
        
        try:
            self.model.save_weights(name)
            print(f"Model weights saved to {name}")
        except Exception as e:
            print(f"Error saving model weights: {e}")
            # Try saving the full model as a fallback
            full_model_name = name.replace('.weights.h5', '_full_model')
            try:
                self.model.save(full_model_name)
                print(f"Full model saved to {full_model_name}")
            except Exception as e2:
                print(f"Error saving full model: {e2}")

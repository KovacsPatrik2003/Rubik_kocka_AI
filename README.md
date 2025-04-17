# Rubik's Cube Solver with Reinforcement Learning

This project implements a Rubik's Cube solver using Deep Q-Learning (DQN), a reinforcement learning technique. The solver is trained to find the optimal sequence of moves to solve a scrambled Rubik's Cube.

## Requirements

- Python 3.7+
- TensorFlow 2.x
- NumPy
- Ursina (for visualization)

Install the required packages:

\`\`\`bash
pip install tensorflow numpy ursina
\`\`\`

## Project Structure

- `main.py`: The original Rubik's Cube visualization using Ursina
- `rubiks_env.py`: A Gym-like environment wrapper for the Rubik's Cube
- `dqn_agent.py`: Implementation of the Deep Q-Learning agent
- `train.py`: Script for training the agent
- `evaluate.py`: Script for evaluating the trained agent
- `visualize.py`: Script for visualizing the agent solving the cube

## Training the Agent

To train the agent, run:

\`\`\`bash
python train.py
\`\`\`

This will start the training process and save the model weights periodically in the `logs` directory.

## Evaluating the Agent

To evaluate the trained agent, run:

\`\`\`bash
python evaluate.py --model logs/rubiks_dqn_model_final.h5 --episodes 10
\`\`\`

This will run the agent on 10 randomly scrambled cubes and report the success rate, average steps, and average time.

## Visualizing the Agent

To watch the agent solve a scrambled cube, run:

\`\`\`bash
python visualize.py --model logs/rubiks_dqn_model_final.h5 --scramble 20 --delay 0.5
\`\`\`

This will scramble the cube with 20 random moves and then let the agent solve it, with a 0.5-second delay between moves for better visualization.

## Customization

You can customize various aspects of the training and evaluation:

- Cube size: Modify the `CUBE_SIZE` parameter in `train.py`
- Training episodes: Modify the `EPISODES` parameter in `train.py`
- Reward function: Modify the `calculate_reward` method in `rubiks_env.py`
- Neural network architecture: Modify the `_build_model` method in `dqn_agent.py`

## Notes

- Training a Rubik's Cube solver with reinforcement learning is computationally intensive and may take a long time.
- The current implementation uses a simplified state representation and reward function, which may not be optimal for all cube sizes.
- For better results, consider using a more sophisticated algorithm like Proximal Policy Optimization (PPO) or a more complex neural network architecture.
\`\`\`

## Key Components Explained

1. **State Representation**: The `get_state` method in `rubiks_env.py` converts the cube's state into a format suitable for the neural network. It captures the grid positions and orientations of each cube.

2. **Reward Function**: The `calculate_reward` method in `rubiks_env.py` defines the reward signal for the agent:
   - Large positive reward (100) for solving the cube
   - Small negative reward (-0.1) for each step to encourage efficiency
   - Progress reward based on how many cubes have correct orientations

3. **DQN Agent**: The agent uses a neural network to approximate the Q-function, which predicts the expected future rewards for each action. It uses experience replay to learn from past experiences and a target network to stabilize training.

4. **Training Process**: The training script runs episodes where the agent interacts with the environment, collects experiences, and learns from them using the replay buffer.

## Next Steps

1. **Start Training**: Run the `train.py` script to start training the agent. This will take time, so be patient.

2. **Monitor Progress**: The training script will print progress information and save model checkpoints periodically.

3. **Evaluate and Visualize**: Once training is complete, use the evaluation and visualization scripts to see how well your agent performs.

4. **Experiment and Improve**: Try different hyperparameters, reward functions, or neural network architectures to improve performance.

Would you like me to explain any specific part of the implementation in more detail?
\`\`\`


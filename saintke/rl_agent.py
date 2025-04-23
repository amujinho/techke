import numpy as np 
import torch
import torch.nn as nn
import torch.optim as optim
import gym
from gym import spaces
from .utils import calculate_reward

class StockTradingEnv:
    def __init__(self, data):
        self.data = data
        self.current_step = 0
        self.balance = 10000 #starting balance
        self.portfolio = 0 # number of shares held
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(5,), dtype=np.float32
        )

    def step(self, action):
        # Implement buying, selling, holding logic
        # update portfolio and balance accordingly
        reward = calculate_reward(self.balance, self.portfolio, self.data[self.current_step])
        self.current_step += 1
        done = self.current_step >= len(self.data)-1
        observation = self._get_observation()
        return observation, reward, done, {}
    
    def reset(self):
        #Reset balance, portfolio, and current step
        self.balance = 10000
        self.portfolio = 0
        self.current_step = 0
        return self._get_observation()
    
    def _get_observation(self):
        return np.array([self.data[self.current_step], self.balance, self.portfolio, 0.5, 0.5], dtype=np.float32)
    
    def get_state(self):
        #Return current market data and portfolio status as a state
        return np.array([self.data[self.current_step], self.balance, self.portfolio])

class QNetwork(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)
    
    def predict(self, state):
        """Use the model to predict Q-values for a given state."""
        with torch.no_grad():
            q_values = self.forward(state)
        return q_values
    
class DQNAgent:
    def __init__(self, q_network, environment):
        self.q_network = q_network
        self.env = environment
        self.gamma = 0.95
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.optimizer = optim.Adam(q_network.parameters(), lr=0.001)

    def choose_action(self, state):
        """Choose an action based on epsilon-greedy policy."""
        if np.random.rand() <= self.epsilon:
            return np.random.choice(3)  # Random action (exploration)
        else:
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.q_network.predict(state_tensor)
            return torch.argmax(q_values).item()  # Choose action with highest Q-value

    def train(self, episodes=500):
        for episode in range(episodes):
            state = self.env.reset()
            done = False
            while not done:
                # Choose action using the epsilon-greedy policy
                action = self.choose_action(state)
                
                # Take action, observe next state and reward
                next_state, reward, done, _ = self.env.step(action)
                
                # Convert states to tensors
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                next_state_tensor = torch.FloatTensor(next_state).unsqueeze(0)
                reward_tensor = torch.tensor([reward], dtype=torch.float)

                # Predict Q-values for current state and next state
                current_q_values = self.q_network(state_tensor)
                next_q_values = self.q_network.predict(next_state_tensor)

                # Compute target Q-value using Bellman equation
                target_q_value = reward_tensor + self.gamma * torch.max(next_q_values)
                target_q_value = target_q_value.detach()

                # Calculate loss
                loss = nn.MSELoss()(current_q_values[0][action], target_q_value)

                # Backpropagation
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

                # Move to the next state
                state = next_state

            # Decay epsilon to reduce exploration over time
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay
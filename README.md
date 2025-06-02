# Reinforcement-Learning-Agent-Escape-the-Castle


This project implements reinforcement learning algorithms to solve **Escape the Castle**, a grid-based survival game inspired by Markov Decision Processes (MDPs). The player must navigate a 5×5 grid, avoid hidden guards, and reach the goal while managing health and decision-making under uncertainty.

## 🔍 Techniques Used

- **Model-Based Monte Carlo (MBMC):** Estimated outcome probabilities (e.g., chance of defeating guards) through environment sampling.
- **Model-Free Monte Carlo (Q-Learning):** Trained an agent using an ε-greedy strategy with dynamic learning rates and reward-based updates.
- **Dimensionality Reduction:** Used for visualizing state representations (e.g., PCA, t-SNE).
- **MDP Simulation:** Designed a state-action-reward structure with stochastic transitions and partial observability.

## ⚙️ Core Files

- `MBMC.py` – Estimates guard victory probabilities via sampling.
- `MFMC.py` – Implements Q-learning and outputs a trained Q-table.
- `mdp_gym.py` – Contains the environment logic with the `env.step()` interface.
- `vis_gym.py` – Pygame-based visualization of gameplay and agent behavior.



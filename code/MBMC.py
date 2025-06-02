import time
import numpy as np
from vis_gym import *
import random

gui_flag = False # Set to True to enable the game state visualization
setup(GUI=gui_flag)
env = game # Gym environment already initialized within vis_gym.py

env.render() # Uncomment to print game state info

def hash(obs):
	x,y = obs['player_position']
	h = obs['player_health']
	g = obs['guard_in_cell']
	if not g:
		g = 0
	else:
		g = int(g[-1])

	return x*(5*3*5) + y*(3*5) + h*5 + g

'''

Complete the function below to do the following:

	1. Run a specified number of episodes of the game (argument num_episodes). An episode refers to starting in some initial 
	   configuration and taking actions until a terminal state is reached.
	2. Keep track of gameplay history in an appropriate format for each of the episodes.
	3. From gameplay history, estimate the probability of victory against each of the guards when taking the fight action.

	Some important notes:

		a. Keep in mind that given some observation [(X,Y), health, guard_in_cell], a fight action is only meaningful if the 
		   last entry corresponding to guard_in_cell is nonzero.

		b. Upon taking the fight action, if the player defeats the guard, the player is moved to a random neighboring cell with 
		   UNCHANGED health. (2 = Full, 1 = Injured, 0 = Critical).

		c. If the player loses the fight, the player is still moved to a random neighboring cell, but the health decreases by 1.

		d. Your player might encounter the same guard in different cells in different episodes.

		e. All interaction with the environment must be done using the env.step() method, which returns the next
		   observation, reward, done (Bool indicating whether terminal state reached) and info. This method should be called as 
		   obs, reward, done, info = env.step(action), where action is an integer representing the action to be taken.

		f. The env.reset() method resets the environment to the initial configuration and returns the initial observation. 
		   Do not forget to also update obs with the initial configuration returned by env.reset().

		g. To simplify the representation of the state space, each state may be hashed into a unique integer value using the hash function provided above.
		   For instance, the observation {'player_position': (1, 2), 'player_health': 2, 'guard_in_cell='G4'} 
		   will be hashed to 1*5*3*5 + 2*3*5 + 2*5 + 4 = 119. There are 375 unique states.

		h. To refresh the game screen if using the GUI, use the refresh(obs, reward, done, info) function, with the 'if gui_flag:' condition.
		   Example usage below. This function should be called after every action.

		   if gui_flag:
		       refresh(obs, reward, done, info)  # Update the game screen [GUI only]

	Finally, return the np array, P which contains four float values, each representing the probability of defeating guards 1-4 respectively.

'''

def estimate_victory_probability(num_episodes=100000):
	"""
    Probability estimator

    Parameters:
    - num_episodes (int): Number of episodes to run.

    Returns:
    - P (numpy array): Empirically estimated probability of defeating guards 1-4.
    """
	P = np.zeros(len(env.guards))
    
	victories = np.zeros(4)  # To keep track of victories against each guard
	fights = np.zeros(4)

	for episode in range(num_episodes):
		reset_return = env.reset()
		if isinstance(reset_return, tuple):
			obs = reset_return[0]
		else:
			obs = reset_return
		done = False

		while not done:
			# Ensure obs is a dictionary
			if isinstance(obs, tuple):
				obs = obs[0]

			if obs['guard_in_cell']:
				# Extract guard number before the fight
				guard_in_cell = obs['guard_in_cell']
				guard_num = int(guard_in_cell[-1]) - 1
				fights[guard_num] += 1

				action = 4  # FIGHT action
				obs, reward, done, info = env.step(action)

				if reward == 10:
					victories[guard_num] += 1

				if gui_flag:
					refresh(obs, reward, done, info)
			else:
				# No guard in the cell, take a random movement action
				action = random.choice([0, 1, 2, 3])  # UP, DOWN, LEFT, RIGHT
				obs, reward, done, info = env.step(action)

				if gui_flag:
					refresh(obs, reward, done, info)

			# Update obs if it's a tuple
			if isinstance(obs, tuple):
				obs = obs[0]
	print(f"Encounters with guards: {fights}")
	print(f"Victories against guards: {victories}")
		# Calculate the probabilities
	for i in range(4):
		if fights[i] > 0:
			P[i] = victories[i] / fights[i]
		else:
			P[i] = 0.0


	return P


		# return P
print(estimate_victory_probability())
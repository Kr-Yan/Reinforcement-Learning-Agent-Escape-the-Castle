import time
import pickle
import numpy as np
from vis_gym import *

gui_flag = False # Set to True to enable the game state visualization
setup(GUI=gui_flag)
env = game # Gym environment already initialized within vis_gym.py

#env.render() # Uncomment to print game state info

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
	2. Instead of saving all gameplay history, maintain and update Q-values for each state-action pair that your agent encounters in a dictionary.
	3. Use the Q-values to select actions in an epsilon-greedy manner. Refer to assignment instructions for a refresher on this.
	4. Update the Q-values using the Q-learning update rule. Refer to assignment instructions for a refresher on this.

	Some important notes:
		
		- The state space is defined by the player's position (x,y), the player's health (h), and the guard in the cell (g).
		
		- To simplify the representation of the state space, each state may be hashed into a unique integer value using the hash function provided above.
		  For instance, the observation {'player_position': (1, 2), 'player_health': 2, 'guard_in_cell='G4'} 
		  will be hashed to 1*5*3*5 + 2*3*5 + 2*5 + 4 = 119. There are 375 unique states.

		- Your Q-table should be a dictionary with keys as the hashed state and 
		  values as another dictionary of actions and their corresponding Q-values.
		  
		  For instance, the agent starts in state (x=0, y=0, health=2, guard=0) which is hashed to 10.
		  If the agent takes action 1 (DOWN) in this state, reaches state (x=0, y=1, health=2, guard=0) which is hashed to 25,
		  and receives a reward of 0, then the Q-table would contain the following entry:
		  
		  Q_table = {10: {1: 0}}. This means that the Q-value for the state 10 and action 1 is 0.

		  Please do not change this representation of the Q-table.
		
		- The four actions are: 0 (UP), 1 (DOWN), 2 (LEFT), 3 (RIGHT), 4 (FIGHT), 5 (HIDE)

		- Don't forget to reset the environment to the initial configuration after each episode by calling:
		  obs, reward, done, info = env.reset()

		- The value of eta is unique for every (s,a) pair, and should be updated as 1/(1 + number of updates to Q_opt(s,a)).

		- The value of epsilon is initialized to 1. You are free to choose the decay rate.
		  No default value is specified for the decay rate, experiment with different values to find what works.

		- To refresh the game screen if using the GUI, use the refresh(obs, reward, done, info) function, with the 'if gui_flag:' condition.
		  Example usage below. This function should be called after every action.
		  if gui_flag:
		      refresh(obs, reward, done, info)  # Update the game screen [GUI only]

	Finally, return the dictionary containing the Q-values (called Q_table).

'''

def Q_learning(num_episodes=10000, gamma=0.9, epsilon=1, decay_rate=0.999):
	"""
	Run Q-learning algorithm for a specified number of episodes.

    Parameters:
    - num_episodes (int): Number of episodes to run.
    - gamma (float): Discount factor.
    - epsilon (float): Exploration rate.
    - decay_rate (float): Rate at which epsilon decays. Epsilon is decayed as epsilon = epsilon * decay_rate after each episode.

    Returns:
    - Q_table (dict): Dictionary containing the Q-values for each state-action pair.
    """
	Q_table = {}
	num_update={}
	move_space = [0, 1, 2, 3]
	battle_space=[4,5]

	for i in range(num_episodes):
		reset_return = env.reset()
		if isinstance(reset_return, tuple):
			obs = reset_return[0]
		else:
			obs = reset_return

		done=False
		while not done: 
				state_name=hash(obs)
				if state_name not in Q_table:
					Q_table[state_name] = np.zeros(6)
					num_update[state_name] = np.zeros(6)
				if obs['guard_in_cell'] !=None:
					if random.random()< epsilon:
						action= random.choice(battle_space)


					else: 
						action = np.argmax(Q_table[state_name][4:])+4

				else:

					if random.random()< epsilon:
							action= random.choice(move_space)

					else: 
							action = np.argmax(Q_table[state_name][:4])

				obs_next, reward, done, info = env.step(action)
				next_state=hash(obs_next)
				if next_state not in Q_table:
					Q_table[next_state] = np.zeros(6)
					num_update[next_state] = np.zeros(6)
				n= 1/ (1+num_update[state_name][action])
				V_val=max(Q_table[next_state]) #optimal move


				Q_opt= (1-n)* Q_table[state_name][action] + n*(reward + gamma* V_val)
	

				num_update[state_name][action]+=1
				Q_table[state_name][action]=Q_opt

				obs=obs_next

		epsilon*=decay_rate
	# print(Q_table)
	return Q_table

decay_rate = 0.999999

Q_table = Q_learning(num_episodes=1000000, gamma=0.9, epsilon=1, decay_rate=decay_rate) # Run Q-learning

# Save the Q-table dict to a file
with open('Q_table.pickle', 'wb') as handle:
    pickle.dump(Q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)


'''
Uncomment the code below to play an episode using the saved Q-table. Useful for debugging/visualization.

Comment before final submission or autograder may fail.
'''

# Q_table = np.load('Q_table.pickle', allow_pickle=True)

	# obs, reward, done, info = env.reset()
	# total_reward = 0
	# while not done:
	# 	state = hash(obs)
	# 	action = max(Q_table[state], key=Q_table[state].get)
	# 	obs, reward, done, info = env.step(action)
	# 	total_reward += reward
	# 	if gui_flag:
	# 		refresh(obs, reward, done, info)  # Update the game screen [GUI only]

	# print("Total reward:", total_reward)

	# # Close the
	# env.close() # Close the environment



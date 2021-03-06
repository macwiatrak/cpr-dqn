from ddqn_agent import *
from environment import *
import numpy as np

env = GameEnv()
observation_space = env.reset()

agent1 = DDQNAgent(observation_space[0].shape, 8)

state_size = observation_space[0].shape[0]
last_rewards = []
episode = 0
max_episode_len = 1000
print(50*'#')
print("Printing agent's hyperparameters:")
print('Learning rate:', agent1.learning_rate, 'Batch size:', agent1.batch_size, 'Eps decay len:', agent1.epsilon_decay_len)
print("UPDATE EVERY 3")
print(50*'#')
while episode < 6001:
    episode += 1
    state = env.reset()
    if episode > 1000:
        if episode < 1010:
            env.render_env()
    state = np.reshape(state[0], [1, state_size])
    agent1_reward = 0
    agent2_reward = 0
    cumulative_reward = 0

    step = 0
    gameover = False
    while not gameover:
        step += 1
        if episode > 1000:
            if episode < 1010:
                env.render_env()
        action_1 = agent1.get_action(state)
        action_2 = np.random.randint(8)
        reward, next_state, done, untagged = env.step([action_1, action_2])
        next_state = np.reshape(next_state[0], [1, state_size])
        agent1_reward += reward[0]
        agent2_reward += reward[1]
        cumulative_reward += reward[0] + reward[1]
        agent1.train_model(action_1, state, next_state, reward[0], done)
        agent1.update_epsilon()
        state = next_state
        terminal = (step >= max_episode_len)
        if done or terminal:
            last_rewards.append([agent1_reward, agent2_reward, cumulative_reward, action_1, action_2, untagged])
            if episode % 3 == 0:
                agent1.update_target_model()
            gameover = True

    print('episode:', episode, 'cumulative reward: ', cumulative_reward, 'agent1 rew:', agent1_reward,
          'agent2 rew:', agent2_reward, 'step', step)

np.savetxt("rewards_dqnvsrandom.txt", last_rewards, fmt='%10d', header="   agent1_rew  agent2_rew   cum_rew   action1   action2  untagged   ")
'''
print(50*'#')
print('Average training reward', np.mean(last_rewards))
print('** EVALUATION PHASE **')
print(50*'#')
eval_rewards = []
agent.epsilon = 0
for i in range(100):
    state = env.reset()
    state = np.reshape(state, [1, state_size])
    # if episode % 100 == 0:
    #   env.render_env()
    total_reward = 0
    step = 0
    gameover = False
    while not gameover:
        step += 1
        action = agent.get_action(state)
        reward, next_state, done = env.step(action)
        next_state = np.reshape(next_state, [1, state_size])
        total_reward += reward
        state = next_state
        terminal = (step >= max_episode_len)
        if done or terminal:
            eval_rewards.append(total_reward)
            gameover = True
    print('episode:', i, 'cumulative reward: ', total_reward, 'epsilon:', agent.epsilon, 'step', step)
print(50*'#')
print('Average evaluation reward', np.mean(eval_rewards))
c=10
mean_rew = []
while c <= len(last_rewards):
        mean_rew.append(np.mean(last_rewards[c-10:c]))
        c+=1
plt.plot([i for i in range(len(mean_rew))], mean_rew, label='DQN; last 10 average')
plt.xlabel('episode')
plt.ylabel('average reward')
plt.title("DQN training")
plt.legend()
plt.show()'''
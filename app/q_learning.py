import numpy as np
from env import GridWorldEnv  # replace with your actual import

# Hyperparameters
ALPHA = 0.1      # learning rate
GAMMA = 0.9      # discount factor
EPSILON = 0.2    # exploration rate
EPISODES = 500   # number of training episodes
MAX_STEPS = 50   # max steps per episode

# Define Q-table: (agent_x, agent_y) -> 4 actions (up, down, left, right)
def create_q_table(size):
    return np.zeros((size, size, 4))

# Training loop
def train_q_learning(task="easy", size=6):
    env = GridWorldEnv(size=size, task=task)
    q_table = create_q_table(size)

    for episode in range(EPISODES):
        state = env.reset()
        agent_pos = state["agent"]
        done = False
        step = 0

        while not done and step < MAX_STEPS:
            x, y = agent_pos

            # Epsilon-greedy action
            if np.random.rand() < EPSILON:
                action = np.random.randint(4)
            else:
                action = np.argmax(q_table[x, y])

            next_state, reward, done, _ = env.step(action)
            next_x, next_y = next_state["agent"]

            # Q-learning update
            best_next = np.max(q_table[next_x, next_y])
            q_table[x, y, action] += ALPHA * (reward + GAMMA * best_next - q_table[x, y, action])

            agent_pos = next_state["agent"]
            step += 1

        if (episode + 1) % 50 == 0:
            print(f"Episode {episode+1}/{EPISODES} completed.")

    print("Training finished!")
    return q_table

# Test the trained agent
def test_agent(q_table, task="easy", size=6):
    env = GridWorldEnv(size=size, task=task)
    state = env.reset()
    agent_pos = state["agent"]
    done = False
    step = 0

    print(f"\n=== Testing agent in {task} ===")
    while not done and step < MAX_STEPS:
        x, y = agent_pos
        action = np.argmax(q_table[x, y])
        state, reward, done, _ = env.step(action)
        agent_pos = state["agent"]
        print(f"Step {step}: Agent {agent_pos}, Reward {reward:.2f}")
        step += 1

    if done and agent_pos == env.goal:
        print("🎯 Goal reached!")
    else:
        print("❌ Did not reach the goal.")

# Example usage
q_table = train_q_learning(task="medium", size=6)
test_agent(q_table, task="medium", size=6)
import numpy as np

class GridWorldEnv:
    def __init__(self, size=6, task="easy"):
        self.size = size
        self.task = task
        self.enemy_enabled = False
        self.max_steps = 100
        self.reset()

    def reset(self):
        self.agent_pos = [0, 0]  # start top-left
        self.goal = [self.size - 1, self.size - 1]  # goal bottom-right
        self.steps = 0
        self.enemy_enabled = False

        # Place obstacles (obstacles/furniture) randomly
        self.obstacles = []
        num_obstacles = {"easy": 3, "medium": 5, "hard": 8}[self.task]
        while len(self.obstacles) < num_obstacles:
            pos = [np.random.randint(self.size), np.random.randint(self.size)]
            if pos != self.agent_pos and pos != self.goal and pos not in self.obstacles:
                self.obstacles.append(pos)

        # Place traps (hazardous zones) randomly
        self.traps = []
        num_traps = {"easy": 1, "medium": 3, "hard": 5}[self.task]
        while len(self.traps) < num_traps:
            pos = [np.random.randint(self.size), np.random.randint(self.size)]
            if pos != self.agent_pos and pos != self.goal and pos not in self.obstacles and pos not in self.traps:
                self.traps.append(pos)

        # Enable enemy for hard task
        if self.task == "hard":
            self.enemy_enabled = True
            while True:
                self.enemy_pos = [np.random.randint(self.size), np.random.randint(self.size)]
                if self.enemy_pos != self.agent_pos and self.enemy_pos != self.goal \
                        and self.enemy_pos not in self.obstacles and self.enemy_pos not in self.traps:
                    break

        # Ensure goal is not surrounded
        self._ensure_goal_accessible()

        return self._get_state()

    def _ensure_goal_accessible(self):
        # Check 4 neighbors of the goal
        neighbors = [
            [self.goal[0] - 1, self.goal[1]],
            [self.goal[0] + 1, self.goal[1]],
            [self.goal[0], self.goal[1] - 1],
            [self.goal[0], self.goal[1] + 1]
        ]
        accessible = False
        for n in neighbors:
            if 0 <= n[0] < self.size and 0 <= n[1] < self.size:
                if n not in self.obstacles and n not in self.traps and (not self.enemy_enabled or n != self.enemy_pos):
                    accessible = True
                    break

        # If all neighbors blocked, free one randomly
        if not accessible:
            free_neighbor = neighbors[np.random.randint(len(neighbors))]
            if free_neighbor in self.obstacles:
                self.obstacles.remove(free_neighbor)
            if free_neighbor in self.traps:
                self.traps.remove(free_neighbor)
            if self.enemy_enabled and free_neighbor == self.enemy_pos:
                # Move enemy somewhere else
                while True:
                    new_pos = [np.random.randint(self.size), np.random.randint(self.size)]
                    if new_pos != self.agent_pos and new_pos != self.goal and new_pos not in self.obstacles and new_pos not in self.traps:
                        self.enemy_pos = new_pos
                        break

    def _get_state(self):
        def fix_pos(pos):
            # Force correct 2D format
            if not isinstance(pos, list):
                return [0, 0]
            if len(pos) == 1:
                return [pos[0], pos[0]]
            if len(pos) >= 2:
                return [int(pos[0]), int(pos[1])]
            return [0, 0]

        return {
            "agent": fix_pos(self.agent_pos),
            "goal": fix_pos(self.goal),
            "obstacles": [fix_pos(o) for o in self.obstacles],
            "traps": [fix_pos(t) for t in self.traps],
            "enemy": fix_pos(self.enemy_pos) if self.enemy_enabled else None
        }




    def _distance(self, pos):
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])

    def _move_enemy(self):
        if not self.enemy_enabled:
            return
        # Random enemy movement
        self.enemy_pos[0] = max(0, min(self.size - 1, self.enemy_pos[0] + np.random.choice([-1, 0, 1])))
        self.enemy_pos[1] = max(0, min(self.size - 1, self.enemy_pos[1] + np.random.choice([-1, 0, 1])))

    def step(self, action):
        x, y = self.agent_pos
        old_dist = self._distance(self.agent_pos)

        # Actions: 0=UP, 1=DOWN, 2=LEFT, 3=RIGHT
        if action == 0: x -= 1
        elif action == 1: x += 1
        elif action == 2: y -= 1
        elif action == 3: y += 1

        # Boundaries
        x = max(0, min(self.size - 1, x))
        y = max(0, min(self.size - 1, y))

        # Collision with obstacles
        if [x, y] in self.obstacles:
            x, y = self.agent_pos  # blocked

        self.agent_pos = [x, y]
        self.steps += 1

        reward = -0.5
        terminated = False
        truncated = self.steps >= 100

        # Distance shaping reward
        new_dist = self._distance(self.agent_pos)
        reward += (old_dist - new_dist) * 0.5

        # Hazard penalty
        if self.agent_pos in self.traps:
            reward -= 5

        # Enemy
        self._move_enemy()
        if self.enemy_enabled and self.agent_pos == self.enemy_pos:
            reward -= 10
            terminated = True

        # Goal
        if self.agent_pos == self.goal:
            reward += 50
            terminated = True

        if self.steps >= self.max_steps:
            truncated = True

        # Normalize reward
        reward = (reward + 10) / 60
        reward = max(0.0, min(1.0, reward))

        return self._get_state(), float(reward), terminated, truncated, {}

    # Optional helper for visualization
    def render(self):
        for r in range(self.size):
            line = ""
            for c in range(self.size):
                pos = [r, c]
                if pos == self.agent_pos:
                    line += "🤖 "
                elif pos == self.goal:
                    line += "💰 "
                elif pos in self.obstacles:
                    line += "🟫 "
                elif pos in self.traps:
                    line += "⚠️ "
                elif self.enemy_enabled and pos == self.enemy_pos:
                    line += "👾 "
                else:
                    line += "⬜ "
            print(line)
        print("\n")
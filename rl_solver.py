# rl_solver.py
import numpy as np
import sys
import time
from utils import load_maze_from_file, find_start_end_positions, save_maze_image
from config import MAZE_CONFIG, COLORS

class QLearningSolver:
    def __init__(self, maze, start, end, episodes=1000, alpha=0.1, gamma=0.9, epsilon=0.2, max_steps_per_episode=1000):
        self.maze = maze
        self.start = start
        self.end = end
        self.episodes = episodes
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = 0.995  # Decay epsilon over time
        self.epsilon_min = 0.01
        self.max_steps_per_episode = max_steps_per_episode
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.q_table = np.zeros((self.rows, self.cols, 4))  # 4 directions: R, L, D, U
        self.actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Right, Left, Down, Up
        self.successful_episodes = 0
        self.training_stats = []

    def is_valid(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols and self.maze[r][c] != 1

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.randint(4)
        return np.argmax(self.q_table[state[0]][state[1]])

    def get_reward(self, current_state, next_state):
        """Calculate reward based on the action taken."""
        if not self.is_valid(next_state):
            return -10  # Heavy penalty for hitting walls
        elif next_state == self.end:
            return 100  # Large reward for reaching the goal
        elif next_state == current_state:
            return -5   # Penalty for staying in place
        else:
            # Small penalty for each step + distance-based reward
            distance_to_goal = abs(next_state[0] - self.end[0]) + abs(next_state[1] - self.end[1])
            return -1 - distance_to_goal * 0.1

    def train(self):
        print(f"Training Q-Learning agent for {self.episodes} episodes...")

        for episode in range(self.episodes):
            state = self.start
            steps = 0
            episode_reward = 0

            # Episode loop with step limit
            while state != self.end and steps < self.max_steps_per_episode:
                action = self.choose_action(state)
                next_state = (state[0] + self.actions[action][0], state[1] + self.actions[action][1])

                # Calculate reward
                reward = self.get_reward(state, next_state)
                episode_reward += reward

                # If invalid move, stay in current state
                if not self.is_valid(next_state):
                    next_state = state

                # Q-learning update
                old_value = self.q_table[state[0]][state[1]][action]
                next_max = np.max(self.q_table[next_state[0]][next_state[1]])
                self.q_table[state[0]][state[1]][action] = \
                    (1 - self.alpha) * old_value + self.alpha * (reward + self.gamma * next_max)

                state = next_state
                steps += 1

            # Track successful episodes
            if state == self.end:
                self.successful_episodes += 1

            # Decay epsilon
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

            # Log progress every 100 episodes
            if (episode + 1) % 100 == 0:
                success_rate = self.successful_episodes / (episode + 1) * 100
                print(f"Episode {episode + 1}/{self.episodes}, Success Rate: {success_rate:.1f}%, "
                      f"Epsilon: {self.epsilon:.3f}, Steps: {steps}, Reward: {episode_reward:.1f}")

        final_success_rate = self.successful_episodes / self.episodes * 100
        print(f"Training completed! Final success rate: {final_success_rate:.1f}%")

    def get_path(self, max_path_length=1000):
        """Extract the learned path from start to end using the Q-table."""
        path = []
        state = self.start
        visited = set()
        steps = 0

        print(f"Extracting path from {self.start} to {self.end}...")

        while state != self.end and state not in visited and steps < max_path_length:
            visited.add(state)
            path.append(state)

            # Choose the best action based on Q-values
            action = np.argmax(self.q_table[state[0]][state[1]])
            next_state = (state[0] + self.actions[action][0], state[1] + self.actions[action][1])

            # Check if the move is valid
            if not self.is_valid(next_state):
                print(f"Invalid move from {state} with action {action}")
                # Try other actions if the best one is invalid
                q_values = self.q_table[state[0]][state[1]]
                sorted_actions = np.argsort(q_values)[::-1]  # Sort in descending order

                found_valid = False
                for alt_action in sorted_actions:
                    alt_next_state = (state[0] + self.actions[alt_action][0], state[1] + self.actions[alt_action][1])
                    if self.is_valid(alt_next_state) and alt_next_state not in visited:
                        next_state = alt_next_state
                        found_valid = True
                        break

                if not found_valid:
                    print(f"No valid moves from {state}, path extraction failed")
                    break

            state = next_state
            steps += 1

        # Add the end state if we reached it
        if state == self.end:
            path.append(state)
            print(f"Successfully found path with {len(path)} steps")
        else:
            print(f"Path extraction failed. Stopped at {state} after {steps} steps")
            if steps >= max_path_length:
                print("Maximum path length exceeded")
            elif state in visited:
                print("Detected loop in path")

        return path

def draw_solution_path_on_image(maze, path, filename="solution.png"):
    import pygame
    pygame.init()
    rows, cols = len(maze), len(maze[0])
    surface = pygame.Surface(((MAZE_CONFIG['CELL_SIZE'] + MAZE_CONFIG['MARGIN']) * cols,
                               (MAZE_CONFIG['CELL_SIZE'] + MAZE_CONFIG['MARGIN']) * rows))

    for r in range(rows):
        for c in range(cols):
            color = COLORS['WHITE']
            if maze[r][c] == 1:
                color = COLORS['BLACK']
            elif maze[r][c] == 2:
                color = COLORS['GREEN']
            elif maze[r][c] == 3:
                color = COLORS['RED']
            rect = pygame.Rect(
                c * (MAZE_CONFIG['CELL_SIZE'] + MAZE_CONFIG['MARGIN']),
                r * (MAZE_CONFIG['CELL_SIZE'] + MAZE_CONFIG['MARGIN']),
                MAZE_CONFIG['CELL_SIZE'],
                MAZE_CONFIG['CELL_SIZE']
            )
            pygame.draw.rect(surface, color, rect)

    for r, c in path:
        if maze[r][c] not in [2, 3]:
            rect = pygame.Rect(
                c * (MAZE_CONFIG['CELL_SIZE'] + MAZE_CONFIG['MARGIN']),
                r * (MAZE_CONFIG['CELL_SIZE'] + MAZE_CONFIG['MARGIN']),
                MAZE_CONFIG['CELL_SIZE'],
                MAZE_CONFIG['CELL_SIZE']
            )
            pygame.draw.rect(surface, COLORS['BLUE'], rect)

    pygame.image.save(surface, filename)
    pygame.quit()

def main():
    try:
        # Parse command line arguments
        maze_file = sys.argv[1] if len(sys.argv) > 1 else "custom_maze.txt"
        headless_mode = len(sys.argv) > 2 and sys.argv[2] == "headless"

        if not headless_mode:
            print(f"Loading maze from: {maze_file}")

        maze = load_maze_from_file(maze_file)
        start, ends = find_start_end_positions(maze)

        if not start or not ends:
            raise ValueError("Start or End point missing.")

        end = ends[0]

        if not headless_mode:
            print(f"Maze loaded: {len(maze)}x{len(maze[0])}")
            print(f"Start: {start}, End: {end}")

        # Create solver with reasonable parameters
        solver = QLearningSolver(
            maze, start, end,
            episodes=300,  # Reduced for web app performance
            alpha=0.1,
            gamma=0.9,
            epsilon=0.3,  # Higher initial exploration
            max_steps_per_episode=300
        )

        start_time = time.time()

        # Train with reduced verbosity in headless mode
        if headless_mode:
            # Temporarily redirect stdout to suppress training output
            import io
            import contextlib

            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                solver.train()
        else:
            solver.train()

        training_time = time.time() - start_time

        if not headless_mode:
            print(f"\nTraining completed in {training_time:.2f} seconds")

        # Extract path
        path_start_time = time.time()

        if headless_mode:
            # Suppress path extraction output in headless mode
            import io
            import contextlib
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                path = solver.get_path()
        else:
            path = solver.get_path()

        path_time = time.time() - path_start_time

        # Always save images (required by web app)
        save_maze_image(maze, "maze.png")
        draw_solution_path_on_image(maze, path, "solution.png")

        # Results - format for web app compatibility
        total_time = time.time() - start_time
        path_found = len(path) > 0 and path[-1] == end

        if path_found:
            print(f"RL Path found! Length: {len(path)}")
            print(f"SUCCESS: Path successfully found using Reinforcement Learning algorithm")
        else:
            print("RL No path found")
            print("FAILURE: No path exists between start and end points")

        print(f"Time taken: {total_time:.3f} seconds")

        if not headless_mode:
            print(f"\n=== DETAILED RESULTS ===")
            print(f"Training time: {training_time:.2f} seconds")
            print(f"Path extraction time: {path_time:.2f} seconds")
            print(f"Success rate: {solver.successful_episodes}/{solver.episodes} ({solver.successful_episodes/solver.episodes*100:.1f}%)")

    except Exception as e:
        print(f"FAILURE: Error in RL solver: {e}")
        if not (len(sys.argv) > 2 and sys.argv[2] == "headless"):
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

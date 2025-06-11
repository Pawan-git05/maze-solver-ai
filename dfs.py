"""
Enhanced DFS pathfinding algorithm with real-time animation.
"""
import sys
import time
from typing import List, Tuple, Optional, Dict, Set
from algorithm_base import PathfindingAlgorithm
from utils import get_neighbors
from config import ALGORITHM_CONFIG

class DFSAlgorithm(PathfindingAlgorithm):
    """Depth-First Search pathfinding algorithm."""

    def __init__(self, maze_file: str, animate: bool = True):
        super().__init__(maze_file, animate)
        self.stack = []

    def solve(self) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        Solve maze using DFS algorithm.

        Returns:
            Tuple of (path, statistics)
        """
        # Initialize stack with start position
        self.stack.append(self.start)

        nodes_explored = 0
        max_stack_size = 1

        while self.stack:
            current = self.stack.pop()

            # Skip if already visited
            if current in self.visited:
                continue

            # Mark as visited
            self.visited.add(current)
            nodes_explored += 1

            # Check if we reached the goal
            if current == self.end:
                path = self.reconstruct_path()
                return path, {
                    'nodes_explored': nodes_explored,
                    'max_stack_size': max_stack_size
                }

            # Update animation
            if self.animate and nodes_explored % 2 == 0:  # Update every 2 nodes for performance
                self.stats['nodes_explored'] = nodes_explored
                self.draw_maze(current, set(self.stack))
                time.sleep(ALGORITHM_CONFIG['ANIMATION_DELAY'])

            # Explore neighbors (in reverse order for DFS)
            neighbors = get_neighbors(current, self.rows, self.cols)
            neighbors.reverse()  # DFS explores in reverse order

            for neighbor in neighbors:
                nr, nc = neighbor

                # Skip walls and visited nodes
                if self.maze[nr][nc] == 1 or neighbor in self.visited:
                    continue

                # Add to stack and record path
                if neighbor not in self.came_from:
                    self.stack.append(neighbor)
                    self.came_from[neighbor] = current

            # Track maximum stack size
            max_stack_size = max(max_stack_size, len(self.stack))

            # Timeout check
            if time.time() - self.stats.get('start_time', time.time()) > ALGORITHM_CONFIG['TIMEOUT_SECONDS']:
                break

        # No path found
        return None, {
            'nodes_explored': nodes_explored,
            'max_stack_size': max_stack_size,
            'timeout': True
        }

def main():
    """Main function to run DFS algorithm."""
    maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"
    animate = len(sys.argv) < 3 or sys.argv[2].lower() != 'false'

    try:
        algorithm = DFSAlgorithm(maze_file, animate)
        path, stats = algorithm.run()

        # Print results with clear success/failure indication
        if path:
            print(f"DFS Path found! Length: {len(path)}")
            print(f"SUCCESS: Path successfully found using DFS algorithm")
        else:
            print("DFS No path found")
            print("FAILURE: No path exists between start and end points")

        print(f"Nodes explored: {stats['nodes_explored']}")
        print(f"Time taken: {stats['execution_time']:.3f} seconds")
        print(f"Max stack size: {stats.get('max_stack_size', 0)}")

        if stats.get('timeout'):
            print("Algorithm timed out")
            print("FAILURE: Algorithm exceeded time limit")

    except Exception as e:
        print(f"Error running DFS algorithm: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

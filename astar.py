"""
Enhanced A* pathfinding algorithm with real-time animation.
"""
import heapq
import sys
import time
from typing import List, Tuple, Optional, Dict, Set
from algorithm_base import PathfindingAlgorithm
from utils import get_neighbors, calculate_distance
from config import ALGORITHM_CONFIG

class AStarAlgorithm(PathfindingAlgorithm):
    """A* pathfinding algorithm with heuristic optimization."""

    def __init__(self, maze_file: str, animate: bool = True):
        super().__init__(maze_file, animate)
        self.g_score = {}  # Cost from start to node
        self.f_score = {}  # g_score + heuristic
        self.open_set = []  # Priority queue
        self.open_set_hash = set()  # For O(1) membership testing

    def heuristic(self, pos: Tuple[int, int]) -> float:
        """
        Calculate heuristic distance (Manhattan distance) to nearest end.

        Args:
            pos: Current position

        Returns:
            Heuristic distance to nearest end
        """
        # Return distance to nearest end point
        if not self.ends:
            return 0
        return min(calculate_distance(pos, end) for end in self.ends)

    def solve(self) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        Solve maze using A* algorithm.

        Returns:
            Tuple of (path, statistics)
        """
        # Initialize scores
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.heuristic(self.start)

        # Initialize open set with start position
        heapq.heappush(self.open_set, (self.f_score[self.start], self.start))
        self.open_set_hash.add(self.start)

        nodes_explored = 0
        max_frontier_size = 0

        while self.open_set:
            # Get node with lowest f_score
            current_f, current = heapq.heappop(self.open_set)
            self.open_set_hash.remove(current)

            # Check if we reached any goal
            if current in self.ends:
                # Update self.end to the reached end point for path reconstruction
                self.end = current
                path = self.reconstruct_path()
                return path, {
                    'nodes_explored': nodes_explored,
                    'max_frontier_size': max_frontier_size,
                    'final_path_cost': self.g_score[current],
                    'end_reached': current
                }

            # Mark as visited
            self.visited.add(current)
            nodes_explored += 1

            # Update animation
            if self.animate and nodes_explored % 5 == 0:  # Update every 5 nodes for performance
                self.stats['nodes_explored'] = nodes_explored
                self.draw_maze(current, self.open_set_hash)
                time.sleep(ALGORITHM_CONFIG['ANIMATION_DELAY'])

            # Explore neighbors
            for neighbor in get_neighbors(current, self.rows, self.cols):
                nr, nc = neighbor

                # Skip walls and visited nodes
                if self.maze[nr][nc] == 1 or neighbor in self.visited:
                    continue

                # Calculate tentative g_score
                tentative_g = self.g_score[current] + 1

                # If this path to neighbor is better than any previous one
                if neighbor not in self.g_score or tentative_g < self.g_score[neighbor]:
                    # Record the best path
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g
                    self.f_score[neighbor] = tentative_g + self.heuristic(neighbor)

                    # Add to open set if not already there
                    if neighbor not in self.open_set_hash:
                        heapq.heappush(self.open_set, (self.f_score[neighbor], neighbor))
                        self.open_set_hash.add(neighbor)

            # Track maximum frontier size
            max_frontier_size = max(max_frontier_size, len(self.open_set))

            # Timeout check
            if time.time() - self.stats.get('start_time', time.time()) > ALGORITHM_CONFIG['TIMEOUT_SECONDS']:
                break

        # No path found
        return None, {
            'nodes_explored': nodes_explored,
            'max_frontier_size': max_frontier_size,
            'timeout': True
        }

def main():
    """Main function to run A* algorithm."""
    maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"

    # Check for headless mode (no animation)
    animate = True
    if len(sys.argv) >= 3:
        if sys.argv[2].lower() in ['false', 'headless', 'no-gui']:
            animate = False

    try:
        algorithm = AStarAlgorithm(maze_file, animate)
        path, stats = algorithm.run()

        # Print results with clear success/failure indication
        if path:
            print(f"A* Path found! Length: {len(path)}")
            print(f"SUCCESS: Path successfully found using A* algorithm")
        else:
            print("A* No path found")
            print("FAILURE: No path exists between start and end points")

        print(f"Nodes explored: {stats['nodes_explored']}")
        print(f"Time taken: {stats['execution_time']:.3f} seconds")
        print(f"Max frontier size: {stats.get('max_frontier_size', 0)}")

        if stats.get('timeout'):
            print("Algorithm timed out")
            print("FAILURE: Algorithm exceeded time limit")

    except Exception as e:
        print(f"Error running A* algorithm: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

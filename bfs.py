"""
Enhanced BFS pathfinding algorithm with real-time animation.
"""
import sys
import time
from collections import deque
from typing import List, Tuple, Optional, Dict, Set
from algorithm_base import PathfindingAlgorithm
from utils import get_neighbors
from config import ALGORITHM_CONFIG

class BFSAlgorithm(PathfindingAlgorithm):
    """Breadth-First Search pathfinding algorithm."""
    
    def __init__(self, maze_file: str, animate: bool = True):
        super().__init__(maze_file, animate)
        self.queue = deque()
    
    def solve(self) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        Solve maze using BFS algorithm.
        
        Returns:
            Tuple of (path, statistics)
        """
        # Initialize queue with start position
        self.queue.append(self.start)
        self.visited.add(self.start)
        
        nodes_explored = 0
        max_queue_size = 1
        
        while self.queue:
            current = self.queue.popleft()
            nodes_explored += 1
            
            # Check if we reached any goal
            if current in self.ends:
                # Update self.end to the reached end point for path reconstruction
                self.end = current
                path = self.reconstruct_path()
                return path, {
                    'nodes_explored': nodes_explored,
                    'max_queue_size': max_queue_size,
                    'end_reached': current
                }
            
            # Update animation
            if self.animate and nodes_explored % 3 == 0:  # Update every 3 nodes for performance
                self.stats['nodes_explored'] = nodes_explored
                self.draw_maze(current, set(self.queue))
                time.sleep(ALGORITHM_CONFIG['ANIMATION_DELAY'])
            
            # Explore neighbors
            for neighbor in get_neighbors(current, self.rows, self.cols):
                nr, nc = neighbor
                
                # Skip walls and visited nodes
                if self.maze[nr][nc] == 1 or neighbor in self.visited:
                    continue
                
                # Add to queue and mark as visited
                self.queue.append(neighbor)
                self.visited.add(neighbor)
                self.came_from[neighbor] = current
            
            # Track maximum queue size
            max_queue_size = max(max_queue_size, len(self.queue))
            
            # Timeout check
            if time.time() - self.stats.get('start_time', time.time()) > ALGORITHM_CONFIG['TIMEOUT_SECONDS']:
                break
        
        # No path found
        return None, {
            'nodes_explored': nodes_explored,
            'max_queue_size': max_queue_size,
            'timeout': True
        }

def main():
    """Main function to run BFS algorithm."""
    maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"

    # Check for headless mode (no animation)
    animate = True
    if len(sys.argv) >= 3:
        if sys.argv[2].lower() in ['false', 'headless', 'no-gui']:
            animate = False
    
    try:
        algorithm = BFSAlgorithm(maze_file, animate)
        path, stats = algorithm.run()
        
        # Print results with clear success/failure indication
        if path:
            print(f"BFS Path found! Length: {len(path)}")
            print(f"SUCCESS: Path successfully found using BFS algorithm")
        else:
            print("BFS No path found")
            print("FAILURE: No path exists between start and end points")

        print(f"Nodes explored: {stats['nodes_explored']}")
        print(f"Time taken: {stats['execution_time']:.3f} seconds")
        print(f"Max queue size: {stats.get('max_queue_size', 0)}")

        if stats.get('timeout'):
            print("Algorithm timed out")
            print("FAILURE: Algorithm exceeded time limit")
            
    except Exception as e:
        print(f"Error running BFS algorithm: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

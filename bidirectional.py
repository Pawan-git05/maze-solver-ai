"""
Bidirectional Search pathfinding algorithm with real-time animation.
"""
import sys
import time
import pygame
from collections import deque
from typing import List, Tuple, Optional, Dict, Set
from algorithm_base import PathfindingAlgorithm
from utils import get_neighbors
from config import ALGORITHM_CONFIG, COLORS

class BidirectionalAlgorithm(PathfindingAlgorithm):
    """Bidirectional Search pathfinding algorithm."""
    
    def __init__(self, maze_file: str, animate: bool = True):
        super().__init__(maze_file, animate)
        self.forward_queue = deque()
        self.backward_queue = deque()
        self.forward_visited = set()
        self.backward_visited = set()
        self.forward_came_from = {}
        self.backward_came_from = {}
    
    def draw_maze(self, current_forward: Optional[Tuple[int, int]] = None, 
                  current_backward: Optional[Tuple[int, int]] = None,
                  frontier_forward: Optional[Set[Tuple[int, int]]] = None,
                  frontier_backward: Optional[Set[Tuple[int, int]]] = None):
        """
        Draw the current state of the bidirectional search.
        
        Args:
            current_forward: Current position being explored from start
            current_backward: Current position being explored from end
            frontier_forward: Forward frontier positions
            frontier_backward: Backward frontier positions
        """
        if not self.animate:
            return
            
        self.screen.fill(COLORS['WHITE'])
        
        for row in range(self.rows):
            for col in range(self.cols):
                pos = (row, col)
                val = self.maze[row][col]
                
                # Determine color based on cell type and state
                if val == 1:  # Wall
                    color = COLORS['BLACK']
                elif val == 2:  # Start
                    color = COLORS['GREEN']
                elif val == 3:  # End
                    color = COLORS['RED']
                elif pos in self.forward_visited and pos in self.backward_visited:  # Meeting point
                    color = (255, 0, 255)  # Magenta for intersection
                elif pos in self.forward_visited:  # Forward visited
                    color = COLORS['LIGHT_BLUE']
                elif pos in self.backward_visited:  # Backward visited
                    color = (255, 192, 203)  # Light pink
                elif frontier_forward and pos in frontier_forward:  # Forward frontier
                    color = COLORS['YELLOW']
                elif frontier_backward and pos in frontier_backward:  # Backward frontier
                    color = COLORS['ORANGE']
                elif pos == current_forward:  # Current forward position
                    color = COLORS['BLUE']
                elif pos == current_backward:  # Current backward position
                    color = (255, 69, 0)  # Orange red
                else:  # Empty path
                    color = COLORS['WHITE']
                
                # Draw cell
                rect = [
                    (self.margin + self.cell_size) * col + self.margin,
                    (self.margin + self.cell_size) * row + self.margin,
                    self.cell_size, self.cell_size
                ]
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, COLORS['GREY'], rect, 1)
        
        # Draw final path if found
        if self.path:
            for pos in self.path:
                if pos not in [self.start, self.end]:
                    row, col = pos
                    rect = [
                        (self.margin + self.cell_size) * col + self.margin,
                        (self.margin + self.cell_size) * row + self.margin,
                        self.cell_size, self.cell_size
                    ]
                    pygame.draw.rect(self.screen, COLORS['BLUE'], rect)
        
        # Draw statistics
        self.draw_stats()
        
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def reconstruct_bidirectional_path(self, meeting_point: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct path from bidirectional search meeting point.
        
        Args:
            meeting_point: The point where forward and backward searches meet
            
        Returns:
            Complete path from start to end
        """
        # Build forward path (start to meeting point)
        forward_path = []
        current = meeting_point
        while current in self.forward_came_from:
            forward_path.append(current)
            current = self.forward_came_from[current]
        forward_path.reverse()
        
        # Build backward path (meeting point to end)
        backward_path = []
        current = meeting_point
        while current in self.backward_came_from:
            current = self.backward_came_from[current]
            backward_path.append(current)
        
        # Combine paths
        return forward_path + backward_path
    
    def solve(self) -> Tuple[Optional[List[Tuple[int, int]]], Dict]:
        """
        Solve maze using bidirectional search.
        
        Returns:
            Tuple of (path, statistics)
        """
        # Initialize both searches
        self.forward_queue.append(self.start)
        self.backward_queue.append(self.end)
        self.forward_visited.add(self.start)
        self.backward_visited.add(self.end)
        
        nodes_explored = 0
        max_queue_size = 2
        
        while self.forward_queue and self.backward_queue:
            # Alternate between forward and backward search
            if len(self.forward_queue) <= len(self.backward_queue):
                # Forward search step
                if not self.forward_queue:
                    break
                    
                current = self.forward_queue.popleft()
                nodes_explored += 1
                
                # Check if we've met the backward search
                if current in self.backward_visited:
                    path = self.reconstruct_bidirectional_path(current)
                    return path, {
                        'nodes_explored': nodes_explored,
                        'max_queue_size': max_queue_size,
                        'meeting_point': current
                    }
                
                # Update animation
                if self.animate and nodes_explored % 3 == 0:
                    self.stats['nodes_explored'] = nodes_explored
                    self.draw_maze(current, None, set(self.forward_queue), set(self.backward_queue))
                    time.sleep(ALGORITHM_CONFIG['ANIMATION_DELAY'])
                
                # Explore neighbors
                for neighbor in get_neighbors(current, self.rows, self.cols):
                    nr, nc = neighbor
                    
                    # Skip walls and visited nodes
                    if self.maze[nr][nc] == 1 or neighbor in self.forward_visited:
                        continue
                    
                    # Add to forward search
                    self.forward_queue.append(neighbor)
                    self.forward_visited.add(neighbor)
                    self.forward_came_from[neighbor] = current
            
            else:
                # Backward search step
                if not self.backward_queue:
                    break
                    
                current = self.backward_queue.popleft()
                nodes_explored += 1
                
                # Check if we've met the forward search
                if current in self.forward_visited:
                    path = self.reconstruct_bidirectional_path(current)
                    return path, {
                        'nodes_explored': nodes_explored,
                        'max_queue_size': max_queue_size,
                        'meeting_point': current
                    }
                
                # Update animation
                if self.animate and nodes_explored % 3 == 0:
                    self.stats['nodes_explored'] = nodes_explored
                    self.draw_maze(None, current, set(self.forward_queue), set(self.backward_queue))
                    time.sleep(ALGORITHM_CONFIG['ANIMATION_DELAY'])
                
                # Explore neighbors
                for neighbor in get_neighbors(current, self.rows, self.cols):
                    nr, nc = neighbor
                    
                    # Skip walls and visited nodes
                    if self.maze[nr][nc] == 1 or neighbor in self.backward_visited:
                        continue
                    
                    # Add to backward search
                    self.backward_queue.append(neighbor)
                    self.backward_visited.add(neighbor)
                    self.backward_came_from[neighbor] = current
            
            # Track maximum queue size
            total_queue_size = len(self.forward_queue) + len(self.backward_queue)
            max_queue_size = max(max_queue_size, total_queue_size)
            
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
    """Main function to run Bidirectional Search algorithm."""
    maze_file = sys.argv[1] if len(sys.argv) > 1 else "manual_maze.txt"
    animate = len(sys.argv) < 3 or sys.argv[2].lower() != 'false'
    
    try:
        algorithm = BidirectionalAlgorithm(maze_file, animate)
        path, stats = algorithm.run()
        
        # Print results with clear success/failure indication
        if path:
            print(f"Bidirectional Search Path found! Length: {len(path)}")
            print(f"SUCCESS: Path successfully found using Bidirectional Search algorithm")
            if 'meeting_point' in stats:
                print(f"Searches met at: {stats['meeting_point']}")
        else:
            print("Bidirectional Search No path found")
            print("FAILURE: No path exists between start and end points")

        print(f"Nodes explored: {stats['nodes_explored']}")
        print(f"Time taken: {stats['execution_time']:.3f} seconds")
        print(f"Max queue size: {stats.get('max_queue_size', 0)}")

        if stats.get('timeout'):
            print("Algorithm timed out")
            print("FAILURE: Algorithm exceeded time limit")
            
    except Exception as e:
        print(f"Error running Bidirectional Search algorithm: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

import heapq

def dijkstra(maze, start, end):
    start_time = time.time()
    heap = [(0, start)]  # (cost, node)
    came_from = {}
    cost_so_far = {start: 0}

    while heap:
        current_cost, current = heapq.heappop(heap)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, time.time() - start_time

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)

            if 0 <= nr < ROWS and 0 <= nc < COLS and maze[nr][nc] != 1:
                new_cost = cost_so_far[current] + 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(heap, (new_cost, neighbor))
                    came_from[neighbor] = current

    return None, time.time() - start_time

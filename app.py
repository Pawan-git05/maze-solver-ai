from flask import Flask, request, jsonify
import subprocess
import os
import sys
import base64

app = Flask(__name__)

@app.route('/solve', methods=['POST'])
def solve_maze():
    data = request.json
    maze_type = data.get('maze_type', 'random')  # "manual" or "random"
    size = str(data.get('size', 25))
    algorithm = data.get('algorithm', 'bfs')  # "astar", "bfs", "dfs", "dijkstra"

    maze_script = "manual_maze.py" if maze_type == "manual" else "random_maze.py"
    maze_file = "manual_maze.txt" if maze_type == "manual" else "random_maze.txt"

    algo_script = {
        "astar": "astar.py",
        "bfs": "bfs.py",
        "dfs": "dfs.py",
        "dijkstra": "dijkstra.py"
    }.get(algorithm)

    if not algo_script:
        return jsonify({"error": "Invalid algorithm selected"}), 400

    try:
        # Step 1: Generate the maze
        subprocess.run([sys.executable, maze_script, size], check=True)

        # Step 2: Solve the maze
        subprocess.run([sys.executable, algo_script, maze_file], check=True)

        # Step 3: Load both images and return as base64
        if not os.path.exists("maze.png") or not os.path.exists("solution.png"):
            return jsonify({"error": "Image(s) not generated"}), 500

        def encode_image(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')

        return jsonify({
            "maze": encode_image("maze.png"),
            "solution": encode_image("solution.png")
        })

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Script error: {e}"}), 500
    except Exception as ex:
        return jsonify({"error": f"Unexpected error: {str(ex)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
import subprocess
import os
import sys
import time
import traceback
from config import APP_CONFIG, setup_logging, validate_maze_size, get_algorithm_script, get_algorithm_info
from utils import encode_image_to_base64, cleanup_temp_files, MazeError, AlgorithmError
from web_maze_generator import generate_web_mazes

# Suppress pygame welcome message before any pygame imports
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Setup logging with reduced verbosity
logger = setup_logging()

app = Flask(__name__)
app.config.update(APP_CONFIG)

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/algorithms', methods=['GET'])
def get_algorithms():
    """Get information about available algorithms."""
    try:
        algorithms = get_algorithm_info()
        return jsonify({
            "success": True,
            "algorithms": algorithms
        })
    except Exception as e:
        logger.error(f"Error getting algorithm info: {e}")
        return jsonify({"error": "Failed to get algorithm information"}), 500

@app.route('/generate-random-mazes', methods=['POST'])
def generate_random_mazes():
    """Generate multiple random mazes for web interface selection."""
    print("🔥 /generate-random-mazes endpoint called!")
    try:
        # Validate request
        if not request.json:
            print("❌ No JSON data in request")
            return jsonify({"error": "No JSON data provided"}), 400

        data = request.json
        print(f"📋 Received data: {data}")

        size = validate_maze_size(data.get('size', 25))
        count = min(max(data.get('count', 5), 1), 10)  # Limit between 1 and 10

        print(f"🎲 Generating {count} random mazes of size {size}x{size}")

        # Generate mazes using web generator
        mazes = generate_web_mazes(size, count)

        if not mazes:
            print("❌ Failed to generate mazes - empty result")
            return jsonify({"error": "Failed to generate mazes"}), 500

        print(f"✅ Successfully generated {len(mazes)} mazes")
        print(f"📊 First maze sample: {mazes[0][:2] if mazes else 'None'}")

        response_data = {
            "success": True,
            "mazes": mazes,
            "count": len(mazes),
            "size": size
        }
        print(f"📤 Sending response with {len(mazes)} mazes")
        return jsonify(response_data)

    except Exception as e:
        print(f"❌ ERROR in generate_random_mazes: {e}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        print(f"❌ Traceback: {traceback.format_exc()}")
        logger.error(f"Error generating random mazes: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": f"Failed to generate random mazes: {str(e)}"}), 500

@app.route('/solve', methods=['POST'])
def solve_maze():
    """
    Solve maze endpoint with comprehensive error handling.
    """
    start_time = time.time()

    try:
        # Validate request
        if not request.json:
            return jsonify({"error": "No JSON data provided"}), 400

        data = request.json
        maze_type = data.get('maze_type', 'random')
        original_size = data.get('size', 25)
        size = validate_maze_size(original_size)
        algorithm = data.get('algorithm', 'bfs').lower()
        custom_maze = data.get('maze_grid', None)

        print(f"Solving maze: type={maze_type}, size={size}, algorithm={algorithm}")

        # Validate inputs
        if maze_type not in ['random', 'custom', 'random_selected']:
            return jsonify({"error": "Invalid maze type. Must be 'random', 'custom', or 'random_selected'"}), 400

        algo_script = get_algorithm_script(algorithm)
        if not algo_script:
            return jsonify({"error": f"Invalid algorithm '{algorithm}'. Supported: astar, bfs, dfs, dijkstra, bidirectional"}), 400

        # Clean up any existing temporary files
        cleanup_temp_files()

        # Handle different maze types
        if maze_type in ['custom', 'random_selected']:
            # Handle custom maze from web editor or selected random maze
            maze_type_name = "custom maze" if maze_type == 'custom' else "selected random maze"
            logger.info(f"Processing {maze_type_name}: size={size}, has_maze_data={custom_maze is not None}")

            if not custom_maze:
                return jsonify({"error": f"Maze data is required for {maze_type_name}"}), 400

            # Validate maze dimensions match the original requested size
            if len(custom_maze) != original_size or any(len(row) != original_size for row in custom_maze):
                return jsonify({"error": f"Maze must be {original_size}x{original_size}"}), 400

            # Update size to match the actual maze size (no validation adjustment for custom mazes)
            size = original_size

            # Check for start and end points
            start_count = sum(row.count(2) for row in custom_maze)
            end_count = sum(row.count(3) for row in custom_maze)

            if start_count != 1:
                return jsonify({"error": "Maze must have exactly one start point (green)"}), 400
            if end_count < 1:
                return jsonify({"error": "Maze must have at least one end point (red)"}), 400

            # Save maze to file
            maze_file = "selected_maze.txt" if maze_type == 'random_selected' else "custom_maze.txt"
            try:
                with open(maze_file, 'w') as f:
                    for row in custom_maze:
                        f.write(str(row) + '\n')
                logger.info(f"Maze saved to {maze_file}")

                # Also generate the initial maze image
                from utils import save_maze_image, load_maze_from_file
                maze_data = load_maze_from_file(maze_file)
                save_maze_image(maze_data, "maze.png")
                logger.info("Maze image generated")

            except Exception as e:
                logger.error(f"Failed to save maze: {e}")
                return jsonify({"error": "Failed to save maze"}), 500

        else:
            # Handle random maze generation with GUI (legacy)
            if maze_type != 'random':
                return jsonify({"error": "Only 'random', 'custom', and 'random_selected' maze types are supported"}), 400

            maze_script = "random_maze.py"
            maze_file = "random_maze.txt"

            # Step 1: Generate the maze
            logger.info(f"Generating {maze_type} maze with size {size}")
            try:
                result = subprocess.run(
                    [sys.executable, maze_script, str(size)],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                logger.info(f"Maze generation completed: {result.stdout}")
            except subprocess.TimeoutExpired:
                logger.error("Maze generation timed out")
                return jsonify({"error": "Maze generation timed out"}), 500
            except subprocess.CalledProcessError as e:
                logger.error(f"Maze generation failed: {e.stderr}")

                # Check if it's a user cancellation error
                if "User closed window" in e.stderr or "missing start or end point" in e.stderr:
                    return jsonify({
                        "error": "Maze generation was cancelled. Please set both start and end points before closing the window.",
                        "user_error": True
                    }), 400
                else:
                    return jsonify({"error": f"Maze generation failed: {e.stderr}"}), 500

            # Verify maze file was created
            if not os.path.exists(maze_file):
                logger.error(f"Maze file {maze_file} was not created")
                return jsonify({"error": "Maze file was not generated"}), 500

        # Step 2: Solve the maze
        logger.info(f"Solving maze with {algorithm} algorithm")
        try:
            # Run algorithm in headless mode (no GUI)
            result = subprocess.run(
                [sys.executable, algo_script, maze_file, "headless"],
                check=True,
                capture_output=True,
                text=True,
                timeout=60
            )
            logger.info(f"Maze solving completed: {result.stdout}")

            # Check if algorithm found a path by examining output
            path_found = False
            if result.stdout:
                logger.info(f"Algorithm output: {result.stdout}")
                if "SUCCESS:" in result.stdout and "Path found!" in result.stdout:
                    path_found = True
                elif "FAILURE:" in result.stdout and ("No path" in result.stdout or "No path found" in result.stdout):
                    path_found = False
                elif "Path found!" in result.stdout:
                    path_found = True
                else:
                    # Default to checking if solution image exists
                    path_found = os.path.exists("solution.png")

        except subprocess.TimeoutExpired:
            logger.error("Maze solving timed out")
            return jsonify({"error": "Maze solving timed out"}), 500
        except subprocess.CalledProcessError as e:
            logger.error(f"Maze solving failed: {e.stderr}")
            return jsonify({"error": f"Maze solving failed: {e.stderr}"}), 500

        # Step 3: Verify images were generated
        maze_image = "maze.png"
        solution_image = "solution.png"

        if not os.path.exists(maze_image):
            logger.error("Maze image was not generated")
            return jsonify({"error": "Maze image was not generated"}), 500

        # Step 4: Handle path found/not found cases
        processing_time = time.time() - start_time

        if not path_found:
            # No path was found
            logger.info(f"No path found with {algorithm} algorithm in {processing_time:.2f} seconds")

            try:
                maze_b64 = encode_image_to_base64(maze_image)

                return jsonify({
                    "success": False,
                    "path_found": False,
                    "maze": maze_b64,
                    "solution": None,
                    "processing_time": round(processing_time, 2),
                    "algorithm": algorithm,
                    "maze_type": maze_type,
                    "size": size,
                    "message": f"No path found between start and end points using {algorithm.upper()} algorithm"
                })
            except Exception as e:
                logger.error(f"Error encoding maze image: {e}")
                return jsonify({"error": f"Error processing maze image: {str(e)}"}), 500

        # Path was found - verify solution image exists
        if not os.path.exists(solution_image):
            logger.error("Solution image was not generated despite path being found")
            return jsonify({"error": "Solution image was not generated"}), 500

        # Step 5: Encode images and return successful response
        try:
            maze_b64 = encode_image_to_base64(maze_image)
            solution_b64 = encode_image_to_base64(solution_image)

            logger.info(f"Maze solved successfully in {processing_time:.2f} seconds")

            return jsonify({
                "success": True,
                "path_found": True,
                "maze": maze_b64,
                "solution": solution_b64,
                "processing_time": round(processing_time, 2),
                "algorithm": algorithm,
                "maze_type": maze_type,
                "size": size,
                "message": f"Path found successfully using {algorithm.upper()} algorithm"
            })

        except Exception as e:
            logger.error(f"Error encoding images: {e}")
            return jsonify({"error": f"Error processing images: {str(e)}"}), 500

    except MazeError as e:
        logger.error(f"Maze error: {e}")
        return jsonify({"error": str(e)}), 400
    except AlgorithmError as e:
        logger.error(f"Algorithm error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🚀 Starting Maze Solver AI Flask application")
    print(f"🌐 Server running at http://{APP_CONFIG['HOST']}:{APP_CONFIG['PORT']}")
    app.run(
        host=APP_CONFIG['HOST'],
        port=APP_CONFIG['PORT'],
        debug=APP_CONFIG['DEBUG']
    )

"""
Debug script to test custom maze functionality step by step.
"""
import json
import os

def test_custom_maze_processing():
    """Test the custom maze processing logic."""
    print("🔍 Debugging Custom Maze Processing")
    print("=" * 50)
    
    # Test maze data (same as what would come from web editor)
    custom_maze = [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    size = 8
    algorithm = "astar"
    
    print(f"📋 Test Data:")
    print(f"   Size: {size}x{size}")
    print(f"   Algorithm: {algorithm}")
    
    # Step 1: Validate maze
    print(f"\n🔍 Step 1: Validating maze...")
    
    if len(custom_maze) != size or any(len(row) != size for row in custom_maze):
        print(f"❌ Size validation failed")
        return False
    else:
        print(f"✅ Size validation passed")
    
    # Check for start and end points
    start_count = sum(row.count(2) for row in custom_maze)
    end_count = sum(row.count(3) for row in custom_maze)
    
    print(f"   Start points found: {start_count}")
    print(f"   End points found: {end_count}")
    
    if start_count != 1:
        print(f"❌ Start point validation failed")
        return False
    if end_count != 1:
        print(f"❌ End point validation failed")
        return False
    
    print(f"✅ Start/End validation passed")
    
    # Step 2: Save maze to file
    print(f"\n🔍 Step 2: Saving maze to file...")
    maze_file = "debug_custom_maze.txt"
    
    try:
        with open(maze_file, 'w') as f:
            for row in custom_maze:
                f.write(str(row) + '\n')
        print(f"✅ Maze saved to {maze_file}")
    except Exception as e:
        print(f"❌ Failed to save maze: {e}")
        return False
    
    # Step 3: Generate maze image
    print(f"\n🔍 Step 3: Generating maze image...")
    try:
        from utils import save_maze_image, load_maze_from_file
        maze_data = load_maze_from_file(maze_file)
        save_maze_image(maze_data, "debug_maze.png")
        print(f"✅ Maze image generated: debug_maze.png")
    except Exception as e:
        print(f"❌ Failed to generate maze image: {e}")
        return False
    
    # Step 4: Run algorithm
    print(f"\n🔍 Step 4: Running algorithm...")
    import subprocess
    import sys
    
    try:
        result = subprocess.run([
            sys.executable, f'{algorithm}.py', maze_file, 'false'
        ], capture_output=True, text=True, timeout=30)
        
        print(f"   Return code: {result.returncode}")
        print(f"   Stdout: {result.stdout}")
        if result.stderr:
            print(f"   Stderr: {result.stderr}")
            
        if result.returncode == 0:
            print(f"✅ Algorithm executed successfully")
            
            # Check for path detection
            if "SUCCESS:" in result.stdout and "Path found!" in result.stdout:
                print(f"✅ Path found successfully")
                path_found = True
            elif "FAILURE:" in result.stdout:
                print(f"⚠️  No path found")
                path_found = False
            else:
                print(f"⚠️  Unclear path status")
                path_found = os.path.exists("solution.png")
                
        else:
            print(f"❌ Algorithm failed")
            return False
            
    except Exception as e:
        print(f"❌ Error running algorithm: {e}")
        return False
    
    # Step 5: Check output files
    print(f"\n🔍 Step 5: Checking output files...")
    
    files_to_check = ["maze.png", "solution.png"]
    for file_name in files_to_check:
        if os.path.exists(file_name):
            file_size = os.path.getsize(file_name)
            print(f"✅ {file_name} exists ({file_size} bytes)")
        else:
            print(f"❌ {file_name} missing")
    
    print(f"\n🎉 Custom maze processing test completed!")
    print(f"   Path found: {path_found}")
    return True

if __name__ == "__main__":
    success = test_custom_maze_processing()
    if success:
        print(f"\n✅ All tests passed! Custom maze functionality is working.")
    else:
        print(f"\n❌ Some tests failed. Check the output above.")

"""
Test custom maze functionality directly.
"""
import json

# Create a simple test maze
test_maze = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# Save to file for testing
with open('test_custom_maze.txt', 'w') as f:
    for row in test_maze:
        f.write(str(row) + '\n')

print("✅ Test custom maze created: test_custom_maze.txt")
print("📋 Maze details:")
print(f"   Size: {len(test_maze)}x{len(test_maze[0])}")

# Find start and end
start = end = None
for i, row in enumerate(test_maze):
    for j, cell in enumerate(row):
        if cell == 2:
            start = (i, j)
        elif cell == 3:
            end = (i, j)

print(f"   Start: {start}")
print(f"   End: {end}")

# Test with algorithm
import subprocess
import sys

print("\n🧪 Testing with A* algorithm...")
try:
    result = subprocess.run([
        sys.executable, 'astar.py', 'test_custom_maze.txt', 'false'
    ], capture_output=True, text=True, timeout=30)
    
    print("📤 Algorithm output:")
    print(result.stdout)
    
    if result.returncode == 0:
        print("✅ Algorithm ran successfully")
        
        # Check if images were created
        import os
        if os.path.exists('maze.png'):
            print("✅ maze.png created")
        else:
            print("❌ maze.png not created")
            
        if os.path.exists('solution.png'):
            print("✅ solution.png created")
        else:
            print("❌ solution.png not created")
    else:
        print("❌ Algorithm failed")
        print("Error:", result.stderr)
        
except Exception as e:
    print(f"❌ Error running algorithm: {e}")

print("\n💡 This test verifies that custom maze processing works correctly.")

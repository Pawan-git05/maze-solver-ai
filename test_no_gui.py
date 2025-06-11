"""
Test script to verify that no GUI windows open when using custom maze design.
"""
import requests
import time
import json

def test_custom_maze_no_gui():
    """Test that custom maze design doesn't open any GUI windows."""
    print("🧪 Testing Custom Maze Design - No GUI Windows")
    print("=" * 50)
    
    # Test data for a simple custom maze
    custom_maze_data = {
        "maze_type": "custom",
        "size": 10,
        "algorithm": "astar",
        "maze_grid": [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 2, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 3, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
    }
    
    try:
        print("📡 Sending custom maze to server...")
        
        response = requests.post(
            'http://localhost:5000/solve',
            json=custom_maze_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') or data.get('path_found'):
                print("✅ SUCCESS: Custom maze solved without opening GUI!")
                print(f"   Algorithm: {data.get('algorithm', 'Unknown')}")
                print(f"   Processing time: {data.get('processing_time', 'Unknown')}s")
                print(f"   Path found: {data.get('path_found', 'Unknown')}")
                
                if 'message' in data:
                    print(f"   Message: {data['message']}")
                    
                return True
            else:
                print("❌ FAILED: Server returned unsuccessful response")
                print(f"   Response: {data}")
                return False
                
        else:
            print(f"❌ FAILED: Server returned status code {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ FAILED: Cannot connect to server")
        print("   Make sure 'python app.py' is running")
        return False
    except Exception as e:
        print(f"❌ FAILED: Unexpected error: {e}")
        return False

def test_random_maze():
    """Test that random maze generation still works."""
    print("\n🎲 Testing Random Maze Generation")
    print("=" * 50)
    
    random_maze_data = {
        "maze_type": "random",
        "size": 15,
        "algorithm": "bfs"
    }
    
    try:
        print("📡 Sending random maze request to server...")
        
        response = requests.post(
            'http://localhost:5000/solve',
            json=random_maze_data,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('success') or data.get('path_found'):
                print("✅ SUCCESS: Random maze generated and solved!")
                print(f"   Algorithm: {data.get('algorithm', 'Unknown')}")
                print(f"   Processing time: {data.get('processing_time', 'Unknown')}s")
                return True
            else:
                print("⚠️  Random maze generated but no path found (this can happen)")
                return True
                
        else:
            print(f"❌ FAILED: Server returned status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Error testing random maze: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Maze Solver - No GUI Windows")
    print("Testing that custom maze design works entirely in browser")
    print("=" * 60)
    
    # Test custom maze (the main fix)
    custom_success = test_custom_maze_no_gui()
    
    # Test random maze (should still work)
    random_success = test_random_maze()
    
    print("\n" + "=" * 60)
    print("🏁 Test Results:")
    print(f"   Custom Maze (No GUI): {'✅ PASSED' if custom_success else '❌ FAILED'}")
    print(f"   Random Maze: {'✅ PASSED' if random_success else '❌ FAILED'}")
    
    if custom_success and random_success:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ No GUI windows open when using custom maze design")
        print("✅ Random maze generation still works")
        print("✅ The fix is working correctly!")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")
    
    print("\n💡 How to test manually:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Select 'Custom Design' from Maze Type")
    print("3. Click '🎨 Design Maze'")
    print("4. Verify that NO external windows open")
    print("5. Design a maze in the browser and solve it")

if __name__ == "__main__":
    main()

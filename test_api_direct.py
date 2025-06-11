"""
Test the custom maze API directly using curl-like approach.
"""
import json
import urllib.request
import urllib.parse

# Test maze data
test_data = {
    "maze_type": "custom",
    "size": 8,
    "algorithm": "astar",
    "maze_grid": [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ]
}

print("🧪 Testing Custom Maze API")
print("=" * 40)

try:
    # Prepare the request
    url = 'http://localhost:5000/solve'
    data = json.dumps(test_data).encode('utf-8')
    
    req = urllib.request.Request(url, data=data)
    req.add_header('Content-Type', 'application/json')
    
    print("📡 Sending request to Flask API...")
    print(f"   URL: {url}")
    print(f"   Data size: {len(data)} bytes")
    
    # Send the request
    with urllib.request.urlopen(req, timeout=30) as response:
        response_data = response.read().decode('utf-8')
        result = json.loads(response_data)
        
        print(f"✅ Response received (status: {response.status})")
        
        # Check the result
        if result.get('success') or result.get('path_found'):
            print("🎉 SUCCESS: Custom maze solved!")
            print(f"   Algorithm: {result.get('algorithm')}")
            print(f"   Processing time: {result.get('processing_time')}s")
            print(f"   Path found: {result.get('path_found')}")
            print(f"   Message: {result.get('message', 'No message')}")
            
            if result.get('maze'):
                print(f"   Maze image: {len(result['maze'])} chars (base64)")
            if result.get('solution'):
                print(f"   Solution image: {len(result['solution'])} chars (base64)")
                
        else:
            print("❌ FAILED: API returned unsuccessful response")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            print(f"   Full response: {result}")

except urllib.error.HTTPError as e:
    print(f"❌ HTTP Error {e.code}: {e.reason}")
    try:
        error_data = e.read().decode('utf-8')
        error_json = json.loads(error_data)
        print(f"   Error details: {error_json}")
    except:
        print(f"   Raw error: {error_data}")
        
except urllib.error.URLError as e:
    print(f"❌ Connection Error: {e.reason}")
    print("   Make sure Flask app is running: python app.py")
    
except Exception as e:
    print(f"❌ Unexpected Error: {e}")

print("\n💡 If this works, the custom maze feature is functioning correctly!")

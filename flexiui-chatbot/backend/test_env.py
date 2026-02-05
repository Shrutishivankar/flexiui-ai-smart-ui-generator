from dotenv import load_dotenv
import os

print("Testing .env file loading...")

# Load .env file
load_dotenv()

# Try to get API key
api_key = os.getenv("GROQ_API_KEY")

if api_key:
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:]}")
    print(f"   Full length: {len(api_key)} characters")
else:
    print("❌ API Key NOT found!")
    print("\nDebugging info:")
    print(f"Current directory: {os.getcwd()}")
    print(f"Looking for .env in: {os.path.abspath('.env')}")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file exists")
        with open('.env', 'r') as f:
            print("\n.env file contents:")
            print(f.read())
    else:
        print("❌ .env file NOT found!")
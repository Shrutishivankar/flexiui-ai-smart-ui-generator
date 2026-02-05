print("Testing imports...")

try:
    import groq
    print("✅ groq imported successfully!")
    print(f"   Location: {groq.__file__}")
except ImportError as e:
    print(f"❌ groq import failed: {e}")

try:
    from flask import Flask
    print("✅ flask imported successfully!")
except ImportError as e:
    print(f"❌ flask import failed: {e}")

try:
    from dotenv import load_dotenv
    print("✅ dotenv imported successfully!")
except ImportError as e:
    print(f"❌ dotenv import failed: {e}")
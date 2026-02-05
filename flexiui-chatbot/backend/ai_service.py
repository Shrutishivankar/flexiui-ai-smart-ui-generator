import os
from groq import Groq
import json
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# THEN initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Model to use (Groq's fastest and best model for code)
MODEL = "llama-3.3-70b-versatile"

# ============================================
# FUNCTION 1: Chat with Bot
# ============================================
def chat_with_bot(user_message, conversation_history=None):
    """
    General chat function - answers questions about FlexiUI
    
    Args:
        user_message (str): The user's question
        conversation_history (list): Previous messages (optional)
    
    Returns:
        str: Bot's response
    """
    try:
        # If no history, start fresh
        if conversation_history is None:
            conversation_history = []
        
        # System prompt - tells AI who it is and what it does
        system_prompt = """You are FlexiUI Assistant, a helpful AI that helps users create UI components.

Your capabilities:
- Generate HTML, CSS, and JavaScript code
- Answer questions about UI design
- Help with FlexiUI software usage
- Provide code examples and best practices

Guidelines:
- Be friendly and helpful
- Give clear, concise answers
- When providing code, format it properly
- If user asks to create something, suggest they use the "Generate UI" feature
"""
        
        # Build messages array
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append(msg)
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Call Groq API
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,  # Controls randomness (0-2)
            max_tokens=1000,  # Maximum response length
        )
        
        # Extract the response text
        bot_response = response.choices[0].message.content
        
        return bot_response
        
    except Exception as e:
        return f"Error: {str(e)}"

# ============================================
# FUNCTION 2: Generate UI Component
# ============================================
def generate_ui_component(prompt, component_type="general"):
    """
    Generate HTML/CSS/JS code based on user prompt
    
    Args:
        prompt (str): Description of what to create
        component_type (str): Type of component (navbar, hero, card, etc.)
    
    Returns:
        dict: Contains html, css, and js code
    """
    try:
        # Import prompts from prompts.py (we'll create this next)
        from prompts import get_ui_generation_prompt
        
        # Get the specialized prompt
        full_prompt = get_ui_generation_prompt(prompt, component_type)
        
        # Call Groq API
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert frontend developer. 
Generate clean, modern, and responsive HTML/CSS/JS code.

IMPORTANT: Return ONLY valid JSON in this exact format:
{
  "html": "your html code here",
  "css": "your css code here",
  "js": "your javascript code here (or empty string if not needed)"
}

Do not include any explanations, just the JSON."""
                },
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0.8,
            max_tokens=2000,
        )
        
        # Get the response
        ai_response = response.choices[0].message.content
        
        # Parse JSON from response
        code_data = parse_code_from_response(ai_response)
        
        return code_data
        
    except Exception as e:
        return {
            "error": str(e),
            "html": "<p>Error generating code</p>",
            "css": "",
            "js": ""
        }

# ============================================
# FUNCTION 3: Parse Code from AI Response
# ============================================
def parse_code_from_response(ai_response):
    """
    Extract and parse code from AI response
    
    Args:
        ai_response (str): Raw response from AI
    
    Returns:
        dict: Parsed HTML, CSS, JS
    """
    try:
        # Try to parse as JSON first
        # Remove markdown code blocks if present
        cleaned_response = ai_response.strip()
        
        # Remove ```json and ``` markers if present
        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]
        
        cleaned_response = cleaned_response.strip()
        
        # Parse JSON
        code_data = json.loads(cleaned_response)
        
        # Validate required fields
        if "html" not in code_data:
            code_data["html"] = ""
        if "css" not in code_data:
            code_data["css"] = ""
        if "js" not in code_data:
            code_data["js"] = ""
        
        return code_data
        
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract code manually
        return extract_code_manually(ai_response)

# ============================================
# FUNCTION 4: Manual Code Extraction (Fallback)
# ============================================
def extract_code_manually(text):
    """
    Fallback method to extract code if JSON parsing fails
    
    Args:
        text (str): Raw text with code blocks
    
    Returns:
        dict: Extracted HTML, CSS, JS
    """
    result = {
        "html": "",
        "css": "",
        "js": ""
    }
    
    # Simple extraction logic
    # Look for ```html, ```css, ```javascript blocks
    lines = text.split('\n')
    current_type = None
    current_code = []
    
    for line in lines:
        if '```html' in line.lower():
            current_type = 'html'
            current_code = []
        elif '```css' in line.lower():
            current_type = 'css'
            current_code = []
        elif '```javascript' in line.lower() or '```js' in line.lower():
            current_type = 'js'
            current_code = []
        elif '```' in line and current_type:
            # End of code block
            result[current_type] = '\n'.join(current_code)
            current_type = None
            current_code = []
        elif current_type:
            current_code.append(line)
    
    return result

# ============================================
# FUNCTION 5: Test Connection
# ============================================
def test_groq_connection():
    """
    Test if Groq API is working
    
    Returns:
        bool: True if working, False otherwise
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": "Say 'hello' if you're working!"}
            ],
            max_tokens=10
        )
        return True
    except Exception as e:
        print(f"Groq API Error: {str(e)}")
        return False

# ============================================
# Test the module
# ============================================
if __name__ == "__main__":
    print("Testing Groq AI Service...")
    
    # Test 1: Connection
    print("\n1. Testing connection...")
    if test_groq_connection():
        print("✅ Groq API connected successfully!")
    else:
        print("❌ Groq API connection failed!")
    
    # Test 2: Chat
    print("\n2. Testing chat...")
    response = chat_with_bot("What is FlexiUI?")
    print(f"Bot: {response[:100]}...")
    
    # Test 3: UI Generation
    print("\n3. Testing UI generation...")
    code = generate_ui_component("Create a simple button")
    print(f"Generated HTML length: {len(code.get('html', ''))} characters")
    print(f"Generated CSS length: {len(code.get('css', ''))} characters")
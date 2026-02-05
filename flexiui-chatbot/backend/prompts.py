"""
Prompt Templates for AI Code Generation

This file contains all the prompt templates used to generate UI components.
Each template is carefully crafted to get the best results from AI.
"""

# ============================================
# COMPONENT TYPE TEMPLATES
# ============================================

COMPONENT_TEMPLATES = {
    "navbar": """
Create a modern, responsive navigation bar with the following features:
- Logo/brand name on the left
- Navigation links in the center/right
- Mobile hamburger menu (responsive)
- Smooth animations
- Modern styling with proper spacing
""",
    
    "hero": """
Create an eye-catching hero section with:
- Large heading and subheading
- Call-to-action button(s)
- Background (gradient or image)
- Responsive layout
- Engaging visual design
""",
    
    "card": """
Create a modern card component with:
- Image/icon at the top
- Title and description
- Optional button/link
- Hover effects
- Clean, card-style design with shadows
""",
    
    "footer": """
Create a professional footer with:
- Multiple columns for links/info
- Social media icons
- Copyright text
- Responsive layout
- Proper spacing and styling
""",
    
    "button": """
Create a stylish button component with:
- Multiple variants (primary, secondary, outline)
- Hover and active states
- Smooth transitions
- Modern design
""",
    
    "form": """
Create a clean, user-friendly form with:
- Input fields with labels
- Proper validation styling
- Submit button
- Responsive layout
- Modern, accessible design
""",
    
    "general": """
Create the requested UI component with:
- Clean, modern design
- Responsive layout
- Smooth animations
- Good user experience
- Professional styling
"""
}

# ============================================
# STYLE THEMES
# ============================================

STYLE_THEMES = {
    "dark": """
Use a DARK theme with:
- Dark background colors (#1a1a1a, #2d2d2d)
- Light text colors (#ffffff, #e0e0e0)
- Accent colors (blue, purple, or neon green)
- High contrast for readability
""",
    
    "light": """
Use a LIGHT theme with:
- Light background colors (#ffffff, #f5f5f5)
- Dark text colors (#333333, #1a1a1a)
- Subtle shadows and borders
- Clean, minimalist design
""",
    
    "colorful": """
Use a COLORFUL theme with:
- Vibrant, bold colors
- Gradients and color transitions
- Eye-catching design
- Modern, energetic feel
""",
    
    "gaming": """
Use a GAMING theme with:
- Dark background with neon accents (#39ff14, #ff006e, #00d9ff)
- Futuristic, tech-inspired design
- Angular shapes and borders
- Glowing effects and animations
""",
    
    "corporate": """
Use a CORPORATE/PROFESSIONAL theme with:
- Clean, minimal design
- Professional color palette (blues, grays)
- Ample whitespace
- Business-appropriate styling
""",
    
    "minimal": """
Use a MINIMAL theme with:
- Maximum whitespace
- Simple typography
- Monochrome or subtle colors
- Focus on content, not decoration
"""
}

# ============================================
# MAIN PROMPT GENERATION FUNCTION
# ============================================

def get_ui_generation_prompt(user_prompt, component_type="general"):
    """
    Generate a complete prompt for UI generation
    
    Args:
        user_prompt (str): User's description
        component_type (str): Type of component to generate
    
    Returns:
        str: Complete, optimized prompt for AI
    """
    
    # Get component template
    component_template = COMPONENT_TEMPLATES.get(
        component_type.lower(), 
        COMPONENT_TEMPLATES["general"]
    )
    
    # Detect theme from user prompt
    theme = detect_theme(user_prompt)
    theme_description = STYLE_THEMES.get(theme, "")
    
    # Build the complete prompt
    prompt = f"""
{component_template}

USER REQUEST: {user_prompt}

{theme_description}

REQUIREMENTS:
1. Generate clean, semantic HTML5 code
2. Use modern CSS with flexbox/grid for layout
3. Make it fully responsive (mobile, tablet, desktop)
4. Add smooth transitions and hover effects
5. Include comments in the code
6. Use BEM naming convention for CSS classes
7. Ensure accessibility (proper ARIA labels, semantic tags)
8. Add JavaScript only if needed for interactivity

IMPORTANT OUTPUT FORMAT:
Return ONLY valid JSON in this exact format (no markdown, no explanations):
{{
  "html": "<!-- Your HTML code here -->",
  "css": "/* Your CSS code here */",
  "js": "// Your JavaScript code here (or empty string if not needed)"
}}

Generate professional, production-ready code that can be used immediately.
"""
    
    return prompt.strip()

# ============================================
# THEME DETECTION
# ============================================

def detect_theme(user_prompt):
    """
    Detect the theme/style from user's prompt
    
    Args:
        user_prompt (str): User's description
    
    Returns:
        str: Detected theme name
    """
    prompt_lower = user_prompt.lower()
    
    # Check for specific keywords
    if any(word in prompt_lower for word in ["dark", "black", "night", "noir"]):
        return "dark"
    
    if any(word in prompt_lower for word in ["gaming", "neon", "futuristic", "cyber"]):
        return "gaming"
    
    if any(word in prompt_lower for word in ["colorful", "vibrant", "rainbow", "bright"]):
        return "colorful"
    
    if any(word in prompt_lower for word in ["minimal", "simple", "clean", "minimalist"]):
        return "minimal"
    
    if any(word in prompt_lower for word in ["corporate", "professional", "business"]):
        return "corporate"
    
    if any(word in prompt_lower for word in ["light", "white", "bright background"]):
        return "light"
    
    # Default theme
    return "dark"

# ============================================
# MODIFICATION PROMPT
# ============================================

def get_modification_prompt(current_code, modification_request):
    """
    Generate prompt for modifying existing code
    
    Args:
        current_code (dict): Current HTML/CSS/JS code
        modification_request (str): What user wants to change
    
    Returns:
        str: Complete prompt for modification
    """
    
    prompt = f"""
You are modifying existing code based on user request.

CURRENT CODE:
HTML:
{current_code.get('html', '')}

CSS:
{current_code.get('css', '')}

JS:
{current_code.get('js', '')}

USER MODIFICATION REQUEST: {modification_request}

INSTRUCTIONS:
1. Modify the code according to the user's request
2. Keep existing functionality that wasn't asked to change
3. Maintain code quality and structure
4. Update only what's necessary

IMPORTANT OUTPUT FORMAT:
Return ONLY valid JSON in this exact format (no markdown, no explanations):
{{
  "html": "<!-- Updated HTML code -->",
  "css": "/* Updated CSS code */",
  "js": "// Updated JavaScript code (or empty string if not needed)"
}}

Generate the complete updated code.
"""
    
    return prompt.strip()

# ============================================
# HELP/QUESTION ANSWERING PROMPT
# ============================================

def get_help_prompt(question):
    """
    Generate prompt for answering user questions
    
    Args:
        question (str): User's question
    
    Returns:
        str: Complete prompt for answering
    """
    
    prompt = f"""
You are FlexiUI Assistant, helping users with UI design and development.

USER QUESTION: {question}

INSTRUCTIONS:
1. Provide a clear, helpful answer
2. If it's about code, include code examples
3. Be friendly and encouraging
4. Keep answers concise but complete
5. If relevant, suggest using FlexiUI features

Provide your helpful response:
"""
    
    return prompt.strip()

# ============================================
# TEST THE MODULE
# ============================================

if __name__ == "__main__":
    print("Testing Prompt Templates...\n")
    
    # Test 1: UI Generation Prompt
    print("1. Testing UI Generation Prompt:")
    print("-" * 50)
    test_prompt = get_ui_generation_prompt(
        "Create a dark navbar with logo", 
        "navbar"
    )
    print(test_prompt[:300] + "...")
    print()
    
    # Test 2: Theme Detection
    print("2. Testing Theme Detection:")
    print("-" * 50)
    test_cases = [
        "Create a dark navbar",
        "Make a colorful hero section",
        "Gaming style button",
        "Minimal design form"
    ]
    for test in test_cases:
        theme = detect_theme(test)
        print(f"   '{test}' → Theme: {theme}")
    print()
    
    # Test 3: Modification Prompt
    print("3. Testing Modification Prompt:")
    print("-" * 50)
    current_code = {
        "html": "<button>Click me</button>",
        "css": "button { background: blue; }",
        "js": ""
    }
    mod_prompt = get_modification_prompt(current_code, "Change color to red")
    print(mod_prompt[:200] + "...")
    print()
    
    print("✅ All prompt templates working!")
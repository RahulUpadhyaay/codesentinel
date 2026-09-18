import json
from google import genai
from google.genai import types
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY) if settings.GEMINI_API_KEY else None

def run_multi_agent_scan(filename: str, code_content: str) -> dict:
    """
    Coordinates Multi-Agent Code Audit using Gemini 3.6 Flash.
    Uses Structured JSON MIME-type enforcement for guaranteed valid JSON.
    """
    if not settings.GEMINI_API_KEY:
        return {
            "security_score": 75,
            "summary": "Mock Audit: Add GEMINI_API_KEY in .env for live AI scanning.",
            "findings": [
                {
                    "issue_title": "Hardcoded Secret Risk",
                    "severity": "HIGH",
                    "description": "Plain text API key detected.",
                    "line_number": 12,
                    "suggested_fix": "Use environment variables."
                }
            ]
        }
    
    prompt = f"""
    You are CodeSentinel AI, a world-class senior application security auditor and code reviewer.
    Analyze the following source code file ('{filename}') for security vulnerabilities, OWASP Top 10 risks, and performance flaws.
    
    SOURCE CODE:
    ```
    {code_content}
    ```
    
    Respond with a JSON object containing:
    1. "security_score": an integer from 0 to 100 representing code safety.
    2. "summary": a 1-2 sentence audit summary.
    3. "findings": an array of vulnerability objects, each having "issue_title", "severity" ("HIGH", "MEDIUM", or "LOW"), "description", "line_number" (integer or null), and "suggested_fix".
    """
    
    try:
        # Enforce application/json output mode natively in Gemini
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        return json.loads(response.text)
    except Exception as e:
        return {
            "security_score": 50,
            "summary": f"AI Scanner Error: {str(e)}",
            "findings": []
        }
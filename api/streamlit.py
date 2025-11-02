"""
Vercel serverless function wrapper for Streamlit app
Note: Vercel has limited support for Streamlit. Consider using Streamlit Cloud instead.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run Streamlit
import subprocess
import json

def handler(request):
    """
    Vercel serverless function handler
    This is a workaround - Vercel is NOT ideal for Streamlit apps
    """
    try:
        # Try to run streamlit
        # Note: This may not work well due to Vercel's serverless limitations
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "text/html"
            },
            "body": """
            <html>
            <head>
                <title>Streamlit App - Vercel Deployment Issue</title>
            </head>
            <body style="font-family: Arial; padding: 40px; max-width: 800px; margin: 0 auto;">
                <h1>⚠️ Streamlit on Vercel - Not Recommended</h1>
                <p>Vercel is designed for serverless functions and static sites, not for long-running applications like Streamlit.</p>
                
                <h2>Recommended Solution: Use Streamlit Cloud</h2>
                <p>Streamlit Cloud is specifically designed for Streamlit apps and provides:</p>
                <ul>
                    <li>✅ Native Streamlit support</li>
                    <li>✅ Free tier</li>
                    <li>✅ Automatic HTTPS</li>
                    <li>✅ Easy deployment from GitHub</li>
                    <li>✅ Environment variable management</li>
                </ul>
                
                <h3>Deploy on Streamlit Cloud:</h3>
                <ol>
                    <li>Go to <a href="https://streamlit.io/cloud">https://streamlit.io/cloud</a></li>
                    <li>Sign up with GitHub</li>
                    <li>Connect your repository</li>
                    <li>Set environment variables in Settings → Secrets</li>
                    <li>Deploy!</li>
                </ol>
                
                <h3>Alternative Platforms:</h3>
                <ul>
                    <li><strong>Railway:</strong> <a href="https://railway.app">https://railway.app</a></li>
                    <li><strong>Render:</strong> <a href="https://render.com">https://render.com</a></li>
                    <li><strong>Heroku:</strong> <a href="https://heroku.com">https://heroku.com</a></li>
                </ul>
                
                <p><strong>Note:</strong> Your code is ready for deployment on these platforms. Just push to GitHub and connect.</p>
            </body>
            </html>
            """
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


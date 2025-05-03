import requests
import os

GROUQ_API_KEY = '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'

def call_grouq_api(prompt):
    print("[DEBUG] Sending request to GrouQ API")

    url = "https://api.grouq.ai/v1/completions"  # Replace with actual GrouQ endpoint
    headers = {
        "Authorization": f"Bearer {GROUQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "grouq-1",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
    }

    print("[DEBUG] Request payload:", data)

    response = requests.post(url, json=data, headers=headers)

    print("[DEBUG] GrouQ API status:", response.status_code)

    if response.status_code == 200:
        result = response.json()
        print("[DEBUG] GrouQ API result:", result)
        return result.get('choices', [])[0].get('text', '').strip()
    else:
        print("[ERROR] GrouQ API error:", response.text)
        return f"Error: {response.status_code} - {response.text}"

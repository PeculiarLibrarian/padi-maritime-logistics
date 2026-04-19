import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

url = "https://openrouter.ai/api/v1/chat/completions"
headers = {"Authorization": f"Bearer {api_key}"}
data = {
    "model": "google/gemini-2.0-flash-001",
    "messages": [{"role": "user", "content": "The Peculiar Librarian here. Confirm Nairobi-01 Node active."}]
}

try:
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print("\n✅ SUCCESS: Nairobi-01 Node is Unbound and Active.")
        print("Response:", response.json()['choices'][0]['message']['content'])
    else:
        print(f"\n❌ FAILED: Status {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"\n⚠️ ERROR: {e}")

import os
from openai import OpenAI

def get_key_manually():
    """Deterministic key extraction from local .env"""
    try:
        with open(".env", "r") as f:
            for line in f:
                if "OPENROUTER_API_KEY" in line:
                    return line.split("=")[1].strip()
    except FileNotFoundError:
        return None
    return None

def verify_sovereignty():
    print("📡 Manually extracting key and dialing OpenRouter...")
    api_key = get_key_manually()
    
    if not api_key:
        print("❌ Error: .env file missing or key not found.")
        return

    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=api_key,
    )

    try:
        response = client.chat.completions.create(
          model="google/gemini-2.0-flash-001",
          messages=[
            {"role": "user", "content": "Nairobi-01 Node: Confirm Handshake."}
          ]
        )
        print("✅ Success: OpenRouter Gateway is ACTIVE.")
        print(f"🤖 Response: {response.choices[0].message.content}")
        print("🏛️ Status: Sovereign Execution Layer is READY.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    verify_sovereignty()

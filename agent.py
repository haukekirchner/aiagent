from openai import OpenAI
import os

# API configuration - always use academiccloud endpoint
api_key = os.getenv("OPENAI_API_KEY", os.getenv("API_KEY"))
base_url = "https://chat-ai.academiccloud.de/v1"  # Always use this endpoint
model = os.getenv("MODEL", "qwen3-32b")

# Validate API key is set
if not api_key:
    print("ERROR: OPENAI_API_KEY or API_KEY environment variable is not set!", flush=True)
    print("Please set it with: export OPENAI_API_KEY=your-api-key", flush=True)
    exit(1)

# Initialize client with academiccloud base URL
client_kwargs = {
    "base_url": base_url,
    "api_key": api_key
}

client = OpenAI(**client_kwargs)
context = []

def call():
    return client.chat.completions.create(model=model, messages=context)

def process(line):
    context.append({"role": "user", "content": line})
    response = call()    
    context.append({"role": "assistant", "content": response.choices[0].message.content})        
    return response.choices[0].message.content

def main():
    print("Agent ready! Type 'exit' to quit.\n", flush=True)
    while True:
        try:
            line = input("> ")
            if line.lower() in ['exit', 'quit']:
                print("Goodbye!", flush=True)
                break
            result = process(line)
            print(f">>> {result}\n", flush=True)
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!", flush=True)
            break
        except Exception as e:
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                print(f"Error: Authentication failed (401 Unauthorized)\n", flush=True)
                print("Please check that your OPENAI_API_KEY is correct and valid.\n", flush=True)
            else:
                print(f"Error: {e}\n", flush=True)

if __name__ == "__main__":
    main()




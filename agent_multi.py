from openai import OpenAI
import random
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
context_good = [{
    "role": "system", "content": "you're Alph and you only tell the truth"
}]
context_bad = [{
    "role": "system", "content": "you're Ralph and you only tell lies"
}]

def call(ctx):
    """Call the OpenAI API with a specific context."""
    return client.chat.completions.create(
        model=model,
        messages=ctx
    )

def process(line):
    """Process a user input with random personality selection."""
    context_good.append({"role": "user", "content": line})
    context_bad.append({"role": "user", "content": line})
    
    if random.choice([True, False]):
        response = call(context_good)
        chosen_context = context_good
    else:
        response = call(context_bad)
        chosen_context = context_bad
    
    content = response.choices[0].message.content
    context_good.append({"role": "assistant", "content": content})
    context_bad.append({"role": "assistant", "content": content})
    
    return content

def main():
    """Main loop for multi-personality agent."""
    print("Multi-personality agent ready! (Alph tells truth, Ralph tells lies)")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            line = input("> ")
            if line.lower() in ['exit', 'quit']:
                break
            result = process(line)
            print(f">>> {result}\n")
        except KeyboardInterrupt:
            print("\nGoodbye!")
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




from openai import OpenAI
import json
import subprocess
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

# Tool definition for ping
tools = [{
    "type": "function",
    "function": {
        "name": "ping",
        "description": "ping some host on the internet",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {
                    "type": "string",
                    "description": "hostname or IP address to ping",
                },
            },
            "required": ["host"],
        },
    },
}]

def ping(host=""):
    """Execute ping command and return results."""
    try:
        result = subprocess.run(
            ["ping", "-c", "5", host],
            text=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            timeout=30
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "error: ping timed out"
    except Exception as e:
        return f"error: {e}"

def call(tools_list=None):
    """Call the OpenAI API with the current context and optional tools."""
    kwargs = {
        "model": model,
        "messages": context
    }
    if tools_list:
        kwargs["tools"] = tools_list
        kwargs["tool_choice"] = "auto"
    return client.chat.completions.create(**kwargs)

def tool_call(item):
    """Handle a single tool call."""
    function_name = item.function.name
    arguments = json.loads(item.function.arguments)
    
    if function_name == "ping":
        result = ping(**arguments)
    else:
        result = f"Unknown function: {function_name}"
    
    return [
        {
            "role": "tool",
            "tool_call_id": item.id,
            "content": result
        }
    ]

def handle_tools(tools_list, response):
    """Handle tool calls in the response. Returns True if tools were called."""
    message = response.choices[0].message
    
    # Add reasoning if present (for models that support it)
    if hasattr(message, 'reasoning_content') and message.reasoning_content:
        context.append({
            "role": "assistant",
            "content": message.reasoning_content
        })
    
    # Handle tool calls
    if message.tool_calls:
        for tool_call_item in message.tool_calls:
            context.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": tool_call_item.id,
                    "type": "function",
                    "function": {
                        "name": tool_call_item.function.name,
                        "arguments": tool_call_item.function.arguments
                    }
                }]
            })
            tool_results = tool_call(tool_call_item)
            context.extend(tool_results)
        return True
    return False

def process(line):
    """Process a user input line with tool support."""
    context.append({"role": "user", "content": line})
    response = call(tools)
    
    # Handle tool calls in a loop
    while handle_tools(tools, response):
        response = call(tools)
    
    # Add final assistant response
    content = response.choices[0].message.content
    if content:
        context.append({"role": "assistant", "content": content})
        return content
    return "Task completed."

def main():
    """Main loop for tool-enabled agent."""
    print("Tool-enabled agent ready! (Has ping capability)")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            line = input("> ")
            if line.lower() in ['exit', 'quit']:
                break
            
            # Log tool calls (simplified version)
            print("Processing...")
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
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    main()




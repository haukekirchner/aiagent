# LLM Agent Implementation

This project reproduces the agent code from the Fly.io blog article: [You Should Write An Agent](https://fly.io/blog/everyone-write-an-agent/).

>[!CAUTION]
>The code in this repository is purely vibe-coded and was created just for fun during a late-evening session.
>Do not use it for anything serious or for real products!

>[!IMPORTANT]
>Instead of using OpenAI, this project uses the SAIA API endpoint, which is fully OpenAI-compatible.
>SAIA is the Scalable Artificial Intelligence (AI) Accelerator developed by the GWDG (where I also work).
>You can request access via our [service catalog](https://kisski.gwdg.de/leistungen/2-02-llm-service/) if you meet the user requirements for the AI service center KISSKI.

## Overview

This repository contains three implementations:

1. **`agent.py`** - Basic chat agent (ChatGPT-like)
2. **`agent_multi.py`** - Multi-personality agent (Alph tells truth, Ralph tells lies)
3. **`agent_tools.py`** - Tool-enabled agent with ping capability

## Prerequisites

- Docker and Docker Compose
- API key for the academiccloud endpoint

## Setup

The agents are configured to always use the SAIA API endpoint: `https://chat-ai.academiccloud.de/v1`

1. Set your API key as an environment variable:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```

2. Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

**Environment Variables:**
- `OPENAI_API_KEY` or `API_KEY` - Your API key (required)
- `MODEL` - Model name to use (defaults to `qwen3-32b`)

**Troubleshooting 401 Unauthorized Error:**
- Make sure your API key is set: `echo $OPENAI_API_KEY`
- Verify the API key is correct and valid for the academiccloud endpoint
- When using Docker, ensure the environment variable is passed: `docker-compose run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY agent`

## Usage

### Basic Agent

Run the basic chat agent (use `run` for interactive input):
```bash
docker-compose run --rm agent
```

Or build and run manually:
```bash
docker build -t aiagent .
docker run -it --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e MODEL=$MODEL \
  aiagent python agent.py
```

### Multi-Personality Agent

Run the multi-personality agent:
```bash
docker-compose run --rm agent-multi
```

Or manually:
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e MODEL=$MODEL \
  aiagent python agent_multi.py
```

### Tool-Enabled Agent

Run the agent with ping tool:
```bash
docker-compose run --rm agent-tools
```

Or manually:
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e MODEL=$MODEL \
  aiagent python agent_tools.py
```

**Note:** Use `docker-compose run` instead of `docker-compose up` for interactive sessions that require input. The `run` command properly handles stdin/stdout for interactive terminals.

## Examples

### Basic Agent
```
> What is 2+2?
>>> 4
```

### Multi-Personality Agent
```
> Who are you?
>>> I'm not Ralph.  (or) Yes—I'm Alph. How can I help?
```

### Tool-Enabled Agent
```
> describe our connectivity to google
>>> [Agent will ping google.com, www.google.com, and 8.8.8.8 automatically]
```

## Notes

- The code uses `qwen3-32b` model by default
- The OpenAI API structure matches the current Chat Completions API
- Tool calls are handled automatically in a loop until the agent is satisfied
- All agents maintain conversation context throughout the session
- **API endpoint is hardcoded to:** `https://chat-ai.academiccloud.de/v1`

## Development

To run locally without Docker:
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your-key
python agent.py  # or agent_multi.py or agent_tools.py
```




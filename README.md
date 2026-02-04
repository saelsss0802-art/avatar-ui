# AVATAR UI

📖 [日本語版はこちら](README.ja.md)

A desktop agent UI for personal AI avatars.  
Core + Console architecture powered by Grok API.

![demo](docs/demo.gif)

[![GeckoTerminal](https://img.shields.io/badge/GeckoTerminal-Token%20Info-blue)](https://www.geckoterminal.com/solana/pools/ky7frWSyXRcHKvN7UXyPuhA5rjP1ypDPDJNEHxJubmJ)
[![Orynth](https://img.shields.io/badge/Orynth-Featured-green)](https://orynth.dev/projects/avatar-ui)

## Features

- **Local-first** – Runs entirely on your machine
- **Approval flow** – Review every command before execution
- **Autonomous loop** – Purpose → Goal → Task hierarchy
- **Extensible** – Add channels, personas, tools

## Usage

1. Launch Core → Console appears
2. Set a purpose → Avatar proposes goals/tasks
3. Approve or reject each action
4. Avatar executes and reports results

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- [xAI API key](https://x.ai/)

### Setup

```bash
git clone https://github.com/siqidev/avatar-ui.git
cd avatar-ui

# Python
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Console
cd command/console && npm install && cd ../..
```

### Environment

Create `.env`:

```bash
XAI_API_KEY=your-xai-api-key
SPECTRA_API_KEY=your-secret-key
SPECTRA_CORE_URL=http://127.0.0.1:8000/v1/think
```

### Run

```bash
# Terminal 1: Core
source .venv/bin/activate
python -m uvicorn core.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Console
cd command/console && npm start
```

## Configuration

Edit `config.yaml`:

```yaml
avatar:
  name: AVATAR

grok:
  model: grok-4-1-fast-non-reasoning
  temperature: 1.0
  daily_token_limit: 100000

system_prompt: |
  Respond concisely in a technical style.
```

## Documentation

- [Architecture](docs/agent_design.md)
- [Implementation Plan](docs/implementation_plan.md)

## Support

AUI is the community token for AVATAR UI.

- [Orynth](https://orynth.dev/projects/avatar-ui)
- [GeckoTerminal](https://www.geckoterminal.com/solana/pools/ky7frWSyXRcHKvN7UXyPuhA5rjP1ypDPDJNEHxJubmJ)

Token CA (Solana): `63rvcwia2reibpdJMCf71bPLqBLvPRu9eM2xmRvNory`

> This section is for informational purposes only.

## Security

AVATAR UI executes commands with OS privileges.

| Principle | Description |
|-----------|-------------|
| **Local only** | Designed for single-user local operation |
| **Approval flow** | Review commands before execution |
| **API key management** | Keep `.env` out of git |

> External access (Discord, Roblox) planned for v0.3.0.

## License

MIT License

© 2025 SIQI (Sito Sikino)

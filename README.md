# AVATAR UI

<p align="center">
  📖 <a href="./README.ja.md">日本語版はこちら</a>
</p>

A next-generation interface foundation where humans and AI coexist.  
Supports Gemini, GPT, and Claude. An agent UI that runs on your desktop.

![demo](./docs/assets/avatar-ui_demo_02.gif)

<p align="center">
  <a href="https://www.geckoterminal.com/solana/pools/ky7frWSyXRcHKvN7UXyPuhA5rjP1ypDPDJNEHxJubmJ" target="_blank" rel="noopener">
    <img src="./docs/assets/geckoterminal-logo.png" alt="GeckoTerminal token info" width="320" />
  </a>
  <br />
  <sub>Token info by GeckoTerminal</sub>
</p>

<p align="center">
  <a href="https://orynth.dev/projects/avatar-ui" target="_blank" rel="noopener">
    <img src="https://orynth.dev/api/badge/avatar-ui?theme=dark&style=default" alt="Featured on Orynth" width="260" height="80" />
  </a>
  <br />
  <sub>Market by Orynth</sub>
</p>

## Features

- **Multi-LLM support** – Switch Gemini / OpenAI / Anthropic via config
- **Extensible tools** – Built-in search sub-agent. MCP integration and adding tools supported
- **Personalized UI** – Three color themes. Swap avatars freely
- **Desktop app** – Runs locally. Supports macOS / Windows / Linux
- **Commercial use OK** – Open source (MIT). Free for personal and commercial use

## Usage

1. Launch the app → the avatar appears in standby
2. Type a message → press `Enter` to send
3. The avatar responds in real time
4. Automatically runs Google Search when needed
5. Quit: `Ctrl+C`

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.12+
- API key (at least one)
  - [Gemini](https://aistudio.google.com/app/apikey)
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Anthropic](https://console.anthropic.com/settings/keys)

> ⚠️ Please follow the terms of service for external APIs (Gemini / OpenAI / Anthropic, etc.). API keys are not included in this repository.

### 1. Get the repository

Download the source code from GitHub (`git clone`).

```bash
git clone https://github.com/siqidev/avatar-ui.git
cd avatar-ui
```

### 2. Set environment variables

Store secrets such as API keys in the `.env` file.  
First, copy the template:

```bash
cp .env.example .env
```

Open `.env` and set the API key for the LLM you want to use:

```dotenv
GOOGLE_API_KEY=your-api-key-here
# If you use OpenAI / Anthropic, set the corresponding keys too
```

### 3. Setup and run

#### macOS / Linux

```bash
# Move to the project root (replace with your path)
# Example: if placed in the Documents folder
cd ~/Documents/avatar-ui

# Server setup (create a Python venv and install dependencies)
cd server
python3 -m venv .venv   # first time only
source .venv/bin/activate
pip install -e .        # first time only

# Run (server + client together)
cd ../app
npm install             # first time only
npm run dev:all
```

#### Windows (PowerShell)

```powershell
# Move to the project root (replace with your path)
# Example: if placed in the Documents folder
cd "$HOME\Documents\avatar-ui"

# Server setup (create a Python venv and install dependencies)
cd server
python -m venv .venv    # first time only
.\.venv\Scripts\Activate.ps1
pip install -e .        # first time only

# Run (server + client together)
cd ..\app
npm install             # first time only
npm run dev:all
```

When it starts, the Electron app opens automatically. During development, you can also open the URL shown in the terminal (e.g. `http://localhost:5173`) in your browser.

## Configuration

Copy the config file and edit it:

```bash
cp settings.default.json5 settings.json5
```

You can change the LLM, theme, and more in `settings.json5`.

### Switch LLMs

```json5
"server": {
  "llmProvider": "gemini",       // gemini | openai | anthropic
  "llmModel": "gemini-2.5-flash"
}
```

Set the corresponding API key in `.env` and restart the server.

### Search sub-agent

The Google Search sub-agent is enabled by default (runs with a Gemini model).  
To disable it:

```json5
"searchSubAgent": {
  "enabled": false
}
```

Because the search sub-agent uses the Gemini API, you must set `GOOGLE_API_KEY`.

### Customization

| Item | Where to configure |
|------|----------|
| System prompt | `settings.json5` → `server.systemPrompt` |
| Theme / colors | `settings.json5` → `ui.theme`, `ui.themes` |
| Avatar images | Place under `app/src/renderer/assets/` |
| Add tools | `server/main.py` → `tools` list |

## Documentation

- [Design doc](./docs/project.md) – Architecture, implementation details, roadmap
- [AG-UI Protocol](https://docs.ag-ui.com/) – Protocol specification (official)
- [Google ADK](https://google.github.io/adk-docs/) – Agent Development Kit (official)

## Support

AUI is the community token for supporting AVATAR UI.  
It is listed on Orynth, and market data is available on GeckoTerminal.

Token CA (Solana): `63rvcwia2reibpdJMCf71bPLqBLvPRu9eM2xmRvNory`

- Orynth: https://orynth.dev/projects/avatar-ui
- GeckoTerminal: https://www.geckoterminal.com/solana/pools/ky7frWSyXRcHKvN7UXyPuhA5rjP1ypDPDJNEHxJubmJ

> This section is for informational purposes only and does not constitute investment advice.

## License

[MIT License](LICENSE)

© 2025 [SIQI](https://siqi.jp) (Sito Sikino)

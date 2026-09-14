# G.T.B - Gonna Take the Boredom

> An AI agent built with **Strands Agents SDK** that transforms conversations into complete projects.

[![Watch Demo](https://img.shields.io/badge/🎬-Watch_Demo-red?style=for-the-badge)](https://youtu.be/HenDkc2Xvvw)

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Google%20Colab-orange)
![AI](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-purple)
![Strands](https://img.shields.io/badge/Strands-Agents%20SDK-blue)

---

## 🎬 Demo Video

[![G.T.B Demo](https://img.youtube.com/vi/HenDkc2Xvvw/maxresdefault.jpg)](https://youtu.be/HenDkc2Xvvw)

**Watch G.T.B in action:** [https://youtu.be/HenDkc2Xvvw](https://youtu.be/HenDkc2Xvvw)

---

## 🎯 The Problem

Developers waste hours on repetitive tasks:
- Setting up file structures
- Writing boilerplate code
- Creating placeholder assets
- Formatting documentation

## 💡 The Solution

**G.T.B** understands natural language, plans tasks using **Strands Agents SDK**, and executes them automatically.

## 🎁 The Value

Free your creativity. Remove boredom from programming. Focus on ideas, not implementation.

---

## 🧠 Strands Agents SDK Integration

G.T.B is built on the open-source **Strands Agents SDK** with three core tools:

| Tool | Function | Description |
|------|----------|-------------|
| `chat_tool` | `chat(message)` | Natural conversation |
| `build_tool` | `build(description)` | Generate complete projects |
| `images_tool` | `images(prompt)` | Create images via AI |

The agent orchestrates these tools using Strands:

```python
from strands import Agent

agent = Agent(
    name="GTB",
    description="G.T.B - Gonna Take the Boredom",
    tools=[chat_tool, build_tool, images_tool]
)
```

---

## ✨ Features

### 🎭 Three Operating Modes

| Mode | Description | Example |
|------|-------------|---------|
| 💬 **Chat** | Natural conversation to discuss ideas | *"I want a portfolio site"* |
| 🏗️ **Build** | Generate complete projects | *"Build what we discussed"* |
| 🖼️ **Images** | AI-powered image generation | *"3 cute cat logos"* |

### 🧠 Strands-Powered Agent
- Built with Strands Agents SDK
- 3 registered tools
- Automatic task orchestration

### 🎨 6 Ready Templates
- 🎨 Portfolio Website
- 🐍 Python Snake Game
- 📝 Blog
- 📊 Data Analysis
- 🛒 E-commerce Store
- 🔌 Flask API

### 🖥️ Full Interface
- Code Editor with live preview
- HTML Preview
- Dark/Light Mode
- History Sidebar (Chats, Projects, Files)
- Export Chat as Markdown
- Self-Learning Memory (editable)

### 🔌 Multi-Provider Support

**LLM Providers:**
| Provider | Model | Status |
|----------|-------|--------|
| Google Colab AI | Gemini 2.5 Flash | ✅ Free, Default |
| ClaudeStore | Claude Sonnet 4.6 | ✅ Works |
| Custom | Any OpenAI-compatible | ✅ Works |

**Image Providers:**
| Provider | Model | Status |
|----------|-------|--------|
| Replicate | Ideogram v3 Turbo | ✅ Works |
| Hugging Face | SDXL Base 1.0 | ✅ Works |
| Custom | Any API | ✅ Works |

---

## 🚀 Quick Start

### Prerequisites
- Google Colab account
- Files uploaded to Google Drive

### Run (Single Cell)

```python
import os, subprocess, time, threading
subprocess.run(["pkill", "-f", "flask"], capture_output=True)
subprocess.run(["fuser", "-k", "5000/tcp"], capture_output=True)
time.sleep(2)
os.chdir("/content/drive/MyDrive/project-forge-agent")
!pip install -q flask fpdf requests huggingface_hub strands-agents groq
def run_flask():
    from app import app
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
threading.Thread(target=run_flask, daemon=True).start()
time.sleep(3)
from google.colab import output
output.serve_kernel_port_as_iframe(5000, height=700)
while True:
    time.sleep(1)
```

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Flask Server (Port 5000)             │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Strands Agent (GTBAgent)                  │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │  │
│  │  │ chat_tool   │ │ build_tool  │ │ images_tool │ │  │
│  │  └─────────────┘ └─────────────┘ └─────────────┘ │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Agent Brain                          │  │
│  │  • Intent Analysis                                │  │
│  │  • Discovery Mode                                 │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Agent Core                           │  │
│  │  • Chat Mode                                      │  │
│  │  • Build Mode                                     │  │
│  │  • Image Mode                                     │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │           LLM Handler                             │  │
│  │  • Colab AI (Gemini 2.5 Flash)                   │  │
│  │  • ClaudeStore (LLMsRelay)                       │  │
│  │  • Custom (OpenAI-compatible)                    │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │          Image Handler                            │  │
│  │  • Replicate (Ideogram v3)                       │  │
│  │  • Hugging Face (SDXL)                           │  │
│  │  • Custom                                        │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │          File Extractor                          │  │
│  │  • Parse LLM output                              │  │
│  │  • Create project files                          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Google Colab + Google Drive                │
│                    (Google Cloud)                       │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `app.py` | Flask server with API endpoints |
| `strands_agent.py` | **Strands Agent** (core agent) |
| `agent_brain.py` | Intent analysis and planning |
| `agent_core.py` | Execution engine |
| `llm_handler.py` | LLM provider management |
| `image_handler.py` | Image generation |
| `pdf_generator.py` | PDF documentation |
| `file_extractor.py` | Parse and create files |
| `config_manager.py` | Settings management |
| `index.html` | Web interface |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| GET | `/api/agent/info` | Strands agent info |
| POST | `/api/chat` | Chat mode |
| POST | `/api/build` | Build project |
| POST | `/api/generate_image` | Generate single image |
| POST | `/api/generate_images_batch` | Generate multiple images |
| GET | `/api/download/<id>` | Download project ZIP |
| GET | `/api/image/<id>/<file>` | Serve image |
| GET | `/api/file/<id>/<file>` | View file |
| POST | `/api/save_file` | Save edited file |
| GET | `/api/memory` | Get agent memory |
| POST | `/api/memory` | Save agent memory |

---

## 🎯 Usage Examples

### Example 1: Chat
```
User: "I want a personal website"
G.T.B: "Great! A portfolio or blog?"
User: "Portfolio with contact section"
G.T.B: "I'll use a clean design. Ready to build?"
```

### Example 2: Build
```
User: "Create a Python snake game"
G.T.B: Generates main.py, game.py, player.py, constants.py
```

### Example 3: Images
```
User: "3 logo designs for a tech startup"
G.T.B: Generates 3 images via Replicate/Hugging Face
```

---

## ☁️ Google Cloud Integration

G.T.B runs on **Google Cloud infrastructure**:

- **Google Colab** — Compute environment (Google Cloud)
- **Google Gemini 2.5 Flash** — AI model (Google Cloud AI)
- **Google Drive** — Cloud storage for projects

---

## ⚙️ Configuration

### Settings Panel (⚙️)

**LLM Provider:**
- Provider selection (Colab AI, ClaudeStore, Custom)
- Base URL (optional)
- Model name (optional)
- API Key (optional)

**Image Provider:**
- Provider selection (Replicate, Hugging Face, Custom)
- Base URL (optional)
- Model name (optional)
- API Key (optional)

**Agent Memory:**
- Editable memory file
- Stores user preferences
- Learns across sessions

---

## 🧠 Self-Learning Memory

G.T.B learns from every interaction:

```
Conversation 1: "I prefer Python" → Stored
Conversation 2: "I like games" → Stored
Conversation 3: "I use Arabic comments" → Stored

Next session: G.T.B remembers and adapts!
```

Memory file: `agent_memory.txt`

---

## 📊 Statistics

| Metric | Value |
|--------|-------|
| Operating Modes | 3 |
| LLM Providers | 3 |
| Image Providers | 3 |
| Templates | 6 |
| API Endpoints | 12 |
| Features | 15+ |
| Strands Tools | 3 |

---

## 🔧 Troubleshooting

### Images not generating?
- Check API Key in Settings ⚙️
- Verify provider selected
- Hugging Face: use `stabilityai/stable-diffusion-xl-base-1.0`
- Replicate free: 6 requests/minute

### LLM not responding?
- Colab AI works without keys (default)
- ClaudeStore: verify API Key format
- Custom: check Base URL ends with `/v1`

### Server not starting?
```bash
pkill -f flask
fuser -k 5000/tcp
pip install flask fpdf requests huggingface_hub strands-agents groq
```

---

## 📜 License

MIT License — see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Strands Agents SDK** — Agent framework
- **Google** — Colab, Gemini 2.5 Flash, Cloud Platform
- **Replicate** — Image generation
- **Hugging Face** — Image generation
- **LLMsRelay** — Claude API
- **Flask** — Web framework

---

## 🏆 Built For

**Agents for Humans Hackathon** — AWS + Strands Agents SDK

---

> **"Gonna Take the Boredom"** — Transform ideas into reality ⚡

**Built with ❤️ on Google Cloud Platform**
```

---

# G.T.B - Gonna Take the Boredom

> An AI agent that transforms conversations into complete projects using Strands Agents SDK.

[![Demo Video](https://img.shields.io/badge/🎬-Watch_Demo-red)](YOUR_VIDEO_LINK)

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Google%20Colab-orange)
![AI](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-purple)
![Strands](https://img.shields.io/badge/Strands-Agents%20SDK-blue)

---

## 🎯 Overview

**G.T.B (Gonna Take the Boredom)** is an AI agent built with **Strands Agents SDK** that transforms natural language into working projects. It eliminates the boredom of repetitive coding tasks by automating project creation, image generation, and intelligent conversations.

### The Problem
Developers waste hours on repetitive tasks — file setup, boilerplate code, placeholder images, and documentation.

### The Solution
G.T.B understands natural language, plans tasks with Strands, and executes them automatically.

### The Value
Free your creativity. Focus on ideas, not implementation.

---

## 🧠 Strands Agents SDK Integration

G.T.B is built on **Strands Agents SDK** with three core tools:

| Tool | Function | Description |
|------|----------|-------------|
| `chat_tool` | `chat(message)` | Natural conversation |
| `build_tool` | `build(description)` | Generate complete projects |
| `images_tool` | `images(prompt)` | Create images via AI |

The agent uses Strands' `Agent` class to orchestrate these tools:

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

### 🎭 Three Modes
| Mode | Description |
|------|-------------|
| 💬 **Chat** | Natural conversation for idea discussion |
| 🏗️ **Build** | Generate complete projects |
| 🖼️ **Images** | AI-powered image generation |

### 🧠 Strands-Powered Agent
- Built with Strands Agents SDK
- 3 registered tools
- Automatic task orchestration

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

### 🖥️ Full Interface
- Code Editor
- HTML Preview
- Dark/Light Mode
- History Sidebar
- 6 Templates
- Export Chat

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

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                Flask Server (5000)                  │
│  ┌───────────────────────────────────────────────┐  │
│  │         Strands Agent (GTBAgent)              │  │
│  │  ┌─────────────┐ ┌─────────────┐ ┌─────────┐ │  │
│  │  │ chat_tool   │ │ build_tool  │ │ images  │ │  │
│  │  └─────────────┘ └─────────────┘ └─────────┘ │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │              Agent Brain                      │  │
│  │  • Intent Analysis                            │  │
│  │  • Discovery Mode                             │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │              Agent Core                       │  │
│  │  • Chat / Build / Images                      │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │           LLM Handler                         │  │
│  │  • Colab AI (Gemini 2.5 Flash)                │  │
│  │  • ClaudeStore • Custom                       │  │
│  └───────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────┐  │
│  │          Image Handler                        │  │
│  │  • Replicate • Hugging Face • Custom          │  │
│  └───────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

| File | Description |
|------|-------------|
| `app.py` | Flask server |
| `strands_agent.py` | **Strands Agent** (core) |
| `agent_brain.py` | Intent analysis |
| `agent_core.py` | Execution engine |
| `llm_handler.py` | LLM providers |
| `image_handler.py` | Image generation |
| `pdf_generator.py` | PDF docs |
| `file_extractor.py` | File parsing |
| `config_manager.py` | Settings |
| `index.html` | Web interface |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| GET | `/api/agent/info` | **Strands agent info** |
| POST | `/api/chat` | Chat mode |
| POST | `/api/build` | Build project |
| POST | `/api/generate_image` | Generate image |
| POST | `/api/generate_images_batch` | Batch images |
| GET | `/api/download/<id>` | Download ZIP |
| GET | `/api/memory` | Get memory |
| POST | `/api/memory` | Save memory |

---

## 🎯 Usage Examples

### Chat
```
User: "I want a personal website"
G.T.B: "Great! A portfolio or blog?"
```

### Build
```
User: "Create a Python snake game"
G.T.B: Generates main.py, game.py, player.py...
```

### Images
```
User: "3 logo designs for a tech startup"
G.T.B: Generates 3 images via Replicate/HF
```

---

## 🔧 Configuration

### Settings Panel (⚙️)
- LLM Provider + API Key + Model
- Image Provider + API Key + Model
- Groq API Key (optional)
- Agent Memory (editable)

---

## 📜 License

MIT License

---

## 🙏 Acknowledgments

- **Strands Agents SDK** — Agent framework
- **Google** — Colab, Gemini 2.5 Flash
- **Replicate** — Image generation
- **Hugging Face** — Image generation

---

> **"Gonna Take the Boredom"** ⚡

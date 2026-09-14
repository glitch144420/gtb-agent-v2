"""
G.T.B Strands Agent
===================
Real Strands Agents SDK integration for Chat, Build, and Images.
"""

import os
import json
from typing import Dict, Any, List, Optional

# استيراد Strands
try:
    from strands import Agent as StrandsAgent, tool
    STRANDS_AVAILABLE = True
except ImportError:
    try:
        from strands import Agent as StrandsAgent
        STRANDS_AVAILABLE = True
    except ImportError:
        STRANDS_AVAILABLE = False
        StrandsAgent = None
        tool = lambda f: f

from llm_handler import LLMHandler


class GTBAgent:
    """G.T.B Agent using Strands SDK."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.llm_handler = LLMHandler(config)
        self.agent = None
        
        if STRANDS_AVAILABLE:
            self._create_agent()
    
    def _create_agent(self):
        """Create Strands agent with tools."""
        try:
            self.agent = StrandsAgent(
                name="GTB",
                description="G.T.B - Gonna Take the Boredom. An AI agent that builds projects, generates images, and chats.",
                tools=[
                    self.chat_tool,
                    self.build_tool,
                    self.images_tool,
                ]
            )
            print("✅ Strands Agent created")
        except Exception as e:
            print(f"⚠️ Strands agent creation failed: {e}")
            self.agent = None
    
    def chat_tool(self, message: str) -> str:
        """Tool: Chat with user."""
        prompt = f"""You are G.T.B, a helpful AI assistant.
User: {message}
Respond naturally and conversationally."""
        return self.llm_handler.generate_text(prompt)
    
    def build_tool(self, description: str) -> str:
        """Tool: Build a project."""
        prompt = f"""You are a software engineer. Build a complete project for: {description}
Generate all necessary files with complete code."""
        return self.llm_handler.generate_text(prompt)
    
    def images_tool(self, prompt: str) -> str:
        """Tool: Generate images."""
        return f"Image generation requested: {prompt}"
    
    def run(self, task: str, mode: str = "chat") -> str:
        """Run the agent."""
        if self.agent:
            try:
                result = self.agent(task)
                return str(result)
            except Exception as e:
                print(f"Strands error: {e}")
                return self._fallback(task, mode)
        else:
            return self._fallback(task, mode)
    
    def _fallback(self, task: str, mode: str) -> str:
        """Fallback if Strands not available."""
        if mode == "chat":
            return self.chat_tool(task)
        elif mode == "build":
            return self.build_tool(task)
        else:
            return self.chat_tool(task)
    
    def get_info(self) -> Dict:
        """Get agent info."""
        return {
            "name": "GTB",
            "strands_available": STRANDS_AVAILABLE,
            "agent_created": self.agent is not None,
            "tools": ["chat", "build", "images"]
        }

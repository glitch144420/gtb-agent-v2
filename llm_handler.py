import json
import os
import requests
from typing import Dict, Any

class LLMHandler:
    """Abstracts multiple LLM providers."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("llm_provider", "colab_ai")
        self.api_key = config.get("llm_api_key", "")
        self.model = config.get("llm_model_name", "")
        self.base_url = config.get("llm_base_url", "")
        self.memory_file = "agent_memory.txt"
        self.aws_config = config.get("aws", {})
    
    def generate_text(self, prompt: str, use_memory: bool = True) -> str:
        """Generate text with memory context."""
        if use_memory:
            memory = self._read_memory()
            if memory:
                prompt = f"Context about user (from previous conversations):\n{memory}\n\n---\n\n{prompt}"
        
        if self.provider == "colab_ai":
            return self._generate_colab_ai(prompt)
        elif self.provider in ["claudestore", "llmsrelay"]:
            return self._generate_claudestore(prompt)
        elif self.provider in ["openai", "custom"]:
            return self._generate_custom(prompt)
        else:
            return self._generate_mock(prompt)
    
    def update_memory(self, conversation_text: str) -> None:
        """Update memory with ONLY essential user preferences."""
        try:
            prompt = f"""
Extract ONLY the user's core preferences from this conversation. 
Keep it VERY brief (max 3 bullet points):
- Preferred programming language
- Preferred project type
- Any strong preference stated

Format: "Prefers Python | Likes games | Uses simple code"

If nothing new, return "NO_UPDATE".
"""
            summary = self.generate_text(prompt, use_memory=False)
            
            if summary and "NO_UPDATE" not in summary and len(summary) < 200:
                with open(self.memory_file, "w", encoding="utf-8") as f:
                    f.write(summary.strip())
                print("✅ Memory updated (brief)")
        except Exception as e:
            print(f"Memory update error: {e}")
    
    def _read_memory(self) -> str:
        """Read memory file."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return f.read().strip()
        except:
            pass
        return ""
    
    def _generate_colab_ai(self, prompt: str) -> str:
        """Generate text using Google Colab AI (FREE)."""
        try:
            from google.colab import ai
            response = ai.generate_text(prompt, model_name='google/gemini-2.5-flash')
            return response
        except Exception as e:
            print(f"Colab AI error: {e}")
            return self._generate_mock(prompt)
    
    def _generate_claudestore(self, prompt: str) -> str:
        """Generate text using LLMsRelay (Anthropic format)."""
        try:
            base = self.base_url or "https://api.llmsrelay.com/v1"
            base = base.rstrip("/")
            url = base + "/messages"
            
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json"
            }
            
            model = self.model or "claude-sonnet-4.6"
            
            data = {
                "model": model,
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            print(f"ClaudeStore URL: {url}")
            print(f"ClaudeStore Model: {model}")
            
            response = requests.post(url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if "content" in result and result["content"]:
                    return result["content"][0]["text"]
            else:
                print(f"ClaudeStore error: {response.text[:200]}")
        except Exception as e:
            print(f"ClaudeStore error: {e}")
        
        return self._generate_mock(prompt)
    
    def _generate_custom(self, prompt: str) -> str:
        """Generate text using custom OpenAI-compatible API."""
        try:
            base = self.base_url or "https://api.openai.com/v1"
            base = base.rstrip("/")
            
            if base.endswith("/chat/completions"):
                url = base
            else:
                url = base + "/chat/completions"
            
            headers = {
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            }
            
            model = self.model or "gpt-3.5-turbo"
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000
            }
            
            print(f"Custom URL: {url}")
            print(f"Custom Model: {model}")
            
            response = requests.post(url, headers=headers, json=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and result["choices"]:
                    return result["choices"][0]["message"]["content"]
            else:
                print(f"Custom error: {response.text[:200]}")
                
        except Exception as e:
            print(f"Custom error: {e}")
        
        return self._generate_mock(prompt)
    
    def _generate_mock(self, prompt: str) -> str:
        """Generate mock response for testing."""
        return "Mock response - provider not available"

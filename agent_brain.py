import json
import os
import re
from typing import Dict, Any, List

class AgentBrain:
    def __init__(self):
        self.conversation_history = []
        self.memory_file = "agent_memory.json"
        self.memory = self.load_memory()
    
    def load_memory(self) -> Dict[str, Any]:
        """Load agent memory from file."""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"preferences": {}, "history": [], "learned": []}
    
    def save_memory(self):
        """Save agent memory to file."""
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)
    
    def process_request(self, user_input: str) -> Dict[str, Any]:
        """Process user request with memory context."""
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # تحليل النية
        intent = self._analyze_intent(user_input)
        
        # إذا كان الطلب مشروعاً، نطرح أسئلة توسعية
        if intent["type"] == "project" and intent["confidence"] > 0.6:
            questions = self._generate_expansion_questions(user_input)
            if questions:
                return {
                    "type": "questions",
                    "data": questions
                }
        
        # إذا كان جواباً على أسئلة، نكمل
        if self.conversation_history[-1].get("role") == "user":
            # تحقق إذا كان هذا رداً على أسئلة سابقة
            last_questions = self.memory.get("pending_questions")
            if last_questions:
                self.memory["pending_questions"] = None
                self.save_memory()
        
        if intent["confidence"] < 0.4:
            return {"type": "clarification", "data": self._generate_clarification(user_input)}
        
        return {"type": "plan", "data": {"steps": ["generate"], "tools": ["llm_handler"]}}
    
    def _generate_expansion_questions(self, user_input: str) -> List[str]:
        """Generate expansion questions before building."""
        questions = []
        
        # أسئلة أساسية
        if not any(k in user_input.lower() for k in ["python", "html", "react", "node", "java"]):
            questions.append("ما لغة البرمجة المفضلة؟ (Python, JavaScript, HTML/CSS...)")
        
        if not any(k in user_input.lower() for k in ["simple", "basic", "advanced", "complex", "بسيط", "متقدم"]):
            questions.append("ما مستوى التعقيد؟ (بسيط، متوسط، متقدم)")
        
        if not any(k in user_input.lower() for k in ["dark", "light", "theme", "لون"]):
            questions.append("هل تفضل مظهراً معيناً؟ (داكن، فاتح، ملون)")
        
        # أسئلة من الذاكرة
        if self.memory["preferences"].get("favorite_language"):
            questions.append(f"هل تريد استخدام {self.memory['preferences']['favorite_language']}؟")
        
        return questions[:3]  # 3 أسئلة كحد أقصى
    
    def _analyze_intent(self, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        has_project = any(k in text_lower for k in ["build", "create", "make", "انشئ", "ابني", "build me", "أريد"])
        return {"type": "project" if has_project else "other", "confidence": 0.9 if has_project else 0.3}
    
    def _generate_clarification(self, user_input: str) -> str:
        return "هل يمكنك توضيح ما تريد بناءه بالضبط؟"
    
    def _summarize_result(self, result: Dict[str, Any]) -> str:
        if result.get("status") == "success":
            return f"✅ تم إنشاء {len(result.get('files', []))} ملفات"
        return "❌ فشل التنفيذ"
    
    def learn_from_interaction(self, user_input: str, result: Dict[str, Any]):
        """Learn from the interaction and update memory."""
        # تعلم اللغة المفضلة
        languages = ["python", "javascript", "html", "css", "react", "node", "java", "c++"]
        for lang in languages:
            if lang in user_input.lower():
                self.memory["preferences"]["favorite_language"] = lang
                break
        
        # تعلم نوع المشروع
        if result.get("status") == "success":
            project_type = result.get("project_type", "general")
            self.memory["history"].append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M"),
                "request": user_input[:100],
                "type": project_type,
                "success": True
            })
            
            # تحديث العدادات
            if "project_counts" not in self.memory:
                self.memory["project_counts"] = {}
            self.memory["project_counts"][project_type] = self.memory["project_counts"].get(project_type, 0) + 1
        
        self.save_memory()

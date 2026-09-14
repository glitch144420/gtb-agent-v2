import os
import json
import uuid
import re
import time
from typing import Dict, Any, List

class AgentCore:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.project_base_path = "temp"
        
        from llm_handler import LLMHandler
        from file_extractor import FileExtractor
        from pdf_generator import PDFGenerator
        from image_handler import ImageHandler
        
        self.llm_handler = LLMHandler(config)
        self.file_extractor = FileExtractor()
        self.pdf_generator = PDFGenerator()
        self.image_handler = ImageHandler(config)
    
    def chat(self, message: str, conversation_history: List[str] = None) -> str:
        """Chat mode - natural conversation, minimal questions."""
        context = "\n".join(conversation_history[-5:]) if conversation_history else ""
        prompt = f"""You are G.T.B, a helpful AI assistant.

Previous conversation:
{context}

User: {message}

Respond naturally and conversationally. Give helpful information and suggestions.
Only ask a question if truly necessary (max 1-2 focused questions).
Do NOT generate code yet.
"""
        return self.llm_handler.generate_text(prompt)
    
    def build(self, message: str, conversation_history: List[str] = None) -> Dict[str, Any]:
        """Build mode - generate actual project."""
        project_id = str(uuid.uuid4())[:8]
        project_path = os.path.join(self.project_base_path, project_id)
        os.makedirs(project_path, exist_ok=True)
        
        context = "\n".join(conversation_history[-10:]) if conversation_history else ""
        
        try:
            llm_response = self._generate_code(message, context)
            files = self._extract_files(llm_response, project_path)
            
            pdf_file = self._create_pdf(message, llm_response, project_path)
            if pdf_file:
                files.append(pdf_file)
            
            # توليد الصور إذا كان مزود الصور مفعلاً
            if self.image_handler.provider != "none" and self.image_handler.api_key:
                print("🎨 توليد الصور للمشروع...")
                image_files = self.generate_images_with_llm(message, project_path)
                files.extend(image_files)
                print(f"✅ تم توليد {len(image_files)} صور")
            
            summary = self._generate_summary(message)
            
            # تحديث الذاكرة
            self.llm_handler.update_memory(f"User request: {message}\nContext: {context}")
            
            return {
                "status": "success",
                "project_id": project_id,
                "files": files,
                "summary": summary,
                "download_url": f"/api/download/{project_id}",
                "project_name": self._extract_project_name(message)
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def _generate_code(self, user_input: str, context: str = "") -> str:
        project_type = self._detect_project_type(user_input)
        
        prompt = f"""
You are an expert software engineer.

Context from discussion:
{context}

Build request: {user_input}
Project type: {project_type}

Generate complete, working code files. Format:

```
filename.ext
```language
file content
```

Include README.md with instructions.
"""
        return self.llm_handler.generate_text(prompt)
    
    def _generate_summary(self, user_input: str) -> str:
        try:
            prompt = f"Summarize in one sentence: {user_input}"
            return self.llm_handler.generate_text(prompt).strip()[:200]
        except:
            return user_input[:100]
    
    def _extract_files(self, response: str, project_path: str) -> List[str]:
        return self.file_extractor.extract_files(response, project_path)
    
    def _create_pdf(self, user_input: str, llm_response: str, project_path: str) -> str:
        try:
            return self.pdf_generator.create_pdf("Documentation", llm_response, os.path.join(project_path, "documentation.pdf"))
        except:
            return None
    
    def _detect_project_type(self, user_input: str) -> str:
        types = {
            "python": ["python", "flask", "django", "fastapi", "script", "game", "لعبة"],
            "web": ["website", "web", "html", "css", "javascript", "موقع"],
            "react": ["react", "next", "vue", "angular"],
            "node": ["node", "express", "api", "server"],
            "data": ["data", "analysis", "pandas", "numpy", "تحليل"]
        }
        text = user_input.lower()
        for t, keywords in types.items():
            if any(k in text for k in keywords):
                return t
        return "general"
    
    def generate_images(self, prompts: List[str], project_path: str) -> List[str]:
        """Generate images from prompts."""
        image_files = []
        assets_path = os.path.join(project_path, "assets", "images")
        os.makedirs(assets_path, exist_ok=True)
        
        for i, prompt in enumerate(prompts):
            try:
                image_url = self.image_handler.generate_image(prompt)
                if image_url:
                    filename = f"image_{i+1}.png"
                    save_path = os.path.join(assets_path, filename)
                    if self.image_handler.download_image(image_url, save_path):
                        image_files.append(f"assets/images/{filename}")
            except Exception as e:
                print(f"Image {i+1} error: {e}")
        
        return image_files
    
    def generate_images_with_llm(self, user_input: str, project_path: str, conversation_history: str = "") -> List[str]:
        """Generate images intelligently using LLM for prompts."""
        image_files = []
        
        try:
            # 1. LLM يصوغ البرومتات
            prompts_prompt = f"""
Based on this request: "{user_input}"
Conversation context: {conversation_history}

Generate 3 image prompts that would be appropriate for this project.
Return ONLY the prompts, one per line. Make them detailed and professional.
"""
            
            response = self.llm_handler.generate_text(prompts_prompt)
            
            # استخراج البرومتات من الرد
            prompts = []
            for line in response.split('\n'):
                line = line.strip()
                if line and len(line) > 5 and not line.startswith('```'):
                    # إزالة الأرقام والرموز
                    cleaned = re.sub(r'^\d+[\.\)\-]\s*', '', line)
                    if cleaned and len(cleaned) > 5:
                        prompts.append(cleaned)
            
            prompts = prompts[:3]
            
            if not prompts:
                print("⚠️ لم يتم استخراج برومتات")
                return []
            
            print(f"🎨 تم توليد {len(prompts)} برومت:")
            for i, p in enumerate(prompts):
                print(f"   {i+1}. {p[:60]}...")
            
            # 2. توليد الصور
            assets_path = os.path.join(project_path, "assets", "images")
            os.makedirs(assets_path, exist_ok=True)
            
            for i, prompt in enumerate(prompts):
                try:
                    # انتظار بين الطلبات لتجنب Rate Limit
                    if i > 0:
                        print(f"⏳ انتظار 5 ثوانٍ قبل الصورة {i+1}...")
                        time.sleep(5)
                    
                    image_url = self.image_handler.generate_image(prompt)
                    if image_url:
                        # 3. LLM يقترح اسماء
                        name_prompt = f"Suggest a short filename for an image with prompt: {prompt}. Return just the filename with .png extension."
                        filename = self.llm_handler.generate_text(name_prompt).strip()
                        
                        # تنظيف الاسم
                        filename = re.sub(r'[^\w\-\.]', '_', filename)
                        if not filename.endswith('.png'):
                            filename += '.png'
                        if len(filename) > 50:
                            filename = f"image_{i+1}.png"
                        
                        save_path = os.path.join(assets_path, filename)
                        
                        if self.image_handler.download_image(image_url, save_path):
                            rel_path = f"assets/images/{filename}"
                            image_files.append(rel_path)
                            print(f"✅ {filename}")
                except Exception as e:
                    print(f"❌ صورة {i+1}: {e}")
            
        except Exception as e:
            print(f"خطأ في توليد الصور: {e}")
        
        return image_files
    
    def generate_images_with_llm(self, user_input: str, project_path: str, conversation_history: str = "") -> List[str]:
        """Generate images intelligently using LLM for prompts."""
        image_files = []
        
        try:
            # 1. LLM يصوغ البرومتات
            prompts_prompt = f"""
Based on this request: "{user_input}"
Conversation context: {conversation_history}

Generate 3 image prompts that would be appropriate for this project.
Return ONLY the prompts, one per line. Make them detailed and professional.
"""
            
            response = self.llm_handler.generate_text(prompts_prompt)
            
            # استخراج البرومتات من الرد
            prompts = []
            for line in response.split('\n'):
                line = line.strip()
                if line and len(line) > 5 and not line.startswith('```'):
                    # إزالة الأرقام والرموز
                    cleaned = re.sub(r'^\d+[\.\)\-]\s*', '', line)
                    if cleaned and len(cleaned) > 5:
                        prompts.append(cleaned)
            
            prompts = prompts[:3]
            
            if not prompts:
                print("⚠️ لم يتم استخراج برومتات")
                return []
            
            print(f"🎨 تم توليد {len(prompts)} برومت:")
            for i, p in enumerate(prompts):
                print(f"   {i+1}. {p[:60]}...")
            
            # 2. توليد الصور
            assets_path = os.path.join(project_path, "assets", "images")
            os.makedirs(assets_path, exist_ok=True)
            
            for i, prompt in enumerate(prompts):
                try:
                    # انتظار بين الطلبات لتجنب Rate Limit
                    if i > 0:
                        print(f"⏳ انتظار 5 ثوانٍ قبل الصورة {i+1}...")
                        time.sleep(5)
                    
                    image_url = self.image_handler.generate_image(prompt)
                    if image_url:
                        # 3. LLM يقترح اسماء
                        name_prompt = f"Suggest a short filename for an image with prompt: {prompt}. Return just the filename with .png extension."
                        filename = self.llm_handler.generate_text(name_prompt).strip()
                        
                        # تنظيف الاسم
                        filename = re.sub(r'[^\w\-\.]', '_', filename)
                        if not filename.endswith('.png'):
                            filename += '.png'
                        if len(filename) > 50:
                            filename = f"image_{i+1}.png"
                        
                        save_path = os.path.join(assets_path, filename)
                        
                        if self.image_handler.download_image(image_url, save_path):
                            rel_path = f"assets/images/{filename}"
                            image_files.append(rel_path)
                            print(f"✅ {filename}")
                except Exception as e:
                    print(f"❌ صورة {i+1}: {e}")
            
        except Exception as e:
            print(f"خطأ في توليد الصور: {e}")
        
        return image_files
    
    def _extract_image_prompts(self, text: str) -> List[str]:
        """Extract image prompts from user input."""
        prompts = []
        
        # 1. البحث عن أوصاف صور بين علامات اقتباس
        quoted = re.findall(r'["\']([^"\']+)["\']', text)
        prompts.extend(quoted)
        
        # 2. البحث عن "image of X" أو "صورة X"
        patterns = [
            r'image of ([^,\.]+)',
            r'images? of ([^,\.]+)',
            r'صورة ([^,\.]+)',
            r'صور ([^,\.]+)'
        ]
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            prompts.extend(matches)
        
        # 3. إذا طلب موقع/مدونة، نولد صور placeholder تلقائياً
        if any(k in text.lower() for k in ["website", "blog", "portfolio", "موقع", "مدونة"]):
            if not prompts:
                prompts = [
                    "modern website hero banner, professional design",
                    "team collaboration illustration, modern flat design",
                    "abstract technology background, blue purple gradient"
                ]
        
        # 4. تنظيف وإزالة التكرار
        cleaned = []
        for p in prompts:
            p = p.strip()
            if p and p not in cleaned:
                cleaned.append(p)
        
        return cleaned[:3]
    
    def _extract_project_name(self, user_input: str) -> str:
        return "-".join(user_input.strip()[:50].split())

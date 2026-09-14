import json
import os
import requests
import base64
import time
from typing import Dict, Any, Optional

class ImageHandler:
    """Handles image generation from multiple providers."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.provider = config.get("image_provider", "none")
        self.api_key = config.get("image_api_key", "")
        self.base_url = config.get("image_base_url", "")
        self.model = config.get("image_model_name", "")
        self.aws_config = config.get("aws", {})
    
    def generate_image(self, prompt: str) -> Optional[str]:
        """Generate an image and return URL or base64."""
        if self.provider == "replicate":
            return self._generate_replicate(prompt)
        elif self.provider == "openai":
            return self._generate_dalle(prompt)
        elif self.provider == "custom":
            return self._generate_custom(prompt)
        elif self.provider == "huggingface":
            return self._generate_huggingface(prompt)
        elif self.provider == "aws_bedrock":
            return self._generate_bedrock(prompt)
        else:
            print("No image provider configured")
            return None
    
    def _generate_replicate(self, prompt: str) -> Optional[str]:
        """Generate image using Replicate."""
        try:
            url = "https://api.replicate.com/v1/predictions"
            headers = {
                "Authorization": "Token " + self.api_key,
                "Content-Type": "application/json"
            }
            
            model_version = self.model or "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b"
            
            data = {
                "version": model_version,
                "input": {"prompt": prompt}
            }
            
            print(f"Replicate URL: {url}")
            print(f"Model: {model_version}")
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code in [200, 201]:
                prediction = response.json()
                
                # التحقق من وجود output مباشرة
                if "output" in prediction and prediction["output"]:
                    output = prediction["output"]
                    if isinstance(output, list) and output:
                        # قد تكون قائمة من URLs أو كائنات
                        first = output[0]
                        if isinstance(first, str):
                            return first
                        elif isinstance(first, dict) and "url" in first:
                            return first["url"]
                        elif isinstance(first, dict) and "image" in first:
                            return first["image"]
                    elif isinstance(output, str):
                        return output
                
                # إذا لم يكن هناك output، ننتظر
                prediction_url = prediction.get("urls", {}).get("get")
                
                if prediction_url:
                    for _ in range(60):
                        time.sleep(2)
                        result = requests.get(prediction_url, headers=headers, timeout=30)
                        if result.status_code == 200:
                            result_data = result.json()
                            status = result_data.get("status")
                            
                            if status == "succeeded":
                                output = result_data.get("output", [])
                                print(f"Output type: {type(output)}")
                                print(f"Output content: {str(output)[:200]}")
                                
                                if isinstance(output, list) and output:
                                    first = output[0]
                                    if isinstance(first, str):
                                        return first
                                    elif isinstance(first, dict):
                                        # البحث عن أي URL في الكائن
                                        for key in ["url", "image", "image_url", "src"]:
                                            if key in first and first[key]:
                                                return first[key]
                                elif isinstance(output, str):
                                    return output
                                elif isinstance(output, dict):
                                    for key in ["url", "image", "image_url", "src"]:
                                        if key in output and output[key]:
                                            return output[key]
                            elif status == "failed":
                                print(f"Failed: {result_data.get('error')}")
                                return None
                
                print("Timeout or no output")
                return None
            
            print(f"Error: {response.text[:300]}")
            return None
            
        except Exception as e:
            print(f"Replicate error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generate_dalle(self, prompt: str) -> Optional[str]:
        """Generate image using OpenAI DALL-E."""
        try:
            url = self.base_url or "https://api.openai.com/v1/images/generations"
            headers = {
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            }
            model = self.model or "dall-e-3"
            data = {
                "model": model,
                "prompt": prompt,
                "size": "1024x1024",
                "quality": "standard",
                "n": 1
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                data_list = result.get("data", [])
                if data_list:
                    return data_list[0].get("url")
            return None
        except Exception as e:
            print(f"DALL-E error: {e}")
            return None
    
    def _generate_custom(self, prompt: str) -> Optional[str]:
        """Generate image using custom API."""
        try:
            url = self.base_url.rstrip("/") if self.base_url else ""
            headers = {
                "Authorization": "Bearer " + self.api_key,
                "Content-Type": "application/json"
            }
            data = {
                "model": self.model,
                "prompt": prompt
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            if response.status_code == 200:
                result = response.json()
                data_list = result.get("data", [])
                if data_list:
                    if "url" in data_list[0]:
                        return data_list[0]["url"]
                    elif "b64_json" in data_list[0]:
                        return "data:image/png;base64," + data_list[0]["b64_json"]
            return None
        except Exception as e:
            print(f"Custom error: {e}")
            return None
    
    def _generate_bedrock(self, prompt: str) -> Optional[str]:
        """Generate image using AWS Bedrock."""
        try:
            import boto3
            
            client = boto3.client(
                'bedrock-runtime',
                region_name=self.aws_config.get("region", "us-east-1"),
                aws_access_key_id=self.aws_config.get("access_key"),
                aws_secret_access_key=self.aws_config.get("secret_key")
            )
            
            body = json.dumps({
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 7,
                "steps": 30,
                "width": 512,
                "height": 512
            })
            
            response = client.invoke_model(
                modelId="stability.stable-diffusion-xl-v1",
                contentType="application/json",
                accept="application/json",
                body=body
            )
            
            response_body = json.loads(response['body'].read())
            if "artifacts" in response_body:
                return "data:image/png;base64," + response_body["artifacts"][0]["base64"]
            return None
        except Exception as e:
            print(f"Bedrock error: {e}")
            return None
    
    def _generate_huggingface(self, prompt: str) -> Optional[str]:
        """Generate image using Hugging Face Hub library."""
        try:
            from huggingface_hub import InferenceClient
            
            model = self.model or "stabilityai/stable-diffusion-xl-base-1.0"
            
            print(f"HuggingFace Model: {model}")
            
            client = InferenceClient(
                model=model,
                token=self.api_key if self.api_key else None
            )
            
            # توليد الصورة
            image = client.text_to_image(prompt)
            
            if image:
                # حفظ الصورة مؤقتاً وإرجاع المسار
                import tempfile
                temp_path = os.path.join(tempfile.gettempdir(), "hf_image.png")
                image.save(temp_path)
                return temp_path
            
            return None
                
        except Exception as e:
            print(f"HuggingFace error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _generate_huggingface(self, prompt: str) -> Optional[str]:
        """Generate image using Hugging Face Hub library."""
        try:
            from huggingface_hub import InferenceClient
            
            model = self.model or "stabilityai/stable-diffusion-xl-base-1.0"
            
            print(f"HuggingFace Model: {model}")
            
            client = InferenceClient(
                model=model,
                token=self.api_key if self.api_key else None
            )
            
            # توليد الصورة
            image = client.text_to_image(prompt)
            
            if image:
                # حفظ الصورة مؤقتاً وإرجاع المسار
                import tempfile
                temp_path = os.path.join(tempfile.gettempdir(), "hf_image.png")
                image.save(temp_path)
                return temp_path
            
            return None
                
        except Exception as e:
            print(f"HuggingFace error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def download_image(self, image_url, save_path: str) -> bool:
        """Download image from URL, base64, bytes, or local file path."""
        try:
            # إذا كان bytes مباشرة
            if isinstance(image_url, bytes):
                with open(save_path, "wb") as f:
                    f.write(image_url)
                return True
            
            # إذا كان مسار ملف محلي
            if isinstance(image_url, str) and os.path.exists(image_url):
                import shutil
                shutil.copy2(image_url, save_path)
                return True
            
            # إذا كان base64
            if isinstance(image_url, str) and image_url.startswith("data:image"):
                image_data = base64.b64decode(image_url.split(",")[1])
                with open(save_path, "wb") as f:
                    f.write(image_data)
                return True
            
            # إذا كان URL
            if isinstance(image_url, str):
                response = requests.get(image_url, timeout=30)
                if response.status_code == 200:
                    with open(save_path, "wb") as f:
                        f.write(response.content)
                    return True
            
            return False
        except Exception as e:
            print(f"Download error: {e}")
            return False

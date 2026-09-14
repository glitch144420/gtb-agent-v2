import os
import zipfile
import json
import time
from flask import Flask, request, jsonify, send_file

from agent_brain import AgentBrain
from agent_core import AgentCore
from config_manager import ConfigManager

app = Flask(__name__)

config_manager = ConfigManager()
agent_brain = AgentBrain()

# تخزين المحادثات في الذاكرة
conversations = {}

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Get agent memory."""
    memory_file = "agent_memory.txt"
    if os.path.exists(memory_file):
        with open(memory_file, "r", encoding="utf-8") as f:
            return jsonify({"memory": f.read()})
    return jsonify({"memory": ""})

@app.route('/api/memory', methods=['POST'])
def save_memory():
    """Save agent memory."""
    data = request.json
    memory = data.get('memory', '')
    
    with open("agent_memory.txt", "w", encoding="utf-8") as f:
        f.write(memory)
    
    return jsonify({"status": "saved"})

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    """Chat mode - discuss without building."""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    if session_id not in conversations:
        conversations[session_id] = []
    
    config = config_manager.load_config()
    
    # دمج إعدادات الصور مباشرة من الطلب
    if data.get("image_provider"):
        config["image_provider"] = data["image_provider"]
    if data.get("image_api_key"):
        config["image_api_key"] = data["image_api_key"]
    if data.get("image_base_url"):
        config["image_base_url"] = data["image_base_url"]
    if data.get("image_model_name"):
        config["image_model_name"] = data["image_model_name"]
    
    # دمج إعدادات LLM
    if data.get("llm_provider"):
        config["llm_provider"] = data["llm_provider"]
    if data.get("llm_api_key"):
        config["llm_api_key"] = data["llm_api_key"]
    if data.get("llm_base_url"):
        config["llm_base_url"] = data["llm_base_url"]
    if data.get("llm_model_name"):
        config["llm_model_name"] = data["llm_model_name"]
    
    print(f"🖼️ مزود الصور: {config.get('image_provider', 'none')}")
    print(f"🖼️ نموذج الصور: {config.get('image_model_name', 'غير محدد')}")
    print(f"🖼️ مفتاح الصور: {config.get('image_api_key', '')[:15] if config.get('image_api_key') else 'غير موجود'}...")
    
    agent_core = AgentCore(config)
    
    response = agent_core.chat(message, conversations[session_id])
    conversations[session_id].append(f"User: {message}")
    conversations[session_id].append(f"Assistant: {response}")
    
    return jsonify({"status": "chat", "message": response})

@app.route('/api/build', methods=['POST'])
def handle_build():
    """Build mode - generate actual project."""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    history = conversations.get(session_id, [])
    
    config = config_manager.load_config()
    
    # دمج إعدادات الصور مباشرة من الطلب
    if data.get("image_provider"):
        config["image_provider"] = data["image_provider"]
    if data.get("image_api_key"):
        config["image_api_key"] = data["image_api_key"]
    if data.get("image_base_url"):
        config["image_base_url"] = data["image_base_url"]
    if data.get("image_model_name"):
        config["image_model_name"] = data["image_model_name"]
    
    # دمج إعدادات LLM
    if data.get("llm_provider"):
        config["llm_provider"] = data["llm_provider"]
    if data.get("llm_api_key"):
        config["llm_api_key"] = data["llm_api_key"]
    if data.get("llm_base_url"):
        config["llm_base_url"] = data["llm_base_url"]
    if data.get("llm_model_name"):
        config["llm_model_name"] = data["llm_model_name"]
    
    print(f"🖼️ مزود الصور: {config.get('image_provider', 'none')}")
    print(f"🖼️ نموذج الصور: {config.get('image_model_name', 'غير محدد')}")
    print(f"🖼️ مفتاح الصور: {config.get('image_api_key', '')[:15] if config.get('image_api_key') else 'غير موجود'}...")
    
    agent_core = AgentCore(config)
    
    result = agent_core.build(message, history)
    
    # حفظ الملخص
    if result.get("status") == "success":
        with open(os.path.join("temp", result["project_id"], "summary.txt"), "w") as f:
            f.write(result.get("summary", ""))
    
    return jsonify(result)

@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    """Generate an image from a prompt."""
    data = request.json
    prompt = data.get('prompt', '')
    project_id = data.get('project_id', 'standalone')
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    config = config_manager.load_config()
    
    # دمج إعدادات الصور من الطلب
    if data.get("image_provider"):
        config["image_provider"] = data["image_provider"]
    if data.get("image_api_key"):
        config["image_api_key"] = data["image_api_key"]
    if data.get("image_base_url"):
        config["image_base_url"] = data["image_base_url"]
    if data.get("image_model_name"):
        config["image_model_name"] = data["image_model_name"]
    
    from image_handler import ImageHandler
    image_handler = ImageHandler(config)
    
    try:
        image_url = image_handler.generate_image(prompt)
        if image_url:
            # حفظ الصورة
            save_dir = os.path.join("temp", project_id, "assets", "images")
            os.makedirs(save_dir, exist_ok=True)
            filename = f"generated_{int(time.time())}.png"
            save_path = os.path.join(save_dir, filename)
            
            if image_handler.download_image(image_url, save_path):
                return jsonify({
                    "status": "success",
                    "image_url": f"/api/image/{project_id}/assets/images/{filename}",
                    "local_path": f"assets/images/{filename}"
                })
            else:
                # إذا فشل التحميل، نرجع الرابط مباشرة
                return jsonify({
                    "status": "success",
                    "image_url": image_url
                })
        else:
            return jsonify({"status": "error", "error": "Failed to generate image"}), 500
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/api/generate_images_batch', methods=['POST'])
def generate_images_batch():
    """Generate multiple images from user request."""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    config = config_manager.load_config()
    
    # دمج إعدادات الصور
    if data.get("image_provider"):
        config["image_provider"] = data["image_provider"]
    if data.get("image_api_key"):
        config["image_api_key"] = data["image_api_key"]
    if data.get("image_model_name"):
        config["image_model_name"] = data["image_model_name"]
    
    agent_core = AgentCore(config)
    
    # توليد الصور فقط
    project_id = str(__import__('uuid').uuid4())[:8]
    project_path = os.path.join("temp", project_id)
    os.makedirs(project_path, exist_ok=True)
    
    image_files = agent_core.generate_images_with_llm(message, project_path)
    
    if image_files:
        return jsonify({
            "status": "success",
            "project_id": project_id,
            "files": image_files,
            "summary": f"تم توليد {len(image_files)} صور",
            "download_url": f"/api/download/{project_id}",
            "project_name": "images-batch"
        })
    else:
        return jsonify({
            "status": "error",
            "error": "فشل توليد الصور. تأكد من الإعدادات."
        }), 500

@app.route('/api/download/<project_id>')
def download_project(project_id):
    project_path = os.path.join("temp", project_id)
    if not os.path.exists(project_path):
        return jsonify({"error": "Not found"}), 404
    
    zip_path = os.path.join("temp", f"{project_id}.zip")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_path):
            for file in files:
                fp = os.path.join(root, file)
                zipf.write(fp, os.path.relpath(fp, project_path))
    
    return send_file(zip_path, as_attachment=True, download_name=f"project_{project_id}.zip")

@app.route('/api/image/<project_id>/<path:filename>')
def get_image(project_id, filename):
    """Serve image files directly."""
    fp = os.path.join("temp", project_id, filename)
    if os.path.exists(fp):
        return send_file(fp, mimetype='image/png')
    return jsonify({"error": "Not found"}), 404

@app.route('/api/file/<project_id>/<path:filename>')
def get_file(project_id, filename):
    fp = os.path.join("temp", project_id, filename)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            return jsonify({"content": f.read()})
    return jsonify({"error": "Not found"}), 404

@app.route('/api/save_file', methods=['POST'])
def save_file():
    data = request.json
    project_id = data.get('project_id')
    filename = data.get('filename')
    content = data.get('content')
    
    fp = os.path.join("temp", project_id, filename)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return jsonify({"status": "saved"})

@app.route('/api/files/<project_id>')
def list_files(project_id):
    project_path = os.path.join("temp", project_id)
    if not os.path.exists(project_path):
        return jsonify({"files": []})
    
    files = []
    for root, dirs, filenames in os.walk(project_path):
        for filename in filenames:
            rel_path = os.path.relpath(os.path.join(root, filename), project_path)
            files.append(rel_path)
    
    return jsonify({"files": files})

# ============ VIDEO STUDIO ENDPOINTS ============

@app.route('/api/download_file/<path:filename>')
def download_file(filename):
    """Download any output file."""
    # البحث في temp
    possible_paths = [
        os.path.join("temp", filename),
        os.path.join("temp/uploads", filename),
        filename
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return send_file(path, as_attachment=True, download_name=filename)
    
    return jsonify({"error": "File not found"}), 404

# ============ VIDEO PIPELINE ============

@app.route('/api/download_file/<path:filename>')
def download_output(filename):
    """Download output file."""
    paths = [
        os.path.join("temp", filename),
        os.path.join("temp/uploads", filename),
        filename
    ]
    for p in paths:
        if os.path.exists(p):
            return send_file(p, as_attachment=True, download_name=filename)
    return jsonify({"error": "File not found"}), 404

@app.route('/api/agent/info', methods=['GET'])
def agent_info():
    """Get Strands agent info."""
    config = config_manager.load_config()
    from strands_agent import GTBAgent
    agent = GTBAgent(config)
    return jsonify(agent.get_info())

if __name__ == '__main__':
    os.makedirs("temp", exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=False)

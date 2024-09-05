from flask import Flask, request, jsonify, send_file
import io
from comfyui_client import ComfyUIClient
from PIL import Image
import os

app = Flask(__name__)

# 初始化 ComfyUI 客戶端
comfyui_client = ComfyUIClient("211.22.118.147:8188")

# 提交圖像生成請求
@app.route('/generate-avatar', methods=['POST'])
def generate_avatar():
    data = request.json
    
    # 加載 workflow.json
    workflow_path = './workflows/basic_avatar_generation.json'
    if not os.path.exists(workflow_path):
        return jsonify({"error": "Workflow file not found"}), 404

    prompt = comfyui_client.load_prompt(workflow_path)
    
    # 更新 workflow 中的題詞 (text) 根據 gender 和 avatar 描述
    gender = data.get("gender", "neutral")
    avatar_description = data.get("avatar_description", "a person portrait")
    print("prompt[6]: ", prompt["6"])
    print("prompt[5]: ", prompt["5"])
    
    
    # 動態更新 CLIPTextEncode 節點中的描述
    if "6" in prompt and "inputs" in prompt["6"] and "text" in prompt["6"]["inputs"]:
        prompt["6"]["inputs"]["text"] = f"{avatar_description} {gender} avatar"
    else:
        return jsonify({"error": "Invalid prompt structure"}), 400

    # 更新解析度
    if "resolution" in data:
        resolution = data["resolution"]
        prompt["5"]["inputs"]["height"] = resolution.get('height', 512)
        prompt["5"]["inputs"]["width"] = resolution.get('width', 512)
    else:
        # 預設解析度 512x512
        prompt["5"]["inputs"]["height"] = 512
        prompt["5"]["inputs"]["width"] = 512

    # 使用 ComfyUIClient 處理 workflow，生成圖像
    images = comfyui_client.get_images(prompt)
    
    # 保存生成的圖片
    comfyui_client.save_images(images)
    
    return jsonify({'message': 'Avatar generation in progress'}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

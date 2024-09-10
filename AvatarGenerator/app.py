from flask import Flask, request, jsonify, send_file
import io
from comfyui_client import ComfyUIClient
import os
import logging
import json

# 設置日誌格式和級別
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

# 初始化 ComfyUI 客戶端
comfyui_client = ComfyUIClient("211.22.118.147:8188")

@app.route('/generate-avatar-by-image', methods=['POST'])
def generate_avatar_by_image():
    data = request.json
    imageName = data.get("imageName", "profile_emily.png")
    gender = data.get("gender", "neutral")
    width = data.get('width', 512)
    height = data.get('height', 512)
    
    logging.info(f"Generating avatar by image: {imageName}, gender: {gender}, resolution: {width}x{height}")
    
    # Validate resolution
    if not (64 <= width <= 2048 and 64 <= height <= 2048):
        return jsonify({"error": "Resolution out of bounds"}), 400
    
    # 使用 ComfyUIClient 處理 workflow，生成圖像
    images = comfyui_client.get_images(imageName, gender, width, height)
    
    # 保存生成的圖片
    comfyui_client.save_images(images)
    
    return jsonify({'message': 'Avatar generation in progress'}), 202    

# 提交圖像生成請求
@app.route('/generate-avatar-by-prompt', methods=['POST'])
def generate_avatar_by_prompt():
    data = request.json
    
    # 加載 workflow.json
    workflow_path = './workflows/basic_avatar_generation.json'
    if not os.path.exists(workflow_path):
        return jsonify({"error": "Workflow file not found"}), 404

    prompt = comfyui_client.load_prompt(workflow_path)
    
    # 更新 workflow 中的題詞 (text) 根據 gender 和 avatar 描述
    gender = data.get("gender", "neutral")
    avatar_description = data.get("avatar_description", "a person portrait")
    
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

@app.route('/upload-image', methods=['POST'])
def upload_image():
    """處理圖片上傳並調用 comfyui_client 上傳到服務器"""
    if 'image' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # 保存圖片到本地
        file_path = os.path.join('./input', file.filename)
        file.save(file_path)
        
        # 調用 comfyui_client 將圖片上傳到服務器
        response = comfyui_client.upload_image(file_path, file.filename)
        
        return jsonify({"message": "Image uploaded successfully!", "response": response}), 200
    else:
        return jsonify({"error": "File upload failed"}), 500
    

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    video_description = data.get("video_description", "")
    # frame_rate = data.get("frame_rate", 8)

    logging.info(f"Generating video with description: {json.dumps(video_description, ensure_ascii=False)}")

    # Validate frame rate
    # if not (1 <= frame_rate <= 60):
    #     return jsonify({"error": "Frame rate out of bounds"}), 400

    # 調用 comfyui_client 的 get_video 方法，並動態替換 workflow 中的描述
    video_file, mime_type = comfyui_client.get_video(video_description)
    logging.debug(f"video_file: {video_file}, mime_type: {mime_type}")

    # 檢查返回的 video_data 是否是 tuple，並提取文件路徑和 MIME 類型
    if not video_file:
        return jsonify({"error": "Failed to generate video"}), 500
    
    # Read the actual video content from the file path
    with open(video_file, 'rb') as f:
        video_data = f.read()

    # 生成的影片返回
    video_io = io.BytesIO(video_data)
    video_filename = os.path.basename(video_file)
        
    return send_file(video_io, mimetype=mime_type, as_attachment=True, download_name=video_filename)

if __name__ == '__main__':
    app.run(debug=True)

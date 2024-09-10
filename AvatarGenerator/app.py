from flask import Flask, request, jsonify, send_file
import io
from comfyui_client import ComfyUIClient
from PIL import Image
import os

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
    
    print(f"Generating avatar by image: {imageName}, gender: {gender}, resolution: {width}x{height}")
    
    # Validate resolution
    if not (64 <= width <= 2048 and 64 <= height <= 2048):
        return jsonify({"error": "Resolution out of bounds"}), 400
    
    # 加載 workflow.json
    workflow_path = './workflows/generate_avatar_by_image.json'
    if not os.path.exists(workflow_path):
        return jsonify({"error": "Workflow file not found"}), 404
    
    positive_prompts = "Anime-style portrait, silver hair, soft lighting, delicate facial features, large reflective eyes, high-detailed, serene background"

    negative_prompts = "Excessive makeup, hyper-realism, distorted anatomy, harsh lighting, exaggerated emotions, overly vibrant or neon colors, blurry or out-of-focus details"

    prompts = {
        "positive": {
            "neutral": positive_prompts + ", neutral gender character, medium-length silver hair, casual outdoor clothing, soft shadows",
            "female": positive_prompts + ", female character, long silver hair with soft waves, sporty jacket, cute expression",
            "male": positive_prompts + ", male character, medium-length silver hair, sporty jacket with subtle masculine design, sharp but gentle features",
        },
     "negative": {
            "neutral": negative_prompts + ", overly masculine or overly feminine features, extreme age (too young or too old), unnatural or neon-colored hair",
         "female": negative_prompts + ", highly masculine features, cluttered background, harsh shadows, overly stylized expressions",
            "male": negative_prompts + ", overly feminine features, exaggerated muscles, harsh shadows, overly vibrant or extreme hair colors",
        }
    }
    
    prompt = comfyui_client.load_prompt(workflow_path)
    
    # 動態更新 CLIPTextEncode 節點中的描述
    if "2" in prompt and "inputs" in prompt["2"] and "text" in prompt["2"]["inputs"]:
        prompt["2"]["inputs"]["text"] = prompts["positive"][gender]
    else:
        return jsonify({"error": "Invalid prompt structure"}), 400
    if "3" in prompt and "inputs" in prompt["3"] and "text" in prompt["3"]["inputs"]:
        prompt["3"]["inputs"]["text"] = prompts["negative"][gender]
    else:
        return jsonify({"error": "Invalid prompt structure"}), 400

    # 更新解析度
    if "height" in data and "5" in prompt and "inputs" in prompt["5"] and "height" in prompt["5"]["inputs"]:
        prompt["5"]["inputs"]["height"] = height
    else:
        # 預設解析度 512x512
        prompt["5"]["inputs"]["height"] = 512

    if "width" in data and "5" in prompt and "inputs" in prompt["5"] and "width" in prompt["5"]["inputs"]:
        prompt["5"]["inputs"]["width"] = width
    else:
        # 預設解析度 512x512
        prompt["5"]["inputs"]["width"] = 512
    
    print(f"Prompt positive: {prompt['2']['inputs']['text']}")
    print(f"Prompt negative: {prompt['3']['inputs']['text']}")
    
    # 使用 ComfyUIClient 處理 workflow，生成圖像
    images = comfyui_client.get_images(prompt)
    
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
    frame_rate = data.get("frame_rate", 8)
    resolution = data.get("resolution", {"width": 512, "height": 512})

    print(f"Generating video with description: {video_description}, resolution: {resolution}, frame rate: {frame_rate}")

    # Validate resolution
    width = resolution.get("width", 512)
    height = resolution.get("height", 512)
    if not (64 <= width <= 2048 and 64 <= height <= 2048):
        return jsonify({"error": "Resolution out of bounds"}), 400

    # Validate frame rate
    if not (1 <= frame_rate <= 60):
        return jsonify({"error": "Frame rate out of bounds"}), 400

    # 調用 comfyui_client 的 get_video 方法，並動態替換 workflow 中的描述
    video_data = comfyui_client.get_video(video_description, width, height, frame_rate)
    if not video_data:
        return jsonify({"error": "Failed to generate video"}), 500

    # 生成的影片返回
    video_io = io.BytesIO(video_data)
    return send_file(video_io, mimetype='video/mp4', as_attachment=True, attachment_filename='generated_video.mp4')
    

if __name__ == '__main__':
    app.run(debug=True)

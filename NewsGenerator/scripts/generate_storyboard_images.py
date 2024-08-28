from diffusers import FluxPipeline
import torch
import os
import re

class ModelManager:
    _pipe = None

    @classmethod
    def get_pipeline(cls):
        if cls._pipe is None:
            print("開始加載 FLUX.1 [schnell] 模型...")
            cls._pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            cls._pipe.to(device)
            cls._pipe.enable_attention_slicing()
            print("模型加載成功。")
        return cls._pipe

def generate_prompt_from_script(script):
    # 使用正則表達式將文本拆分為句子
    sentences = re.split(r'(?<=[。！？])', script.strip())
    prompts = []
    # 為每一行生成提示並添加風格
    for sentence in sentences:
        clean_sentence = sentence.strip()
        if clean_sentence:
            # 生成針對每個句子的 prompt
            prompt = f"Generate a professional illustration in a consistent minimalist style depicting the following content: {clean_sentence}"
            prompts.append(prompt)

    return prompts

def generate_storyboard_images(script_path):
    try:
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"文件 {script_path} 未找到")

        with open(script_path, 'r') as file:
            script = file.read().strip()

        prompts = generate_prompt_from_script(script)
        print(f"生成分鏡稿圖片的提示列表: {prompts}")

        pipe = ModelManager.get_pipeline()
        if pipe is None:
            print("模型加載失敗，終止生成圖片。")
            return []

        # 確保輸出文件夾存在
        os.makedirs('data/output', exist_ok=True)

        output_paths = []
        for i, prompt in enumerate(prompts):
            print(f"正在生成圖片: {prompt}")
            image = pipe(prompt, guidance_scale=7.5, num_inference_steps=100).images[0]  # 對每個 prompt 生成一張圖片
            output_path = f'data/output/storyboard_image_{i+1}.png'
            image.save(output_path)
            output_paths.append(output_path)

        print(f"已保存分鏡稿圖片: {output_paths}")
        return output_paths
    except Exception as e:
        print(f"生成分鏡稿圖片時出錯: {e}")
        return []

# 執行腳本，自動生成分鏡稿圖片
generate_storyboard_images('data/output/news_script.txt')
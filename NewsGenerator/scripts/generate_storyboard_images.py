from diffusers import FluxPipeline
import torch
import os

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
    lines = script.strip().splitlines()
    non_empty_lines = [line.strip() for line in lines if line.strip()]
    prompts = []
    # 為每一行生成提示並添加風格
    for line in non_empty_lines:
        prompt = f"Generate a professional illustration in a consistent minimalist style depicting the following content: {line}"
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

        # 确保输出目录存在
        os.makedirs('data/output', exist_ok=True)

        output_paths = []
        for i, prompt in enumerate(prompts):
            print(f"正在生成图片: {prompt}")
            # 使用更多的推理步數來提高圖片質量
            image = pipe(prompt, guidance_scale=7.5, num_inference_steps=100).images[0]
            output_path = f'data/output/storyboard_image_{i+1}.png'
            image.save(output_path)
            output_paths.append(output_path)

        print(f"已保存分鏡稿圖片: {output_paths}")
        return output_paths
    except Exception as e:
        print(f"生成分鏡稿圖片時出錯: {e}")
        return []

# 執行腳步，生成分鏡稿圖片
generate_storyboard_images('data/output/news_script.txt')

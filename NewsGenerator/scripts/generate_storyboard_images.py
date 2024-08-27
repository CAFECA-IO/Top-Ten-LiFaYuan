from diffusers import DiffusionPipeline
import torch
import os

def load_model():
    try:
        print("開始加載 FLUX.1 [schnell] 模型...")
        pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16) # 使用 bfloat16 以減少內存占用
        pipe.to("cpu")  # 明確指定使用 CPU
        pipe.enable_model_cpu_offload()  # 使用 accelerate 來優化 CPU 記憶體使用
        print("模型加載成功。")
        return pipe
    except Exception as e:
        print(f"加載模型時出錯: {e}")
        return None

def generate_storyboard_images(script_path):
    try:
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"文件 {script_path} 未找到")

        with open(script_path, 'r') as file:
            script = file.read().strip()

        # 限制文本長度到模型的最大序列長度
        max_length = 38
        if len(script) > max_length:
            script = script[:max_length].rsplit(' ', 1)[0]  # 確保不會在句子中間截斷

        pipe = load_model()
        if pipe is None:
            print("模型加載失敗，終止生成圖片。")
            return []

        # 生成分鏡稿圖片
        images = pipe(script, guidance_scale=0.0, num_inference_steps=2).images
        
        # 確保輸出目錄存在
        os.makedirs('data/output', exist_ok=True)
        
        output_paths = []
        for i, image in enumerate(images):
            output_path = f'data/output/storyboard_image_{i+1}.png'
            image.save(output_path)
            output_paths.append(output_path)

        print(f"已保存分鏡稿圖片: {output_paths}")
        return output_paths
    except Exception as e:
        print(f"生成分鏡稿圖片時出錯: {e}")
        return []

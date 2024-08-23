from diffusers import DiffusionPipeline
import torch

def generate_storyboard_images(script_path):
    try:
        # 讀取新聞稿文本
        with open(script_path, 'r') as file:
            script = file.read()

        # 加載 FLUX.1 [schnell] 模型
        pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
        pipe.enable_model_cpu_offload()  # 可選：通過將部分處理卸載到 CPU 來節省顯存

        # 從文本提示生成圖片
        images = pipe(script, guidance_scale=0.0, num_inference_steps=4).images
        output_paths = []

        # 將每個生成的圖片保存到 output 文件夾
        for i, image in enumerate(images):
            output_path = f'data/output/storyboard_image_{i+1}.png'
            image.save(output_path)
            output_paths.append(output_path)
            
        print(f"已保存分鏡稿圖片: {output_path}")

        # 返回圖片列表
        return output_path
    except Exception as e:
        print(f"生成分鏡稿圖片時出錯: {e}")
        return []

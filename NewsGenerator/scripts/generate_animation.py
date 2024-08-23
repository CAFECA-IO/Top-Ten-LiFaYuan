from diffusers import DiffusionPipeline
import torch

def generate_animation_from_images(image_paths):
    try:
        # 加載 AnimateDiff 模型
        pipeline = DiffusionPipeline.from_pretrained("animate-diffusion-model/animatediff", torch_dtype=torch.float16)
        pipeline.to("cuda")  # 假設有 CUDA 支持

        # 生成動畫
        animation = pipeline(image_paths, num_inference_steps=50)

        # 保存生成的動畫
        output_path = 'data/output/generated_animation.mp4'
        animation.save(output_path)

        print(f"已保存生成的動畫: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成動畫時出錯: {e}")
        return None
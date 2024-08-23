from diffusers import DiffusionPipeline
import torch

def generate_anchor_animation(anchor_image_path, voiceover_path):
    try:
        # 加載 AnimateDiff 模型
        pipeline = DiffusionPipeline.from_pretrained("animate-diffusion-model/animatediff", torch_dtype=torch.float16)
        pipeline.to("cuda")  # 假設有 CUDA 支持

        # 生成動畫，將主播圖片和語音結合
        prompt = f"A news anchor speaking with the voiceover provided."
        animation = pipeline(prompt, image=anchor_image_path, audio=voiceover_path, num_inference_steps=50)

        # 保存生成的動畫
        output_path = 'data/output/anchor_animation.mp4'
        animation.save(output_path)
        print(f"已保存生成的主播動畫: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成主播動畫時出錯: {e}")
        return None
import torch
import os
from diffusers import AnimateDiffPipeline, DDIMScheduler, MotionAdapter
from diffusers.utils import export_to_gif

def generate_anchor_animation(anchor_image_path):
    try:
        # 加載 Motion Adapter
        print("開始加載 Motion Adapter...")
        adapter = MotionAdapter.from_pretrained("guoyww/animatediff-motion-adapter-v1-5-2", torch_dtype=torch.float16)
        
        # 加載 AnimateDiff 模型
        print("加載 AnimateDiff 模型管道...")
        model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
        pipeline = AnimateDiffPipeline.from_pretrained(model_id, motion_adapter=adapter, torch_dtype=torch.float16)
        pipeline.to("cuda")  # 使用 GPU 加速
        
        # 配置調度器
        print("配置調度器...")
        scheduler = DDIMScheduler.from_pretrained(
            model_id,
            subfolder="scheduler",
            clip_sample=False,
            timestep_spacing="linspace",
            beta_schedule="linear",
            steps_offset=1,
        )
        pipeline.scheduler = scheduler

        # 啟用記憶體優化（根據需要）
        pipeline.enable_vae_slicing()
        pipeline.enable_model_cpu_offload()

        print("開始生成動畫...")
        # 生成動畫，將主播圖片和語音結合
        prompt = "A news anchor speaking with the voiceover provided."
        output = pipeline(
            prompt=prompt,
            image=anchor_image_path,
            num_frames=16,
            guidance_scale=7.5,
            num_inference_steps=50,
            generator=torch.Generator("cuda").manual_seed(42),
        )

        # 保存生成的動畫
        output_path = 'data/output/anchor_animation.gif'
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        if output.frames:
            print("將生成的動畫保存為 GIF...")
            export_to_gif(output.frames[0], output_path)  # 如果需要保存為GIF
        else:
            print("未生成任何動畫幀。")
        
        print(f"已保存生成的主播動畫: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成主播動畫時出錯: {e}")
        return None


image_paths = ['data/output/news_anchor.png']
generate_anchor_animation(image_paths)

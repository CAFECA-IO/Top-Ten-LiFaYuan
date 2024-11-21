import torch
import os
from diffusers import AnimateDiffSparseControlNetPipeline, AutoencoderKL, MotionAdapter, SparseControlNetModel, DPMSolverMultistepScheduler
from diffusers.utils import export_to_gif, load_image
from typing import List
from PIL import Image
from moviepy.editor import ImageSequenceClip
import numpy as np


def export_to_mp4(frames, output_video_path, fps=24):
    # 檢查是否所有幀都是 PIL.Image.Image 對象
    if all(isinstance(frame, Image.Image) for frame in frames):
        # 如果需要訪問幀的形狀，將其轉換為 NumPy 數組
        img_array = np.array(frames[0])
        print(f"幀的尺寸（高度, 寬度, 通道數）: {img_array.shape}")
    else:
        raise ValueError("All frames should be PIL.Image.Image objects")

    # 使用 moviepy 將圖像幀列表轉換為 MP4 視頻
    clip = ImageSequenceClip([np.array(frame) for frame in frames], fps=fps)
    clip.write_videofile(output_video_path, codec="libx264", audio=False)


def export_to_gif(images: List[Image.Image], output_gif_path: str = None, fps: int = 10, duration_per_frame: float = None) -> str:
    if output_gif_path is None:
        output_gif_path = tempfile.NamedTemporaryFile(suffix=".gif").name

    if duration_per_frame is not None:
        duration_ms = int(duration_per_frame * 1000)  # 將秒轉換為毫秒
    else:
        duration_ms = 1000 // fps  # 默認基於 fps 計算

    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=duration_ms,
        loop=0,
    )
    return output_gif_path

def generate_animation_from_images(image_paths, total_duration=45):
    try:
        # 模型和設備設定
        print("開始設定模型和設備...")
        model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
        motion_adapter_id = "guoyww/animatediff-motion-adapter-v1-5-3"
        controlnet_id = "guoyww/animatediff-sparsectrl-scribble"
        lora_adapter_id = "guoyww/animatediff-motion-lora-v1-5-3"
        vae_id = "stabilityai/sd-vae-ft-mse"
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # 加載 Motion Adapter, ControlNet, VAE 和 Scheduler
        print("加載 Motion Adapter 模型...")
        motion_adapter = MotionAdapter.from_pretrained(motion_adapter_id, torch_dtype=torch.float16).to(device)
        print("加載 ControlNet 模型...")
        controlnet = SparseControlNetModel.from_pretrained(controlnet_id, torch_dtype=torch.float16).to(device)
        print("加載 VAE 模型...")
        vae = AutoencoderKL.from_pretrained(vae_id, torch_dtype=torch.float16).to(device)
        print("加載 Scheduler...")
        scheduler = DPMSolverMultistepScheduler.from_pretrained(
            model_id,
            subfolder="scheduler",
            beta_schedule="linear",
            algorithm_type="dpmsolver++",
            use_karras_sigmas=True,
        )

        # 加載 AnimateDiff 模型管道
        print("加載 AnimateDiff 模型管道...")
        pipeline = AnimateDiffSparseControlNetPipeline.from_pretrained(
            model_id,
            motion_adapter=motion_adapter,
            controlnet=controlnet,
            vae=vae,
            scheduler=scheduler,
            torch_dtype=torch.float16,
        ).to(device)
        
        # 加載 LoRA 權重
        print("加載 LoRA 權重...")
        pipeline.load_lora_weights(lora_adapter_id, adapter_name="motion_lora")
        pipeline.fuse_lora(lora_scale=1.0)

        # 加載並處理輸入圖片
        print("加載並處理輸入圖片...")
        conditioning_frames = [load_image(img_path) for img_path in image_paths]
        condition_frame_indices = list(range(len(image_paths)))
        
        # 每幀持續時間，以確保總時長為45秒
        # total_frames = len(image_paths)
        # duration_per_frame = total_duration / total_frames

        # 生成動畫
        print("開始生成動畫...")
        video = pipeline(
            prompt="Generate a high-quality animation in a consistent minimalist style that closely follows the provided reference images suitable for news broadcasting. The animation should depict the scene of a news anchor presenting the latest updates in a studio setting.",
            negative_prompt="complex patterns, abstract, unrelated elements",
            num_inference_steps=5,
            conditioning_frames=conditioning_frames,
            controlnet_conditioning_scale=2.0,
            controlnet_frame_indices=condition_frame_indices,
            generator=torch.Generator().manual_seed(42),
        # ).frames[0]
        ).frames
        
        # 檢查 video 的內容和類型
        print(f"生成的 video 類型: {type(video)}")
        if isinstance(video, list) and len(video) > 0 and isinstance(video[0], list):
            video = [frame for sublist in video for frame in sublist]
            print(f"video 列表的長度: {len(video)}")
            if len(video) > 0:
                print(f"第一幀的類型: {type(video[0])}")
        else:
            print("生成的 video 並非一個列表。")
            
        # 如果幀不是 PIL.Image.Image 對象，報錯
        for i, frame in enumerate(video):
            if not isinstance(frame, Image.Image):
                print(f"第 {i} 幀不是 PIL.Image.Image 對象，它是: {type(frame)}")
                raise ValueError("All frames should be PIL.Image.Image objects")

        # 保存生成的動畫
        # output_path = 'data/output/generated_animation.gif'  
        # 保存生成的動畫為 MP4
        output_path = 'data/output/generated_animation.mp4'
        print(f"確保輸出目錄存在: {os.path.dirname(output_path)}")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 將生成的動畫保存為 GIF
        # print("將生成的動畫保存為 GIF...")
        # export_to_gif(video, output_gif_path=output_path, duration_per_frame=duration_per_frame)
        print("將生成的動畫保存為 MP4...")
        fps=int(len(video) / total_duration)
        if fps <= 0:
            print(f"計算的 FPS: {fps}, len(video): {len(video)}, total_duration: {total_duration}")
            fps = 24
        export_to_mp4(video, output_video_path=output_path, fps=fps)


        print(f"已保存生成的動畫: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成動畫時出錯: {e}")
        return None

image_paths = ['data/output/storyboard_image_1.png', 'data/output/storyboard_image_2.png', 'data/output/storyboard_image_3.png', 'data/output/storyboard_image_4.png', 'data/output/storyboard_image_5.png', 'data/output/storyboard_image_6.png', 'data/output/storyboard_image_7.png', 'data/output/storyboard_image_8.png']
generate_animation_from_images(image_paths, 45)

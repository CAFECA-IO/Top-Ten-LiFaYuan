import torch
from diffusers import AnimateDiffSparseControlNetPipeline, AutoencoderKL, MotionAdapter, SparseControlNetModel, DPMSolverMultistepScheduler
from diffusers.utils import export_to_gif, load_image

def generate_animation_from_images(image_paths):
    try:
        # 模型和設備設定
        model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
        motion_adapter_id = "guoyww/animatediff-motion-adapter-v1-5-3"
        controlnet_id = "guoyww/animatediff-sparsectrl-scribble"
        lora_adapter_id = "guoyww/animatediff-motion-lora-v1-5-3"
        vae_id = "stabilityai/sd-vae-ft-mse"
        device = "cuda"

        # 加載 Motion Adapter, ControlNet, VAE 和 Scheduler
        motion_adapter = MotionAdapter.from_pretrained(motion_adapter_id, torch_dtype=torch.float16).to(device)
        controlnet = SparseControlNetModel.from_pretrained(controlnet_id, torch_dtype=torch.float16).to(device)
        vae = AutoencoderKL.from_pretrained(vae_id, torch_dtype=torch.float16).to(device)
        scheduler = DPMSolverMultistepScheduler.from_pretrained(
            model_id,
            subfolder="scheduler",
            beta_schedule="linear",
            algorithm_type="dpmsolver++",
            use_karras_sigmas=True,
        )

        # 加載 AnimateDiff 模型管道
        pipeline = AnimateDiffSparseControlNetPipeline.from_pretrained(
            model_id,
            motion_adapter=motion_adapter,
            controlnet=controlnet,
            vae=vae,
            scheduler=scheduler,
            torch_dtype=torch.float16,
        ).to(device)
        
        # 加載 LoRA 權重
        pipeline.load_lora_weights(lora_adapter_id, adapter_name="motion_lora")
        pipeline.fuse_lora(lora_scale=1.0)

        # 加載並處理輸入圖片
        conditioning_frames = [load_image(img_path) for img_path in image_paths]
        condition_frame_indices = list(range(len(image_paths)))

        # 生成動畫
        prompt = "an aerial view of a cyberpunk city, night time, neon lights, masterpiece, high quality"
        negative_prompt = "low quality, worst quality, letterboxed"

        video = pipeline(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=25,
            conditioning_frames=conditioning_frames,
            controlnet_conditioning_scale=1.0,
            controlnet_frame_indices=condition_frame_indices,
            generator=torch.Generator().manual_seed(1337),
        ).frames[0]

        # 保存生成的動畫
        output_path = 'data/output/generated_animation.gif'
        export_to_gif(video, output_path)

        print(f"已保存生成的動畫: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成動畫時出錯: {e}")
        return None

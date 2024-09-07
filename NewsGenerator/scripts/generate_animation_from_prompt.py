import torch
import os
import re
from diffusers import AnimateDiffSparseControlNetPipeline, AutoencoderKL, MotionAdapter, SparseControlNetModel, DPMSolverMultistepScheduler
from diffusers.utils import export_to_gif, load_image
from googletrans import Translator

# 初始化翻譯器
translator = Translator()

def translate_with_retry(text, retries=3):
    for attempt in range(retries):
        try:
            return translator.translate(text, src='zh-CN', dest='en')
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
    return None

def generate_prompt_from_script(script_path):
    try:
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"文件 {script_path} 未找到")

        with open(script_path, 'r') as file:
            script = file.read().strip()
            
        sentences = re.split(r'(?<=[。！？])', script.strip())
        prompts = []

        for sentence in sentences:
            clean_sentence = sentence.strip()
            if clean_sentence:
                try:
                    translated = translate_with_retry(clean_sentence)
                    print(f"Original: {clean_sentence}, Translated: {translated.text if translated else 'None'}")
                    if translated and translated.text:
                        # 避免抽象或不具體的prompt
                        if "press release" not in translated.text.lower():
                            prompt = f"Generate a professional illustration in a consistent minimalist style depicting the following content: {translated.text}"
                            prompts.append(prompt)
                        else:
                            print(f"Skipping non-specific prompt: {translated.text}")
                    else:
                        print(f"Translation failed for sentence: {clean_sentence}")
                except Exception as e:
                    print(f"Error during translation: {e}")
                    continue
    except Exception as e:
        print(f"generate_prompt_from_script出錯: {e}")
        return []   

    return prompts

def refine_prompt(prompt):
    # 這裡可以根據需要進行一些簡單的規則過濾或修改
    if len(prompt) > 100:
        print(f"Prompt too long, simplifying: {prompt}")
        prompt = prompt[:100] + "..."
    return prompt

def generate_animation_from_prompts(prompts, total_duration=45, output_path='data/output/generated_animation_by_prompt.gif'):
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

        # 每幀持續時間，以確保總時長為45秒
        total_frames = len(prompts)
        duration_per_frame = total_duration / total_frames

        # 開始生成動畫
        video_frames = []
        for i, prompt in enumerate(prompts):
            refined_prompt = refine_prompt(prompt)
            print(f"生成動畫幀 {i+1}/{total_frames}: {refined_prompt}")
            video = pipeline(
                prompt=refined_prompt,
                num_inference_steps=50,
                generator=torch.Generator().manual_seed(1337),
            ).frames
    
            if video is None or len(video) == 0:
                print(f"生成失敗，跳過此幀: {refined_prompt}")
                continue
    
        video_frames.extend(video)

        # 確保輸出目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 將生成的動畫保存為 GIF
        print("將生成的動畫保存為 GIF...")
        export_to_gif(video_frames, output_path, duration=duration_per_frame)
        print(f"已保存生成的動畫: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成動畫時出錯: {e}")
        return None

# 生成提示列表
prompts = generate_prompt_from_script('data/output/news_script.txt')

# 根據提示列表生成動畫
generate_animation_from_prompts(prompts, total_duration=45)

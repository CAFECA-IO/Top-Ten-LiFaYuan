import requests
import json

# 定義 ComfyUI API 的端點
url = "http://211.22.118.147:8188/api/prompt"

# 建立 API 請求的負載
payload = {
    "client_id": "d69ba57a5d5c42b4bbfac39c6ff13a5b",
    "prompt": {
        "2": {
            "inputs": {
                "seed": 722020139875983,
                "steps": 20,
                "cfg": 7,
                "sampler_name": "ddpm",
                "scheduler": "normal",
                "denoise": 1,
                "preview_method": "auto",
                "vae_decode": "true",
                "model": ["4", 0],
                "positive": ["8", 0],
                "negative": ["15", 2],
                "latent_image": ["15", 3],
                "optional_vae": ["15", 4]
            },
            "class_type": "KSampler (Efficient)"
        },
        "4": {
            "inputs": {
                "model_name": "v3_sd15_mm.ckpt",
                "beta_schedule": "sqrt_linear (AnimateDiff)",
                "motion_scale": 1.08,
                "apply_v2_models_properly": True,
                "model": ["15", 0],
                "context_options": ["6", 0]
            },
            "class_type": "ADE_AnimateDiffLoaderWithContext"
        },
        "6": {
            "inputs": {
                "context_length": 16,
                "context_stride": 1,
                "context_overlap": 2,
                "closed_loop": False,
                "fuse_method": "pyramid",
                "use_on_equal_length": False,
                "start_percent": 0,
                "guarantee_steps": 1
            },
            "class_type": "ADE_LoopedUniformContextOptions"
        },
        "7": {
            "inputs": {
                "frame_rate": 8,
                "loop_count": 0,
                "filename_prefix": "AnimateDiff",
                "format": "video/h264-mp4",
                "pix_fmt": "yuv420p",
                "crf": 22,
                "save_metadata": False,
                "pingpong": False,
                "save_output": False,
                "images": ["33", 0]
            },
            "class_type": "VHS_VideoCombine"
        },
        "8": {
            "inputs": {
                "text": "\"0\" :\"Anime girl closed eyes (happy:1.2) listening to music,seaside\",\n\"6\" :\"Anime girl open eyes (happy:1.2) listening to music,seaside\",\n\"9\" :\"Anime girl open eyes (happy, smiling:1.2) listening to music,seaside\"\n\n",
                "max_frames": 16,
                "print_output": False,
                "pre_text": "best quality, masterpiece, beautiful, extreme detailed, highest detailed,\n",
                "start_frame": 0,
                "end_frame": 0,
                "clip": ["15", 5]
            },
            "class_type": "BatchPromptSchedule"
        },
        "15": {
            "inputs": {
                "ckpt_name": "dreamshaper_8.safetensors",
                "vae_name": "Baked VAE",
                "clip_skip": -1,
                "lora_name": "SD1.5/animatediff/v3_sd15_adapter.ckpt",
                "lora_model_strength": 0.8,
                "lora_clip_strength": 0.8,
                "positive": "best quality, masterpiece, beautiful, extreme detailed, highest detailed,\n",
                "negative": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face",
                "token_normalization": "none",
                "weight_interpretation": "comfy",
                "empty_latent_width": 512,
                "empty_latent_height": 512,
                "batch_size": 16
            },
            "class_type": "Efficient Loader"
        },
        "25": {
            "inputs": {
                "strength": 0.8,
                "start_percent": 0.062,
                "end_percent": 0.8,
                "positive": ["8", 0],
                "negative": ["15", 2],
                "control_net": ["38", 0],
                "image": ["2", 5]
            },
            "class_type": "ACN_AdvancedControlNetApply"
        },
        "28": {
            "inputs": {
                "seed": 1037631207225729,
                "steps": 25,
                "cfg": 8.5,
                "sampler_name": "ddpm",
                "scheduler": "normal",
                "denoise": 0.7,
                "model": ["4", 0],
                "positive": ["25", 0],
                "negative": ["25", 1],
                "latent_image": ["36", 0]
            },
            "class_type": "KSampler"
        },
        "31": {
            "inputs": {
                "samples": ["28", 0],
                "vae": ["2", 4]
            },
            "class_type": "VAEDecode"
        },
        "32": {
            "inputs": {
                "sharpen_radius": 1,
                "sigma": 0.4,
                "alpha": 0.6,
                "image": ["31", 0]
            },
            "class_type": "ImageSharpen"
        },
        "33": {
            "inputs": {
                "ckpt_name": "rife47.pth",
                "clear_cache_after_n_frames": 10,
                "multiplier": 3,
                "fast_mode": True,
                "ensemble": True,
                "scale_factor": 1,
                "frames": ["32", 0]
            },
            "class_type": "RIFE VFI"
        },
        "36": {
            "inputs": {
                "upscale_method": "nearest-exact",
                "scale_by": 1.5,
                "samples": ["2", 3]
            },
            "class_type": "LatentUpscaleBy"
        },
        "38": {
            "inputs": {
                "control_net_name": "controlnet_checkpoint.ckpt"
            },
            "class_type": "ControlNetLoader"
        }
    }
}

# 發送 POST 請求
response = requests.post(url, json=payload)

# 處理回應
if response.status_code == 200:
    print("請求成功！")
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    print(f"請求失敗，狀態碼：{response.status_code}")

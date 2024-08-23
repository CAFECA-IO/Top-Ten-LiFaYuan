from diffusers import DiffusionPipeline
import torch

def generate_anchor_image(prompt):
    try:
        # 加載 FLUX.1 [schnell] 模型
        pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
        pipe.enable_model_cpu_offload()  # 可選：通過將部分處理卸載到 CPU 來節省顯存

        # 從文本提示生成主播圖片
        anchor_image = pipe(prompt, guidance_scale=0.0, num_inference_steps=4).images[0]
        
        # 保存並返回圖片路徑
        output_path = 'data/output/news_anchor.png'
        anchor_image.save(output_path)

        print(f"已保存主播圖片: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成主播圖片時出錯: {e}")
        return None

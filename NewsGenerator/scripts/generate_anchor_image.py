import torch
import os
from diffusers import DiffusionPipeline
from contextlib import contextmanager

@contextmanager
def manage_pipeline():
    pipe = None
    try:
        print("開始加載 FLUX.1 [schnell] 模型...")
        pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.float16) # 使用 float16 來減少內存占用
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe.to(device)  # 明確指定使用 GPU 或 CPU
        pipe.enable_attention_slicing()  # 啟用注意力切片來減少 GPU 記憶體使用
        print("模型加載成功。")
        yield pipe
    except Exception as e:
        print(f"加載模型時出錯: {e}")
    finally:
        if pipe is not None:
            del pipe  # 明確刪除對象，幫助釋放資源
            torch.cuda.empty_cache()  # 清空 CUDA 緩存（如果適用）

def generate_anchor_image():
    try:
        with manage_pipeline() as pipe:
            if pipe is None:
                print("模型加載失敗，終止生成圖片。")
                return []
            
            # 從文本提示生成主播圖片
            prompt = "Generate an image of a news anchor"
            anchor_image = pipe(prompt, guidance_scale=7.5, num_inference_steps=50).images[0]  # 使用更高的 guidance_scale 以獲得更高質量的圖像
            
            # 保存並返回圖片路徑
            output_path = 'data/output/news_anchor.png'
            # 確保目錄存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            anchor_image.save(output_path)

            print(f"已保存主播圖片: {output_path}")

            return output_path
    except Exception as e:
        print(f"生成主播圖片時出錯: {e}")
        return None

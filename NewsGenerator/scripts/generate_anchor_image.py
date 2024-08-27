from diffusers import DiffusionPipeline
import torch
from contextlib import contextmanager

@contextmanager
def manage_pipeline():
    pipe = None
    try:
        print("開始加載 FLUX.1 [schnell] 模型...")
        pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.float32)
        pipe.to("cpu")  # 明確指定使用 CPU
        pipe.enable_model_cpu_offload()  # 使用 accelerate 來優化 CPU 記憶體使用
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
            anchor_image = pipe(prompt, guidance_scale=0.0, num_inference_steps=1).images[0]
            
            # 保存並返回圖片路徑
            output_path = 'data/output/news_anchor.png'
            anchor_image.save(output_path)

            print(f"已保存主播圖片: {output_path}")

            return output_path
    except Exception as e:
        print(f"生成主播圖片時出錯: {e}")
        return None

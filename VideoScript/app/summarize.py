from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from .utils import setup_logger, save_to_file, clear_gpu_memory
import torch

# 設置 logger
logger = setup_logger('summarize', 'summarize.log')

def generate_summary(optimized_transcript_path, summary_path, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=None):
    with open(optimized_transcript_path, 'r') as f:
        optimized_transcriptions = json.load(f)
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    try:
        clear_gpu_memory()
        model.to(device)
    except torch.cuda.OutOfMemoryError:
        print("CUDA out of memory, switching to CPU")
        device = torch.device("cpu")
        model.to(device)
    
    # 合併所有段落文本
    full_text = " ".join([seg["text"] for seg in optimized_transcriptions])
    inputs = tokenizer(full_text, return_tensors="pt").to(model.device)

    # 設置生成配置
    generation_config = {
        "max_new_tokens": 300,      # 限制生成的最大token數
        "min_length": 50,           # 生成的最小token數
        "temperature": 0.7,         # 控制生成的隨機性
        "top_k": 50,                # 只考慮概率最高的前k個標記
        "top_p": 0.9,               # 只考慮累積概率超過p的標記
        "do_sample": False,         # 不使用取樣
        "num_beams": 3,             # Beam search中的beam數量
        "early_stopping": True,     # 提前停止
        "repetition_penalty": 1.2,  # 懲罰重複的標記
        "length_penalty": 1.0,      # 控制生成文本長度的懲罰
        "no_repeat_ngram_size": 2   # 禁止在生成文本中出現的n-gram的大小
    }

    logger.info(f"Generating summary for optimized transcript.")  # 添加日誌記錄
    summary_outputs = model.generate(**inputs, **generation_config)
    summary_text = tokenizer.decode(summary_outputs[0], skip_special_tokens=True)
    
    save_to_file(summary_text, summary_path)
    
    logger.info(f"Summary generated: {summary_text}")  # 添加日誌記錄
    return summary_text
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
from .utils import setup_logger, save_to_file, clear_gpu_memory
import torch

# 設置 logger
logger = setup_logger('summarize', 'output.log')

# 設定會議總結的提示模板
template = """
系統：你是一個專門用於總結會議內容的助手。請使用以下多人的發言記錄來總結會議內容。請保持總結簡潔、邏輯清晰且架構明確，每個總結最多使用三句話，字數不超過500。請使用繁體中文回答。
用戶：會議片段：
{context}
助理：會議總結：
"""

def create_prompt(context):
    return template.format(context=context)

def filter_non_informative_segments(segments):
    filtered_segments = []
    for segment in segments:
        text = segment["text"]
        if any(word in text for word in ["中文字幕组", "字幕組", "所以我希望大家能夠多多多多多多多多多多多多"]):
            continue
        filtered_segments.append(segment)
    return filtered_segments



def generate_summary(optimized_transcript_path, summary_path, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=None):
    with open(optimized_transcript_path, 'r') as f:
        optimized_transcriptions = json.load(f)

    optimized_transcriptions = filter_non_informative_segments(optimized_transcriptions)
    
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
    
    # 合併所有段落文本並生成提示
    full_text = ' '.join([seg["text"] for seg in optimized_transcriptions])
    prompt = create_prompt(full_text)
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    # 確保摘要短於輸入文本
    full_text = ' '.join([seg["text"] for seg in optimized_transcriptions])
    input_length = len(full_text.split())
    max_new_tokens = max(300, input_length // 2)  # 確保生成的摘要比輸入文本短，且不超過300字

    inputs = tokenizer(full_text, return_tensors="pt").to(device)

    # 設置生成配置
    generation_config = {
        "max_new_tokens": max_new_tokens,  # 限制生成的最大token數
        "min_length": 250,                 # 生成的最小token數，設置為100以確保摘要完整性
        "temperature": 0.7,                # 控制生成的隨機性
        "top_k": 50,                       # 只考慮概率最高的前k個標記
        "top_p": 0.9,                      # 只考慮累積概率超過p的標記
        "do_sample": False,                # 不使用取樣
        "num_beams": 5,                    # Beam search中的beam數量，提高為5以提升生成質量
        "early_stopping": True,            # 提前停止
        "repetition_penalty": 1.2,         # 懲罰重複的標記
        "length_penalty": 0.7,             # 控制生成文本長度的懲罰
        "no_repeat_ngram_size": 2          # 禁止在生成文本中出現的n-gram的大小
    }

    try:
        summary_outputs = model.generate(**inputs, **generation_config)
        summary_text = tokenizer.decode(summary_outputs[0], skip_special_tokens=True)
    except torch.cuda.OutOfMemoryError:
         # 切換到 CPU
        print("CUDA memory is full, switching to CPU.")
        device = torch.device("cpu")
        model.to(device)
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        summary_outputs = model.generate(**inputs, **generation_config)
        summary_text = tokenizer.decode(summary_outputs[0], skip_special_tokens=True)
        
    print(f"Generating summary for optimized transcript.", summary_outputs)  # 添加日誌記錄
    
    summary_text = tokenizer.decode(summary_outputs[0], skip_special_tokens=True)

    # 清理生成的文本，移除系統提示和上下文，僅保留摘要內容
    summary_text = summary_text.split("助理：會議總結：")[-1].strip()
    
    save_to_file(summary_text, summary_path)
    
    logger.info(f"Summary generated: {summary_text}")  # 添加日誌記錄
    return summary_text
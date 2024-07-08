# app/optimize.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import json
from .utils import save_to_file

def optimize_transcription(transcript_path, optimized_path, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=None):
    with open(transcript_path, 'r') as f:
        segments = json.load(f)
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
    
    optimized_transcriptions = []
    for segment in segments:
        input_text = segment["text"]
        inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

        # 設置生成配置
        generation_config = {
            "max_new_tokens": 100,       # 限制生成的最大token數
            "min_length": 10,            # 生成的最小token數
            "temperature": 0.7,          # 控制生成的隨機性
            "top_k": 50,                 # 只考慮概率最高的前k個標記
            "top_p": 0.9,                # 只考慮累積概率超過p的標記
            "do_sample": False,          # 不使用取樣
            "num_beams": 3,              # Beam search中的beam數量
            "early_stopping": True,      # 提前停止
            "repetition_penalty": 1.2,   # 懲罰重複的標記
            "length_penalty": 1.0,       # 控制生成文本長度的懲罰
            "no_repeat_ngram_size": 2    # 禁止在生成文本中出現的n-gram的大小
        }

        print(f"Generating text for segment: {input_text}")  # 添加日誌記錄
        outputs = model.generate(**inputs, **generation_config)
        optimized_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        optimized_transcriptions.append({
            "speaker": segment["speaker"],
            "start": segment["start"],
            "end": segment["end"],
            "text": optimized_text
        })
        print(f"Optimized text: {optimized_text}")  # 添加日誌記錄
    
    save_to_file(optimized_transcriptions, optimized_path)
    return optimized_transcriptions

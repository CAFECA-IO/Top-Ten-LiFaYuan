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
        inputs = tokenizer(input_text, return_tensors="pt")

        # 設置 max_new_tokens 或 max_length
        generation_config = {
            "max_new_tokens": 50  # 你可以根據需要調整這個值
        }

        outputs = model.generate(**inputs, **generation_config)
        optimized_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        optimized_transcriptions.append({
            # "speaker": segment["speaker"],
            "start": segment["start"],
            "end": segment["end"],
            "text": optimized_text
        })
    

    save_to_file(segments, optimized_path)
    return optimized_transcriptions

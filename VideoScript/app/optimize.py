# app/optimize.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import json
from .utils import save_to_file

def optimize_transcription(filename, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=None):
    with open(os.path.join('scripts', filename), 'r') as f:
        segments = json.load(f)
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
    
    optimized_transcriptions = []
    for segment in segments:
        input_text = segment["text"]
        inputs = tokenizer(input_text, return_tensors="pt")
        outputs = model.generate(**inputs)
        optimized_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        optimized_transcriptions.append({
            "speaker": segment["speaker"],
            "start": segment["start"],
            "end": segment["end"],
            "text": optimized_text
        })
    

    save_to_file(segments, os.path.join('scripts', f'optimize_{filename}.json'))
    return optimized_transcriptions

# app/optimize.py

from transformers import AutoTokenizer, AutoModelForCausalLM

def optimize_transcription(segments, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=None):
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
    
    return optimized_transcriptions

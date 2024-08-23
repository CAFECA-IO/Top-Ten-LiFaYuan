from bark import SAMPLE_RATE, generate_audio, preload_models
import torchaudio
import torch

def generate_background_music(script_path):
    try:
        with open(script_path, 'r') as file:
            script = file.read()
            
        preload_models()  # 預加載模型

        audio_array = generate_audio(script)

         # 保存生成的背景音樂
        output_path = 'data/output/background_music.wav'
        torchaudio.save(output_path, torch.tensor(audio_array).unsqueeze(0), SAMPLE_RATE)
        print(f"已保存生成的背景音樂: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成背景音樂時出錯: {e}")
        return None
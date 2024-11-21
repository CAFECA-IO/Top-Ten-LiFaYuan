from bark_suno import SAMPLE_RATE, generate_audio, preload_models
import torchaudio
import torch
import os

def generate_background_music(script_path):
    try:
        # 檢查腳本文件是否存在
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"文件 {script_path} 未找到")

        # 讀取腳本內容
        with open(script_path, 'r') as file:
            script = file.read().strip()

        preload_models()  # 預加載模型

        # 設置設備為 GPU，如果可用的話
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        # 使用 GPU 進行推理，同時禁用梯度計算。保留這個設置可以避免在推理過程中計算不必要的梯度，節省記憶體和加快運算速度。
        with torch.no_grad():
            audio_array = generate_audio(script).to(device)

        # 檢查生成的音頻數組是否有效
        if audio_array is None or len(audio_array) == 0:
            raise ValueError("生成的音頻數據無效")

        # 確保輸出目錄存在
        os.makedirs('data/output', exist_ok=True)

        # 將音頻數組移回 CPU，以便保存為 WAV 文件
        audio_array = audio_array.cpu()

        # 保存生成的背景音樂
        output_path = 'data/output/background_music.wav'
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        torchaudio.save(output_path, torch.tensor(audio_array).unsqueeze(0), SAMPLE_RATE)
        print(f"已保存生成的背景音樂: {output_path}")

        return output_path
    except Exception as e:
        print(f"生成背景音樂時出錯: {e}")
        return None

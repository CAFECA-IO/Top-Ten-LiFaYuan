from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
import torchaudio
import os
import torch

def generate_voiceover(script_path):
    try:
        # 檢查腳本文件是否存在
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"文件 {script_path} 未找到")
        
        # 讀取新聞稿文本
        with open(script_path, 'r') as file:
            script = file.read()

        # 檢查是否有可用的 GPU
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        # 使用 SFT 模型進行推理
        cosyvoice = CosyVoice('pretrained_models/CosyVoice-300M-SFT', torch_dtype=torch_dtype)
        cosyvoice.to(device)
        output = cosyvoice.inference_sft(script, '中文女')

        # 確保目標目錄存在
        os.makedirs('data/output', exist_ok=True)

        # 保存生成的語音文件
        output_path = 'data/output/news_voiceover.mp3'
        torchaudio.save(output_path, output['tts_speech'].cpu(), 22050)  # 確保音頻數據在 CPU 上進行保存
        print(f"已保存生成的語音: {output_path}")

        return output_path
    except Exception as e:
        import traceback
        print(f"生成語音時出錯: {e}")
        traceback.print_exc()
        return None

from cosyvoice.cli.cosyvoice import CosyVoice
from cosyvoice.utils.file_utils import load_wav
import torchaudio
import os

def generate_voiceover(script_path):
    try:
        # 讀取新聞稿文本
        with open(script_path, 'r') as file:
            script = file.read()

        # 使用 SFT 模型進行推理
        cosyvoice = CosyVoice('pretrained_models/CosyVoice-300M-SFT')
        output = cosyvoice.inference_sft(script, '中文女')
        
        # 確保目標目錄存在
        os.makedirs('data/output', exist_ok=True)

        # 保存生成的語音文件
        output_path = 'data/output/news_voiceover.mp3'
        torchaudio.save(output_path, output['tts_speech'], 22050)
        print(f"已保存生成的語音: {output_path}")

        return output_path
    except Exception as e:
        import traceback
        print(f"生成語音時出錯: {e}")
        traceback.print_exc()
        return None

import whisper
from .utils import setup_logger

# 設置 logger
logger = setup_logger('speech_to_text', 'speech_to_text.log')

def transcribe_audio(audio_path, transcript_path):
    
    # 加載 Whisper 模型
    model = whisper.load_model("base")
    
    # 轉錄音頻文件
    result = model.transcribe(audio_path, language='zh')
    
    # 提取轉錄文本
    transcript = result['text']
    logger.info(f"音頻轉換為逐字稿成功")
    
    # 將逐字稿寫入指定的文件
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
        logger.info(f"逐字稿已寫入文件：{transcript_path}")
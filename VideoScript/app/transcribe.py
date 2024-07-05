# app/transcribe.py

import os
import time
import whisperx
from inaSpeechSegmenter import Segmenter
from pyannote.audio import Pipeline
from .utils import setup_logger, save_to_file
import torch

# 設置 logger
logger = setup_logger('transcribe', 'transcribe.log')

def transcribe_audio(audio_path, output_path, model_name="base", language="zh", diarization_model="inaSpeechSegmenter"):
    start_time = time.time()

    # 確認 CUDA 設置
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Loading model: {model_name} on device: {device}")

    # 設置 ASR 選項
    asr_options = {
        'max_new_tokens': 1024, # 限制生成的最大 token 數
        'clip_timestamps': True, # 控制是否對時間戳進行截斷，使其對應的轉錄片段更準確。True: 轉錄片段的時間戳會被截斷，更精確地對應實際的音頻片段，適合需要精確對應時間戳的應用。
        'hallucination_silence_threshold': 0.2, # 設置模型識別的沉默門檻，用於過濾掉誤判為語音的靜音段。設置範圍: 0.0 - 1.0。根據噪音水平調整。
        'hotwords': ["低碳", "碳排放", "再生能源", "低碳發電", "賴清德", "不實文件", "能源政策",]
    }

    # 加載模型，傳遞正確的參數
    model = whisperx.load_model(
        whisper_arch=model_name, # 選擇模型架構，例如 'base'
        device=device.type, # 指定設備類型，例如 'cuda' 或 'cpu'
        compute_type="float32", # 指定計算類型，影響模型計算的精度和速度。，例如 'float32' 或 'float16'。'float32': 更高的精度，但計算速度較慢，內存佔用較高。
        asr_options=asr_options, # 傳遞 ASR 選項
        language=language, # 指定語言，例如 'zh' 表示中文
        threads=4 # 設置線程數，用於加速模型推理
    )
    logger.info(f"Model loaded successfully. Time taken: {time.time() - start_time} seconds")
    
    # 轉錄
    start_time = time.time()
    result = model.transcribe(audio_path, language=language)
    logger.info(f"Transcription completed. Time taken: {time.time() - start_time} seconds")
    
    segments = result["segments"]  # 包含不同人發言的時間段信息和文本

    # 說話者辨識
    start_time = time.time()
    try:
        if diarization_model == "inaSpeechSegmenter":
            segmenter = Segmenter()
            segmentation = segmenter(audio_path)
            speaker_segments = [(float(start), float(end), label) for start, end, label in segmentation if label not in ('noEnergy', 'noise')]
        elif diarization_model == "pyannote":
            huggingface_token = os.getenv("HUGGINGFACE_API_TOKEN")
            pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=huggingface_token)
            pipeline.to(device)
            diarization = pipeline(audio_path)
            speaker_segments = [(turn.start, turn.end, speaker) for turn, _, speaker in diarization.itertracks(yield_label=True)]
        else:
            raise ValueError(f"Unsupported diarization model: {diarization_model}")
        logger.info(f"Speaker diarization completed using {diarization_model}. Time taken: {time.time() - start_time} seconds")
    except Exception as e:
        print(f"Error during speaker diarization: {e}")
        return
    
    # 合併分割信息和轉錄信息
    for segment in segments:
        segment["speaker"] = "unknown"
        for start, end, label in speaker_segments:
            try:
                if start <= segment["start"] <= end or start <= segment["end"] <= end:
                    segment["speaker"] = label
                    break
            except ValueError:
                continue  # 跳過無法轉換為浮點數的標籤
    
    save_to_file(segments, output_path)
    return segments

"""
def transcribe_audio_by_whisper(audio_path, transcript_path):
    
    # 加載 Whisper 模型
    model = whisper.load_model("base")
    
    # 轉錄音頻文件
    result = model.transcribe(audio_path, language='zh')
    
    # 提取轉錄文本
    transcript = result['text']
    logger.info(f"音頻轉換為逐字稿成功")
    
    # 將逐字稿寫入指定的文件
    save_to_file(transcript, transcript_path)

def transcribe_audio_by_sr(audio_path, transcript_path):
    
    # 使用 speech_recognition 庫進行語音識別，將音頻轉換為文字。

    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    # version_and_id = '_'.join(os.path.basename(audio_path).strip('.wav').split('_')[2:])
    filename = os.path.basename(audio_path).strip('.wav')
    
    # 分割音頻文件，每段1分鐘
    chunk_length_ms = 60000  # 1分鐘
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    
    transcript = ""

    audio_dir = os.path.join(os.getcwd(), 'audios')
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    chunks_dir = os.path.join(audio_dir, f'chunks_{filename}')
    if not os.path.exists(chunks_dir):
        os.makedirs(chunks_dir)

    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(chunks_dir, f'chunk_{i}.wav')
        chunk.export(chunk_path, format="wav")
        
        with sr.AudioFile(chunk_path) as source:
            audio_data = recognizer.record(source)
            
            try:
                text = recognizer.recognize_google(audio_data, language="zh-TW")
                transcript += text + " "
                print(f"Chunk {i} transcribed successfully.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
    
    # 將逐字稿寫入指定的文件
    save_to_file(transcript, transcript_path)
    
    logger.info(f"Transcription saved at: {transcript_path}")

"""
# app/transcribe.py

import os
import time
import whisperx
from .optimize import optimize_transcription
from .utils import setup_logger, save_to_file
# import whisper
# from pydub import AudioSegment
# import speech_recognition as sr

# 設置 logger
logger = setup_logger('transcribe', 'transcribe.log')

def transcribe_audio(audio_path, model_name="base", device="cpu", language="zh"):
    start_time = time.time()
    logger.info(f"Loading model: {model_name} on device: {device}")

    # 設置 ASR 選項
    asr_options = {
        'max_new_tokens': 1024,
        'clip_timestamps': True,
        'hallucination_silence_threshold': 0.1,
        'hotwords': None
    }

    # 加載模型，傳遞正確的參數
    model = whisperx.load_model(
        whisper_arch=model_name,
        device=device,
        compute_type="float32",
        asr_options=asr_options,
        language=language,
        threads=4
    )
    
    logger.info(f"Model loaded successfully. Time taken: {time.time() - start_time} seconds")
    
    start_time = time.time()
    result = model.transcribe(audio_path)
    logger.info(f"Transcription completed. Time taken: {time.time() - start_time} seconds")
    
    segments = result["segments"]  # 包含不同人發言的時間段信息和文本

    filename = os.path.basename(audio_path).strip('.wav')
    save_to_file(segments, os.path.join('scripts', f'segments_{filename}.json'))
    return segments



def transcribe_and_optimize_audio(audio_path, transcript_path, model_name="base", device="cpu", optimize_model="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", language="zh", token=None):
    print("Transcribing audio...")
    segments = transcribe_audio(audio_path=audio_path, model_name=model_name, device=device, language=language)
    
    print("Optimizing transcription...")
    optimized_transcriptions = optimize_transcription(segments, model_name=optimize_model, token=token)
    
    print("Saving to file...")
    save_to_file(optimized_transcriptions, transcript_path)
    
    print(f"Transcription saved to {transcript_path}")

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
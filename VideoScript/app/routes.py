# app/routes.py

from flask import request, jsonify
import os
import threading
from . import app
from .downloader import download_video, get_video_source
from .audio_extractor import extract_audio, process_audio
from .transcribe import transcribe_audio
from .optimize import optimize_transcription
from dotenv import load_dotenv
from .utils import setup_logger

# 設置 logger
logger = setup_logger('routes', 'routes.log')

# 加載 .env 文件
load_dotenv()

@app.route('/api/transcribe', methods=['POST'])
def transcribe_video():
    video_url = request.json.get('url')
    
    video_id = video_url.split('/')[-1]
    video_filename = f'downloaded_meeting_{video_id}.mp4'
    audio_filename = f'converted_meeting_{video_id}.wav'
    processed_audio_filename = f'processed_audio_{video_id}.wav'
    transcript_filename = f'meeting_script_{video_id}.json'
    optimized_filename = f'optimized_script{video_id}.json'

    downloads_dir = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    
    audios_dir = os.path.join(os.getcwd(), 'audios')
    if not os.path.exists(audios_dir):
        os.makedirs(audios_dir)
    
    scripts_dir = os.path.join(os.getcwd(), 'scripts')
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)
    
    video_path = os.path.join('downloads', video_filename)
    audio_path = os.path.join('audios', audio_filename)
    processed_audio_path = os.path.join('audios', processed_audio_filename)
    transcript_path = os.path.join('scripts', transcript_filename)
    optimized_path = os.path.join('scripts', optimized_filename)
    
    # 檢查視頻文件是否存在
    if not os.path.exists(video_path):
        m3u8_url = get_video_source(video_url)
        if not m3u8_url:
            return jsonify({'error': '無法獲取視頻源地址'}), 400
        
        logger.info(f"Downloading video from {m3u8_url} to {video_path}")
        download_thread = threading.Thread(target=download_video, args=(m3u8_url, video_path))
        download_thread.start()
        download_thread.join()

        if not os.path.exists(video_path):
            logger.error(f"Failed to download video from {m3u8_url}")
            return jsonify({'error': '下載視頻失敗'}), 500
    else:
        logger.info(f"視頻文件已存在：{video_path}")
    
    # 檢查音頻文件是否存在
    if not os.path.exists(audio_path):
        logger.info(f"Converting video from {video_path} to {audio_path}")
        extract_audio(video_path, audio_path)

        if not os.path.exists(audio_path):
            logger.error(f"Failed to convert video from {video_path} to {audio_path}")
            return jsonify({'error': '轉換音頻失敗'}), 500
    else:
        logger.info(f"音頻文件已存在：{audio_path}")
        
    # 檢查音頻是否已處理
    if not os.path.exists(processed_audio_path):
        logger.info(f"Processing audio from {audio_path} to {processed_audio_path}")
        process_audio(audio_path, processed_audio_path)
        
        if not os.path.exists(processed_audio_path):
            logger.error(f"Failed to process audio from {audio_path} to {processed_audio_path}")
            return jsonify({'error': '處理音頻失敗'}), 500
    else:
        logger.info(f"音頻文件已處理：{processed_audio_path}")
    
    # 檢查逐字稿文件是否存在
    if not os.path.exists(transcript_path):
        logger.info(f"Transcribing audio from {audio_path} to {transcript_path}")
        transcribe_audio(audio_path, transcript_path)
        
        if not os.path.exists(transcript_path):
            logger.error(f"Failed to transcribe audio from {audio_path} to {transcript_path}")
            return jsonify({'error': '轉換逐字稿失敗'}), 500
    else:
        logger.info(f"逐字稿文件已存在：{transcript_path}")

    # 檢查優化逐字稿文件是否存在
    if not os.path.exists(optimized_path):
        logger.info(f"Optimizing transcription from {transcript_path} to {optimized_path}")
        # 獲取 API Token
        token = os.getenv("HUGGINGFACE_API_TOKEN")
        optimized_transcriptions = optimize_transcription(transcript_path, optimized_path, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=token)

        if not os.path.exists(optimized_path):
            logger.error(f"Failed to optimize transcription from {transcript_path} to {optimized_path}")
            return jsonify({'error': '優化逐字稿失敗'}), 500
    else:
        logger.info(f"優化逐字稿文件已存在：{optimized_path}")
    
    return jsonify({'message': '轉換成功', 'script': optimized_transcriptions}), 200

from flask import request, jsonify
import os
import threading
from . import app
from .downloader import download_video, get_video_source
from .audio_extractor import convert_video_to_audio
from .speech_to_text import transcribe_audio
from .utils import setup_logger

# 設置 logger
logger = setup_logger('routes', 'routes.log')

@app.route('/api/transcribe', methods=['POST'])
def transcribe_video():
    video_url = request.json.get('url')
    
    video_id = video_url.split('/')[-1]
    video_filename = f'downloaded_meeting_{video_id}.mp4'
    audio_filename = f'converted_meeting_{video_id}.wav'
    transcript_filename = f'meeting_script_{video_id}.txt'

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
    transcript_path = os.path.join('scripts', transcript_filename)
    
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
        convert_video_to_audio(video_path, audio_path)

        if not os.path.exists(audio_path):
            logger.error(f"Failed to convert video from {video_path} to {audio_path}")
            return jsonify({'error': '轉換音頻失敗'}), 500
    
    # 檢查逐字稿文件是否存在
    if not os.path.exists(transcript_path):
        logger.info(f"Transcribing audio from {audio_path} to {transcript_path}")
        transcribe_audio(audio_path, transcript_path)
        
        if not os.path.exists(transcript_path):
            logger.error(f"Failed to transcribe audio from {audio_path} to {transcript_path}")
            return jsonify({'error': '轉換逐字稿失敗'}), 500
    else:
        logger.info(f"逐字稿文件已存在：{transcript_path}")
    
    return jsonify({'message': '轉換成功'}), 200

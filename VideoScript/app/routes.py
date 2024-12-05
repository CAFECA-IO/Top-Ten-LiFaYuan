# app/routes.py

from flask import request, jsonify
import os
import threading
from . import app
from .audio_extractor import extract_audio, process_audio
from .transcribe import transcribe_audio
from .optimize import optimize_transcription
from dotenv import load_dotenv
from .utils import setup_logger, get_path

# 設置 logger
logger = setup_logger('script_routes', 'output.log')

# 加載 .env 文件
load_dotenv()

@app.route('/')
def index():
    return "Welcome to VideoScript!"


@app.route('/api/extract_audio', methods=['POST'])
def extract_audio_from_video():
    video_id = request.json.get('video_id')
    
    video_path = get_path("shared_data/videos", f"{video_id}.mp4")
    audio_path = get_path("shared_data/audios", f"{video_id}.wav")
    
    if not os.path.exists(video_path):
        return jsonify({'error': '視頻文件不存在'}), 404
    
    if os.path.exists(audio_path):
        return jsonify({'message': '音頻文件已存在', 'audio_path': audio_path}), 200
    
    logger.info(f"Extracting audio from {video_path} to {audio_path}")
    extract_audio(video_path, audio_path)
    
    if os.path.exists(audio_path):
        return jsonify({'message': '提取音頻成功', 'audio_path': audio_path}), 200
    else:
        return jsonify({'error': '提取音頻失敗'}), 500
    

@app.route('/api/transcribe', methods=['POST'])
def transcribe_audio():
    video_id = request.json.get('video_id')
    
    audio_path = get_path("shared_data/audios", f"{video_id}.wav")
    transcript_path = get_path("shared_data/transcripts", f"{video_id}.json")
    
    if not os.path.exists(audio_path):
        return jsonify({'error': '音頻文件不存在'}), 404
    
    if os.path.exists(transcript_path):
        return jsonify({'message': '字幕文件已存在', 'transcript_path': transcript_path}), 200
    
    logger.info(f"Transcribing audio from {audio_path} to {transcript_path}")
    transcribe_audio(audio_path, transcript_path)
    
    if os.path.exists(transcript_path):
        return jsonify({'message': '音頻轉文字成功', 'transcript_path': transcript_path}), 200
    else:
        return jsonify({'error': '音頻轉文字失敗'}), 500
# app/transcriber.py
import os
import requests
from app.utils import setup_logger, get_path

logger = setup_logger('transcriber', 'logs/transcriber.log')

BASE_URL = "http://localhost:5001"  # VideoScript API 地址

def transcribe_video(video_id):
    """將視頻轉換為字幕，並保存到 shared_data/transcripts"""
    video_path = get_path("shared_data/videos", f"{video_id}.mp4")
    transcript_path = get_path("shared_data/transcripts", f"{video_id}.json")

    if not os.path.exists(video_path):
        logger.error(f"Video file not found: {video_path}")
        return

    response = requests.post(f"{BASE_URL}/api/transcribe", json={"url": video_path})
    if response.status_code == 200:
        logger.info(f"Transcribed video: {video_id} -> {transcript_path}")
    else:
        logger.error(f"Failed to transcribe video: {video_id}")

# app/summarizer.py
import os
import requests
from app.utils import setup_logger, get_path

logger = setup_logger('summarizer', 'logs/summarizer.log')

BASE_URL = "http://localhost:5002"  # EventSummarizer API 地址

def summarize_transcript(video_id):
    """生成摘要，並保存到 shared_data/summaries"""
    transcript_path = get_path("shared_data/transcripts", f"{video_id}.json")
    summary_path = get_path("shared_data/summaries", f"{video_id}.txt")

    if not os.path.exists(transcript_path):
        logger.error(f"Transcript file not found: {transcript_path}")
        return

    response = requests.get(f"{BASE_URL}/api/summarize", json={"url": transcript_path})
    if response.status_code == 200:
        logger.info(f"Summarized transcript: {video_id} -> {summary_path}")
    else:
        logger.error(f"Failed to summarize transcript: {video_id}")

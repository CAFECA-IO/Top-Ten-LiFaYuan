# app/transcriber.py
import os
import aiohttp
from app.utils import setup_logger, get_path
import json

logger = setup_logger('transcriber', 'logs/transcriber.log')

BASE_URL = "http://localhost:5001"  # VideoScript API 地址

async def transcribe_video(video_id):
    """將視頻轉換為字幕，並保存到 shared_data/transcripts"""
    video_path = get_path("shared_data/videos", f"{video_id}.mp4")
    transcript_path = get_path("shared_data/transcripts", f"{video_id}.json")

    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BASE_URL}/api/transcribe", json={"video_id": video_id}) as response:
                if response.status == 200:
                    transcript = await response.json()
                    with open(transcript_path, 'w') as f:
                        json.dump(transcript, f)
                    logger.info(f"Transcribed video: {video_id} -> {transcript_path}")
                else:
                    raise Exception(f"Failed to transcribe video: HTTP {response.status}")
    except Exception as e:
        logger.error(f"Error during transcription for video {video_id}: {str(e)}")
        raise  # 將異常拋出給調用方

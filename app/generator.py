# app/generator.py
import os
import aiohttp
from app.utils import setup_logger, get_path

logger = setup_logger('generator', 'logs/generator.log')

BASE_URL = "http://localhost:5003"  # Vocal & Video API 地址

async def generate_vocal(video_id):
    """基於摘要生成配音"""
    summary_path = get_path("shared_data/summaries", f"{video_id}.txt")
    audio_path = get_path("shared_data/audios", f"{video_id}.wav")

    if not os.path.exists(summary_path):
        logger.error(f"Summary file not found: {summary_path}")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/generate-vocal", json={"text": summary_path}) as response:
            if response.status == 200:
                logger.info(f"Generated vocal: {video_id} -> {audio_path}")
            else:
                logger.error(f"Failed to generate vocal: {video_id}")

async def generate_video(video_id):
    """基於配音生成新聞視頻"""
    audio_path = get_path("shared_data/audios", f"{video_id}.wav")
    video_output_path = get_path("shared_data/videos", f"news_{video_id}.mp4")

    if not os.path.exists(audio_path):
        logger.error(f"Audio file not found: {audio_path}")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/generate-video", json={"audio_path": audio_path}) as response:
            if response.status == 200:
                logger.info(f"Generated video: {video_id} -> {video_output_path}")
            else:
                logger.error(f"Failed to generate video: {video_id}")

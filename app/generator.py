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

    # 檢查摘要文件是否存在
    if not os.path.exists(summary_path):
        error_message = f"Summary file not found: {summary_path}"
        logger.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BASE_URL}/generate-vocal", json={"text": summary_path}) as response:
                if response.status == 200:
                    with open(audio_path, 'wb') as f:
                        f.write(await response.read())
                    logger.info(f"Generated vocal: {video_id} -> {audio_path}")
                    return audio_path
                else:
                    error_message = f"Failed to generate vocal for video {video_id}: HTTP {response.status}"
                    logger.error(error_message)
                    raise Exception(error_message)
    except Exception as e:
        error_message = f"Unexpected error while generating vocal for video {video_id}: {str(e)}"
        logger.error(error_message)
        raise  # 將異常拋出給調用方

async def generate_video(video_id):
    """基於配音生成新聞視頻"""
    audio_path = get_path("shared_data/audios", f"{video_id}.wav")
    video_output_path = get_path("shared_data/videos", f"news_{video_id}.mp4")

    # 檢查配音文件是否存在
    if not os.path.exists(audio_path):
        error_message = f"Audio file not found: {audio_path}"
        logger.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BASE_URL}/generate-video", json={"audio_path": audio_path}) as response:
                if response.status == 200:
                    with open(video_output_path, 'wb') as f:
                        f.write(await response.read())
                    logger.info(f"Generated video: {video_id} -> {video_output_path}")
                    return video_output_path
                else:
                    error_message = f"Failed to generate video for audio {audio_path}: HTTP {response.status}"
                    logger.error(error_message)
                    raise Exception(error_message)
    except Exception as e:
        error_message = f"Unexpected error while generating video for audio {audio_path}: {str(e)}"
        logger.error(error_message)
        raise  # 將異常拋出給調用方

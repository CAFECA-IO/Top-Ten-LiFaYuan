# app/summarizer.py
import os
import aiohttp
from app.utils import setup_logger, get_path

logger = setup_logger('summarizer', 'logs/summarizer.log')

BASE_URL = "http://localhost:5002"  # EventSummarizer API 地址

async def summarize_transcript(video_id):
    """生成摘要，並保存到 shared_data/summaries"""
    transcript_path = get_path("shared_data/transcripts", f"{video_id}.json")
    summary_path = get_path("shared_data/summaries", f"{video_id}.txt")

    if not os.path.exists(transcript_path):
        logger.error(f"Transcript file not found: {transcript_path}")
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/api/summarize", json={"url": transcript_path}) as response:
            if response.status == 200:
                summary = await response.text()
                with open(summary_path, 'w') as f:
                    f.write(summary)
                logger.info(f"Generated summary for video: {video_id}")
            else:
                logger.error(f"Failed to generate summary for video: {video_id}")

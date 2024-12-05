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

    # 檢查轉錄文件是否存在
    if not os.path.exists(transcript_path):
        error_message = f"Transcript file not found: {transcript_path}"
        logger.error(error_message)
        raise FileNotFoundError(error_message)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{BASE_URL}/api/summarize", json={"url": transcript_path}) as response:
                if response.status == 200:
                    summary = await response.text()
                    with open(summary_path, 'w') as f:
                        f.write(summary)
                    logger.info(f"Generated summary for video: {video_id}")
                    return summary_path
                else:
                    error_message = (
                        f"Failed to generate summary for video {video_id}: HTTP {response.status}"
                    )
                    logger.error(error_message)
                    raise Exception(error_message)
    except Exception as e:
        error_message = f"Unexpected error while summarizing transcript for video {video_id}: {str(e)}"
        logger.error(error_message)
        raise  # 將異常拋出給調用方

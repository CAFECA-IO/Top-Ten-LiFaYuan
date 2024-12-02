# app/crawler.py
import requests
from datetime import datetime
from app.utils import setup_logger, get_path

logger = setup_logger('crawler', 'logs/crawler.log')

BASE_URL = "http://localhost:5000"  # SmartLegiCrawler API 地址

def fetch_meetings(date):
    """根據日期爬取會議列表"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
    response = requests.get(f"{BASE_URL}/api/meetings?start_date={date}&end_date={date}")
    if response.status_code == 200:
        meetings = response.json().get('meetings', [])
        logger.info(f"Fetched {len(meetings)} meetings for date: {date}")
        return meetings
    else:
        logger.error(f"Failed to fetch meetings for date: {date}")
        return []

def download_video(video_url, video_id):
    """下載視頻並保存到 shared_data/videos"""
    video_path = get_path("shared_data/videos", f"{video_id}.mp4")
    response = requests.post(f"{BASE_URL}/api/download", json={"url": video_url})
    if response.status_code == 200:
        logger.info(f"Downloaded video: {video_url} -> {video_path}")
    else:
        logger.error(f"Failed to download video: {video_url}")

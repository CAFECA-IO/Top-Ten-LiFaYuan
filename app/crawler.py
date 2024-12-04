# app/crawler.py
import aiohttp
from datetime import datetime
from app.utils import setup_logger, get_path

logger = setup_logger('crawler', 'logs/crawler.log')

BASE_URL = "http://localhost:5000"  # SmartLegiCrawler API 地址

async def fetch_meetings(date):
    """根據日期爬取會議列表"""
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")
        print(f"date: {date}")
    async with aiohttp.ClientSession() as session:
        print(f"{BASE_URL}/api/meetings?start_date={date}&end_date={date}")
        async with session.get(f"{BASE_URL}/api/meetings?start_date={date}&end_date={date}") as response:
            if response.status == 200:
                meetings = await response.json()
                logger.info(f"Fetched {len(meetings['meetings'])} meetings for date: {date}")
                return meetings['meetings']
            else:
                logger.error(f"Failed to fetch meetings for date: {date}")
                return []

async def download_video(video_url, video_id):
    """非同步下載視頻並保存到 shared_data/videos"""
    video_path = get_path("shared_data/videos", f"{video_id}.mp4")
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/api/download", json={"url": video_url}) as response:
            if response.status == 200:
                video_content = await response.read()
                with open(video_path, 'wb') as f:
                    f.write(video_content)
                logger.info(f"Downloaded video: {video_url} -> {video_path}")
            else:
                logger.error(f"Failed to download video: {video_url}")

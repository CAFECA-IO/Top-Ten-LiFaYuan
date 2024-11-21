# app/downloader.py

import subprocess
import os
import time
import sys
import asyncio
import threading
from pyppeteer import launch
from .utils import setup_logger, init_driver, get_path

logger = setup_logger('downloader', 'output.log')

def download_video(m3u8_url, output_filename):
    command = [
        'ffmpeg',
        '-i', m3u8_url,
        '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc',
        output_filename
    ]
    
    try:
        subprocess.run(command, check=True)
        if os.path.exists(output_filename):
            logger.info(f"視頻已成功下載至：{output_filename}")
            file_size = os.path.getsize(output_filename)
            logger.info(f"下載的文件大小：{file_size} 字節")
        else:
            logger.error(f"文件下載失敗：{output_filename} 不存在")
    except subprocess.CalledProcessError as e:
        logger.error(f"錯誤：{e}")

def get_video_source(url):
    driver = init_driver()
    driver.get(url)
    time.sleep(10)
    filelink = driver.execute_script("return _filelink;")
    logger.info("視頻源地址：", filelink)
    driver.quit()

    return filelink

async def get_video_source_by_puppeteer(url):
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle2'})

    # 獲取視頻源地址
    filelink = await page.evaluate('window._filelink')
    logger.info("視頻源地址：", filelink)

    await browser.close()
    return filelink

async def download(video_url):
    logger.info(f"開始下載視頻：{video_url}")
    video_id = video_url.split('/')[-1]
    video_path = get_path('videos', f'{video_id}.mp4')
    
    try:
        m3u8_url = await get_video_source_by_puppeteer(video_url)
        if not m3u8_url:
            logger.info("Failed to get video source")
            return {"status": "error", "message": "Failed to get video source"}
    except Exception as e:
        logger.error(f"Error during fetching video source: {e}")
        return {"status": "error", "message": str(e)}

    logger.info(f"Downloading video from {m3u8_url} to {video_path}")
    await asyncio.to_thread(download_video, m3u8_url, video_path)

    if not os.path.exists(video_path):
        logger.error(f"Failed to download video from {video_path}")
        return {"status": "error", "message": "Failed to download video"}
    else:
        logger.info(f"Video downloaded successfully from {video_path}")
        return {"status": "success", "message": "Video downloaded successfully"}
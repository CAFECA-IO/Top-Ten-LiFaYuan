# app/downloader.py

import subprocess
import os
import time
from .utils import setup_logger, init_driver

logger = setup_logger('downloader', 'downloader.log')

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
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from .utils import setup_logger

# 設置 logger
logger = setup_logger('downloader', 'downloader.log')

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

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
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(10)
    filelink = driver.execute_script("return _filelink;")
    logger.info("視頻源地址：", filelink)
    driver.quit()

    return filelink

def get_output_filename(video_url):
    downloads_dir = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    last_value = video_url.split('/')[-1]
    output_filename = os.path.join(downloads_dir, f'downloaded_meeting_{last_value}.mp4')
    return output_filename
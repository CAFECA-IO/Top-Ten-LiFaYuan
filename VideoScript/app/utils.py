# app/utils.py

import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import torch

def clear_gpu_memory():
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def save_to_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def ensure_dir_exists(directory):
    dir_path = os.path.join(os.getcwd(), directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_shared_data_path():
    # 取得 VideoScript 資料夾的絕對路徑
    video_script_path = os.path.abspath(os.path.join(__file__, '../../..'))

    # 拼接 shared_data 的路徑
    shared_data_path = os.path.join(video_script_path, 'shared_data')

    return shared_data_path

def get_path(folder, file_name):
    # 讀取配置文件中的資料夾路徑
    shared_data_path = get_shared_data_path()
    folder_path = os.path.join(shared_data_path, folder)
    path = os.path.join(folder_path, file_name)
    return path
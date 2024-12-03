# app/utils.py

import json
import logging
import os

PROGRESS_FILE = "progress.json"

def save_progress(stage, details):
    """保存當前的執行進度"""
    progress = load_progress()
    progress[stage] = details
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=4)

def load_progress():
    """加載執行進度"""
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, "r") as f:
        return json.load(f)

def setup_logger(name, log_file, level=logging.INFO):
    """設置日誌記錄器"""
    # 確保目錄存在
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 檔案處理器
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # 控制台處理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # 格式化
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_path(directory, filename):
    """動態生成文件路徑"""
    base_dir = os.getcwd()
    full_path = os.path.join(base_dir, directory)
    os.makedirs(full_path, exist_ok=True)
    return os.path.join(full_path, filename)

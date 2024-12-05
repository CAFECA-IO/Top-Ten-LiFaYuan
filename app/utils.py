# app/utils.py

import json
import logging
import os

PROGRESS_FILE = "progress.json"

def decode_nested(data):
    """
    遞歸解碼 JSON 結構中的雙重編碼字串
    """
    if isinstance(data, str):
        try:
            # 嘗試將字串解碼
            return data.encode("latin1").decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            return data  # 如果解碼失敗，返回原始數據
    elif isinstance(data, list):
        # 處理列表
        return [decode_nested(item) for item in data]
    elif isinstance(data, dict):
        # 處理字典
        return {key: decode_nested(value) for key, value in data.items()}
    else:
        return data  # 非字串類型直接返回

def save_progress(stage, details):
    """
    保存當前的執行進度，並自動解碼 Unicode 資料
    """
    progress = load_progress()
    decoded_details = decode_nested(details)
    progress[stage] = decoded_details
    # 保存進度到文件
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=4, ensure_ascii=False)  # 確保輸出中文等非 ASCII 字符

def load_progress():
    """加載執行進度"""
    if not os.path.exists(PROGRESS_FILE):
        logger = setup_logger('progress', 'logs/progress.log')
        logger.warning(f"{PROGRESS_FILE} not found. Returning empty progress.")
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

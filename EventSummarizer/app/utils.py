# app/utils.py

import os
import json
import logging
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

def save_to_file(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def ensure_dir_exists(directory):
    dir_path = os.path.join(os.getcwd(), directory)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def get_path(folder, file_name):
    # 讀取配置文件中的資料夾路徑
    config_path = os.path.join(os.path.dirname(__file__), '../config.json')
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    path = os.path.join(config[folder], file_name)
    return path
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


def get_shared_data_path():
    # 取得目前檔案(utils.py)的絕對路徑
    current_file_path = os.path.abspath(__file__)

    # 取得 EventSummarizer 資料夾的絕對路徑
    event_summarizer_path = os.path.dirname(os.path.dirname(current_file_path))

    # 取得 Top-Ten-LiFaYuan 資料夾的絕對路徑
    top_ten_lifayuan_path = os.path.dirname(event_summarizer_path)

    # 拼接 share_data 的路徑
    shared_data_path = os.path.join(top_ten_lifayuan_path, 'shared_data')

    return shared_data_path

# 測試函數
print(get_shared_data_path())

def get_path(folder, file_name):
    # 讀取配置文件中的資料夾路徑
    shared_data_path = get_shared_data_path()
    folder_path = os.path.join(shared_data_path, folder)
    path = os.path.join(folder_path, file_name)
    return path
# app/utils.py

import os
import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

def get_path(dir_name, file_name, extension):
    ensure_dir_exists(dir_name)
    path = os.path.join(dir_name, f'{file_name}.{extension}')
    return path
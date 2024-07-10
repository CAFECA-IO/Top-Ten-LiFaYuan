import logging
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
from pyppeteer import launch
import os
import json

# 配置日誌紀錄
def setup_logger(name, log_file, level=logging.INFO):
    """
    配置日誌紀錄
    :param name: 日誌紀錄器的名稱
    :param log_file: 日誌文件路徑
    :param level: 日誌紀錄級別
    :return: 配置好的日誌紀錄器
    """
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

# 日期解析函数
def parse_meeting_date(date_element):
    """
    解析會議信息中的日期元素
    :param date_element: BeautifulSoup解析后的日期元素
    :return: 解析後的日期字符串，格式為 "YYYY/MM/DD"
    """
    if not date_element:
        return None
    
    year = date_element.find('b').text.strip()
    month_day = date_element.find('strong').text.strip()
    if year and month_day:
        return f"{year}/{month_day}"

    return None

# 初始化瀏覽器驅動
# def init_driver():
#     """
#     配置瀏覽器選項
#     """
#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')
#     options.add_argument('--disable-gpu')
#     options.add_argument('--no-sandbox')
#     options.add_argument('start-maximized')
#     options.add_argument('disable-infobars')
#     options.add_argument('--disable-extensions')

#     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

async def init_driver():
    """
    配置瀏覽器選項
    """
    browser = await launch(headless=True, args=['--no-sandbox'])
    return browser

def get_shared_data_path():
    # 取得 SmartLegiCrawler 資料夾的絕對路徑
    smart_legi_crawler_path = os.path.abspath(os.path.join(__file__, '../../..'))

    # 拼接 shared_data 的路徑
    shared_data_path = os.path.join(smart_legi_crawler_path, 'shared_data')

    return shared_data_path

def get_path(folder, file_name):
    # 讀取配置文件中的資料夾路徑
    shared_data_path = get_shared_data_path()
    folder_path = os.path.join(shared_data_path, folder)
    path = os.path.join(folder_path, file_name)
    return path
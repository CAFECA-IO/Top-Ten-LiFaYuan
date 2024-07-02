import logging
from datetime import datetime

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
    month_day = date_element.find('strong').text.strip().replace("/", "")
    if year and month_day:
        return f"{year}/{month_day}"

    return None

# 檢查字符串是否包含特定文本
def contains_text(element, text):
    """
    檢查元素中是否包含特定文本
    :param element: BeautifulSoup解析後的元素
    :param text: 要檢查的文本
    :return: 是否包含該文本文本的布尔值
    """
    if not element:
        return False
    return text in element.get_text()

# 其他工具函数可以根据需要添加

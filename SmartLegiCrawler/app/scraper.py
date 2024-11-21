from bs4 import BeautifulSoup
import re
import asyncio
from .utils import parse_meeting_date, setup_logger, init_driver

# 設置 logger
logger = setup_logger('scraper', 'output.log')

def get_url(page=None, start_date=None, end_date=None, q=None, committee=None):
    """生成會議列表的URL"""
    url = 'https://www.ly.gov.tw/Pages/MeetingList.aspx?nodeid=135'
    params = []

    if page is not None:
        params.append(f'idx={page - 1}')
    else:
        params.append(f'idx=0')
    if start_date:
        params.append(f'qsd={start_date}')
    if end_date:
        params.append(f'qed={end_date}')
    if q:
        params.append(f'q={q}')
    if committee:
        params.append(f'Committee={committee}')

    if params:
        url += '&' + '&'.join(params)

    return url

async def get_page_content(browser, url):
    """取得頁面內容"""
    page = await browser.newPage()
    await page.goto(url)
    content = await page.content()
    await page.close()
    return content

def parse_video_element(video_element):
    """解析單個視頻元素，提取視頻信息"""
    video_info = {}
    base_url = 'https://ivod.ly.gov.tw'
    
    committee_info = video_element.find('div', class_='clip-list-text')
    if committee_info:
        p_tags = committee_info.find_all('p')
        for p in p_tags:
            if '委員：' in p.get_text():
                video_info['member'] = p.get_text(strip=True).replace('委員：', '')
            if '委員發言時間：' in p.get_text():
                video_info['speech_time'] = p.get_text(strip=True).replace('委員發言時間：', '')
            if '影片長度：' in p.get_text():
                video_info['video_length'] = p.get_text(strip=True).replace('影片長度：', '')

    committee_video = video_element.find('div', class_='clip-list-thumbnail')
    if committee_video:
        video_info['video_links'] = {}
        links = committee_video.find_all('a')
        for link in links:
            video_info['video_links'][link['title']] = base_url + link['href']

    return video_info

async def scrape_video_links(meeting_id):
    browser = await init_driver()
    """爬取會議視頻鏈接"""
    base_url = 'https://ivod.ly.gov.tw'
    meeting_url = f'http://ivod.ly.gov.tw/Demand/Meetvod?Meet={meeting_id}'
    page = 1
    video_details = {
        'meeting_id': meeting_id,
        'meeting_time': '',
        'meeting_name': '',
        'video_links': []
    }
    
    while True:
        paginated_url = f"{meeting_url}&page={page}"
        logger.info(f"正在爬取 URL: {paginated_url}")
        page_content = await get_page_content(browser, paginated_url)
        soup = BeautifulSoup(page_content, 'html.parser')

        if page == 1:
            committee_data = soup.select_one('div.committee-data-info')
            if committee_data:
                committee_info = committee_data.find('div', class_='clip-list-text')
                if committee_info:
                    video_details['committee'] = committee_info.find('h5').get_text(strip=True)
                    video_details['meeting_time'] = committee_info.find('span', class_='time').text
                    video_details['meeting_name'] = committee_info.find('span', class_='metdec').text

                committee_video = committee_data.find('div', class_='clip-list-thumbnail')
                if committee_video:
                    video_info = {'type': 'full', 'video_links': {}}
                    for a in committee_video.find_all('a'):
                        video_info['video_links'][a['title']] = base_url + a['href']
                    video_details['video_links'].append(video_info)

        no_data_div = soup.find('div', class_='list-nodate')
        if no_data_div:
            break
        
        clip_list = soup.find('div', class_='clip-list')
        if clip_list:
            for ul in clip_list.find_all('ul'):
                video_info = parse_video_element(ul)
                video_info['type'] = 'clip'
                video_details['video_links'].append(video_info)

        page += 1

    return video_details

async def parse_meeting_element(browser, date, meeting_element):
    """解析單個會議元素，提取會議信息"""
    meeting = {'date': date}

    time_div = meeting_element.find('div', class_='room', string=lambda text: '時間' in text)
    if time_div:
        meeting['time'] = time_div.text.strip()

    committee_div = meeting_element.find('div', class_='room', attrs={'data-name': True})
    if committee_div:
        meeting['committee'] = committee_div.text.strip()

    label_div = meeting_element.find('div', class_='label')
    if label_div:
        meeting['label'] = label_div.text.strip()

    location_div = meeting_element.find('div', class_='label', string=lambda text: '地點' in text)
    if location_div:
        meeting['location'] = location_div.text.strip()

    heading_div = meeting_element.find('div', class_='heading')
    if heading_div:
        meeting['title'] = heading_div.get_text(separator=' ', strip=True)
        link_tag = heading_div.find('a')
        if link_tag:
            meeting['meeting_url'] = link_tag['href']
            meeting_id = re.search(r'Meet=([0-9]+)', link_tag['href'])
            if meeting_id:
                meeting['meeting_id'] = meeting_id.group(1)
                video_links = await scrape_video_links(browser, meeting_id.group(1))
                meeting['video_links'] = video_links

    con_data_div = meeting_element.find('div', class_='con_data')
    if con_data_div:
        description_div = con_data_div.find('div')
        if description_div:
            meeting['description'] = description_div.text.strip()

    return meeting

async def scrape_meetings(start_date=None, end_date=None, page=None, q=None, committee=None, limit=100):
    """爬取會議列表"""
    browser = await init_driver()
    meetings = []
    current_page = page if page else 1

    while True:
        url = get_url(current_page, start_date, end_date, q, committee)
        logger.info(f"正在爬取 URL: {url}")
        page_content = await get_page_content(browser, url)
        soup = BeautifulSoup(page_content, 'html.parser')

        meeting_elements = soup.select('ul.list-group.newsType2 li')
        date = None
        tasks = []
        for meeting_element in meeting_elements:
            date_element = meeting_element.find('div', class_='date')
            if date_element:
                date = parse_meeting_date(date_element)
            tasks.append(parse_meeting_element(browser, date, meeting_element))
        
        meetings_batch = await asyncio.gather(*tasks)
        meetings.extend(meetings_batch)
        if len(meetings) >= limit:
            break

        # 檢查是否還有更多頁面
        pagination = soup.select_one('ul.pagination')
        if pagination is None:
            page_content = await get_page_content(browser, url)
            soup = BeautifulSoup(page_content, 'html.parser')
            pagination = soup.select_one('ul.pagination')
        pagination_items = pagination.find_all('li')
        if not pagination_items:
            break
        last_item = pagination_items[-1]
        if '»' in last_item.text.strip():
            current_page += 1
        else:
            try:
                last_page_num = int(last_item.text.strip())
                if current_page >= last_page_num:
                    break
                current_page += 1
            except ValueError:
                break

    await browser.close()
    return meetings, len(meetings) >= limit, current_page
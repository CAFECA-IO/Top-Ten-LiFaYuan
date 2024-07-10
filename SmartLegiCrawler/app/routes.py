from quart import request, jsonify
import os
import threading
import json
import asyncio
from . import app
from .scraper import scrape_meetings, scrape_video_links
from .downloader import download_video, get_video_source, get_output_filename
from .utils import setup_logger

# 設置 logger
logger = setup_logger('routes', 'routes.log')

# 第一個 API：查詢會議視頻
@app.route('/api/meetings', methods=['GET'])
async def get_meetings():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    q = request.args.get('q', None)
    committee = request.args.get('committee', None)
    limit = request.args.get('limit', default=100, type=int)
    
    loop = asyncio.new_event_loop()
    try:
        meetings, has_more, current_page = await scrape_meetings(start_date, end_date, page, q, committee, limit)
        response = {
            'total': len(meetings),
            'has_more': has_more,
            'current_page': current_page,
            'message': f'總數量超過 {limit}，請帶入當前頁面的下一頁接續查詢，每次最多查詢100筆，當前頁面為 {current_page}頁。' if has_more else '這是搜尋結果的最後一頁。',
            'meetings': meetings,
        }

        return app.response_class(
            response=json.dumps(response, ensure_ascii=False),
            mimetype='application/json'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 第二個 API：會議視頻詳情
@app.route('/api/meetings/<meeting_id>', methods=['GET'])
def get_meeting_videos(meeting_id):
    videos_source = scrape_video_links(meeting_id)

    response = {
        'details': videos_source,
    }

    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        mimetype='application/json'
    )

# 第三個 API：下載視頻
@app.route('/api/download', methods=['POST'])
def download():
    video_url = request.json.get('url')
    
    # 獲取視頻源地址
    m3u8_url = get_video_source(video_url)
    if not m3u8_url:
        return jsonify({'error': '無法獲取視頻源地址'}), 400
    
    output_filename = get_output_filename(video_url)
    
    # 使用多線程下載視頻，防止阻塞
    download_thread = threading.Thread(target=download_video, args=(m3u8_url, output_filename))
    download_thread.start()
    download_thread.join()

    # 檢查文件是否存在以及大小
    if os.path.exists(output_filename):
        file_size = os.path.getsize(output_filename)
        logger.info(f"下載的文件大小：{file_size} 字節")
        try:
            # 打印文件的絕對路徑以便調試
            abs_path = os.path.abspath(output_filename)
            logger.info(f"文件的絕對路徑：{abs_path}")
            return send_file(abs_path, as_attachment=True)
        except FileNotFoundError:
            logger.error(f"文件未找到：{abs_path}")
            return jsonify({'error': '文件未找到'}), 500
    else:
        return jsonify({'error': '下載失敗'}), 500

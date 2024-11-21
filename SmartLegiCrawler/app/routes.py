from quart import request, jsonify
import os
import json
from . import app
from .scraper import scrape_meetings, scrape_video_links
from .downloader import download
from .utils import setup_logger, get_path

def download_if_needed(video_url, video_id):
    video_path = get_path('videos', f'{video_id}.mp4')
    if not os.path.exists(video_path):
        logger.info(f"Video not found, downloading video from {video_url}")
        download(video_url)
    return video_path

# 設置 logger
logger = setup_logger('crawler_routes', 'output.log')

@app.route('/')
def index():
    return "Welcome to SmartLegiCrawler!"

# 第一個 API：查詢會議視頻
@app.route('/api/meetings', methods=['GET'])
async def get_meetings():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    page = int(request.args.get('page', 1))
    q = request.args.get('q', None)
    committee = request.args.get('committee', None)
    limit = request.args.get('limit', default=100, type=int)
    
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
async def get_meeting_videos(meeting_id):
    print(f"meeting_id: {meeting_id}")
    videos_source = await scrape_video_links(meeting_id)

    response = {
        'details': videos_source,
    }

    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        mimetype='application/json'
    )

# 第三個 API：下載視頻
@app.route('/api/download', methods=['POST'])
async def downloader():
    request_data = await request.get_json()
    video_url = request_data.get('url')
    
    if not video_url:
        return jsonify({"status": "error", "message": "Missing video URL"}), 400

    result = await download(video_url)
    return jsonify(result)

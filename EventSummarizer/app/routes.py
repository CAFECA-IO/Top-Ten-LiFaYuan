# app/routes.py

from flask import request, jsonify
import os
from . import app
from .summarize import generate_summary
from dotenv import load_dotenv
from .utils import setup_logger, get_path

# 設置 logger
logger = setup_logger('routes', 'routes.log')

# 加載 .env 文件
load_dotenv()

@app.route('/')
def index():
    return "Welcome to EventSummarizer!"

@app.route('/api/summarize', methods=['GET'])
def summarizer():
    video_url = request.json.get('url')
    video_id = video_url.split('/')[-1]
    transcript_path = get_path('transcripts', f'{video_id}.json')
    summarize_path = get_path('summarized_transcripts', f'{video_id}.txt')
    
    # 檢查總結逐字稿文件是否存在
    if not os.path.exists(summarize_path):
        logger.info(f"Summarizing transcription from {transcript_path} to {summarize_path}")
        # 獲取 API Token
        token = os.getenv("HUGGINGFACE_API_TOKEN")
        summarized_transcriptions = generate_summary(transcript_path, summarize_path, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=token)

        if not os.path.exists(summarize_path):
            logger.error(f"Failed to summarize transcription from {transcript_path} to {summarize_path}")
            return jsonify({'error': '優化逐字稿失敗'}), 500
    else:
        logger.info(f"總結逐字稿文件已存在：{summarize_path}")
    
    return jsonify({'message': '總結成功', 'script': summarized_transcriptions}), 200

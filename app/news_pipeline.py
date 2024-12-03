# app/news_pipeline.py
from app.crawler import fetch_meetings, download_video
from app.transcriber import transcribe_video
from app.summarizer import summarize_transcript
from app.generator import generate_vocal, generate_video
from app.utils import load_progress, save_progress

def process_news_pipeline(date):
    """整合流程，完成新聞生成"""
    # 爬取會議並下載
    meetings = fetch_meetings(date)
    for meeting in meetings:
        for video in meeting.get("videos", []):
            download_video(video["url"], video["video_id"])

    # 轉換字幕
    for meeting in meetings:
        for video in meeting.get("videos", []):
            transcribe_video(video["video_id"])

    # 生成摘要
    for meeting in meetings:
        for video in meeting.get("videos", []):
            summarize_transcript(video["video_id"])

    # 配音和生成視頻
    for meeting in meetings:
        for video in meeting.get("videos", []):
            generate_vocal(video["video_id"])
            generate_video(video["video_id"])

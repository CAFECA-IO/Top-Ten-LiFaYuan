# app/progress_checker.py

from app.crawler import fetch_meetings, download_video
from app.transcriber import transcribe_video
from app.summarizer import summarize_transcript
from app.generator import generate_vocal, generate_video
from app.utils import load_progress, save_progress

def process_videos(date=None):
    """處理影片的完整流程，從指定日期或上一次進度開始"""
    progress = load_progress()
    
    # 檢查是否有指定日期，優先處理新日期
    if date:
        progress["date"] = date
        save_progress("date", {"date": date})

    date_to_process = progress.get("date")
    if not date_to_process:
        raise ValueError("未指定影片日期且無上一次進度記錄。")

    # 爬取會議列表
    meetings = fetch_meetings(date_to_process)
    save_progress("meetings", {"meetings": meetings})

    # 下載視頻
    for meeting in meetings:
        for video in meeting.get("videos", []):
            download_video(video["url"])
            save_progress("download", {"video_id": video["video_id"]})

    # 字幕轉換
    for meeting in meetings:
        for video in meeting.get("videos", []):
            transcribe_video(video["url"])
            save_progress("transcribe", {"video_id": video["video_id"]})

    # 摘要生成
    for meeting in meetings:
        for video in meeting.get("videos", []):
            summarize_transcript(video["url"])
            save_progress("summarize", {"video_id": video["video_id"]})

    # 配音與視頻生成
    for meeting in meetings:
        for video in meeting.get("videos", []):
            transcript = f"transcripts/{video['video_id']}.json"
            summary = f"summaries/{video['video_id']}.txt"
            generate_vocal(summary)
            generate_video(summary)
            save_progress("generate", {"video_id": video["video_id"]})

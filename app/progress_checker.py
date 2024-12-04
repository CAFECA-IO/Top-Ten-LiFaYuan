import asyncio
from datetime import datetime, timedelta
from app.crawler import fetch_meetings, download_video
from app.transcriber import transcribe_video
from app.summarizer import summarize_transcript
from app.generator import generate_vocal, generate_video
from app.utils import load_progress, save_progress


async def process_videos(date=None):
    """處理影片的完整流程，會從上次進度接續處理，或處理指定日期的影片"""
    progress = load_progress()

    # **步驟 1: 處理日期**
    if "date" not in progress:
        date_to_process = date or (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        progress["date"] = date_to_process
        save_progress("date", date_to_process)
    else:
        date_to_process = progress["date"]
    print(f"處理日期：{date_to_process}")

    # **步驟 2: 取得會議列表**
    if "meetings" not in progress or not progress["meetings"]:
        print("正在爬取會議列表...")
        meetings = await fetch_meetings(date_to_process)
        progress["meetings"] = meetings
        save_progress("meetings", meetings)
    else:
        meetings = progress["meetings"]

    # **步驟 3: 處理每個會議的影片**
    for meeting in meetings:
        meeting_id = meeting.get("meeting_id")
        videos = meeting.get("video_links", {}).get("video_links", [])

        # 過濾並排序 `clip` 類型的影片
        clip_videos = sorted(
            [video for video in videos if video.get("type") == "clip"],
            key=lambda x: int(x["video_links"]["窄頻"].split("/")[-1])
        )

        # 初始化會議的進度
        if "results" not in progress:
            progress["results"] = {}
        if meeting_id not in progress["results"]:
            progress["results"][meeting_id] = {}

        for video in clip_videos:
            video_id = video["video_links"]["窄頻"].split("/")[-1]
            video_url = video["video_links"]["窄頻"]

            # 初始化影片的進度
            if video_id not in progress["results"][meeting_id]:
                progress["results"][meeting_id][video_id] = {
                    "status": "pending",
                    "steps": {
                        "download": False,
                        "transcribe": False,
                        "summarize": False,
                        "generate_audio": False,
                        "generate_video": False
                    },
                    "audio": None,
                    "video": None,
                    "summary": None,
                    "error": None
                }

            video_progress = progress["results"][meeting_id][video_id]

            try:
                # **下載影片**
                if not video_progress["steps"]["download"]:
                    print(f"下載影片：{video_url}")
                    try:
                        await download_video(video_url, video_id)
                        video_progress["steps"]["download"] = True
                        save_progress("results", progress["results"])
                    except Exception as e:
                        video_progress["error"] = f"下載失敗：{str(e)}"
                        save_progress("results", progress["results"])
                        print(f"下載影片 {video_id} 時發生錯誤：{e}")

                        
                # **轉錄字幕**
                if not video_progress["steps"]["transcribe"] and video_progress["steps"]["download"]:
                    print(f"轉錄字幕：{video_id}")
                    await transcribe_video(video_id)
                    video_progress["steps"]["transcribe"] = True
                    save_progress("results", progress["results"])

                # **生成摘要**
                if not video_progress["steps"]["summarize"] and video_progress["steps"]["transcribe"]:
                    print(f"生成摘要：{video_id}")
                    summary_path = await summarize_transcript(video_id)
                    video_progress["steps"]["summarize"] = True
                    video_progress["summary"] = summary_path
                    save_progress("results", progress["results"])

                # **生成配音**
                if not video_progress["steps"]["generate_audio"] and video_progress["steps"]["summarize"]:
                    print(f"生成配音：{video_id}")
                    audio_path = await generate_vocal(video_id)
                    video_progress["steps"]["generate_audio"] = True
                    video_progress["audio"] = audio_path
                    save_progress("results", progress["results"])

                # **生成影片**
                if not video_progress["steps"]["generate_video"] and video_progress["steps"]["summarize"]:
                    print(f"生成影片：{video_id}")
                    video_path = await generate_video(video_id)
                    video_progress["steps"]["generate_video"] = True
                    video_progress["video"] = video_path
                    video_progress["status"] = "completed"
                    save_progress("results", progress["results"])

                # Todo: 把同一個meeting裡面所有的video拼成一個
                
            except Exception as e:
                # 記錄錯誤並跳過
                video_progress["error"] = str(e)
                save_progress("results", progress["results"])
                print(f"處理影片 {video_id} 時發生錯誤：{e}")

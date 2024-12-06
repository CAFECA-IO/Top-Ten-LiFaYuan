import os
from app.utils import setup_logger, get_path
from moviepy import concatenate_videoclips, VideoFileClip

logger = setup_logger('news_generator', 'logs/news_generator.log')

def generate_news(meeting_id, video_ids):
    """
    將同一個 meeting 的所有 video 拼接成一個新聞視頻
    :param meeting_id: 會議 ID
    :param video_ids: 該會議中所有 clip 類型影片的 ID 列表
    :return: 拼接後的新聞視頻路徑
    """
    try:
        video_clips = []
        for video_id in video_ids:
            video_path = get_path("shared_data/videos", f"{video_id}.mp4")
            if not os.path.exists(video_path):
                logger.error(f"Video file not found: {video_path}")
                raise FileNotFoundError(f"Video file not found: {video_path}")
            video_clips.append(VideoFileClip(video_path))

        # 拼接影片
        logger.info(f"開始拼接影片: {video_ids}")
        final_clip = concatenate_videoclips(video_clips, method="compose")
        news_video_path = get_path("shared_data/news", f"news_{meeting_id}.mp4")
        os.makedirs(os.path.dirname(news_video_path), exist_ok=True)
        final_clip.write_videofile(news_video_path, codec="libx264", audio_codec="aac")
        logger.info(f"新聞影片生成成功: {news_video_path}")

        # 關閉所有 clip 資源
        for clip in video_clips:
            clip.close()
        final_clip.close()

        return news_video_path
    except Exception as e:
        logger.error(f"生成新聞影片失敗: {str(e)}")
        raise

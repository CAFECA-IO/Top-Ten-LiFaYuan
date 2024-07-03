import subprocess
from pydub import AudioSegment
from .utils import setup_logger

# 設置 logger
logger = setup_logger('audio_extractor', 'audio_extractor.log')

def extract_audio(video_path, audio_path):
    """
    優點：
    1. 高效：ffmpeg 是一個高性能的多媒體處理工具，對於大文件和長視頻的處理速度更快。
    2. 功能強大：ffmpeg 提供了豐富的參數和選項，可以進行各種音視頻處理操作。
    3. 廣泛支持：ffmpeg 支持多種格式的音視頻文件，適用範圍更廣。
    缺點：
    1. 依賴外部工具：需要系統安裝 ffmpeg，並且在一些受限環境中可能無法使用。
    2. 學習曲線：ffmpeg 的參數和命令較多，對初學者來說有一定的學習曲線。
    """
    command = [
        'ffmpeg',
        '-i', video_path,   # 輸入文件
        '-q:a', '0',        # 音質設置為最好
        '-map', 'a',        # 僅提取音頻
        audio_path          # 輸出音頻文件路徑
    ]
    
    try:
        subprocess.run(command, check=True)
        logger.info(f"音頻已成功提取並儲存至：{audio_path}")
    except subprocess.CalledProcessError as e:
        logger.info(f"提取音頻時出現錯誤：{e}")


def extract_audio_by_pudub(video_path, audio_path):
    """
    優點：
    1. 單易用：代碼簡潔，易於理解和使用。
    2. 跨平台：pydub 是基於 Python 的庫，能在多個平台上運行（Windows、macOS、Linux）。
    3. 不依賴外部工具：不需要依賴 ffmpeg 作為外部工具，只需要安裝 pydub 和相應的音頻處理後端（如 ffmpeg 或 libav）。
    缺點：
    1. 性能較差：對於大文件或長視頻，處理時間可能較長，性能不如 ffmpeg。
    2. 功能有限：相比 ffmpeg，pydub 的功能相對簡單，無法處理一些複雜的音視頻轉換需求。
    """
    try:
        # 提取音頻
        video = AudioSegment.from_file(video_path)
        video.export(audio_path, format="wav")
        logger.info(f"音頻已成功提取並儲存至 by pudub：{audio_path}")
    except Exception as e:
        logger.info(f"提取音頻時出現錯誤 by pudub：{e}")
# app/audio_extractor.py

import subprocess
from pydub import AudioSegment
import noisereduce as nr
from .utils import setup_logger, get_path

# 設置 logger
logger = setup_logger('audio_extractor', 'output.log')

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
    """
    高品質壓縮音頻
    command = [
        'ffmpeg',
        '-i', video_path,   # 輸入文件
        '-q:a', '0',        # 音質設置為最好
        '-map', 'a',        # 僅提取音頻
        audio_path          # 輸出音頻文件路徑
    ]
    """
    """
    使用 FFmpeg 從視頻中提取無損音頻。
    """
    command = [
        'ffmpeg',
        '-i', video_path,           # 輸入視頻文件路徑
        '-vn',                      # 僅提取音頻
        '-acodec', 'pcm_s16le',     # 使用無損音頻編碼
        '-ar', '44100',             # 設置採樣率為 44100 Hz
        '-ac', '2',                 # 設置聲道數為 2（立體聲）
        audio_path                  # 輸出音頻文件路徑
    ]
    
    try:
        subprocess.run(command, check=True)
        logger.info(f"音頻已成功提取並儲存至：{audio_path}")
    except subprocess.CalledProcessError as e:
        logger.info(f"提取音頻時出現錯誤：{e}")


def process_audio(input_path, output_path, low_pass_freq=8000, high_pass_freq=100):
    """
    使用 pydub 讀取音頻文件並進行處理，包括降噪、歸一化和應用高通、低通濾波器。
    """
    # 使用 pydub 讀取音頻文件
    audio = AudioSegment.from_file(input_path)
    samples = audio.get_array_of_samples()
    sample_rate = audio.frame_rate

    # 使用 noisereduce 進行降噪處理
    reduced_noise = nr.reduce_noise(y=samples, sr=sample_rate)

    # 更新音頻數據
    audio = audio._spawn(reduced_noise.tobytes())
    
    # 基本音頻處理，例如音頻歸一化
    audio = audio.normalize()
    
    # 進行更多處理，如降噪、均衡等
    # 這裡僅做簡單的均衡處理
    audio = audio.low_pass_filter(low_pass_freq)  # 低通濾波器，去除高頻噪音
    audio = audio.high_pass_filter(high_pass_freq)  # 高通濾波器，去除低頻噪音
    
    # 保存處理後的音頻
    audio.export(output_path, format="wav", codec="pcm_s16le")
    logger.info(f"音頻已處理並儲存至：{output_path}")

"""
def extract_audio_by_pudub(video_path, audio_path):

    # 優點：
    # 1. 單易用：代碼簡潔，易於理解和使用。
    # 2. 跨平台：pydub 是基於 Python 的庫，能在多個平台上運行（Windows、macOS、Linux）。
    # 3. 不依賴外部工具：不需要依賴 ffmpeg 作為外部工具，只需要安裝 pydub 和相應的音頻處理後端（如 ffmpeg 或 libav）。
    # 缺點：
    # 1. 性能較差：對於大文件或長視頻，處理時間可能較長，性能不如 ffmpeg。
    # 2. 功能有限：相比 ffmpeg，pydub 的功能相對簡單，無法處理一些複雜的音視頻轉換需求。

    try:
        # 提取音頻
        video = AudioSegment.from_file(video_path)
        video.export(audio_path, format="wav")
        logger.info(f"音頻已成功提取並儲存至 by pudub：{audio_path}")
    except Exception as e:
        logger.info(f"提取音頻時出現錯誤 by pudub：{e}")
"""
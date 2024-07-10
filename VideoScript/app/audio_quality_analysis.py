import os
import numpy as np
import matplotlib.pyplot as plt
import wave
from pydub import AudioSegment
from .utils import setup_logger


# 設置 logger
logger = setup_logger('audio_quality_analysis', 'output.log')

def get_audio_data(audio_path):
    # 使用 pydub 讀取音頻文件
    audio = AudioSegment.from_wav(audio_path)
    audio_data = np.array(audio.get_array_of_samples())
    n_channels = audio.channels
    sampwidth = audio.sample_width
    framerate = audio.frame_rate
    n_frames = len(audio_data) // n_channels
    return audio_data, n_channels, sampwidth, framerate, n_frames

def get_audio_data_by_wave(audio_path):
    """
    wave 模塊是 Python 標準庫的一部分，用於處理 WAV 文件。它只能處理未壓縮的 PCM 格式的 WAV 文件，並且提供了較低級的接口來讀取和寫入音頻數據。輕量級，不需要安裝額外的庫。適用於處理簡單的 WAV 文件。
    pydub 是一個強大的音頻處理庫，能夠處理多種音頻格式（如 WAV、MP3、AAC 等）。它依賴於 ffmpeg 或 libav 來處理音頻文件，提供了高級接口來讀取、寫入和處理音頻數據。支持多種音頻格式，不僅限於 WAV 文件。提供豐富的音頻處理功能，如轉換、切割、合併、效果應用等。
    """
    # 使用 wave 讀取音頻文件
    with wave.open(audio_path, 'rb') as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_content = wf.readframes(n_frames)
    
    # 將音頻數據轉換為 numpy 數組
    audio_data = np.frombuffer(audio_content, dtype=np.int16)   
    return audio_data, n_channels, sampwidth, framerate, n_frames

def check_audio_quality(audio_data, n_channels, sampwidth, framerate, n_frames, audio_file_name):
    # 計算音頻持續時間
    duration = n_frames / framerate

    # 分析音頻質量
    # 檢查靜音（幅度接近零）和削波（幅度接近最大值）
    max_amplitude = np.max(np.abs(audio_data))
    min_amplitude = np.min(np.abs(audio_data))
    average_amplitude = np.mean(np.abs(audio_data))

    # 確定是否有明顯的靜音期或削波
    silence_threshold = 0.01 * max_amplitude
    clipping_threshold = 0.95 * max_amplitude

    num_silent_samples = np.sum(np.abs(audio_data) < silence_threshold)
    num_clipping_samples = np.sum(np.abs(audio_data) > clipping_threshold)

    audio_quality = {
        "duration_seconds": duration,
        "max_amplitude": max_amplitude,
        "min_amplitude": min_amplitude,
        "average_amplitude": average_amplitude,
        "num_silent_samples": num_silent_samples,
        "num_clipping_samples": num_clipping_samples,
    }

    logger.info(f"[{audio_file_name}]: {audio_quality}")

    return audio_quality

def draw_audio_waveform(audio_data, n_channels, sampwidth, framerate, n_frames, audio_file_name):
    # 降采樣以減少數據點數量（例如，每 100 個點取一個）
    downsampled_data = audio_data[::100]

    # 繪製音頻波形
    plt.figure(figsize=(10, 4))
    plt.plot(downsampled_data)
    plt.title(f'Audio Waveform {audio_file_name}')
    plt.xlabel('Sample Index (Downsampled)')
    plt.ylabel('Amplitude')
    
    # 確保 analysis 文件夾存在
    os.makedirs('analysis', exist_ok=True)
    
    # 保存圖形到 analysis 文件夾
    output_path = os.path.join('analysis', f'audio_waveform_{audio_file_name}.png')
    plt.savefig(output_path)
    plt.close()


def analysis(audio_path, video_id, version):
    audio_data, n_channels, sampwidth, framerate, n_frames = get_audio_data(audio_path)
    audio_file_name = os.path.basename(audio_path)
    check_audio_quality(audio_data, n_channels, sampwidth, framerate, n_frames, audio_file_name)
    draw_audio_waveform(audio_data, n_channels, sampwidth, framerate, n_frames, audio_file_name)
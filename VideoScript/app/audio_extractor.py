# # app/audio_extractor.py

# from pydub import AudioSegment

# def extract_audio(video_path, audio_path):
#     try:
#         # 提取音頻
#         video = AudioSegment.from_file(video_path)
#         video.export(audio_path, format="wav")
#         print(f"音頻已成功提取並儲存至：{audio_path}")
#     except Exception as e:
#         print(f"提取音頻時出現錯誤：{e}")

import subprocess

def convert_video_to_audio(video_path, audio_path):
    command = [
        'ffmpeg',
        '-i', video_path,   # 输入文件
        '-q:a', '0',        # 音质设置为最好
        '-map', 'a',        # 仅提取音频
        audio_path          # 输出音频文件路径
    ]
    
    try:
        subprocess.run(command, check=True)
        print("音频提取成功，保存为：{}".format(audio_path))
    except subprocess.CalledProcessError as e:
        print("错误：音频提取失败", e)

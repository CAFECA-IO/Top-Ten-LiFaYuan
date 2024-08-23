import subprocess

def combine_media(animation_file_path, voiceover_file_path, music_file_path):
    output_file_path = 'data/output/final_news_video.mp4'
    command = [
        'ffmpeg',
        '-i', animation_file_path,
        '-i', voiceover_file_path,
        '-i', music_file_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        output_file_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f'新聞播報影片已生成：{output_file_path}')
    except subprocess.CalledProcessError as e:
        print(f'合成影片時出錯: {e}')
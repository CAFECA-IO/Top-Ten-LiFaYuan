# run.py

import sys
import os
import threading
from app import app
from app.audio_quality_analysis import analysis
from app.audio_extractor import extract_audio, process_audio
from app.transcribe import transcribe_audio
from app.optimize import optimize_transcription
from app.downloader import download_video, get_video_source

video_id = "154397"
video_url = f"https://ivod.ly.gov.tw/Play/Clip/300K/{video_id}"

if __name__ == '__main__':
    # app.run(debug=True)
    downloads_dir = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(downloads_dir):
        os.makedirs(downloads_dir)
    
    audios_dir = os.path.join(os.getcwd(), 'audios')
    if not os.path.exists(audios_dir):
        os.makedirs(audios_dir)
    
    scripts_dir = os.path.join(os.getcwd(), 'scripts')
    if not os.path.exists(scripts_dir):
        os.makedirs(scripts_dir)

    if len(sys.argv) > 1:
        if 'download' in sys.argv:
            print(f"Downloading video from {video_url}")
            video_path = os.path.join('downloads', f'downloaded_meeting_{video_id}.mp4')
            m3u8_url = get_video_source(video_url)
            if not m3u8_url:
                print("Failed to get video source")
                sys.exit(1)
            print(f"Downloading video from {m3u8_url} to {video_path}")
            download_thread = threading.Thread(target=download_video, args=(m3u8_url, video_path))
            download_thread.start()
            download_thread.join()

            if not os.path.exists(video_path):
                print(f"Failed to download video from {m3u8_url}")
                sys.exit(1)

        if 'extract' in sys.argv: 
            video_path = os.path.join('downloads', f'downloaded_meeting_{video_id}.mp4')
            audio_path = os.path.join('audios', f'converted_meeting_{video_id}.wav')
            print(f"Extracting audio from {video_path} to {audio_path}")
            extract_audio(video_path, audio_path)

        if 'process' in sys.argv:
            audio_path = os.path.join('audios', f'converted_meeting_{video_id}.wav')
            processed_audio_path = os.path.join('audios', f'processed_audio_{video_id}.wav')
            print(f"Processing audio from {audio_path} to {processed_audio_path}")
            process_audio(audio_path, processed_audio_path)

        if 'transcribe' in sys.argv:
            processed_audio_path = os.path.join('audios', f'processed_audio_{video_id}.wav')
            transcript_path = os.path.join('scripts', f'meeting_script_{video_id}.json')
            print(f"Transcribing audio from {processed_audio_path} to {transcript_path}")
            transcribe_audio(processed_audio_path, transcript_path, model_name="base", language="zh")

        if 'optimize' in sys.argv:
            transcript_path = os.path.join('scripts', f'meeting_script_{video_id}.json')
            optimized_path = os.path.join('scripts', f'optimized_script{video_id}.json')
            token = os.getenv("HUGGINGFACE_API_TOKEN")
            optimized_transcriptions = optimize_transcription(transcript_path, optimized_path, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=token)
            
    else:
        app.run(debug=True)

# run.py

import sys
import os
from app import app
# from app.audio_quality_analysis import analysis
from app.audio_extractor import extract_audio, process_audio
from app.transcribe import transcribe_audio
from app.optimize import optimize_transcription
from app.downloader import download
from app.summarize import generate_summary
from app.utils import get_path, setup_logger

logger = setup_logger('run', 'run.log')

video_url = "https://ivod.ly.gov.tw/Play/Clip/300K/154522"

def download_if_needed(video_url, video_id):
    video_path = get_path('downloads', video_id, 'mp4')
    if not os.path.exists(video_path):
        logger.info(f"Video not found, downloading video from {video_url}")
        download(video_url)
    return video_path

def extract_audio_if_needed(video_path, video_id):
    audio_path = get_path('audios', video_id, 'wav')
    if not os.path.exists(audio_path):
        logger.info(f"Extracting audio from {video_path} to {audio_path}")
        extract_audio(video_path, audio_path)
    return audio_path

def process_audio_if_needed(audio_path, video_id, low_pass_freq=6000, high_pass_freq=150):
    processed_path = get_path('audios', f'processed_{video_id}', 'wav')
    if not os.path.exists(processed_path):
        logger.info(f"Processing audio from {audio_path} to {processed_path}")
        process_audio(audio_path, processed_path, low_pass_freq=low_pass_freq, high_pass_freq=high_pass_freq)
    return processed_path

def transcribe_if_needed(processed_path, video_id, model_name="medium", language="zh"):
    transcript_path = get_path('scripts', video_id, 'json')
    if not os.path.exists(transcript_path):
        logger.info(f"Transcribing audio from {processed_path} to {transcript_path}")
        transcribe_audio(processed_path, transcript_path, model_name=model_name, language=language)
    return transcript_path

def optimize_if_needed(transcript_path, video_id):
    optimized_path = get_path('scripts', f'optimized_{video_id}', 'json')
    if not os.path.exists(optimized_path):
        logger.info(f"Optimizing transcript from {transcript_path}")
        optimize_transcription(transcript_path, optimized_path)
    return optimized_path

def summarize_if_needed(optimized_path, video_id):
    summary_path = get_path('scripts', f'summary_{video_id}', 'txt')
    logger.info(f"Generating summary from {optimized_path} to {summary_path}")
    generate_summary(optimized_path, summary_path)
    return summary_path

if __name__ == '__main__':
    # app.run(debug=True)

    if len(sys.argv) > 1:
        if len(sys.argv) < 3:
            logger.info(f"Usage: python script.py download <video_url> or use default video url {video_url}")
        else:
            video_url = sys.argv[2]
        video_id = video_url.split('/')[-1]

        if 'download' in sys.argv:
            download(video_url)

        elif 'extract' in sys.argv:
            video_path = download_if_needed(video_url, video_id)
            extract_audio_if_needed(video_path, video_id)

        elif 'process' in sys.argv:
            video_path = download_if_needed(video_url, video_id)
            audio_path = extract_audio_if_needed(video_path, video_id)
            process_audio_if_needed(audio_path, video_id)

        elif 'transcribe' in sys.argv:
            video_path = download_if_needed(video_url, video_id)
            print(video_path)
            audio_path = extract_audio_if_needed(video_path, video_id)
            print(audio_path)
            processed_path = process_audio_if_needed(audio_path, video_id)
            print(processed_path)
            transcribe_if_needed(processed_path, video_id)
            print('done!')

        elif 'optimize' in sys.argv:
            video_path = download_if_needed(video_url, video_id)
            audio_path = extract_audio_if_needed(video_path, video_id)
            processed_path = process_audio_if_needed(audio_path, video_id)
            transcript_path = transcribe_if_needed(processed_path, video_id)
            optimize_if_needed(transcript_path, video_id)

        elif 'summarize' in sys.argv:
            video_path = download_if_needed(video_url, video_id)
            audio_path = extract_audio_if_needed(video_path, video_id)
            processed_path = process_audio_if_needed(audio_path, video_id)
            transcript_path = transcribe_if_needed(processed_path, video_id)
            optimized_path = optimize_if_needed(transcript_path, video_id)
            summarize_if_needed(optimized_path, video_id)
            
        else:
            print("Invalid command")
    else:
        app.run(debug=True)

# run.py

import sys
import os
import argparse
from app import app
from app.summarize import generate_summary
from app.utils import get_path, setup_logger

logger = setup_logger('run', 'run.log')
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'

video_url = "https://ivod.ly.gov.tw/Play/Clip/300K/154522"

def download_if_needed(video_id):
    video_path = get_path('videos', f'{video_id}.mp4')
    if not os.path.exists(video_path):
        logger.info(f"Video not found, please download video first")
        sys.exit(1)
        

def extract_audio_if_needed(video_id):
    audio_path = get_path('audios', f'{video_id}.wav')
    if not os.path.exists(audio_path):
        logger.info(f"Audio not found, please extract audio first")
        sys.exit(1)

def process_audio_if_needed(video_id):
    processed_path = get_path('processed_audios', f'{video_id}.wav')
    if not os.path.exists(processed_path):
        logger.info(f"Processed audio not found, please process audio first")
        sys.exit(1)

def transcribe_if_needed(video_id):
    transcript_path = get_path('transcripts', f'{video_id}.json')
    if not os.path.exists(transcript_path):
        logger.info(f"Transcript not found, please transcribe audio first")
        sys.exit(1)

def optimize_if_needed(video_id):
    optimized_path = get_path('optimized_transcripts', f'{video_id}.json')
    if not os.path.exists(optimized_path):
        logger.info(f"Optimized transcript not found, please optimize transcript first")
        sys.exit(1)

def summarize_if_needed(script_path, video_id):
    summary_path = get_path('summarized_transcripts', f'{video_id}.txt')
    logger.info(f"Generating summary from {script_path} to {summary_path}")
    generate_summary(script_path, summary_path)
    return summary_path

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv) < 3:
            logger.info(f"Usage: python script.py download <video_url> or use default video url {video_url}")
        else:
            video_url = sys.argv[2]
        video_id = video_url.split('/')[-1]

        if 'summarize' in sys.argv:
            video_path = download_if_needed(video_id)
            audio_path = extract_audio_if_needed(video_path, video_id)
            processed_path = process_audio_if_needed(audio_path, video_id)
            transcript_path = transcribe_if_needed(processed_path, video_id)
            summarize_if_needed(transcript_path, video_id)
            
        else:
            print("Invalid command")
    else:
        parser = argparse.ArgumentParser(description='Run the Flask app.')
        parser.add_argument('--port', type=int, default=5002, help='Port to run the Flask app on.')
        args = parser.parse_args()

        app.run(host='0.0.0.0', port= args.port, debug=True)

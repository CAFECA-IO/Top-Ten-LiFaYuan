# run.py

import sys
import os
import json
from app import app
from app.audio_quality_analysis import analysis
from app.audio_extractor import extract_audio, process_audio
from app.transcribe import transcribe_and_optimize_audio
from app.optimize import optimize_transcription

if __name__ == '__main__':
    # app.run(debug=True)
    if len(sys.argv) > 1 and 'analyze' in sys.argv:
        video_id = "154397"  # 視頻 ID
        version = "v2"
        audio_path = os.path.join('audios', f'converted_meeting_{video_id}_{version}.wav') 
        analysis(audio_path, video_id, version)
    
    elif len(sys.argv) > 1 and 'extract' in sys.argv:
        video_id = "154397"
        version = "v2"
        video_path = os.path.join('downloads', f'downloaded_meeting_{video_id}.mp4')
        audio_path = os.path.join('audios', f'converted_meeting_{video_id}_{version}.wav')
        processed_audio_path = os.path.join('audios', f'processed_audio_{video_id}_{version}.wav')
        extract_audio(video_path, audio_path)
        process_audio(audio_path, processed_audio_path)

    elif len(sys.argv) > 1 and 'transcribe' in sys.argv:
        video_id = "154397"
        version = "v2"
        processed_audio_path = os.path.join('audios', f'processed_audio_{video_id}_{version}.wav')
        transcript_path = os.path.join('scripts', f'meeting_script_{video_id}_v3.txt')
        print(f"Transcribing audio from {processed_audio_path}...")
        token = os.getenv("HUGGINGFACE_API_TOKEN")
        transcribe_and_optimize_audio(processed_audio_path, transcript_path, model_name="base", device="cpu", optimize_model="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", language="zh", token=token)

    elif len(sys.argv) > 1 and 'optimize' in sys.argv:
        filename = "segments_processed_audio_154397_v2.json"
        token = os.getenv("HUGGINGFACE_API_TOKEN")
        optimized_transcriptions = optimize_transcription(filename, model_name="taide/Llama3-TAIDE-LX-8B-Chat-Alpha1", token=token)

    else:
        app.run(debug=True)

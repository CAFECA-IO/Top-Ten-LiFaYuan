from app import app
import argparse
import os
import json

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Quart app.')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the Quart app on.')
    parser.add_argument('--shared_data', type=str, required=True, help='Path to the shared data folder.')
    parser.add_argument('--videos', type=str, required=True, help='Path to the videos folder.')
    parser.add_argument('--audios', type=str, required=True, help='Path to the audios folder.')
    parser.add_argument('--processed_audios', type=str, required=True, help='Path to the processed audios folder.')
    parser.add_argument('--transcripts', type=str, required=True, help='Path to the transcripts folder.')
    parser.add_argument('--optimized_transcripts', type=str, required=True, help='Path to the optimized transcripts folder.')
    parser.add_argument('--summarized_transcripts', type=str, required=True, help='Path to the summarized transcripts folder.')
    args = parser.parse_args()

    # 將資料夾路徑寫入配置文件
    config = {
        'shared_data': args.shared_data,
        'videos': args.videos,
        'audios': args.audios,
        'processed_audios': args.processed_audios,
        'transcripts': args.transcripts,
        'optimized_transcripts': args.optimized_transcripts,
        'summarized_transcripts': args.summarized_transcripts,
    }
    
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file)

    print(f"Configuration saved to {config_path}")

    app.run(host='0.0.0.0', port=args.port, debug=True)

import argparse
from app import app
import logging

# 配置日誌
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask app.')
    parser.add_argument('--port', type=int, default=5003, help='Port to run the Flask app on.')
    args = parser.parse_args()

    port = args.port
    logging.info(f"Starting ComfyFlowGen on port {port}")
    print(f"Starting ComfyFlowGen on port {port}")

    app.run(host='0.0.0.0', port=port, debug=True)

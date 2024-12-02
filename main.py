# main.py

from flask import Flask, request, jsonify
from app.progress_checker import process_videos

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to the Automated Video Processor!"

@app.route("/start", methods=["POST"])
def start_processing():
    try:
        data = request.json
        date = data.get("date")  # 指定新日期，格式 YYYY-MM-DD
        process_videos(date)
        return jsonify({"message": "Processing started", "date": date}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting video processing service...")
    process_videos()  # 啟動時自動檢查進度並處理
    app.run(host="0.0.0.0", port=8000)

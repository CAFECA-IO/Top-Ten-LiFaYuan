import subprocess
import time
import os

# 定義共用資料夾和子資料夾的路徑
shared_data_path = os.path.join(os.getcwd(), 'shared_data')
folders = [
    "videos",
    "audios",
    "processed_audios",
    "transcripts",
    "optimized_transcripts",
    "summarized_transcripts"
]

# 如果共用資料夾或子資料夾不存在，則創建它們
if not os.path.exists(shared_data_path):
    os.makedirs(shared_data_path)
    print(f"Created shared data folder at: {shared_data_path}")

subfolder_paths = {}
for folder in folders:
    folder_path = os.path.join(shared_data_path, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder {folder} at: {folder_path}")
    subfolder_paths[folder] = folder_path

# 定義每個小專案的啟動命令和分配的端口
projects = [
    {"name": "SmartLegiCrawler", "path": "./SmartLegiCrawler", "port": 5000},
    {"name": "VideoScript", "path": "./VideoScript", "port": 5001},
    {"name": "EventSummarizer", "path": "./EventSummarizer", "port": 5002},
    # 可以繼續添加更多的專案
]

# 用於儲存 subprocess Popen 對象的列表
processes = []

# 啟動每個小專案
for project in projects:
    command = (
        f"python run.py --port {project['port']} --shared_data {shared_data_path} "
        f"--videos {subfolder_paths['videos']} --audios {subfolder_paths['audios']} "
        f"--processed_audios {subfolder_paths['processed_audios']} --transcripts {subfolder_paths['transcripts']} "
        f"--optimized_transcripts {subfolder_paths['optimized_transcripts']} --summarized_transcripts {subfolder_paths['summarized_transcripts']}"
    )
    print(f"Starting {project['name']} on port {project['port']}...")
    process = subprocess.Popen(command, shell=True, cwd=project['path'])
    processes.append({"name": project['name'], "process": process})
    time.sleep(1)  # 延遲一秒以確保每個專案有時間啟動

# 等待並保持所有小專案運行
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping all projects...")
    for process in processes:
        process["process"].terminate()
        print(f"Stopped {process['name']}")

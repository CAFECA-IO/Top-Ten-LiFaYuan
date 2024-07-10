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
    # 配置虛擬環境並安裝依賴
    venv_path = os.path.join(project["path"], "venv")
    if not os.path.exists(venv_path):
        print(f"Setting up virtual environment for {project['name']}...")
        subprocess.run(f"python3 -m venv venv", shell=True, cwd=project["path"])
        if os.name == 'nt':
            activate_command = os.path.join(venv_path, "Scripts", "activate.bat")
        else:
            activate_command = f"source {os.path.join(venv_path, 'bin', 'activate')}"
        
        subprocess.run(f"{activate_command} && pip install -r requirements.txt", shell=True, cwd=project["path"])
    
    # 啟動項目
    command = (
        f"{activate_command} && python run.py --port {project['port']}"
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

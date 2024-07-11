import os
import subprocess
import sys
import time
import signal

# 項目信息
PROJECTS = [
    {
        "name": "SmartLegiCrawler",
        "path": "./SmartLegiCrawler",
        "port": 5000,
    },
    {
        "name": "VideoScript",
        "path": "./VideoScript",
        "port": 5001,
    },
    {
        "name": "EventSummarizer",
        "path": "./EventSummarizer",
        "port": 5002,
    }
]

# 創建共用資料夾和子資料夾
SHARED_DATA_PATH = os.path.join(os.getcwd(), "shared_data")
FOLDERS = ["videos", "audios", "processed_audios", "transcripts", "optimized_transcripts", "summarized_transcripts"]

if not os.path.exists(SHARED_DATA_PATH):
    os.makedirs(SHARED_DATA_PATH)

for folder in FOLDERS:
    folder_path = os.path.join(SHARED_DATA_PATH, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# 獲取當前操作系統
IS_WINDOWS = sys.platform == "win32"

# 啟動專案
def start_project(project):
    project_path = project["path"]
    port = project["port"]
    venv_path = os.path.join(project_path, "venv")

    if not os.path.exists(project_path):
        print(f"專案路徑 {project_path} 不存在")
        return

    if not os.path.exists(venv_path):
        print(f"為 {project['name']} 設置虛擬環境...")
        subprocess.run([sys.executable, "-m", "venv", venv_path])

    # 根據操作系統設置虛擬環境的Python解釋器路徑
    python_executable = os.path.join(venv_path, "Scripts", "python.exe") if IS_WINDOWS else os.path.join(venv_path, "bin", "python")
    
    requirements_path = os.path.join(project_path, "requirements.txt")

    if os.path.exists(requirements_path):
        print(f"為 {project['name']} 安裝依賴...")
        subprocess.run([python_executable, "-m", "pip", "install", "-r", requirements_path])
    
    output_log = os.path.join(project_path, "output.log")
    with open(output_log, "w") as log_file:
        print(f"啟動 {project['name']}，使用端口 {port}...")
        process = subprocess.Popen(
            [python_executable, "run.py", "--port", str(port)],
            cwd=project_path,
            stdout=log_file,
            stderr=log_file,
            preexec_fn=os.setsid if not IS_WINDOWS else None
        )
        return process

processes = []

try:
    for project in PROJECTS:
        process = start_project(project)
        if process:
            processes.append(process)
            time.sleep(1)  # 等待項目啟動

    print("所有專案已啟動。按 Ctrl+C 停止。")
    signal.pause()
except KeyboardInterrupt:
    print("停止所有專案...")
    for process in processes:
        os.killpg(os.getpgid(process.pid), signal.SIGTERM) if not IS_WINDOWS else process.terminate()
    print("所有專案已停止。")

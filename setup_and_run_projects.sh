#!/bin/bash

LOG_FILE="setup_and_run_projects.log"
exec > >(tee -a $LOG_FILE) 2>&1

# 打印調試信息
echo "Starting setup_and_run_projects.sh script..."
date

# 定義共用資料夾和子資料夾的路徑
SHARED_DATA_PATH=$(pwd)/shared_data
FOLDERS=("videos" "audios" "processed_audios" "transcripts" "optimized_transcripts" "summarized_transcripts")

# 打印共用資料夾和子資料夾的路徑
echo "Shared data path: $SHARED_DATA_PATH"
echo "Folders: ${FOLDERS[@]}"

# 如果共用資料夾或子資料夾不存在，則創建它們
if [ ! -d "$SHARED_DATA_PATH" ]; then
    mkdir -p "$SHARED_DATA_PATH"
    echo "Created shared data folder at: $SHARED_DATA_PATH"
fi

for folder in "${FOLDERS[@]}"; do
    FOLDER_PATH="$SHARED_DATA_PATH/$folder"
    if [ ! -d "$FOLDER_PATH" ]; then
        mkdir -p "$FOLDER_PATH"
        echo "Created folder $folder at: $FOLDER_PATH"
    fi
done

# 定義每個小專案的名稱、路徑和分配的端口
PROJECT_NAMES=("SmartLegiCrawler" "VideoScript" "EventSummarizer")
PROJECT_PORTS=(5000 5001 5002)

# 啟動每個小專案
for i in "${!PROJECT_NAMES[@]}"; do
    project=${PROJECT_NAMES[$i]}
    PORT=${PROJECT_PORTS[$i]}
    PROJECT_PATH="./$project"
    VENV_PATH="$PROJECT_PATH/venv"

    echo "Setting up and starting $project on port $PORT..."

    # 檢查專案資料夾是否存在
    if [ ! -d "$PROJECT_PATH" ]; then
        echo "Project path $PROJECT_PATH does not exist"
        exit 1
    fi

    # 配置虛擬環境並安裝依賴
    if [ ! -d "$VENV_PATH" ]; then
        echo "Setting up virtual environment for $project..."
        python3 -m venv "$VENV_PATH"
        if [ $? -ne 0 ]; then
            echo "Failed to create virtual environment for $project"
            exit 1
        fi
    fi

    # 激活虛擬環境並安裝依賴
    if [ "$(uname)" == "Darwin" ] || [ "$(uname)" == "Linux" ]; then
        source "$VENV_PATH/bin/activate"
    elif [ "$(uname)" == "CYGWIN" ] || [ "$(uname)" == "MINGW" ]; then
        source "$VENV_PATH/Scripts/activate"
    fi

    echo "Installing requirements for $project..."
    if [ ! -f "$PROJECT_PATH/requirements.txt" ]; then
        echo "requirements.txt not found in $PROJECT_PATH"
        exit 1
    fi
    pip install -r "$PROJECT_PATH/requirements.txt"
    if [ $? -ne 0 ]; then
        echo "Failed to install requirements for $project"
        exit 1
    fi

    # 確保 output.log 文件可以創建
    OUTPUT_LOG="$PROJECT_PATH/output.log"
    echo "Creating output.log at $OUTPUT_LOG"
    touch "$OUTPUT_LOG"
    if [ $? -ne 0 ]; then
        echo "Failed to create log file for $project at $OUTPUT_LOG"
        exit 1
    fi

    ls -l "$PROJECT_PATH"  # 列出項目目錄內容，確認 output.log 是否創建成功

    # 啟動項目
    echo "Starting $project on port $PORT..."
    cd "$PROJECT_PATH"
    nohup python run.py --port "$PORT" >> "output.log" 2>&1 &
    if [ $? -ne 0 ]; then
        echo "Failed to start $project"
        exit 1
    fi
    cd -  # 返回腳本執行目錄
    sleep 1  # 延遲一秒以確保每個專案有時間啟動

    # 檢查項目是否啟動
    if lsof -i:$PORT; then
        echo "$project started successfully on port $PORT"
    else
        echo "Failed to start $project on port $PORT"
        echo "Log output from $project:"
        cat "$OUTPUT_LOG"
        exit 1
    fi
done

echo "All projects started. Press Ctrl+C to stop."

# 等待並保持所有小專案運行
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
while :; do sleep 1; done

#!/bin/bash

LOG_FILE="setup_and_run_projects.log"
exec > >(tee -a $LOG_FILE) 2>&1

# 記錄初始工作目錄
ROOT_DIR=$(pwd)
echo "Initial working directory: $ROOT_DIR"

# 定義共用資料夾和子資料夾的絕對路徑
SHARED_DATA_PATH="$ROOT_DIR/shared_data"
FOLDERS=("videos" "audios" "processed_audios" "transcripts" "optimized_transcripts" "summarized_transcripts")

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
PROJECT_NAMES=("SmartLegiCrawler" "VideoScript" "EventSummarizer" "ComfyFlowGen")
PROJECT_PORTS=(5000 5001 5002 5003)

check_port() {
    local port=$1
    if lsof -i:$port > /dev/null; then
        echo "Port $port is already in use. Please check if the corresponding service is running."
        return 1
    else
        return 0
    fi
}

terminate_previous_process() {
    local port=$1
    lsof -t -i:$port | xargs kill -9
}

for i in "${!PROJECT_NAMES[@]}"; do
    project=${PROJECT_NAMES[$i]}
    PORT=${PROJECT_PORTS[$i]}
    PROJECT_PATH="$ROOT_DIR/$project"  # 使用絕對路徑
    VENV_PATH="$PROJECT_PATH/venv"
    OUTPUT_LOG="$PROJECT_PATH/output.log"

    echo "Setting up and starting $project on port $PORT..."
    echo "Checking if project directory exists: $PROJECT_PATH"

    # 檢查專案資料夾是否存在
    if [ ! -d "$PROJECT_PATH" ]; then
        echo "Project path $PROJECT_PATH does not exist"
        exit 1
    fi

    # 確保有寫入許可權
    if [ ! -w "$PROJECT_PATH" ]; then
        echo "No write permission for $PROJECT_PATH"
        exit 1
    fi

    # # 如果端口已被佔用，跳過該服務
    # if ! check_port $PORT; then
    #     echo "Skipping $project due to port $PORT conflict."
    #     continue
    # fi

    # 配置虛擬環境並安裝依賴
    if [ ! -d "$VENV_PATH" ]; then
        echo "Setting up virtual environment for $project..."
        python3 -m venv "$VENV_PATH"
    # 檢查虛擬環境是否有效
    elif [ ! -x "$VENV_PATH/bin/python" ] || ! "$VENV_PATH/bin/python" --version > /dev/null 2>&1; then
            echo "Invalid virtual environment detected. Recreating it for $project..."
            rm -rf "$VENV_PATH"
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

    echo "Creating output.log at $OUTPUT_LOG"
    touch "$OUTPUT_LOG"
    if [ $? -ne 0 ]; then
        echo "Failed to create log file for $project at $OUTPUT_LOG"
        exit 1
    fi

    # 檢查 output.log 是否存在且可寫
    if [ ! -f "$OUTPUT_LOG" ] || [ ! -w "$OUTPUT_LOG" ]; then
        echo "Log file $OUTPUT_LOG does not exist or is not writable"
        exit 1
    fi

    echo "Current working directory: $(pwd)"
    echo "Checking directory permissions..."
    ls -ld "$(pwd)"
    ls -ld "$PROJECT_PATH"

    echo "Checking file permissions for output.log..."
    ls -l "$OUTPUT_LOG"

    while ! check_port $PORT; do
        echo "Port $PORT is in use. Trying a new port..."
        terminate_previous_process $PORT
        PORT=$((PORT+1))
    done

    echo "Starting $project on port $PORT..."
    cd "$PROJECT_PATH"
    echo "Command: nohup python run.py --port $PORT >> $OUTPUT_LOG 2>&1 &"
    nohup python run.py --port "$PORT" >> "$OUTPUT_LOG" 2>&1 &
    sleep 3  # 延遲三秒以確保每個專案有時間啟動

    # 改進進程啟動檢查邏輯
    if lsof -i:$PORT | grep LISTEN > /dev/null; then
        echo "$project started successfully on port $PORT"
    else
        echo "Failed to start $project on port $PORT"
        echo "Log output from $project:"
        cat "$OUTPUT_LOG"
        continue
    fi

    # 返回初始工作目錄
    cd "$ROOT_DIR"
done

echo "All projects started. Press Ctrl+C to stop."

# 等待並保持所有小專案運行
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM
while :; do sleep 1; done

# Top-Ten-LiFaYuan

臺灣立法院提供了豐富的公開資料，包括會議錄影、立法委員的簡介、各項議案的詳細狀態、預算和決算報告，以及各類委員會的工作情況。這些資訊雖然全面，但由於其龐大的資料量，公眾很難即時、客觀、準確地獲取和理解所有資訊。因此我們打算藉由網路爬蟲技術定期且即時收集所有的內容，透過 AI 模型識讀內容並進行摘要。同時針對內容設計議題重要性、社會影響力、知識教育性、改革創造性、特殊娛樂性等五大指標，由 AI 模型進行評分，最後排名選出關鍵的立法院十大好球，幫助公眾快速掌握重要且正確的資訊。

以下是一個 `README.md` 的範例，說明如何使用 `setup_and_run_projects.sh` 腳本來設置和啟動專案：

## Multi-Project Setup and Launch Script

此專案包含多個子專案，每個子專案都有自己的虛擬環境和依賴。這個 `setup_and_run_projects.sh` 腳本將會幫助你自動配置和啟動所有的子專案。

## 專案結構

```plaintext
Top-Ten-LiFaYuan/
│
├── share_data/
│   ├── videos/
│   ├── audios/
│   ├── processed_audios/
│   ├── transcripts/
│   ├── optimized_transcripts/
│   └── summarized_transcripts/
│
├── SmartLegiCrawler/
│   ├── app  
│   │    ├── __init__.py         # 初始化 Flask 應用
│   │    ├── routes.py           # 定義 API 路由
│   │    ├── utils.py            # 工具函數
│   │   
│   ├── venv/                   # 虛擬環境
│   │
│   ├── requirements.txt        # 專案依賴
│   │
│   ├── run.py                  # 啟動應用
│   ├── readme.md               # 專案說明文件
│   │
│   └── .gitignore              # Git 忽略文件
│
├── VideoScript/
│   ├── app  
│   │    ├── __init__.py         # 初始化 Flask 應用
│   │    ├── routes.py           # 定義 API 路由
│   │    ├── utils.py            # 工具函數
│   │   
│   ├── venv/                   # 虛擬環境
│   │
│   ├── requirements.txt        # 專案依賴
│   │
│   ├── run.py                  # 啟動應用
│   ├── readme.md               # 專案說明文件
│   │
│   └── .gitignore              # Git 忽略文件
│
├── EventSummarizer/
│   ├── app  
│   │    ├── __init__.py         # 初始化 Flask 應用
│   │    ├── routes.py           # 定義 API 路由
│   │    ├── utils.py            # 工具函數
│   │   
│   ├── venv/                   # 虛擬環境
│   │
│   ├── requirements.txt        # 專案依賴
│   │
│   ├── run.py                  # 啟動應用
│   ├── readme.md               # 專案說明文件
│   │
│   └── .gitignore              # Git 忽略文件
│
├── setup_and_run_projects.sh   # 設置和啟動腳本
│
└── README.md                   # 專案說明文件
```

## 使用說明

### 前置要求

- Python 3
- Bash (在 Windows 上建議使用 Git Bash 或 WSL)

### 步驟

1. 克隆此專案到本地：

    ```sh
    git clone https://github.com/your-repo/Top-Ten-LiFaYuan.git
    cd Top-Ten-LiFaYuan
    ```

2. 確保 `setup_and_run_projects.sh` 腳本有執行權限：

    ```sh
    chmod +x setup_and_run_projects.sh
    ```

3. 執行腳本來配置和啟動所有子專案：

    ```sh
    ./setup_and_run_projects.sh
    ```

### 腳本功能

- 創建共用資料夾和子資料夾（如果不存在）。
- 為每個子專案配置虛擬環境並安裝依賴。
- 啟動每個子專案並分配指定的端口。

### 停止所有專案

要停止所有運行中的子專案，可以使用 `Ctrl + C` 中斷腳本。腳本會自動停止所有子專案。

### 注意事項

- 確保你的系統已安裝 Python 3。
- 腳本假設每個子專案的虛擬環境和依賴文件（`requirements.txt`）都放在相應的目錄中。

## 問題排除

如果遇到任何問題，請檢查以下內容：

- 確保已經安裝 Python 3。
- 確保在啟動腳本前已經在專案根目錄中。
- 檢查各子專案目錄中的 `requirements.txt` 文件是否存在。

如有其他問題，請在此專案的 GitHub 問題頁面報告。

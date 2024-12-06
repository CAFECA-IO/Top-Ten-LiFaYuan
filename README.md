# Top-Ten-LiFaYuan

## 簡介

**Top-Ten-LiFaYuan** 是一個專案，旨在有效解讀並呈現臺灣立法院的公開數據。臺灣立法院提供了豐富的資訊，包括：

- 會議錄影與逐字稿
- 立法委員的資料與議案詳細狀態
- 預算與決算報告
- 各類委員會的工作情況

由於資訊龐雜，公眾難以快速掌握核心內容。本專案運用以下技術助力數據解讀：

1. **網路爬蟲技術**：定期收集並整理資料。
2. **AI 模型**：生成逐字稿、摘要，並基於五大指標進行評分。
3. **任務進度管理**：自動化流程支持中斷續跑。
4. **多模組設計**：實現資料自動化處理和可視化。

透過這些技術，專案生成「立法院十大好球」，幫助用戶迅速理解重點議題。

---

## Multi-Project Setup and Launch Script

此專案包含多個子專案，通過腳本 `setup_and_run_projects.sh` 自動完成以下操作：

- 子專案虛擬環境的安裝與依賴配置。
- 各子服務的啟動與監控。
- 錯誤排查與日誌記錄。

---

## 專案結構

```plaintext
Top-Ten-LiFaYuan/
├── app/
│   ├── progress_checker.py      # 檢查與管理任務進度
│   ├── crawler.py               # 爬取會議列表和下載視頻
│   ├── audio_extractor.py       # 音頻提取
│   ├── transcriber.py           # 視頻轉字幕
│   ├── summarizer.py            # 生成摘要
│   ├── generator.py             # 配音和視頻生成
│   ├── news_pipeline.py         # 整合新聞生成的邏輯
│   └── utils.py                 # 通用工具函數
│
├── logs/                        # 日誌文件
│   ├── main.log                 # 主流程日誌
│   ├── progress_checker.log     # 任務日誌
│   ├── crawler.log              # 爬取日誌
│   ├── audio_extractor.log      # 音頻日誌
│   ├── transcriber.log          # 字幕生成日誌
│   ├── summarizer.log           # 摘要生成日誌
│   └── generator.log            # 配音與視頻生成日誌
│
├── shared_data/                 # 共用的數據存儲
│   ├── videos/                  # 爬取的視頻
│   ├── audios/                  # 提取的音頻
│   ├── transcripts/             # 生成的逐字稿
│   └── summaries/               # 生成的摘要
│
├── setup_and_run_projects.sh    # 配置與啟動腳本
├── README.md                    # 說明文件
└── 子專案目錄
    ├── SmartLegiCrawler/        # 爬蟲模組
    ├── VideoScript/             # 視頻與逐字稿模組
    ├── EventSummarizer/         # 摘要生成模組
    ├── ComfyFlowGen/            # 視頻生成模組
```

---

## 使用說明

### **1. 前置要求**

- **Python 版本**：需要 Python 3.7 以上版本。
- **Bash 環境**：適用於 MacOS、Linux 或 Windows (Git Bash 或 WSL)。
- **FFmpeg**：視頻處理工具。

---

### **2. 啟動步驟**

#### **1. 克隆專案**

```bash
git clone https://github.com/your-repo/Top-Ten-LiFaYuan.git
cd Top-Ten-LiFaYuan
```

#### **2. 檢查腳本執行權限**

```bash
chmod +x setup_and_run_projects.sh
```

#### **3. 配置和啟動子專案**

```bash
./setup_and_run_projects.sh
```

#### **4. 確認服務狀態**

- 檢查控制台輸出，確保所有服務正常啟動。
- 每個子服務會在特定端口運行，例如：
  - `SmartLegiCrawler`: `http://localhost:5000`
  - `VideoScript`: `http://localhost:5001`
  - `EventSummarizer`: `http://localhost:5002`
  - `ComfyFlowGen`: `http://localhost:5003`

---

### **3. 啟動著任務**

#### **1. 啟動服務**

運行主腳本啟動服務：

```bash
python3 main.py
```

#### **2. 確認自動檢查進度**

- 檢查日誌或輸出，確保服務能正確執行未完成的步驟。

#### **3. 提交新任務**

使用 API 指定新日期：

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"date": "2024-12-03"}' \
http://localhost:8000/start
```

#### **4. 驗證輸出**

- 檢查 `videos/`、`transcripts/`、`summaries/` 和 `output/` 目錄，確認是否生成正確的文件。

### **4. 任務流程管理**

#### 進度檢查與續跑

專案使用進度記錄文件 `progress.json` 管理任務狀態，包括：

- 視頻爬取
- 音頻提取
- 字幕生成
- 摘要生成
- 視頻整合

#### 從中斷的地方繼續

重啟時，系統會自動檢查未完成的步驟並繼續執行。

---

## 常見問題及排查

### **1. 端口已佔用**

**錯誤訊息：**

```bash
Port <port_number> is already in use.
```

**解決方法：**

- 列出所以python使用的端口：
  
  ```bash
  ps aux | grep "python run.py"
  ```

- 確認端口占用：

  ```bash
  lsof -i:<port_number>
  ```

- 終止佔用進程：

  ```bash
  kill -9 <PID>
  ```

---

### **2. 虛擬環境問題**

**錯誤訊息：**

```bash
/path/to/venv/bin/pip: bad interpreter
```

**解決方法：**

- 重新創建虛擬環境:

```bash
rm -rf <project_path>/venv
python3 -m venv <project_path>/venv
source <project_path>/venv/bin/activate
pip install -r <project_path>/requirements.txt
```

- 重建虛擬環境:

重新創建虛擬環境並重新安裝依賴項辦法：

1. 清除現有環境：

   ```bash
   conda deactivate
   conda remove --name newsgenerator --all
   ```

2. 重建環境：

   ```bash
   conda create --name newsgenerator python=3.9
   conda activate newsgenerator
   pip install -r requirements.txt
   ```

3. 再次運行程序：

   ```bash
   python3 main.py
   ```

## 自動化腳本功能

- 自動檢查子專案目錄是否存在。
- 為每個子專案創建虛擬環境。
- 支持動態配置服務端口，避免衝突。
- 在特定端口啟動每個服務並記錄日誌。

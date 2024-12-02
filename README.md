# Top-Ten-LiFaYuan

臺灣立法院提供了豐富的公開資料，包括會議錄影、立法委員的簡介、各項議案的詳細狀態、預算和決算報告，以及各類委員會的工作情況。這些資訊雖然全面，但由於其龐大的資料量，公眾很難即時、客觀、準確地獲取和理解所有資訊。因此，我們使用網路爬蟲技術定期且即時收集所有內容，並透過 AI 模型識讀和摘要資訊。針對內容，設計了五大指標（議題重要性、社會影響力、知識教育性、改革創造性、特殊娛樂性），由 AI 模型進行評分，選出關鍵的「立法院十大好球」，幫助公眾快速掌握重要且正確的資訊。

## Multi-Project Setup and Launch Script

此專案包含多個子專案，每個子專案都有自己的虛擬環境和依賴。`setup_and_run_projects.sh` 腳本可以幫助您自動配置和啟動所有子專案。

---

## 專案結構

```plaintext
Top-Ten-LiFaYuan/
│
├── shared_data/                    # 共用的資料夾
│   ├── videos/
│   ├── audios/
│   ├── processed_audios/
│   ├── transcripts/
│   ├── optimized_transcripts/
│   └── summarized_transcripts/
│
├── SmartLegiCrawler/               # 子專案 1
├── VideoScript/                    # 子專案 2
├── EventSummarizer/                # 子專案 3
├── ComfyFlowGen/                   # 子專案 4
├── setup_and_run_projects.sh       # 設置和啟動腳本
└── README.md                       # 專案說明文件
```

---

## 使用說明

### 前置要求

- 安裝 **Python 3**
- Bash 環境（在 Windows 上建議使用 Git Bash 或 WSL）

### 啟動步驟

1. **克隆專案：**

   ```bash
   git clone https://github.com/your-repo/Top-Ten-LiFaYuan.git
   cd Top-Ten-LiFaYuan
   ```

2. **檢查腳本執行權限：**

   ```bash
   chmod +x setup_and_run_projects.sh
   ```

3. **執行腳本以配置和啟動專案：**

   ```bash
   ./setup_and_run_projects.sh
   ```

4. **確認服務是否正常運行：**
   - 每個子專案會顯示其對應的端口（例如，ComfyFlowGen 啟動於 `http://localhost:5003`）。
   - 可以在瀏覽器或 API 工具（如 Postman）中測試這些服務。

---

## 啟動服務失敗時的問題排除

### 常見問題及解決方法

#### 1. **端口已被佔用**

**錯誤訊息：**

```bash
Port <port_number> is already in use. Please check if the corresponding service is running.
Skipping <project_name> due to port <port_number> conflict.
```

**原因：**

- 指定的端口已被另一個進程佔用。

**解決方法：**

- 列出所以python使用的端口：
  
  ```bash
  ps aux | grep "python run.py"
  ```

- 或是確認端口是否被其他進程佔用：

  ```bash
  lsof -i:<port_number>
  ```

- 如果確定該端口應該由該服務使用，可以終止佔用進程：

  ```bash
  kill -9 <PID>
  ```

#### 2. **虛擬環境損壞**

**錯誤訊息：**

```bash
/path/to/venv/bin/pip: bad interpreter: No such file or directory
```

**原因：**

- 虛擬環境內的 Python 解釋器路徑指向了一個已刪除的 Python 版本。

**解決方法：**

- 刪除並重建虛擬環境：

  ```bash
  rm -rf <project_path>/venv
  python3 -m venv <project_path>/venv
  source <project_path>/venv/bin/activate
  pip install -r <project_path>/requirements.txt
  deactivate
  ```

#### 3. **子專案目錄或文件缺失**

**錯誤訊息：**

```bash
Project path <project_path> does not exist
```

**原因：**

- 子專案目錄不存在，可能是專案未完整下載。

**解決方法：**

- 確認子專案目錄是否存在。如果確實缺失，可以重新克隆專案：

  ```bash
  git pull origin main
  ```

#### 4. **依賴安裝失敗**

**錯誤訊息：**

```bash
Failed to install requirements for <project_name>
```

**原因：**

- `requirements.txt` 中的依賴安裝失敗，可能是版本問題或缺少權限。

**解決方法：**

- 手動安裝依賴，並查看具體錯誤：

  ```bash
  source <project_path>/venv/bin/activate
  pip install -r <project_path>/requirements.txt
  ```

#### 5. **服務無法啟動**

**錯誤訊息：**

```bash
Failed to start <project_name> on port <port_number>
```

**原因：**

- 子專案的啟動邏輯出現問題（如主程序文件 `run.py` 缺失）。

**解決方法：**

- 查看專案的 `output.log` 文件以獲取具體錯誤訊息：

  ```bash
  cat <project_path>/output.log
  ```

**如果檔案存在卻出現  can't open file '<project_path>': [Errno 2] No such file or directory**

可以嘗試檢查目錄權限

執行以下命令，確保腳本有權訪問 `<project_path>`：

```bash
ls -ld <project_path>
```

如果權限不足，可以嘗試修改權限：

```bash
chmod +rwx <project_path>
```

---

## 清理緩存和環境

1. **清理 `.pyc` 文件和緩存目錄：**

   ```bash
   find . -name "*.pyc" -delete
   find . -name "__pycache__" -delete
   ```

2. **刪除並重建虛擬環境：**

   ```bash
   rm -rf <project_path>/venv
   python3 -m venv <project_path>/venv
   ```

---

## 腳本功能概述

- 自動檢查子專案目錄是否存在。
- 為每個子專案創建虛擬環境並安裝依賴。
- 在特定端口啟動每個服務，並記錄日誌。
- 如果端口被佔用，跳過該服務並提示用戶檢查。

# Video Script

## 簡介

Video Script 是一個專案，旨在將會議視頻自動轉換為逐字稿並進行優化。它結合了多種工具和技術，支持以下功能：

- 使用 `ffmpeg` 提取音頻。
- 使用 Whisperx 對逐字稿進行語音識別與分段。
- 基於國研院開發的 Llama3-TAIDE 模型進一步優化逐字稿內容。

---

## 環境配置

### **1. 建立 Python 虛擬環境**

確保已安裝 Python 3，然後建立並激活虛擬環境：

```bash
python3 -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows
```

---

### **2. 安裝必要的套件**

在虛擬環境中安裝專案依賴：

```bash
pip install -r requirements.txt
```

---

### **3. 安裝 FFmpeg**

根據操作系統選擇適當的安裝方法：

- **MacOS**：使用 Homebrew

  ```bash
  brew install ffmpeg
  ```

- **Windows**：
  - 從 [FFmpeg 官網](https://ffmpeg.org/download.html) 下載 FFmpeg 的壓縮包。
  - 解壓縮到一個目錄，例如 `C:\Program Files\ffmpeg`。
  - 將 `ffmpeg` 目錄下的 `bin` 目錄添加到你的系統環境變數 PATH 中。
- **Linux**：

  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

---

### **4. 配置 Hugging Face API Token**

1. 確保接受模型使用條款，訪問 [taide/Llama3-TAIDE-LX-8B-Chat-Alpha1 模型頁面](https://huggingface.co/taide/Llama3-TAIDE-LX-8B-Chat-Alpha1)，並接受使用條款。
2. 登錄到 [Hugging Face](https://huggingface.co/settings/tokens)。
3. 選擇 "New token"，類型選擇 "Fine-grained (custom)"。
4. 生成後複製該 token。
5. 點擊 "Edit Access Token Permissions"，在 "Repositories permissions" 裡面搜尋 `taide/Llama3-TAIDE-LX-8B-Chat-Alpha1`，然後勾選 "Read access to contents of selected repos"。
6. 回到本地端，通過 `huggingface-cli login` 貼上先前複製的 token，並選擇 "Add token as git credential? (Y/n)" 回答 "Y"。

### 5. 環境變量配置

為了安全地管理環境變量，例如 Hugging Face API Token，您可以使用 `.env` 文件。

#### 1. 創建 `.env` 文件

在專案目錄中創建一個名為 `.env` 的文件，並添加以下內容：

```plaintext
HUGGINGFACE_API_TOKEN=您的 Hugging Face API Token
```

---

## 專案結構

```plaintext
shared_data/              # 音頻、視頻和逐字稿的存儲
├── videos/               # 下載的視頻文件
├── audios/               # 提取的音頻文件
|
VideoScriptProject/
│
├── app/                      # 核心應用代碼
│   ├── __init__.py           # 初始化 Flask 應用
│   ├── routes.py             # API 路由定義
│   ├── downloader.py         # 視頻下載邏輯
│   ├── audio_extractor.py    # 音頻提取邏輯
│   ├── transcribe.py         # 語音轉文字邏輯
│   ├── optimize.py           # 逐字稿優化邏輯
│   ├── utils.py              # 工具函數
│
│   ├── transcripts/          # 生成的逐字稿
│
├── venv/                     # Python 虛擬環境
│
├── requirements.txt          # 專案依賴
├── run.py                    # 啟動應用
└── readme.md                 # 說明文件
```

---

## 操作步驟

### **1. 啟動應用**

執行以下命令啟動 Flask 應用，提供 API 服務：

```bash
python run.py
```

應用啟動後，可通過 `http://localhost:5001` 訪問 API。

---

### **2. API 使用說明**

#### **API 1: 提取音頻**

- **URL**: `/api/extract_audio`  
- **方法**: `POST`  
- **功能**: 從指定視頻中提取音頻，並保存為 `.wav` 格式。

**請求體**:

```json
{
    "video_id": "12345"
}
```

**範例請求**:

```bash
curl -X POST http://localhost:5001/api/extract_audio \
-H "Content-Type: application/json" \
-d '{"video_id": "12345"}'
```

**回應**:

- 成功:

  ```json
  {
      "message": "提取音頻成功",
      "audio_path": "/path/to/audio/12345.wav"
  }
  ```

- 失敗:

  ```json
  {
      "error": "視頻文件不存在"
  }
  ```

---

#### **API 2: 轉錄音頻**

- **URL**: `/api/transcribe`  
- **方法**: `POST`  
- **功能**: 將音頻文件轉錄為逐字稿，並保存為 `.json` 格式。

**請求體**:

```json
{
    "video_id": "12345"
}
```

**範例請求**:

```bash
curl -X POST http://localhost:5001/api/transcribe \
-H "Content-Type: application/json" \
-d '{"video_id": "12345"}'
```

**回應**:

- 成功:

  ```json
  {
      "message": "音頻轉文字成功",
      "transcript_path": "/path/to/transcripts/12345.json"
  }
  ```

- 失敗:

  ```json
  {
      "error": "音頻文件不存在"
  }
  ```

---

### **3. 任務流程**

#### **下載視頻**

```bash
python run.py download
```

#### **提取音頻**

```bash
python run.py extract
```

#### **轉錄逐字稿**

```bash
python run.py transcribe
```

#### **優化逐字稿**

```bash
python run.py optimize
```

---

## 貢獻指南

本專案開放源碼，並遵循 [CC0](https://ti-wb.github.io/creativecommon-tw/cc0.html) 公眾領域貢獻宣告。歡迎透過 GitHub 提交 Issue 或 PR 參與貢獻！

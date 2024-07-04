# Video Script

## 簡介

這個專案提供了一個基於 Flask 的網頁應用，用於下載會議視頻並將其轉換為逐字稿。通過使用 `ffmpeg` 提取音頻，利用 Whisperx 切分不同發言人的逐字稿，再使用財團法人國家實驗研究院（以下稱「國研院」）開發並建置的 Llama3-TAIDE 模型來優化逐字稿。

## 環境配置

### 1. 建立 Python 虛擬環境

確保你已安裝 Python 3。然後，使用以下命令來建立虛擬環境並啟動它：

```bash
python3 -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows
```

### 2. 安裝必要的套件

在虛擬環境中安裝所需的 Python 套件：

```bash
pip install -r requirements.txt
```

### 3. 安裝 FFmpeg

根據你的操作系統安裝 FFmpeg：

- **MacOS**：

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

### 4. 生成 Hugging Face API Token

1. 登錄到 [Hugging Face](https://huggingface.co/settings/tokens)。
2. 選擇 "New token"，類型選擇 "Fine-grained (custom)"。
3. 生成後複製該 token。
4. 點擊 "Edit Access Token Permissions"，在 "Repositories permissions" 裡面搜尋 `taide/Llama3-TAIDE-LX-8B-Chat-Alpha1`，然後勾選 "Read access to contents of selected repos"。
5. 回到本地端，通過 `huggingface-cli login` 貼上先前複製的 token，並選擇 "Add token as git credential? (Y/n)" 回答 "Y"。

### 5. 環境變量配置

為了安全地管理環境變量，例如 Hugging Face API Token，您可以使用 `.env` 文件。

#### 1. 創建 `.env` 文件

在專案目錄中創建一個名為 `.env` 的文件，並添加以下內容：

```bash
HUGGINGFACE_API_TOKEN=您的 Hugging Face API Token
```

#### 2. 加載 `.env` 文件

在代碼中使用 `python-dotenv` 庫來加載 `.env` 文件中的環境變量。

在您的代碼中添加以下內容：

```python
from dotenv import load_dotenv
import os

# 加載 .env 文件
load_dotenv()

# 獲取 API Token
token = os.getenv("HUGGINGFACE_API_TOKEN")
```

## 項目結構

```plaintext
TranscriptionProject/
│
├── app/
│   ├── __init__.py         # 初始化 Flask 應用
│   ├── routes.py           # 定義 API 路由
│   ├── downloader.py       # 視頻下載邏輯
│   ├── audio_extractor.py  # 音頻提取邏輯
│   ├── transcribe.py       # 語音轉文字邏輯
│   ├── optimize.py         # 逐字稿優化邏輯
│   ├── utils.py            # 工具函數
│
├── downloads/              # 下載的視頻
│
├── audios/                 # 轉換的音頻
│
├── scripts/                # 生成的逐字稿
│
├── venv/                   # 虛擬環境
│
├── requirements.txt        # 專案依賴
│
├── run.py                  # 啟動應用
├── readme.md               # 專案說明文件
│
└── .gitignore              # Git 忽略文件
```

## 啟動應用

使用以下命令啟動 Flask 應用：

```bash
python run.py
```

## 使用說明

這個應用提供了一個 API 來下載會議視頻、轉換音頻並生成逐字稿。

### 1. 轉換視頻為逐字稿

**URL**: `/api/transcribe`

**方法**: `POST`

**請求體**:

```json
{
    "url": "https://ivod.ly.gov.tw/Play/Clip/300K/154397"
}
```

**範例**:

```sh
curl -X POST http://localhost:5000/api/transcribe -H "Content-Type: application/json" -d '{"url": "https://ivod.ly.gov.tw/Play/Clip/300K/154397"}'
```

**回應**:

```json
{
    "message": "轉換成功"
}
```

### API 邏輯

當 API 被調用時，會執行以下步驟：

1. 檢查視頻是否已經存在於 `downloads` 目錄中。
2. 如果視頻不存在，從提供的 URL 下載視頻。
3. 檢查音頻是否已經存在於 `audios` 目錄中。
4. 如果音頻不存在，從視頻中提取音頻並保存。
5. 檢查逐字稿是否已經存在於 `scripts` 目錄中。
6. 如果逐字稿不存在，轉錄音頻並保存逐字稿。
7. 返回轉換成功的消息。

感謝您的指正，以下是整合了 `pip install --no-user -r requirements.txt` 命令的完整步驟，用於在 TWCC 容器中配置並運行您的專案。

## 在 TWCC 容器中配置並運行專案

### 1. 更新包管理器和安裝必要的工具

首先，確保管理器是最新的，並安裝 `python3-venv` 和 `wget`：

```bash
sudo apt-get update
sudo apt-get install -y python3-venv wget
```

### 2. 創建虛擬環境

創建並激活 Python 虛擬環境：

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝依賴

在虛擬環境中安裝所需的 Python 包：

#### 確保 include-system-site-packages 設置為 false

首先，檢查並確保 venv/pyvenv.cfg 文件中的 include-system-site-packages 設置為 false，以確保虛擬環境不使用系統的 site-packages：

```bash
Copy code
nano venv/pyvenv.cfg
```

確保文件中的 include-system-site-packages 設置為 false：

```plaintext
include-system-site-packages = false
```

保存更改並退出編輯器。

```bash
pip install --no-user --upgrade pip
pip install --no-user -r requirements.txt
```

### 4. 安裝 Google Chrome 和 ChromeDriver

創建一個臨時目錄來下載並安裝 Google Chrome：

```bash
mkdir -p ~/tmp_download && cd ~/tmp_download

# 下載 Google Chrome 安裝包
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

# 修改文件權限
chmod 644 google-chrome-stable_current_amd64.deb

# 安裝 Google Chrome
sudo apt install ./google-chrome-stable_current_amd64.deb

# 清理臨時目錄
cd ~
rm -rf ~/tmp_download
```

### 5. 安裝 ChromeDriver 和其他必要依賴

在虛擬環境中安裝 `selenium` 和 `webdriver-manager`，並確保 ChromeDriver 能夠自動下載和安裝：

```bash
pip install selenium webdriver-manager
```

### 7. 確保 FFmpeg 安裝正確

安裝 FFmpeg：

```bash
sudo apt-get install -y ffmpeg
```

### 8. 運行應用

激活虛擬環境並運行您的應用：

```bash
source venv/bin/activate
python run.py download
```

## 開發與貢獻

鄉民玩 AI 系列基於取之於鄉民，用之於鄉民的精神，全系列進行 [CC0](https://ti-wb.github.io/creativecommon-tw/cc0.html) 「公眾領域貢獻宣告 」，歡迎所有讀者自由使用，也歡迎透過 GitHub 與我們一同協作，或是提交 Issues 給予我們建議。

感謝您使用 Video Script！

# Event Summarizer

## 簡介

這個專案提供了將會議逐字稿用財團法人國家實驗研究院（以下稱「國研院」）開發並建置的 Llama3-TAIDE 模型來總結。

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

### 3. 生成 Hugging Face API Token

1. 確保接受模型使用條款，訪問 [taide/Llama3-TAIDE-LX-8B-Chat-Alpha1 模型頁面](https://huggingface.co/taide/Llama3-TAIDE-LX-8B-Chat-Alpha1)，並接受使用條款。
2. 登錄到 [Hugging Face](https://huggingface.co/settings/tokens)。
3. 選擇 "New token"，類型選擇 "Fine-grained (custom)"。
4. 生成後複製該 token。
5. 點擊 "Edit Access Token Permissions"，在 "Repositories permissions" 裡面搜尋 `taide/Llama3-TAIDE-LX-8B-Chat-Alpha1`，然後勾選 "Read access to contents of selected repos"。
6. 回到本地端，通過 `huggingface-cli login` 貼上先前複製的 token，並選擇 "Add token as git credential? (Y/n)" 回答 "Y"。

### 4. 環境變量配置

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
│   ├── summarize.py        # 總結逐字稿邏輯
│   └── utils.py            # 工具函數
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

要啟動 Flask 應用，請按照以下步驟進行：

### 1. 準備工作

確保您已經完成了環境配置部分的所有步驟，包括建立 Python 虛擬環境、安裝必要的套件、生成 Hugging Face API Token 以及配置環境變量。

### 2. 總結逐字稿

使用 Llama3-TAIDE 模型來優化生成的逐字稿，請運行以下命令：

```bash
python run.py summarize
```

這將優化逐字稿並將結果保存到 `scripts` 目錄中。

### 3. 啟動 Flask 應用

如果您希望啟動完整的 Flask 應用來提供 API 服務，可以運行以下命令：

```bash
python run.py
```

這將啟動 Flask 應用，您可以通過 `http://localhost:5000` 訪問應用並使用其提供的 API。


## 在 TWCC 容器中配置並運行專案

### 1. 更新包管理器和安裝必要的工具

首先，確保管理器是最新的，並安裝 `python3-venv` 和 `wget`：

```bash
sudo apt-get update
sudo apt-get install -y python3-venv wget
```

### 3. 創建虛擬環境

創建並激活 Python 虛擬環境：

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. 安裝依賴

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

### 5. 運行應用

激活虛擬環境並運行您的應用：

```bash
source venv/bin/activate
python run.py summarize
```

## 開發與貢獻

鄉民玩 AI 系列基於取之於鄉民，用之於鄉民的精神，全系列進行 [CC0](https://ti-wb.github.io/creativecommon-tw/cc0.html) 「公眾領域貢獻宣告 」，歡迎所有讀者自由使用，也歡迎透過 GitHub 與我們一同協作，或是提交 Issues 給予我們建議。

感謝您使用 Event Summarizer！

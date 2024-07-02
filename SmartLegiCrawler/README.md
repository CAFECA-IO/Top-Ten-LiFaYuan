# Smart Legi Crawler

Smart Legi Crawler 是一個網頁爬蟲專案，設計用於從台灣立法院網站抓取並處理立法會議的信息。此專案使用 Flask 作為後端框架，並使用 Selenium 進行網頁爬蟲，透過 BeautifulSoup 解析網頁內容，以及 FFmpeg 進行視頻下載。提供 API 來查詢和下載會議視頻。

## 專案結構

```bash
TaiwanLegislativeVideoDownloader/
│
├── app/
│   ├── __init__.py       # 初始化 Flask 應用
│   ├── main.py           # 主程序入口
│   ├── routes.py         # 定義 API 路由
│   ├── scraper.py        # 網頁爬取邏輯
│   ├── downloader.py     # 視頻下載邏輯
│   ├── utils.py          # 工具函數
│
├── venv/                 # 虛擬環境
│
├── requirements.txt      # 專案依賴
│
├── run.py                # 啟動應用
└── readme.md             # 專案說明文件
```

## 安裝與使用

### 1. 克隆此專案

```bash
Copy code
git clone https://github.com/CAFECA-IO/Top-Ten-LiFaYuan.git
cd Top-Ten-LiFaYuan/SmartLegiCrawler
```

### 2. 環境準備

確保您的系統已安裝 Python 3 以及 pip。接著，創建並啟動虛擬環境：

```bash
python3 -m venv venv
source venv/bin/activate  # 對於 Windows 用戶：venv\Scripts\activate
```

### 3. 安裝依賴

安裝專案所需的 Python 套件：

```bash
pip install -r requirements.txt
```

### 4. 配置環境

下載並安裝 ChromeDriver。可以使用 `webdriver_manager` 自動管理 ChromeDriver，無需手動下載。

### 5. 啟動應用

在專案根目錄下運行：

```bash
python run.py
```

### 6. 使用 API

#### 查詢會議視頻

```http
GET /api/meetings
```

**參數：**

- `start_date` (optional): 查詢起始日期，格式 `YYYY-MM-DD`
- `end_date` (optional): 查詢結束日期，格式 `YYYY-MM-DD`
- `page` (optional): 查詢頁數，預設為 1
- `q` (optional): 搜尋關鍵字
- `committee` (optional): 查詢特定委員會
- `limit` (optional): 每次查詢的最大會議數量，預設為 100

**示例：**

```bash
curl "http://localhost:5000/api/meetings?start_date=2024/06/01&end_date=2024/07/01&limit=50"
```

#### 會議視頻詳情

```http
GET /api/meetings/<meeting_id>
```

**參數：**

- `meeting_id`: 會議 ID

**示例：**

```bash
curl "http://localhost:5000/api/meetings/12345"
```

#### 下載視頻

```http
POST /api/download
```

**參數：**

- `url`: 視頻頁面 URL

**示例：**

```bash
curl -X POST http://127.0.0.1:5000/api/download -H "Content-Type: application/json" -d '{"url": "https://ivod.ly.gov.tw/Play/..."}'
```

## 開發與貢獻

鄉民玩 AI 系列基於取之於鄉民，用之於鄉民的精神，全系列進行 [CC0](https://ti-wb.github.io/creativecommon-tw/cc0.html) 「公眾領域貢獻宣告 」，歡迎所有讀者自由使用，也歡迎透過 GitHub 與我們一同協作，或是提交 Issues 給予我們建議。

感謝您使用 Smart Legi Crawler！

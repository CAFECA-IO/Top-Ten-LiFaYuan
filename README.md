# Top-Ten-LiFaYuan
臺灣立法院提供了豐富的公開資料，包括會議錄影、立法委員的簡介、各項議案的詳細狀態、預算和決算報告，以及各類委員會的工作情況。這些資訊雖然全面，但由於其龐大的資料量，公眾很難即時、客觀、準確地獲取和理解所有資訊。因此我們打算藉由網路爬蟲技術定期且即時收集所有的內容，透過 AI 模型識讀內容並進行摘要。同時針對內容設計議題重要性、社會影響力、知識教育性、改革創造性、特殊娛樂性等五大指標，由 AI 模型進行評分，最後排名選出關鍵的立法院十大好球，幫助公眾快速掌握重要且正確的資訊。

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
│
├── SmartLegiCrawler/
│   ├── app  
|   |    ├── __init__.py         # 初始化 Flask 應用
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
│
│
├── VideoScript/
│   ├── app  
|   |    ├── __init__.py         # 初始化 Flask 應用
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
│
│
├── EventSummarizer/
│   ├── app  
|   |    ├── __init__.py         # 初始化 Flask 應用
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
├── run.py                      # 啟動應用
│ 
├── readme.md                   # 專案說明文件
│ 
└── .gitignore                  # Git 忽略文件
```

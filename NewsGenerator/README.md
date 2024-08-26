# NewsGenerator

## 專案簡介

**NewsGenerator** 是一個基於多種生成式 AI 技術的自動化新聞播報系統。該系統利用 LLaMA、FLUX.1、AnimateDiff、CosyVoice 和 Suno 等工具，從新聞摘要生成完整的新聞播報影片。專案旨在自動化生成新聞稿、圖片、動畫、語音和背景音樂，並最終合成一個完整的視頻。

## 功能概述

- **生成新聞稿**：利用 LLaMA 模型從新聞摘要生成詳細的新聞稿。
- **生成分鏡稿圖片**：使用 FLUX.1 模型生成新聞播報的分鏡稿圖片。
- **生成主播圖片**：利用 FLUX.1 模型生成虛擬新聞主播的圖片。
- **生成動畫**：通過 AnimateDiff 模型生成動畫，包括整體動畫和基於主播的動畫。
- **生成語音**：使用 CosyVoice 模型生成對應新聞稿的語音。
- **生成背景音樂**：利用 Suno 的 Bark 模型生成新聞背景音樂。
- **合成影片**：使用 FFmpeg 將所有生成的內容合成為最終的新聞播報影片。

## 系統需求

- Python 3.8 或更高版本
- `conda` 或其他虛擬環境管理工具
- 一個具備 GPU 支持的運行環境（建議）

## 安裝指南

1. **克隆專案**

   首先，將專案克隆到本地：

   ```bash
   git clone https://github.com/yourusername/NewsGenerator.git
   cd NewsGenerator
   ```

2. **建立並啟動虛擬環境**

   使用 `conda` 建立並啟動一個新的虛擬環境：

   ```bash
   conda create -n newsgenerator python=3.8
   conda activate newsgenerator
   ```

   2.1 **刪除虛擬環境**

   ```bash
   conda deactivate
   conda remove --name newsgenerator --all     
   ```

3. **安裝依賴項**

   安裝專案所需的所有 Python 庫：

   ```bash
   <!-- conda install pytorch torchvision -c pytorch -->
   pip install -r requirements.txt
   ```

   卸載所有安裝包:

   ```bash
   pip freeze | xargs pip uninstall -y
   ```

### 4. 在 `NewsGenerator` 專案中克隆 CosyVoice

在 `NewsGenerator` 專案目錄中克隆 CosyVoice 倉庫：

```bash
git clone --recursive https://github.com/FunAudioLLM/CosyVoice.git
```

這將在 `NewsGenerator` 目錄下創建一個 `CosyVoice` 文件夾，包含了 CosyVoice 的所有源代碼和子模塊。

### 5. 初始化和配置 CosyVoice

進入 `CosyVoice` 目錄，並按照以下步驟初始化和配置 CosyVoice：

```bash
cd CosyVoice
git submodule update --init --recursive
conda install -y -c conda-forge pynini==2.1.5
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com
```

這些命令將會：

- 初始化並更新 CosyVoice 的子模塊。
- 安裝 `pynini` 作為必須的依賴項。
- 安裝 `CosyVoice` 所需的其他 Python 庫。

### 6. 下載和配置 CosyVoice 的預訓練模型

使用 ModelScope 下載 CosyVoice 的預訓練模型。您可以在 `NewsGenerator` 的根目錄下創建一個新的 Python 腳本（例如 `download_models.py`），並運行該腳本來下載模型：

```bash
cd ../  # 返回到 NewsGenerator 目錄
touch download_models.py
```

將以下代碼寫入 `download_models.py` 文件中：

```python
from modelscope import snapshot_download

# 下載 CosyVoice 預訓練模型
snapshot_download('iic/CosyVoice-300M', local_dir='CosyVoice/pretrained_models/CosyVoice-300M')
snapshot_download('iic/CosyVoice-300M-SFT', local_dir='CosyVoice/pretrained_models/CosyVoice-300M-SFT')
snapshot_download('iic/CosyVoice-300M-Instruct', local_dir='CosyVoice/pretrained_models/CosyVoice-300M-Instruct')
snapshot_download('iic/CosyVoice-ttsfrd', local_dir='CosyVoice/pretrained_models/CosyVoice-ttsfrd')
```

然後運行這個腳本來下載模型：

```bash
python download_models.py
```

這將把模型下載到 `CosyVoice` 目錄下的 `pretrained_models` 文件夾中。

### 7. 在 NewsGenerator 中使用 CosyVoice

現在就可以在 `NewsGenerator` 中的代碼直接引用 `CosyVoice`，並使用已下載的模型來進行語音生成。

## 使用方法

1. **準備新聞摘要**

   編輯 `main.py` 文件中的 `summary` 變數，將您的新聞摘要填入該變數：

   ```python
   summary = """
   1. 使用者向總統和相關部門官員提出關於 Peer-to-Peer(P2P) 監管問題的擔憂，尤其是在缺乏法律約束和自我監管下的非法活動。
   2. 官員承認在目前的法律框架下，對於 P2P 平臺的管理存在困難，但強調正在研究各種選項，包括成立行業協會和逐步實施分級管理。
   3. 用戶表達了對政府在面對金融科技快速發展時，是否具備明確的戰略和行動計劃的疑慮。
   4. 金融監督管理委員會（FSC）表示，他們正在努力平衡創新和風險管理，同時呼籲企業遵守相關法律法規。
   5. 會上還提及了房地產市場泡沫和銀行信貸比例過高的問題，官方承諾將與中央銀行協調，採取相應措施防止金融危機。
   6. 與會者同意進一步研究並追蹤相關議題，以促進金融業的健康發展。
   """
   ```

2. **生成新聞播報影片**

   運行 `main.py` 生成新聞播報影片：

   ```bash
   python main.py
   ```

   生成的影片將會被保存到 `data/output/final_news_video.mp4`。

## 開發與貢獻

鄉民玩 AI 系列基於取之於鄉民，用之於鄉民的精神，全系列進行 [CC0](https://ti-wb.github.io/creativecommon-tw/cc0.html) 「公眾領域貢獻宣告 」，歡迎所有讀者自由使用，也歡迎透過 GitHub 與我們一同協作，或是提交 Issues 給予我們建議。

感謝您使用 NewsGenerator！

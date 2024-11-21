# ComfyUI Workflow Generator

這個服務允許使用者上傳照片，並根據指定的參數生成頭像圖像、影片和聲音。使用者可以先上傳圖片，之後生成頭像。此外，還可以使用 ComfyUI 的 prompt queue 生成可用的 prompt 來進行自定義的圖像生成。

## Features

- 上傳圖片
- 根據上傳的圖片生成頭像
- 根據描述生成影片
- 根據文字生成聲音
- 支援性別選項（男性、女性、中性）
- 支援不同解析度的圖像生成
- 使用 ComfyUI prompt queue 生成可用的 prompt

## Prerequisites

- Python 3.x
- 安裝所需依賴庫
  - `pip install -r requirements.txt`

## Getting Started

### 1. 啟動服務

首先，請確保已經配置好所需的依賴，然後執行以下命令來啟動 Flask 服務：

```bash
python app.py
```

這將啟動後端服務，並接受 RESTful API 請求。

### 2. 上傳圖片

在生成頭像之前，你必須先上傳圖片。可以通過以下 API 發送請求：

**API 路徑：**

```api
POST /upload_image
```

**參數說明：**

- `file`: 使用者上傳的圖片文件

**範例請求：**

```bash
curl -X POST http://127.0.0.1:5000/upload-image \
-F "image=@/path/to/your/image.jpg"
```

該請求會將圖片上傳到服務器，並返回圖片的名稱。

### 3. 生成頭像

上傳圖片後，你可以通過 `generate-avatar-by-image` API 生成頭像。

**API 路徑：**

```api
POST /generate-avatar-by-image
```

**參數說明：**

- `imageName`: 上傳圖片後返回的圖片名稱
- `gender`: 頭像生成的性別選項，值可以是 `male`, `female`, `neutral`，默認為 `neutral`
- `width`: 頭像寬度（預設為 512）
- `height`: 頭像高度（預設為 512）

**範例請求：**

```bash
curl -X POST "http://127.0.0.1:5000/generate-avatar-by-image" \
  -H "Content-Type: application/json" \
  -d '{
    "imageName": "your_uploaded_image.jpg",
    "gender": "female",
    "width": 1024,
    "height": 1024
  }'
```

### 4. 生成影片

**API 路徑：**

```api
POST /generate-video
```

**參數說明：**

- `video_description`: 描述影片內容的 JSON 字符串，描述將會影響影片的不同時間點的場景

**範例請求：**

```bash
curl -X POST http://localhost:5000/generate-video \
-H "Content-Type: application/json" \
-d '{
    "video_description": {
        "0": "A happy panda starts spinning in circles, full of energy.",
        "6": "After a few spins, the panda jumps up with excitement, still smiling.",
        "9": "Landing gracefully, the panda continues to spin happily in place."
    }
}'
```

### 5. 生成聲音

**API 路徑：**

```api
POST /generate-vocal
```

**參數說明：**

- `text`: 要生成的聲音的文字內容
- `speed`: 聲音的語速，默認為 1.5
- `inference_mode`: 推理模式，預設為 `0`，可選值有：'预训练音色', '3s极速复刻', '跨语种复刻', '自然语言控制'
- `spf_spk`: 語音風格選項，預設為 `0`，可選值有：'中文女', '中文男', '日语男', '粤语女', '英文女', '英文男', '韩语女'

**範例請求：**

```bash
curl -X POST http://localhost:5000/generate-vocal \
-H "Content-Type: application/json" \
-d '{
    "text": "2024年，全球在多個領域發生了影響深遠的重大事件，涵蓋了政治、氣候、國際安全和經濟發展。選舉年與民主挑戰，今年有超過40億選民在76個國家參與選舉，這些選舉不僅影響到本國的政治前景，也對全球民主體系的未來至關重要。在美國和印度等主要民主國家，年輕選民和女性的投票意向被認為將決定選舉結果，而極右和極左勢力的崛起成為值得關注的現象。阿根廷新任總統哈維爾·米萊的勝選，以及荷蘭的極右領袖格特·威爾德斯在選舉中的成功，突顯了全球範圍內政治極化的加劇。氣候變化與國際應對，全球氣候變化問題在2024年達到新的高度，11月的COP29會議在亞塞拜然的巴庫召開，成為全球應對氣候危機的重要里程碑。會議將專注於如何推動化石燃料的逐步淘汰，並為最脆弱國家提供財政支持。氣候基金在此次會議上再度成為焦點，全球各國將共同商討如何確保資金能夠有效支持應對氣候變化的措施。國際安全與衝突升級，2024年國際安全局勢進一步緊張，烏克蘭戰爭持續延燒，俄羅斯的軍事行動引發了全球範圍內的安全擔憂。加沙地區的以巴衝突再度激化，而蘇丹的內戰已造成數十萬人流離失所。國際社會對這些衝突的外交解決方案進展緩慢，衝突各方的軍事行動加劇了全球的不穩定局勢。全球峰會與多邊合作，2024年舉行的多個國際峰會，成為各國應對全球挑戰的關鍵平台。北約在美國華盛頓舉行的峰會慶祝了聯盟成立75週年，並討論了如何應對俄烏戰爭及中國崛起帶來的挑戰。同時，聯合國「未來峰會」集中探討如何加強數字技術管理和推動全球治理改革，為解決21世紀的新興挑戰提供框架。\n\n這些事件顯示，2024年是全球政治和經濟發展的重要轉折點。各國如何應對這些挑戰，將對未來的全球格局產生深遠影響。",
    "speed": 1.5,
    "inference_mode": 0,
    "spf_spk": 0
}'
```

### 6. 使用 ComfyUI Prompt Queue

使用 ComfyUI 完成工作流程後，你可以使用 prompt queue 來生成並發送 prompt。要找到生成的 prompt，請按以下步驟操作：

#### 步驟

1. 打開 ComfyUI 並開始構建工作流程。
2. 完成工作流程後，透過 ComfyUI 的介面將點 queue prompt。
3. 使用瀏覽器的開發者工具（Web Developer Tool）來監控發送的請求。
   - 在 Chrome 或 Firefox 中，按 `F12` 打開開發者工具，然後切換到 "Network" 頁籤。
   - 找到發送到 `/prompt` API 的請求。
4. 點擊該請求，然後查看 `Request Payload`，即請求中的 `body` 部分。
5. 該 `body` 內容就是可以直接用來進行生成圖像的 prompt。

#### 提取和使用 `prompt`

以下是範例提取的 `prompt` 結構：

```json
{
  "1": {
    "inputs": { "ckpt_name": "dreamshaper_8.safetensors" },
    "class_type": "CheckpointLoaderSimple"
  },
  "2": {
    "inputs": {
      "text": "soft lighting, gentle shadows, pastel color palette, slight 3D effect on the face and hair, delicate facial features, blurred grey background,",
      "clip": ["1", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "3": {
    "inputs": {
      "text": "ugly, tiling, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad anatomy, watermark, signature, cut off, low contrast, underexposed, overexposed, bad art, beginner, amateur, distorted face, animal-human hybrid, anthropomorphic, creature with human features, chimera, mixed species, human-animal mutation, deformed eyes, extra eyes, poorly drawn eyes, distorted eyes, asymmetrical eyes, misaligned eyes",
      "clip": ["1", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "4": {
    "inputs": {
      "seed": 0,
      "steps": 70,
      "cfg": 6,
      "sampler_name": "dpmpp_2m",
      "scheduler": "karras",
      "denoise": 0.6,
      "model": ["1", 0],
      "positive": ["23", 0],
      "negative": ["3", 0],
      "latent_image": ["26", 0]
    },
    "class_type": "KSampler"
  },
  "5": {
    "inputs": { "width": 512, "height": 512, "batch_size": 1 },
    "class_type": "EmptyLatentImage"
  },
  "7": { "inputs": { "images": ["15", 0] }, "class_type": "PreviewImage" },
  "15": {
    "inputs": { "samples": ["4", 0], "vae": ["1", 2] },
    "class_type": "VAEDecode"
  },
  "22": {
    "inputs": {
      "text": "best quality, masterpiece, avatar, facing forward, looking at the camera, symmetrical face, relaxed body posture,",
      "clip": ["1", 1]
    },
    "class_type": "CLIPTextEncode"
  },
  "23": {
    "inputs": { "conditioning1": ["22", 0], "conditioning2": ["2", 0] },
    "class_type": "ImpactConcatConditionings"
  },
  "25": {
    "inputs": { "image": "profile_emily.png", "upload": "image" },
    "class_type": "LoadImage"
  },
  "26": {
    "inputs": { "pixels": ["25", 0], "vae": ["1", 2] },
    "class_type": "VAEEncode"
  }
}
```

將這些 prompt 作為生成圖像的內容發送至 ComfyUI 或其他圖像生成系統。

### 7. 圖片儲存

生成的圖像將被保存到本地資料夾 `./generated_avatar`。你可以在 ComfyUIClient 類的 `save_images` 方法中修改圖片儲存位置。若指定了 `upload_url`，則會自動將圖片上傳到該 URL。

## 文件說明

- `app.py`: 主應用文件，包含上傳圖片與生成頭像的 API 實現邏輯。
- `comfyui_client.py`: 與 ComfyUI 進行交互，負責圖像生成並處理圖片的保存與上傳。

## 錯誤處理

- 如果上傳過程中出現錯誤（如文件無效或解析度不符合規範），服務會返回相應的錯誤信息。
- 圖片解析與儲存失敗的錯誤會打印在服務日誌中。

## 結語

這個系統允許用戶上傳圖片並根據參數生成頭像，同時也可以靈活使用 ComfyUI 的 prompt queue 來生成並提取 prompt。你可以根據需要調整生成圖像的參數與儲存方式。

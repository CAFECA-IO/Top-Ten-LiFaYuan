# Avatar Generation Service

這個服務允許使用者上傳照片，並根據指定的參數生成頭像圖像。使用者需要先上傳圖片，之後再生成頭像圖像。此外，你可以使用 ComfyUI 的 prompt queue 並通過 web 開發者工具來獲取工作流程生成的 prompt。

## Features

- 上傳圖片
- 根據上傳的圖片生成頭像
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

### 4. 使用 ComfyUI Prompt Queue

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

### 5. 圖片儲存

生成的圖像將被保存到本地資料夾 `./generated_avatar`。你可以在 ComfyUIClient 類的 `save_images` 方法中修改圖片儲存位置。若指定了 `upload_url`，則會自動將圖片上傳到該 URL。

## 文件說明

- `app.py`: 主應用文件，包含上傳圖片與生成頭像的 API 實現邏輯。
- `comfyui_client.py`: 與 ComfyUI 進行交互，負責圖像生成並處理圖片的保存與上傳。

## 錯誤處理

- 如果上傳過程中出現錯誤（如文件無效或解析度不符合規範），服務會返回相應的錯誤信息。
- 圖片解析與儲存失敗的錯誤會打印在服務日誌中。

## 結語

這個系統允許用戶上傳圖片並根據參數生成頭像，同時也可以靈活使用 ComfyUI 的 prompt queue 來生成並提取 prompt。你可以根據需要調整生成圖像的參數與儲存方式。

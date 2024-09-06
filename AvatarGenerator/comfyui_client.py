import os
import websocket
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io
import mimetypes

class ComfyUIClient:
    def __init__(self, server_address):
        """初始化 ComfyUI 客戶端"""
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

    def load_prompt(self, filepath):
        """從指定路徑加載 prompt 檔案"""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def queue_prompt(self, prompt):
        """將生成任務排隊"""
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
        print(f"提交生成任務: http://{self.server_address}/prompt")
        return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        """根據檔名、子資料夾及類型獲取生成的圖片"""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def get_history(self, prompt_id):
        """通過 prompt_id 獲取生成歷史"""
        with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
            return json.loads(response.read())

    def ensure_directory(self, directory):
        """確保指定的資料夾存在，若不存在則創建"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def get_images(self, prompt):
        """根據 prompt 通過 WebSocket 獲取生成的圖片"""
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")
        print(f"Connected to ws://{self.server_address}/ws?clientId={self.client_id}")
        prompt_id = self.queue_prompt(prompt)['prompt_id']
        print(f"Prompt ID: {prompt_id}")
        output_images = {}

        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing' and message['data']['node'] is None:
                    break  # 任務執行完成

        history = self.get_history(prompt_id)[prompt_id]
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            images_output = []
            if 'images' in node_output:
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

        return output_images
    
    def upload_image(self, file_path, file_name):
        """
        將圖片上傳。
        
        參數:
        - file_path: 本地圖片文件的路徑
        - file_name: 上傳時使用的文件名
        """
        try:
            # 確定文件的 MIME 類型，如果找不到則默認為 'application/octet-stream'
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            # 打開圖片文件
            with open(file_path, 'rb') as image_file:
                # 讀取文件內容
                image_data = image_file.read()

            # 構建 multipart form-data 的邊界
            boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
            
            # 構建 multipart form-data 數據
            data = (
                f'--{boundary}\r\n'
                f'Content-Disposition: form-data; name="image"; filename="{file_name}"\r\n'
                f'Content-Type: {mime_type}\r\n\r\n'
                f'{image_data.decode("ISO-8859-1")}\r\n'
                f'--{boundary}--\r\n'
            ).encode('ISO-8859-1')

            # 構建請求頭
            headers = {
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'Content-Length': str(len(data)),
            }

            # 構建請求對象
            request = urllib.request.Request(f"http://{self.server_address}/upload/image", data=data, headers=headers, method='POST')

            # 發送請求並獲取響應
            with urllib.request.urlopen(request) as response:
                response_data = response.read().decode('utf-8')
                if response.status == 200:
                    print("圖片上傳成功!")
                    return response_data
                else:
                    print(f"上傳圖片失敗，狀態碼: {response.status}")
                    return None

        except Exception as e:
            print(f"上傳圖片時發生錯誤: {e}")
            return None

    def save_images(self, images, output_dir='./generated_avatar', upload_url=None):
        """
        將生成的圖片保存到指定資料夾，並選擇性地上傳到指定的 API。
        
        參數:
        - images: 生成的圖像數據
        - output_dir: 保存圖片的本地目錄
        - upload_url: （可選）圖片上傳的 API URL
        """
        self.ensure_directory(output_dir)
    
        for node_id, image_data_list in images.items():
            for idx, image_data in enumerate(image_data_list):
                random_id = str(uuid.uuid4())
                output_filename = os.path.join(output_dir, f"avatar_{node_id}_{random_id}_{idx}.png")

                try:
                    # 將圖片保存到本地
                    image = Image.open(io.BytesIO(image_data))
                    image.save(output_filename, 'PNG')
                    print(f"圖片已保存到 {output_filename}")

                    # 如果提供了 upload_url，則上傳圖片
                    if upload_url:
                        self.upload_image(upload_url, output_filename, f"avatar_{random_id}_{idx}.png")

                except Exception as e:
                    print(f"保存圖片失敗: {e}")

import os
import websocket
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io

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
        prompt_id = self.queue_prompt(prompt)['prompt_id']
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
        
    def save_images(self, images, output_dir='./generated_avatar'):
        """將生成的圖片保存到指定資料夾"""
        self.ensure_directory(output_dir)
    
        for node_id, image_data_list in images.items():
            for idx, image_data in enumerate(image_data_list):
                random_id = str(uuid.uuid4())
                output_filename = os.path.join(output_dir, f"avatar_{node_id}_{random_id}_{idx}.png")

            try:
                image = Image.open(io.BytesIO(image_data))
                image.save(output_filename, 'PNG')
                print(f"圖片已保存到 {output_filename}")
            except Exception as e:
                print(f"保存圖片失敗: {e}")
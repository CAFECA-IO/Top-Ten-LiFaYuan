import os
import websocket
import uuid
import json
import urllib.request
import urllib.parse
from PIL import Image
import io
import mimetypes
from flask import jsonify
import logging

# 設置日誌格式和級別
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ComfyUIClient:
    def __init__(self, server_address):
        """初始化 ComfyUI 客戶端"""
        self.server_address = server_address
        self.client_id = str(uuid.uuid4())

    def get_video(self, video_description, frame_rate=8, retry_attempts=3):
        """
        使用 WebSocket 發送生成影片的請求，並根據 promptId 獲取歷史結果下載影片。
        參數:
        - video_description: 用戶提供的動畫描述，替代 workflow 中的預設描述。
        - frame_rate: 影片的幀率。
        - retry_attempts: 最大重試次數。

        返回:
        - 影片的位元資料（bytes），若失敗則返回 None。
        """
        try:
            attempt = 1
            workflow = self._load_workflow('./workflows/prompt_to_video.json')
            
            video_description_str = ""
            for key, value in video_description.items():
                video_description_str += f"\"{key}\" :\"{value}\",\n"
            workflow["8"]["inputs"]["text"] = video_description_str.strip() # 動態替換動畫描述
            # workflow["7"]["inputs"]["frame_rate"] = frame_rate  # 更新幀率
            
            """根據 prompt 通過 WebSocket 獲取生成的圖片"""
            ws = self._create_websocket()  # 手動創建 WebSocket 連接
            
            prompt_id = self.queue_prompt(workflow)['prompt_id']
            logging.info(f"Prompt ID: {prompt_id}")

            # 等待影片生成完成
            self._wait_for_completion(ws)
            video_file = self._get_output_video(prompt_id)

            # 如果影片生成成功，返回影片文件
            if video_file:
                logging.info(f"影片生成成功，Prompt ID: {prompt_id}")
                return video_file
            else:
                logging.error("影片生成失敗，嘗試重試")

        except Exception as e:
            attempt += 1
            logging.error(f"生成影片時發生錯誤 (嘗試 {attempt}/{retry_attempts}): {e}")
            
            # 最後一次重試後仍失敗，返回 None
            if attempt >= retry_attempts:
                logging.error("所有重試均失敗，返回 None")
                return None

        finally:
            # 確保 WebSocket 被正確關閉
            ws.close()

    def upload_image(self, file_path, file_name):
        """
        將圖片上傳至伺服器。
        
        參數:
        - file_path: 圖片文件的路徑。
        - file_name: 上傳時的文件名。
        """
        try:
            return self._upload_file(file_path, file_name, 'upload/image')
        except Exception as e:
            logging.error(f"上傳圖片時發生錯誤: {e}")
            return None

    def fetch_video(self, filename, subfolder='', file_type='temp', format='video/h264-mp4', frame_rate=8, force_size='835.406x?', output_dir='./generated_videos'):
        """
        通過參數化的 API 請求下載影片並保存到指定目錄。

        參數:
        - filename (必須): 視頻的文件名，例如 'AnimateDiff_00007.mp4'。
        - subfolder (可選): 視頻所在的子目錄，默認為空。
        - file_type (可選): 文件的類型，默認為 'temp'。
        - format (必須): 視頻的格式，默認為 'video/h264-mp4'。
        - frame_rate (可選): 視頻的幀率，默認為 8。
        - force_size (可選): 視頻的尺寸，默認為 '835.406x?'。
        - output_dir (可選): 保存視頻的目錄，默認為 './generated_videos'。

        返回:
        - 影片數據和內容類型，若失敗則返回 None。
        """
        try:
            params = {
                'filename': filename,
                'subfolder': subfolder,
                'type': file_type,
                'format': format,
                'frame_rate': frame_rate,
                'force_size': force_size
            }
            return self._download_file('viewvideo', params, output_dir)
        except Exception as e:
            logging.error(f"請求視頻時發生錯誤: {e}")
            return None, None

    def save_images(self, images, output_dir='./generated_avatar', upload_url=None):
        """
        將生成的圖片保存到指定資料夾，並選擇性地上傳到指定的 API。
        
        參數:
        - images: 生成的圖像數據。
        - output_dir: 保存圖片的本地目錄。
        - upload_url: 圖片上傳的 API URL（可選）。
        """
        self.ensure_directory(output_dir)
    
        for node_id, image_data_list in images.items():
            for idx, image_data in enumerate(image_data_list):
                random_id = str(uuid.uuid4())
                output_filename = os.path.join(output_dir, f"avatar_{node_id}_{random_id}_{idx}.png")

                try:
                    # 保存圖片到本地
                    image = Image.open(io.BytesIO(image_data))
                    image.save(output_filename, 'PNG')
                    logging.info(f"圖片已保存到 {output_filename}")

                    # 若提供了上傳 URL，則上傳圖片
                    if upload_url:
                        self.upload_image(output_filename, f"avatar_{random_id}_{idx}.png")

                except Exception as e:
                    logging.error(f"保存圖片失敗: {e}")

    def get_images(self, imageName, gender, width, height):
        workflow = self.handle_avatar_generation_by_image_workflow(imageName, gender, width, height)
        
        """根據 prompt 通過 WebSocket 獲取生成的圖片"""
        ws = self._create_websocket()  # 手動創建 WebSocket 連接
        try:
            prompt_id = self.queue_prompt(workflow)['prompt_id']
            logging.info(f"Prompt ID: {prompt_id}")
            self._wait_for_completion(ws)  # 等待完成
            return self._get_output_images(prompt_id)
        finally:
            ws.close()  # 確保 WebSocket 在完成後被正確關閉

    def _load_workflow(self, filepath):
        """從指定路徑加載工作流配置"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(f"工作流配置文件未找到: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"工作流配置文件格式錯誤: {e}")
            raise

    def _upload_file(self, file_path, file_name, endpoint):
        """私有方法：上傳文件"""
        mime_type = self._get_mime_type(file_path)
        with open(file_path, 'rb') as file:
            file_data = file.read()

        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        data = self._create_multipart_form_data(boundary, file_name, mime_type, file_data)
        headers = self._create_headers_for_upload(boundary, len(data))

        return self._send_post_request(f"http://{self.server_address}/{endpoint}", data, headers)

    def _download_file(self, api, params, output_dir):
        """私有方法：通用下載文件功能"""
        url = f"http://{self.server_address}/api/{api}"
        full_url = f"{url}?{urllib.parse.urlencode(params)}"
        logging.info(f"正在下載: {full_url}")

        try:
            # 嘗試發送請求並檢查 HTTP 狀態碼
            with urllib.request.urlopen(full_url) as response:
                if response.status != 200:
                    logging.error(f"下載失敗，伺服器返回狀態碼: {response.status}")
                    return None, None

                file_data = response.read()
                content_type = response.headers.get('content-type')
                
                if len(file_data) == 0:
                    logging.error("下載的文件為空，請檢查伺服器端是否正確生成了文件")
                else:
                    logging.info(f"成功下載了文件，大小為 {len(file_data)} 字節，類型為 {content_type}")

                self.ensure_directory(output_dir)
                output_filepath = os.path.join(output_dir, params['filename'])
                
                if 'video/webm' in content_type:
                    output_filepath = os.path.join(output_dir, params['filename'].replace('.mp4', '.webm'))
                    
                with open(output_filepath, 'wb') as f:
                    f.write(file_data)
                    logging.info(f"文件寫入完成，檔案大小為 {os.path.getsize(output_filepath)}")

                logging.info(f"文件已保存到 {output_filepath}")
                return output_filepath, content_type
        except Exception as e:
            logging.error(f"下載文件時發生錯誤: {e}")
            return None, None

    def _create_websocket(self):
        """私有方法: 建立 WebSocket 連接"""
        ws = websocket.WebSocket()
        ws.connect(f"ws://{self.server_address}/ws?clientId={self.client_id}")
        logging.info(f"已連接 WebSocket: ws://{self.server_address}/ws?clientId={self.client_id}")
        return ws

    def _wait_for_completion(self, ws):
        """私有方法: 監控任務直到完成"""
        while True:
            message = json.loads(ws.recv())
            logging.debug(f"收到消息: {message}")
            if message['type'] == 'executing' and message['data']['node'] is None:
                logging.info("任務完成。")
                break

    def queue_prompt(self, prompt):
        """將生成任務排隊"""
        try:
            p = {"prompt": prompt, "client_id": self.client_id}
            data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(f"http://{self.server_address}/prompt", data=data)
            logging.info(f"提交生成任務: http://{self.server_address}/prompt")
            return json.loads(urllib.request.urlopen(req).read())
        except Exception as e:
            logging.error(f"提交生成任務時發生錯誤: {e}")
            return None

    def get_history(self, prompt_id):
        """通過 prompt_id 獲取生成歷史"""
        try:
            with urllib.request.urlopen(f"http://{self.server_address}/history/{prompt_id}") as response:
                return json.loads(response.read())
        except Exception as e:
            logging.error(f"獲取生成歷史時發生錯誤: {e}")
            return {}

    def _get_output_video(self, prompt_id):
        """根據 prompt_id 獲取生成的影片"""
        history = self.get_history(prompt_id).get(prompt_id, {})
        for node_id, node_output in history.get('outputs', {}).items():
            if 'gifs' in node_output:
                video_filename = node_output['gifs'][0]['filename']
                logging.info(f"影片生成成功: {video_filename}")
                return self.fetch_video(video_filename)
        logging.warning("未找到影片輸出。")
        return None

    def _get_output_images(self, prompt_id):
        """根據 prompt_id 獲取生成的圖片"""
        history = self.get_history(prompt_id).get(prompt_id, {})
        output_images = {}

        for node_id, node_output in history.get('outputs', {}).items():
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = self.get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
                output_images[node_id] = images_output

        return output_images

    def get_image(self, filename, subfolder, folder_type):
        """根據檔名、子資料夾及類型獲取生成的圖片"""
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://{self.server_address}/view?{url_values}") as response:
            return response.read()

    def _get_mime_type(self, file_path):
        """根據文件路徑獲取 MIME 類型"""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'application/octet-stream'

    def _create_multipart_form_data(self, boundary, file_name, mime_type, file_data):
        """創建 multipart form-data 用於文件上傳"""
        return (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'
            f'Content-Type: {mime_type}\r\n\r\n'
            f'{file_data.decode("ISO-8859-1")}\r\n'
            f'--{boundary}--\r\n'
        ).encode('ISO-8859-1')

    def _create_headers_for_upload(self, boundary, data_length):
        """創建上傳文件所需的請求頭"""
        return {
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'Content-Length': str(data_length),
        }

    def _send_post_request(self, url, data, headers):
        """發送 HTTP POST 請求並返回響應"""
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            return response.read()

    def ensure_directory(self, directory):
        """確保指定的資料夾存在，若不存在則創建"""
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"已創建目錄: {directory}")
            
    def handle_avatar_generation_by_image_workflow(self, imageName, gender, width, height):
        workflow = self._load_workflow('./workflows/generate_avatar_by_image.json')
        
        if "25" in workflow and "inputs" in workflow["25"] and "image" in workflow["25"]["inputs"]:
            workflow["25"]["inputs"]["image"] = imageName
        
        positive_prompts = "Anime-style portrait, silver hair, soft lighting, delicate facial features, large reflective eyes, high-detailed, serene background"
        negative_prompts = "Excessive makeup, hyper-realism, distorted anatomy, harsh lighting, exaggerated emotions, overly vibrant or neon colors, blurry or out-of-focus details"

        prompts = {
            "positive": {
                "neutral": positive_prompts + ", neutral gender character, medium-length silver hair, casual outdoor clothing, soft shadows",
                "female": positive_prompts + ", female character, long silver hair with soft waves, sporty jacket, cute expression",
                "male": positive_prompts + ", male character, medium-length silver hair, sporty jacket with subtle masculine design, sharp but gentle features",
            },
            "negative": {
                "neutral": negative_prompts + ", overly masculine or overly feminine features, extreme age (too young or too old), unnatural or neon-colored hair",
                "female": negative_prompts + ", highly masculine features, cluttered background, harsh shadows, overly stylized expressions",
                "male": negative_prompts + ", overly feminine features, exaggerated muscles, harsh shadows, overly vibrant or extreme hair colors",
            }
        }
        
        # 動態更新 CLIPTextEncode 節點中的描述
        if "2" in workflow and "inputs" in workflow["2"] and "text" in workflow["2"]["inputs"]:
            workflow["2"]["inputs"]["text"] = prompts["positive"][gender]
        else:
            return jsonify({"error": "Invalid workflow structure"}), 400
        if "3" in workflow and "inputs" in workflow["3"] and "text" in workflow["3"]["inputs"]:
            workflow["3"]["inputs"]["text"] = prompts["negative"][gender]
        else:
            return jsonify({"error": "Invalid workflow structure"}), 400

        # 更新解析度
        if "5" in workflow and "inputs" in workflow["5"] and "height" in workflow["5"]["inputs"]:
            workflow["5"]["inputs"]["height"] = height
        else:
            # 預設解析度 512x512
            workflow["5"]["inputs"]["height"] = 512

        if "5" in workflow and "inputs" in workflow["5"] and "width" in workflow["5"]["inputs"]:
            workflow["5"]["inputs"]["width"] = width
        else:
            # 預設解析度 512x512
            workflow["5"]["inputs"]["width"] = 512
            
        
    
        print(f"Prompt positive: {workflow['2']['inputs']['text']}")
        print(f"Prompt negative: {workflow['3']['inputs']['text']}")
        
        return workflow

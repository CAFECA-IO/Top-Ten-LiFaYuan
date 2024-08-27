import requests
import json
import os

def extract_text_from_responses(response_content):
    # 將字符串拆分為獨立的 JSON 對象
    response_lines = response_content.splitlines()
    
    # 初始化一个空字符串来儲存結果
    full_text = ""
    
    for line in response_lines:
        # 將每行轉換為 JSON 對象
        json_obj = json.loads(line)
        
        # 提取 response 字段，并追加到 full_text
        full_text += json_obj.get("response", "")
    
    return full_text

def generate_news_script(summary):
    ai_url = 'http://211.22.118.147/api/generate'
    request_data = {
        "model": "llama3.1:70b",
        "prompt": f"根據以下摘要生成新聞稿：「{summary}」，並用「哎呦呦，這件事情在我看來...」做總結"
    }
    
    try:
        response = requests.post(ai_url, json=request_data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        
        script = extract_text_from_responses(response.text)
        output_path = 'data/output/news_script.txt'
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # 將生成的新聞稿保存到 output 文件夾
        with open(output_path, 'w') as f:
            f.write(script)
        print(f'新聞稿已生成：{output_path}')
        
        return output_path
    except requests.exceptions.RequestException as e:
        print(f"生成新聞稿時出錯: {e}")
        return None

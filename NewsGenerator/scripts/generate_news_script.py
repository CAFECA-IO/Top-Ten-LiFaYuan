import requests

def generate_news_script(summary):
    ai_url = 'http://211.22.118.146:11434/api/generate'
    request_data = {
        "model": "llama3.1",
        "prompt": f"根據以下摘要生成新聞稿：「{summary}」，並用「哎呦呦，這件事情在我看來...」做總結"
    }
    
    try:
        response = requests.post(ai_url, json=request_data, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        script = response.text
        output_path = 'data/output/news_script.txt'

        # 將生成的新聞稿保存到 output 文件夾
        with open(output_path, 'w') as f:
            f.write(script)
        print(f'新聞稿已生成：{output_path}')
        
        return output_path
    except requests.exceptions.RequestException as e:
        print(f"生成新聞稿時出錯: {e}")
        return None

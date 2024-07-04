from transformers import pipeline
import os

token = os.getenv("HUGGINGFACE_API_TOKEN")

# 測試訪問令牌是否有效
try:
    pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", use_auth_token=token)
    print("Token is valid.")
except Exception as e:
    print(f"Error: {e}")
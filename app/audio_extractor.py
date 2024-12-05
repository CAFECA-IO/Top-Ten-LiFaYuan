import aiohttp
from app.utils import setup_logger

logger = setup_logger('audio_extractor_client', 'output.log')

BASE_URL = "http://localhost:5001"  # VideoScript API 地址

async def extract_audio(video_id):
    """
    通過 HTTP 請求提取音頻。
    """
    url = f"{BASE_URL}/api/extract_audio"
    payload = {"video_id": video_id}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"提取音頻成功: {data['audio_path']}")
                    return data["audio_path"]
                elif response.status == 404:
                    error_message = f"視頻文件不存在，無法提取音頻: {video_id}"
                    logger.error(error_message)
                    raise FileNotFoundError(error_message)
                else:
                    error_message = f"提取音頻失敗，狀態碼: {response.status}"
                    logger.error(error_message)
                    raise Exception(error_message)
    except Exception as e:
        logger.error(f"HTTP 請求提取音頻失敗: {str(e)}")
        raise

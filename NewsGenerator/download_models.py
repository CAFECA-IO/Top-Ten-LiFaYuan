from modelscope import snapshot_download

# 下載 CosyVoice 預訓練模型
snapshot_download('iic/CosyVoice-300M', local_dir='CosyVoice/pretrained_models/CosyVoice-300M')
snapshot_download('iic/CosyVoice-300M-SFT', local_dir='CosyVoice/pretrained_models/CosyVoice-300M-SFT')
snapshot_download('iic/CosyVoice-300M-Instruct', local_dir='CosyVoice/pretrained_models/CosyVoice-300M-Instruct')
snapshot_download('iic/CosyVoice-ttsfrd', local_dir='CosyVoice/pretrained_models/CosyVoice-ttsfrd')
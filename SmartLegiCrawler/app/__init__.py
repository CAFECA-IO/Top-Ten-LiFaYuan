from flask import Flask

# 初始化 Flask 應用
app = Flask(__name__)

# 導入其他模塊中的路由
from . import routes

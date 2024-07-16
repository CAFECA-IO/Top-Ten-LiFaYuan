from quart import Quart

# 初始化 Quart 應用
app = Quart(__name__)

# 導入其他模塊中的路由
from . import routes

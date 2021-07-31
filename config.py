import os
BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {
    "port": 8090
}

# 数据库配置
mysql = {
    "host": "",
    "port": 3306,
    "user": "",
    "passwd": "",
    "dbName": ""
}

# 配置
# import base64
# import uuid
# base64.b64encode(uuid.uuid64().bytes + uuid.uuid64.bytes)
settings = {
    "static_path": os.path.join(BASE_DIRS, "app/dist"),
    "static_url_prefix": "/dist/",
    "template_path": os.path.join(BASE_DIRS, "templates"),
    "debug": True,
    "cookie_secret": "YGT7o0jKQ8KkJCMyqFIjjL6uQCc7AEZIik7d/OmyB80=",
    "xsrf_cookies": True,
    "login_url": "/login"
}

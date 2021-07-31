from tornado.web import RequestHandler


# 登录逻辑判断
async def check_user(name, passwd):
    result = {
        "is_success": False,
        "token": ""
    }
    if name == "1" and passwd == "1":
        result = {
            "is_success": True,
            "token": "good"
        }
    return result


# 登录，返回json
class LoginHandler(RequestHandler):
    def check_xsrf_cookie(self):
        # 在单页面禁用xsrf_cookie的检查
        return True

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    async def post(self, *args, **kwargs):
        next_url = self.get_query_argument("next", "/home")
        name = self.get_body_argument("name", "")
        passwd = self.get_body_argument("passwd", "")
        result = await check_user(name, passwd)
        if result["is_success"]:
            # 登录令牌要保存到redis
            self.write({
                "is_success": True,
                "token": result["token"],
                "next": next_url
            })
        else:
            self.write({
                "is_success": False,
                "token": "",
                "next": next_url
            })

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

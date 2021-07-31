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


# 登录，跳转
class LoginHandler(RequestHandler):
    def get(self, *args, **kwargs):
        next_url = self.get_query_argument("next", "/home")
        self.render("login.html", url="/login?next=" + next_url)

    async def post(self, *args, **kwargs):
        next_url = self.get_query_argument("next", "/home")
        name = self.get_body_argument("name", "")
        passwd = self.get_body_argument("passwd", "")
        result = await check_user(name, passwd)
        if result["is_success"]:
            self.set_secure_cookie("token", result["token"])
            self.redirect(next_url)
        else:
            self.redirect("/login?next=" + next_url)


# 登录，返回json
class LoginHandler2(RequestHandler):
    async def post(self, *args, **kwargs):
        next_url = self.get_query_argument("next", "/home")
        name = self.get_body_argument("name", "")
        passwd = self.get_body_argument("passwd", "")
        result = await check_user(name, passwd)
        if result["is_success"]:
            self.set_secure_cookie("token", result["token"])
            self.write({
                "is_success": True,
                "next": next_url
            })
        else:
            self.write({
                "is_success": False,
                "next": next_url
            })


# 注销
class LogOutHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie("token")
        self.write({"is_success": True})
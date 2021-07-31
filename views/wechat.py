import uuid
import json
import itertools

from tornado.websocket import WebSocketHandler

from models.client import InteractiveClient


class WeChatHandler(WebSocketHandler):
    def __init__(self, application, request):
        super().__init__(application, request)
        self.client = InteractiveClient()
        if self.client is not None:
            self.client.register("input", self._handle_input)
            self.client.register("output", self._handle_output)
            self.client.register("err", self._handle_err)

    def check_origin(self, origin):
        return True

    def open(self):
        print("[%s]登录了" % self.request.remote_ip)
        msg_id = "id_" + str(uuid.uuid4())
        self.write_message({"id": msg_id, "type": "output",
                            "data": {"type": "text", "content": "[%s]登录了" % self.request.remote_ip},
                            "desc": {}})

    async def on_message(self, message):
        print("recv message:", message)
        msg_id = "id_" + str(uuid.uuid4())
        msg_obj = json.loads(message)
        await self.write_message({"id": msg_id, "type": "code", "data": msg_obj["data"], "desc": {}})
        # edit mode
        if msg_obj["mode"] == "edit":
            if msg_obj["language"] == "python3":
                msg_obj_data = msg_obj["data"].strip()
                msg_obj_desc = msg_obj["desc"]
                if msg_obj_data == "" or self.client is None:
                    return
                current_sequence = await self._handle_python3(self.client, msg_obj["type"], msg_obj_data, msg_obj_desc)
                await self.write_message({"id": msg_id, "type": "sequence", "data": current_sequence, "desc": {}})
            elif msg_obj["language"] == "markdown":
                pass
        # command mode
        elif msg_obj["mode"] == "command":
            pass

    def on_close(self):
        print("[%s]退出了" % self.request.remote_ip)

    async def _handle_python3(self, client, msg_obj_type, msg_obj_data, msg_obj_desc):
        if msg_obj_type == "compute":
            return await client.runcode(msg_obj_data, msg_obj_desc)
        elif msg_obj_type == "complete":
            results = []
            for state in itertools.count():
                comp = client.complete(msg_obj_data, state)
                if comp is None:
                    break
                results.append(comp)
            self._handle_complete(results)
        return 0

    def _handle_input(self):
        msg_id = "id_" + str(uuid.uuid4())
        self.write_message({"id": msg_id, "type": "input"})

    def _handle_output(self, omsg, code, desc):
        handler = getattr(self, "handle_%s" % omsg.msg_type)
        if handler is not None:
            handler(omsg, code, desc)

    def _handle_err(self, err, code, desc):
        print(err.etype, ':', err.evalue)
        print(''.join(err.traceback))
        msg_id = "id_" + str(uuid.uuid4())
        self.write_message({"id": msg_id, "type": "error", "code": code, "data": err.traceback, "desc": desc})

    def _handle_complete(self, results):
        for item in results:
            msg_id = "id_" + str(uuid.uuid4())
            self.write_message({"id": msg_id, "type": "complete", "data": item, "desc": {}})

    def handle_pyin(self, omsg, code, desc):
        pass

    def handle_pyout(self, omsg, code, desc):
        msg_id = "id_" + str(uuid.uuid4())
        category = getattr(omsg.content.data, "category", None)
        content = getattr(omsg.content.data, "content", None)
        if category is not None:
            self.write_message({"id": msg_id, "type": "output", "code": code,
                                "data": {"type": category, "content": content},
                                "desc": desc})
        else:
            resp = content.rstrip()
            if resp == "":
                return
            self.write_message({"id": msg_id, "type": "output", "code": code,
                                "data": {"type": "text", "content": resp},
                                "desc": desc})

    def handle_stream(self, omsg, code, desc):
        if omsg.content.name == "stdout":
            msg_id = "id_" + str(uuid.uuid4())
            resp = omsg.content.data.rstrip()
            if resp == "":
                return
            self.write_message({"id": msg_id, "type": "stream", "code": code, "data": resp, "desc": desc})
        else:
            print("*ERR*")
            print(omsg.content.data)

    def handle_pyerr(self, omsg, code, desc):
        pass


class InputHandler(WebSocketHandler):
    def check_origin(self, origin):
        return True

    def on_message(self, message):
        client = InteractiveClient()
        if client is not None:
            client.input(message)

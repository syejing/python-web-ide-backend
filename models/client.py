import sys
import time
import itertools
import asyncio

import zmq

import models.session

REQUEST_RETRIES = 1000


class InteractiveClient(object):
    _instance = None
    _init__flag = False

    def __new__(cls, *args, **kwargs):
        if InteractiveClient._instance is None:
            InteractiveClient._instance = super().__new__(cls, *args, **kwargs)

        return InteractiveClient._instance

    def __init__(self):
        if InteractiveClient._init__flag is False:
            InteractiveClient._init__flag = True

            ip = "127.0.0.1"
            port_base = 5555
            connection = ("tcp://%s" % ip) + ":%i"
            req_conn = connection % port_base
            sub_conn = connection % (port_base + 1)
            rep_conn = connection % (port_base + 2)

            self.session = models.session.Session()

            self.ctx = zmq.Context()

            self.req_socket = self.ctx.socket(zmq.DEALER)
            self.req_socket.setsockopt(zmq.LINGER, 0)
            self.req_socket.connect(req_conn)

            self.sub_socket = self.ctx.socket(zmq.SUB)
            self.sub_socket.connect(sub_conn)
            self.sub_socket.setsockopt(zmq.SUBSCRIBE, b"")

            self.rep_socket = self.ctx.socket(zmq.ROUTER)
            self.rep_socket.connect(rep_conn)
            self.rep_ident = None
            self.rep_msg = None

            self.poller = zmq.Poller()
            self.poller.register(self.req_socket, zmq.POLLIN)
            self.child_poller = zmq.Poller()
            self.child_poller.register(self.sub_socket, zmq.POLLIN)
            self.child_poller.register(self.rep_socket, zmq.POLLIN)

            self.handlers = {}

            self.retries_left = REQUEST_RETRIES
            self.messages = {}
            self.matches = []
            self.sequence = itertools.count(start=1)

            self.future = None

    def register(self, name, handler):
        self.handlers["handle_"+name] = handler

    # 执行
    async def runcode(self, buffer, desc):
        omsg = self.session.send(self.req_socket, "execute_request", dict(code=buffer))
        self.messages[omsg.header.msg_id] = omsg
        self.retries_left = REQUEST_RETRIES
        while True:
            try:
                socks = dict(self.poller.poll(50))
                if self.req_socket in socks and socks[self.req_socket] == zmq.POLLIN:
                    await self.recv_output(buffer, desc)
                    rep = self.session.recv(self.req_socket)
                    print("[client]", rep)
                    if rep is not None:
                        if rep.content.status == "error":
                            handler = self.handlers.get("handle_err", None)
                            if handler is not None:
                                handler(rep.content, buffer, desc)
                            else:
                                self.input("[client] unregistered handle_err")
                        elif rep.content.status == "aborted":
                            print("[client]", "ERROR: ABORTED", file=sys.stderr)
                            ab = self.messages[rep.parent_header.msg_id].content
                            if "code" in ab:
                                print("[client]", ab.code, file=sys.stderr)
                            else:
                                print("[client]", ab, file=sys.stderr)
                        return next(self.sequence)
                await self.recv_output(buffer, desc)
                self.retries_left -= 1
                if self.retries_left == 0:
                    print("[client] Server seems to be offline, abandoning")
                    break
            except KeyboardInterrupt:
                self.rep_socket.close()
                self.sub_socket.close()
                self.req_socket.close()
                self.ctx.destroy()

    async def recv_output(self, code, desc):
        while True:
            try:
                child_socks = dict(self.child_poller.poll(1000))
                if self.sub_socket in child_socks and child_socks[self.sub_socket] == zmq.POLLIN:
                    omsg = self.session.recv(self.sub_socket)
                    if omsg is not None:
                        print("[client]", omsg)
                        self._handle_output(omsg, code, desc)
                elif self.rep_socket in child_socks and child_socks[self.rep_socket] == zmq.POLLIN:
                    ident = self.rep_socket.recv()
                    assert self.rep_socket.rcvmore, "Unexpected missing message part."
                    msg = self.rep_socket.recv_json()
                    omsg = models.session.Message(msg)
                    if omsg is not None:
                        print("[client]", omsg)
                        await self._handle_input(ident, omsg)
                else:
                    break
            except:
                raise

    async def _handle_input(self, ident, omsg):
        if omsg.msg_type == "input_request":
            self.rep_ident = ident
            self.rep_msg = self.session.msg("input_reply", {"data": ""}, omsg)
            handler = self.handlers.get("handle_input", None)
            if handler is not None:
                handler()
                self.future = asyncio.get_event_loop().create_future()
                await self.future
            else:
                self.input("[client] unregistered handle_input")

    def input(self, value):
        if self.rep_ident is not None:
            self.rep_socket.send(self.rep_ident, zmq.SNDMORE)
            self.rep_msg["content"]["data"] = value
            self.rep_socket.send_json(self.rep_msg)
            self.future.set_result(None)

    def _handle_output(self, omsg, code, desc):
        if hasattr(omsg.parent_header, "session") and omsg.parent_header.session == self.session.session:
            handler = self.handlers.get("handle_output", None)
            if handler is not None:
                handler(omsg, code, desc)
            else:
                print("[client] unregistered handle_output")
        else:
            pass

    # tab补全
    def complete(self, text, state):
        if state == 0:
            matches = self._request_completion(text)
            if matches is None:
                self.matches = []
            else:
                self.matches = matches
        try:
            return self.matches[state]
        except IndexError:
            return None

    def _request_completion(self, text):
        self.session.send(self.req_socket, "complete_request", dict(text=text))
        for i in range(5):
            try:
                rep = self.session.recv(self.req_socket)
                print("[client] _request_completion", rep)
                if rep is not None and rep.msg_type == "complete_reply":
                    matches = rep.content.matches
                    break
                time.sleep(0.1)
            except KeyboardInterrupt:
                pass
        else:
            print("[client]", "TIMEOUT")  # Can't see this message...
            matches = None
        return matches

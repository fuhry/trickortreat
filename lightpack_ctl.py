#!/usr/bin/env python3

from flask import Flask, request
import socket
import time
import re
import json


API_KEY = '{00000000-0000-0000-0000-000000000000}'
LIGHTPACK_HOST = 'lightpack-server.home.lan'
LIGHTPACK_PORT = 3636

app = Flask(__name__)

class LightpackControl:
    socket_fd: socket.socket

    def __init__(self, host: str, port: int, api_key: str):
        self.socket_fd = socket.socket()
        self.socket_fd.connect((host, port,))

        # read welcome message
        self._read_line()

        self.authenticate(api_key)
        self.lock()

    def __del__(self):
        self.unlock()

    def authenticate(self, api_key: str):
        result = self._cmd("apikey:%s" % (api_key))
        if result != 'ok':
            raise RuntimeError("api authentication failed: %s" % (result))

    def lock(self):
        result = self._cmd("lock")
        if result != "lock:success":
            raise RuntimeError("failed to lock device: %s" % (result))

    def solid(self, r: int, g: int, b: int):
        parts = ";".join([
            "%d-%d,%d,%d" % (i, r, g, b)
            for i in range(1, 11)
        ])
        self._cmd("setcolor:%s" % (parts))

    def unlock(self):
        self._cmd("unlock")

    def _read_line(self):
        return self.socket_fd.recv(1024)

    def _cmd(self, cmd: str):
        cmd = cmd.encode('utf-8') + b'\n'
        self.socket_fd.send(cmd)
        return self._read_line().decode('utf-8').rstrip()


lpc = LightpackControl(LIGHTPACK_HOST, LIGHTPACK_PORT, API_KEY)


@app.route('/solid', methods=['POST'])
def route_solid():
    inputs = {}
    for k in ['r', 'g', 'b']:
        if not k in request.form:
            raise KeyError("Missing required argument: %s" % (k))
        if re.match('^[0-9]+$', request.form[k]) is None:
            raise KeyError("Invalid argument: %s is expected to be an integer 0-255" % (k))
        inputs[k] = int(request.form[k])
        if inputs[k] < 0 or inputs[k] > 255:
            raise KeyError("Invalid argument: %s is expected to be an integer 0-255" % (k))

    lpc.solid(inputs['r'], inputs['g'], inputs['b'])

    return {"success": True}

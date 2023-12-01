import asyncio
import json
import threading
from typing import Callable

import requests
import websocket
from websocket import *

from ..common.camera import Camera
from ..common.system import System


class RobotBase:
    """ Robot 基类

    实例化的时候会通过websocket连接到对应设备的控制端口！
    """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001,
                 on_connected: Callable = None, on_message: Callable = None,
                 on_close: Callable = None, on_error: Callable = None):
        if ssl:
            self._baseurl: str = f'https://{host}:{port}'
            self._ws_url = f'wss://{host}:{port}/ws'
        else:
            self._baseurl: str = f'http://{host}:{port}'
            self._ws_url: str = f'ws://{host}:{port}/ws'

        try:
            self._ws: WebSocket = create_connection(self._ws_url)
        except ConnectionRefusedError as e:
            print(f'链接Robot设备出错。请检查server状态... {e}')
            return
        except Exception as e:
            print(f'链接Robot设备出错... {e}')
            return

        self._on_connected = on_connected
        self._on_message = on_message
        self._on_close = on_close
        self._on_error = on_error

        self.camera = Camera(self._baseurl)
        self.system = System()

        self._receive_thread = threading.Thread(target=self._event)
        self._receive_thread.start()

    def _event(self):
        if self._on_connected:
            asyncio.run(self._on_connected())
        try:
            while True:
                message = self._ws.recv()
                if self._on_message:
                    asyncio.run(self._on_message(message))
        except websocket.WebSocketConnectionClosedException:
            if self._on_close:
                asyncio.run(self._on_close())
        except websocket.WebSocketException as e:
            if self._on_error:
                asyncio.run(self._on_error(e))

    def _send_websocket_msg(self, message: json):
        self._ws.send(json.dumps(message))

    def _send_request(self, url: str, method: str = 'GET', params=None, json=None):
        try:
            response = requests.request(method, f'{self._baseurl}{url}', params=params, json=json)
            return response.json()
        except Exception as e:
            print(f'下发指令失败，请检查设备server状态 {e}')
            return {"code": -1, "msg": f"下发指令失败，请检查设备server状态", "data": None}

    def _send_request_stream(self, url: str, method: str = 'GET', params=None, json=None):
        response = requests.request(method, f'{self._baseurl}{url}', params=params, json=json, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                yield chunk

    @classmethod
    def _cover_param(cls, param: float, value: str, min_threshold: float, max_threshold: float) -> float:
        if param is None:
            print(f"Illegal parameter: {value} = {param}")
            param = 0
        if param > max_threshold:
            print(
                f"Illegal parameter: {value} = {param}, "
                f"greater than maximum, expected not to be greater than {max_threshold}, actual {param}")
            param = max_threshold
        if param < min_threshold:
            print(
                f"Illegal parameter: {value} = {param}, "
                f"greater than maximum, expected not to be less than {min_threshold}, actual {param}")
            param = min_threshold
        return param

    def start(self):
        """ 启动

        当你想要控制Robot设备的时候，你的第一个指令
        """
        return self._send_request(url='/robot/start', method='POST')

    def stop(self):
        """ 停止

        ``该命令优先于其他命令! 会掉电停止。请在紧急情况下触发``
        """
        return self._send_request(url="/robot/stop", method="POST")

    def exit(self):
        """ 断开Robot链接 """
        self._ws.close()

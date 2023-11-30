from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Callable

from rocs_client.robot.robot_base import RobotBase


@dataclass
class Motor:
    no: str
    orientation: str
    angle: float = 0


@dataclass
class ArmAction(Enum):
    # 归零
    RESET = "RESET"
    # 左挥手
    LEFT_ARM_WAVE = "LEFT_ARM_WAVE"
    # 甩胳膊
    ARMS_SWING = "ARMS_SWING"
    # 打招呼
    HELLO = "HELLO"


@dataclass
class HandAction(Enum):
    # 半握手
    HALF_HANDSHAKE = "HALF_HANDSHAKE"
    # 竖大拇指
    THUMB_UP = "THUMB_UP"
    # 手张开
    OPEN = "OPEN"
    # 手微屈
    SLIGHTLY_BENT = "SLIGHTLY_BENT"
    # 抓握
    GRASP = "GRASP"
    # 抖动手
    TREMBLE = "TREMBLE"
    # 握手
    HANDSHAKE = "HANDSHAKE"


class Human(RobotBase):
    """
    When you need to connect a Human, you can create a Human() object!
    This will connect to the control system in the background,
    and provide the corresponding control function and status monitoring!

    Args:

        ssl(bool): Indicates whether ssl authentication is enabled. Default False
        host(str): indicates the network IP address of the car
        port(int): specifies the PORT of the car control service
        on_connected(callable): This listener is triggered when the car connection is successful
        on_message(callable): This listener will be triggered when the car sends system status
        on_close(callable): This listener will be triggered when the car connection is closed
        on_error(callable): This listener will be triggered when a car error occurs
    """
    motor_limits: list
    """ This is the maximum limit and minimum limit Angle of the motor """

    def __init__(self, ssl: bool = False, host: str = '127.0.0.1', port: int = 8001, on_connected: Callable = None,
                 on_message: Callable = None, on_close: Callable = None, on_error: Callable = None):
        super().__init__(ssl, host, port, on_connected, on_message, on_close, on_error)
        self.motor_limits = self._get_motor_limit_list()['data']

    def stand(self) -> Dict[str, Any]:
        """
        The GR-01 Human device will stand in place

        If you want to command the GR-01 humanoid device after start!
        you also need to call this function to set its position to stand mode.
        If you need to stop during a walk, you can also call this function to stand

        Returns:

             Dict:
                `code` (int): statu code，0: Normal -1: Anomaly
                `msg` (str): result msg
        """
        return self._send_request(url='/robot/stand', method='POST')

    def reset(self):
        """
        Reset/zero/calibration of the initial state of the device
        """
        return self._send_request(url='/robot/reset', method="POST")

    def get_joint_limit(self) -> Dict[str, Any]:
        """
        Obtain joint limit

        Returns:

            Dict:
                - `code` (int):
                    statu code，0: Normal    -1: Anomaly

                - `msg` (str):
                    result msg

                - `data` (dict):
                    results

                    - function (str):
                        函数名称

                    - data(dict):
                        - jointlimit (list): 关节限制列表，每个元素是一个字典
                            - name (str): 关节名称
                            - qdotaMax (float): 关节最大速度，单位：rad/s
                            - qaMax (float): 关节最大弧度，单位：rad
                            - qaMin (float): 关节最小角度，单位：rad
                            - tauaMax (float): 最大扭矩，单位：n*m


        Example:

        .. code-block:: json

            {
                "code": 0,
                "msg": "ok",
                "data": {
                    "data": {
                        "jointlimit": [
                            {
                                "name": "left_hip_roll",
                                "qaMax": 0.523598775598299,
                                "qaMin": -0.087266462599716,
                                "qdotaMax": 12.56637061435917,
                                "tauaMax": 82.5
                            },
                            {
                                "name": "left_hip_yaw",
                                "qaMax": 0.392699081698724,
                                "qaMin": -0.392699081698724,
                                "qdotaMax": 12.56637061435917,
                                "tauaMax": 82.5
                            },
                            {
                                "name": "left_hip_pitch",
                                "qaMax": 0.698131700797732,
                                "qaMin": -1.221730476396031,
                                "qdotaMax": 22.441443522143093,
                                "tauaMax": 200
                            },
                            {
                                "name": "left_knee_pitch",
                                "qaMax": 2.094395102393195,
                                "qaMin": -0.087266462599716,
                                "qdotaMax": 22.441443522143093,
                                "tauaMax": 200
                            }

                        ]
                    },
                    "function": "SonnieGetStatesLimit"
                }
            }
        """
        return self._send_request(url='/robot/joint_limit', method="GET")

    def get_joint_states(self) -> Dict[str, Any]:
        """
        获取关节状态

        Returns:

            Dict: 返回数据包含以下字段:

            - `code` (int): 状态码，0 表示正常，-1 表示异常
            - `msg` (str): 状态信息，"ok" 表示正常
            - `data` (dict): 响应数据，包含以下字段：

                - `data` (dict): 状态数据，包含以下字段：

                    - `bodyandlegstate` (dict): 身体和腿部状态，包含以下字段：

                        - `currentstatus` (str): 当前状态，"StartComplete" 表示启动完成
                        - `log` (dict): 日志信息，包含以下字段：

                            - `logBuffer` (list): 日志缓冲区，包含以下字段：

                                - `log` (str): 日志内容，"GRPC system state response init complete" 表示 GRPC 系统状态响应初始化完成

                    - `leftarmstate` (dict): 左侧手臂状态，包含以下字段：

                        - `armstatus` (str): 手臂状态，"Swing" 表示摆臂模式

                    - `rightarmstate` (dict): 右侧手臂状态，包含以下字段：

                        - `armstatus` (str): 手臂状态，"Swing" 表示摆臂模式

                - `function` (str): 调用该接口的函数名，"SonnieGetSystemStates" 表示获取系统状态接口

        Example:

        .. code-block:: json

            {
                "code": 0,
                "msg": "ok",
                "data": {
                    "data": {
                        "bodyandlegstate": {
                            "currentstatus": "StartComplete",
                            "log": {
                                "logBuffer": [
                                    {
                                        "log": "GRPC system state response init complete"
                                    }
                                ]
                            }
                        },
                        "leftarmstate": {
                            "armstatus": "Swing"
                        },
                        "rightarmstate": {
                            "armstatus": "Swing"
                        }
                    },
                    "function": "SonnieGetSystemStates"
                }
            }

        """
        return self._send_request(url='/robot/joint_states', method="GET")

    def enable_debug_state(self, frequence: int = 1):
        """
        open debug mode

        Triggering this function will trigger the GR-01 human device to actively send status values in the background,
        so you need to listen to the on_message function for processing

        Args:

            frequence(int): frequency

        Returns:

            Dict:

                - log (dict): log

                    - logBuffer (list): logBuffers

                        - log (str): content

                - states (dict): joint data content

                    - basestate (dict): robot status data

                        - a (float): hip roll
                        - b (float): hip Pitch
                        - c (float): hip Yaw
                        - va (float): not use
                        - vb (float): not use
                        - vc (float): not use
                        - vx (float): 前进方向速度，单位m/s
                        - vy (float): 左右方向速度，单位m/s
                        - vz (float): not use
                        - x (float): base  X，站立时X位置
                        - y (float): base  Y，站立时Y位置
                        - z (float): base  Z，站立时Z位置

                    - fsmstatename (dict): 有关状态机状态的数据

                        - currentstatus (str): 当前状态 Unknown、Start、Zero、Stand、Walk、Stop
                    - jointStates (list): 关节状态列表

                        - name (str): 关节名称
                        - qa (float): 真实的关节角度，单位：rad（弧度）
                        - qdota (float): 真实的关节速度，单位：rad/s（弧度/秒）
                        - taua (float): 真实的扭矩，单位:n*m
                        - qc (float): 期望的关节速度，单位：rad
                        - qdotc (float): 期望的关节速度，单位：rad/s（弧度/秒）
                        - tauc (float): 期望的关节扭矩，单位：unit:n*m
                    - stanceindex (dict): 姿态索引 not use
                    - contactforce (dict): 接触力数据 not use

                        - fxL (float): 左脚接触力
                        - fyL (float): 左脚接触力
                        - fzL (float): 左脚接触力
                        - mxL (float): 左脚接触力
                        - myL (float): 左脚接触力
                        - mzL (float): 左脚接触力
                        - fxR (float): 右脚接触力
                        - fyR (float): 右脚接触力
                        - fzR (float): 右脚接触力
                        - mxR (float): 右脚接触力
                        - myR (float): 右脚接触力
                        - mzR (float): 右脚接触力
                - timestamp (dict): 时间戳

                    - nanos (int):
                    - seconds (str):

            function (str): interface name / function name

        Example:

        .. code-block:: json

            {
                "data": {
                    "states": {
                        "basestate": {
                            "a": -0.00008816774229518624,
                            "b": -0.0031777816310660227,
                            "c": 0,
                            "va": -3.2955695877132929e-9,
                            "vb": -6.542262024864478e-7,
                            "vc": 2.0403557796187139e-8,
                            "vx": 0,
                            "vy": 0,
                            "vz": 0,
                            "x": 0,
                            "y": 0,
                            "z": 0
                        },
                        "contactforce": {
                            "fxL": 0,
                            "fxR": 6,
                            "fyL": 1,
                            "fyR": 7,
                            "fzL": 2,
                            "fzR": 8,
                            "mxL": 3,
                            "mxR": 9,
                            "myL": 4,
                            "myR": 10,
                            "mzL": 5,
                            "mzR": 11
                        },
                        "fsmstatename": {
                            "currentstatus": "Start"
                        },
                        "jointStates": [
                            {
                                "name": "left_hip_roll",
                                "qa": -0.000002967348844382189,
                                "qc": -4.195799309522971e-9,
                                "qdota": -1.2811068419807388e-8,
                                "qdotc": -2.5650460977039419e-9,
                                "taua": 0.00000421397498061693,
                                "tauc": 0.00000421397498061693
                            },
                            {
                                "name": "left_hip_yaw",
                                "qa": 1.1561011056000389e-7,
                                "qc": 5.763118985802831e-10,
                                "qdota": 5.413053331490085e-10,
                                "qdotc": -1.998095673038479e-9,
                                "taua": -5.607576848879348e-7,
                                "tauc": -5.607576848879348e-7
                            },
                            {
                                "name": "left_hip_pitch",
                                "qa": 0.00004391517501779261,
                                "qc": 1.515751869369811e-8,
                                "qdota": 1.9014878092501132e-7,
                                "qdotc": -4.227869290635517e-8,
                                "taua": -0.000007239519592483131,
                                "tauc": -0.000007239519592483131
                            },
                            {
                                "name": "left_knee_pitch",
                                "qa": 0.00004577103623661791,
                                "qc": 1.825644254205245e-8,
                                "qdota": 1.9871683938840232e-7,
                                "qdotc": -1.3400628221563269e-7,
                                "taua": -0.000004188456587918816,
                                "tauc": -0.000004188456587918816
                            },
                            {
                                "name": "left_ankle_pitch",
                                "qa": 0.0000515945298803933,
                                "qc": 2.2981673142499234e-8,
                                "qdota": 2.242746827673787e-7,
                                "qdotc": -2.258893072672217e-7,
                                "taua": -7.153918887352573e-8,
                                "tauc": -7.153918887352573e-8
                            },
                            {
                                "name": "left_ankle_roll",
                                "qa": 6.419495520105573e-7,
                                "qc": 3.706374175342285e-11,
                                "qdota": 2.794181899265958e-9,
                                "qdotc": -5.949285977052194e-9,
                                "taua": 1.093729550329863e-10,
                                "tauc": 1.093729550329863e-10
                            },
                            {
                                "name": "right_hip_roll",
                                "qa": 0.0000028389355052439439,
                                "qc": 4.865708590789946e-9,
                                "qdota": 1.2246925191446977e-8,
                                "qdotc": -3.962174546204988e-9,
                                "taua": -0.000004837825973754749,
                                "tauc": -0.000004837825973754749
                            },
                            {
                                "name": "right_hip_yaw",
                                "qa": -4.364693140246345e-7,
                                "qc": 6.000702384094449e-10,
                                "qdota": -1.8497568931031923e-9,
                                "qdotc": -1.7781221204499439e-9,
                                "taua": -5.867529228984824e-7,
                                "tauc": -5.867529228984824e-7
                            },
                            {
                                "name": "right_hip_pitch",
                                "qa": 0.000045113585488131829,
                                "qc": 2.367752787246051e-8,
                                "qdota": 1.950714297088208e-7,
                                "qdotc": -6.520824184784889e-8,
                                "taua": -0.000011320537478692172,
                                "tauc": -0.000011320537478692172
                            },
                            {
                                "name": "right_knee_pitch",
                                "qa": 0.0000479437468878189,
                                "qc": 2.324249646390596e-8,
                                "qdota": 2.0757655546078694e-7,
                                "qdotc": -1.4486023522267125e-7,
                                "taua": -0.00000557281564261239,
                                "tauc": -0.00000557281564261239
                            },
                            {
                                "name": "right_ankle_pitch",
                                "qa": 0.00005468652781599774,
                                "qc": 2.4630029782206445e-8,
                                "qdota": 2.3684484798495586e-7,
                                "qdotc": -2.2533190930925487e-7,
                                "taua": -7.817536142908409e-8,
                                "tauc": -7.817536142908409e-8
                            },
                            {
                                "name": "right_ankle_roll",
                                "qa": -1.4411157156501987e-7,
                                "qc": 8.786951464767337e-11,
                                "qdota": -6.347293532005193e-10,
                                "qdotc": -6.275949957243541e-9,
                                "taua": 5.977234519649815e-11,
                                "tauc": 5.977234519649815e-11
                            },
                            {
                                "name": "waist_yaw",
                                "qa": 2.7287197903010758e-10,
                                "qc": -1.9509172839224989e-10,
                                "qdota": 2.182983232727597e-7,
                                "qdotc": -1.5630533392766103e-7,
                                "taua": -0.000003249343357926737,
                                "tauc": -0.0000017639729379187398
                            },
                            {
                                "name": "waist_pitch",
                                "qa": -1.1411541437762108e-8,
                                "qc": -5.783273072262379e-9,
                                "qdota": -5.121972652033971e-13,
                                "qdotc": 3.810219915783962e-8,
                                "taua": 0.000011505459672511687,
                                "tauc": 0.000005496170595926694
                            },
                            {
                                "name": "waist_roll",
                                "qa": -1.302909426086466e-8,
                                "qc": -6.480917136286735e-9,
                                "qdota": -3.6044103175709825e-13,
                                "qdotc": -4.3982596326637839e-10,
                                "taua": 0.000013027709577777855,
                                "tauc": 0.000006483935166648911
                            },
                            {
                                "name": "head_yaw",
                                "qa": 0,
                                "qc": 0,
                                "qdota": 0,
                                "qdotc": 0,
                                "taua": 0,
                                "tauc": 0
                            },
                            {
                                "name": "head_pitch",
                                "qa": 0,
                                "qc": 0,
                                "qdota": 0,
                                "qdotc": 0,
                                "taua": 0,
                                "tauc": 0
                            },
                            {
                                "name": "head_roll",
                                "qa": 0,
                                "qc": 0,
                                "qdota": 0,
                                "qdotc": 0,
                                "taua": 0,
                                "tauc": 0
                            }
                        ],
                        "stanceindex": {}
                    },
                    "timestamp": {
                        "nanos": 2,
                        "seconds": "1"
                    }
                },
                "function": "SonnieGetStates"
            }
        """
        return self._send_request(url=f'/robot/enable_states_listen?frequence={frequence}', method="GET")

    def disable_debug_state(self) -> Dict[str, Any]:
        """ 关闭state调试模式

        Returns:

            Dict:

            - code (int): 返回码，0-表示成功，-1-表示失败
            - msg (str): 返回消息，ok表示正常，失败返回错误信息
            - data (dict): 数据对象，包含具体数据
        """
        return self._send_request(url='/robot/disable_states_listen', method="GET")

    def walk(self, angle: float, speed: float):
        """
        控制GR-01人形设备行走

        ``该请求维持了长链接的方式进行发送``

        Args:

             angle(float): 角度 控制方向，取值范围为正负45度。向左为正，向右为负！(浮点数8位)
             speed(float): 速度 控制前后，取值范围为正负0.8米/秒。向前为正，向后为负！(浮点数8位)
        """
        angle = self._cover_param(angle, 'angle', -45, 45)
        speed = self._cover_param(speed, 'speed', -0.8, 0.8)
        self._send_websocket_msg({
            'command': 'move',
            'data': {
                'angle': angle,
                'speed': speed
            }
        })

    def head(self, roll: float, pitch: float, yaw: float):
        """
        控制GR-01人形头部运动

        ``该请求维持了长链接的方式进行发送``

        Args:

             roll(float): roll（翻滚角）：描述围绕x轴旋转的角度，左转头为负，向右转为正，范围（-17.1887-17.1887）
             pitch(float): pitch（俯仰角）：描述围绕y轴旋转的角度。前点头为正，后点头为负，范围（-17.1887-17.1887）
             yaw(float): yaw（偏航角）：描述围绕z轴旋转的角度。左扭头为负，右扭头为正，范围（-17.1887-17.1887）
        """
        self._send_websocket_msg({
            'command': 'head',
            'data': {
                'roll': self._cover_param(roll, "roll", -17.1887, 17.1887),
                'pitch': self._cover_param(pitch, "pitch", -17.1887, 17.1887),
                'yaw': self._cover_param(yaw, "yaw", -17.1887, 17.1887)
            }
        })

    def upper_body(self, arm: ArmAction = None, hand: HandAction = None):
        """
        上肢预设动作，手、胳膊设定好动作
        Args:
            - arm_action: (str): 胳膊动作:RESET（归零）、LEFT_ARM_WAVE（左挥手）、TWO_ARMS_WAVE（双臂挥手）、ARMS_SWING（甩胳膊）、HELLO（打招呼）
            - hand_action: (str): 手动作:HALF_HANDSHAKE（半握手）、THUMBS_UP（竖大拇指）、OPEN（手张开）、SLIGHTLY_BENT（手微屈）、GRASP（抓握）、TREMBLE（抖动手）、HANDSHAKE（握手）


        Returns:
            - code (int): 返回码，0-表示成功，-1-表示失败
            - msg (str): 返回消息，ok表示正常，失败返回错误信息
            - data (dict): 数据对象，包含具体数据

        """
        upper_body_action = {}
        if arm:
            upper_body_action["arm_action"] = arm.value
        if hand:
            upper_body_action["hand_action"] = hand.value
        return self._send_request(url='/robot/upper_body', method="POST", json=upper_body_action)

    def _get_motor_limit_list(self):
        """ 获取电机限位

        Returns:

            Dict: 返回一个结果集

            - code (int): 返回码，0-表示成功，-1-表示失败
            - msg (str): 返回消息，ok表示正常，失败返回错误信息
            - data (dict): 数据对象，包含具体数据
        """
        response = self._send_request(url='/robot/motor/limit/list', method="GET")
        self.motor_limits = response['data']
        print(f'human_motor_limit: {self.motor_limits}')
        return response

    def _control_svr_start(self):
        for chunk in self._send_request_stream(url='/robot/sdk_ctrl/start', method="GET"):
            print(chunk.decode("utf-8"))

    def _control_svr_log_view(self):
        for chunk in self._send_request_stream(url='/robot/sdk_ctrl/log', method="GET"):
            print(chunk.decode("utf-8"))

    def _control_svr_close(self) -> Dict[str, Any]:
        return self._send_request(url='/robot/sdk_ctrl/close', method="GET")

    def _control_svr_status(self) -> Dict[str, Any]:
        return self._send_request(url='/robot/sdk_ctrl/status', method="GET")

    def _move_joint(self, *args: Motor):
        """ 移动关节

        Args:

            *args: (Motor) : 关节对象，所有字段都必传。具体的限位等信息可以通过 motor_limits 属性获取

        Returns:

        """
        motors = []
        target_list = []
        for motor in args:
            motors.append({"no": motor.no, "orientation": motor.orientation, "angle": motor.angle})
        for item1 in motors:
            for item2 in self.motor_limits:
                if item1.get('no') == item2.get('no') and item1.get('orientation') == item2.get('orientation'):
                    merged_item = {**item1, **item2}
                    target_list.append(merged_item)
        if len(target_list):
            for motor in target_list:
                motor['angle'] = (
                    self._cover_param(motor.get('angle'), 'angle', motor.get('min_angle'), motor.get('max_angle')))
                motor.pop('min_angle', 0)
                motor.pop('max_angle', 0)
                motor.pop('ip', 0)
            self._send_websocket_msg({'command': 'move_joint', 'data': {"command": target_list}})

    def move_motor(self, no, orientation: str, angle: float):
        self._move_joint(Motor(no=str(no), orientation=orientation, angle=angle))

    def set_motor_pd_flag(self, no: str, orientation: str):
        data = {
            'no': no,
            'orientation': orientation
        }
        self._send_websocket_msg({'command': 'check_motor_for_flag', 'data': {"command": data}})
        print(f"Set PID mode on! please reboot motor:  {no}-{orientation}")

    def set_motor_pd(self, no: str, orientation: str, p: float, d: float):
        data = {
            'no': no,
            'orientation': orientation,
            'p': p,
            'd': d
        }
        self._send_websocket_msg({'command': 'check_motor_for_set_pd', 'data': {"command": data}})
        print(f"Parameter setting successful! please reboot motor:  {no}-{orientation}")

    def enable_motor(self, no: str, orientation: str):
        data = {
            'no': no,
            'orientation': orientation
        }
        self._send_websocket_msg({'command': 'enable_motor', 'data': {"command": data}})
        print(f"Motor enabled successful:  {no}-{orientation}")

    def disable_motor(self, no: str, orientation: str):
        data = {
            'no': no,
            'orientation': orientation
        }
        self._send_websocket_msg({'command': 'disable_motor', 'data': {"command": data}})
        print(f"Motor disabled successful:  {no}-{orientation}")

    def get_motor_pvc(self, no: str, orientation: str):
        data = {
            'no': str(no),
            'orientation': orientation
        }
        return self._send_request(url='/robot/motor/pvc', method="POST", json=data)

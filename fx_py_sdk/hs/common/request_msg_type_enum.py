# -*- coding: utf-8 -*-
from enum import Enum, unique


@unique
class RequestMsgTypeEnum(Enum):

    HEART_BEAT = 0   # 心跳
    REQUEST = 1      # 请求
    RESPONSE = 2     # 响应
    NOTIFY = 3       # 推送

    @staticmethod
    def from_id(id: int) -> Enum:
        for name, phase in RequestMsgTypeEnum.__members__.items():
            if phase.value == id:
                return phase

    @staticmethod
    def get_id(enum_value: Enum) -> int:
        return enum_value.value

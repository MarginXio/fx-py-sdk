# -*- coding: utf-8 -*-

class RequestMsgHeader:

    @property
    def sz_header_flag(self):
        return self._sz_header_flag

    @property
    def msg_type(self):
        return self._msg_type

    @msg_type.setter
    def msg_type(self, msg_type):
        self._msg_type = msg_type

    @property
    def proto_fmt_type(self):
        return self._proto_fmt_type

    @proto_fmt_type.setter
    def proto_fmt_type(self, proto_fmt_type):
        self._proto_fmt_type = proto_fmt_type

    @property
    def proto_ver(self):
        return self._proto_ver

    @property
    def serial_no(self):
        return self._serial_no

    @serial_no.setter
    def serial_no(self, serial_no):
        self._serial_no = serial_no

    @property
    def body_len(self):
        return self._body_len

    @body_len.setter
    def body_len(self, body_len):
        self._body_len = body_len

    @property
    def body_sha1(self):
        return self._body_sha1

    @body_sha1.setter
    def body_sha1(self, body_sha1):
        self._body_sha1 = body_sha1

    @property
    def compress_algorithm(self):
        return self._compress_algorithm

    @property
    def reserved(self):
        return self._reserved

    @reserved.setter
    def reserved(self, reserved):
        self._reserved = reserved

    def __init__(self, sz_header_flag="HS",
                 msg_type=0,
                 proto_fmt_type=0,
                 proto_ver=0,
                 serial_no=0,
                 body_len=0,
                 body_sha1=bytearray(128),
                 compress_algorithm=0,
                 reserved=1):
        """
        u8_t szHeaderFlag[2];   //2s-[2字节] 包头起始标志，固定为：“HS”
        u8_t msgType[2];        //1h-[2字节] 消息类型0：心跳 1：请求 2：响应 3：推送
        u8_t protoFmtType;      //B-[1字节] 协议格式类型，0为Protobuf格式
        u8_t protoVer;          //B-[1字节] 协议版本，用于迭代兼容, 目前填0
        u32_t serialNo;         //I-[4字节] 包序列号，用于对应请求包和回包，要求递增
        u32_t bodyLen;          //I-[4字节] 包体长度
        u8_t bodySHA1[128];     //128s-[128字节] 包体原始数据(加密后)的SHA1哈希值
        u8_t compressAlgorithm; //B-[1字节] 压缩算法，0：不压缩
        u8_t reserved[8];       //Q-[8字节] 保留8字节扩展
        """
        self._sz_header_flag = sz_header_flag
        self._msg_type = msg_type
        self._proto_fmt_type = proto_fmt_type
        self._proto_ver = proto_ver
        self._serial_no = serial_no
        self._body_len = body_len
        self._body_sha1 = body_sha1
        self._compress_algorithm = compress_algorithm
        self._reserved = reserved


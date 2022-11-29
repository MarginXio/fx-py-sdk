# -*- coding: utf-8 -*-
from glob import glob
import os
import sys


def protoc(proto_path, src_dir, dest_dir):
    """编译协议文件
    :param proto_path proto文件根目录
    :param src_dir: .proto 源文件目录
    :param dest_dir: python 输出文件目录
    """
    # 检查源目录
    if not os.path.exists(src_dir):
       print(repr(src_dir), 'does not exists.')
       sys.exit(1)

    # 准备目标目录
    if not os.path.exists(dest_dir):
       os.makedirs(dest_dir)
       initpy = os.path.join(dest_dir, '../__init__.py')
       if not os.path.exists(initpy):
           with open(initpy, 'w'):
               pass

    # 编译 .proto 文件
    srcfiles = glob(os.path.join(src_dir, '*.proto'))
    command = ' '.join(['protoc',
                        '--proto_path=' + proto_path,
                        '-I' + src_dir,
                        '--python_out=' + dest_dir,
                        ' '.join(srcfiles)
                       ])
    print(command)
    os.system(command)


if __name__ == '__main__':
    # mac环境使用python处理protobuf
    # 1. 准备工作 $brew install protoc
    # 2. 然后再安装protobuf需要的依赖(依赖如果已经安装就忽略该步) $brew install autoconf automake libtool
    # 3. 验证是否安装成功，protoc版本是否一致 $protoc --version # v3.13.0 $pip show protobuf
    root = os.path.abspath(os.path.dirname(__file__))
    src_array = ["/common/constant",
                 "/common/init",
                 "/common/msg",
                 "/common/response",
                 "/hq/dto",
                 "/hq/notify",
                 "/hq/request",
                 "/hq/request/subscriber",
                 "/hq/response",
                 "/plateform/request",
                 "/plateform/response",
                 "/plateform/vo",
                 "/trade/notify",
                 "/trade/request",
                 "/trade/request/futures",
                 "/trade/response",
                 "/trade/response/futures",
                 "/trade/vo",
                 "/trade/vo/futures"]
    for src in src_array:
        protoc(root, root + src, os.path.join(root, 'out'))
    print("Generated All Proto Python Files Already, Please Do The Next Manually!")

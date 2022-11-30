## 如何使用 (Instructions)

### 1. 克隆代码到本地 (Clone code to local)

```shell
git clone git@github.com:falcons-x/fx-py-sdk.git

cd fx-py-sdk
```

### 2. 构建当前项目的Python虚拟环境 (Construct python virtual environment)

1. 创建虚拟目录 venv (Construct virtual environment)

```
python3 -m venv venv
```

2. 激活虚拟环境 (Activate virtual environment)

```
source ./venv/bin/activate
```
> Windows: venv\Scripts\activate

### 3. 安装项目依赖 (Install dependencies and requirements)

```
pip install -r requirements.txt
```

> 如果网速不行,可以使用腾讯云的pip镜像加速 (If internet speed is slow, can consider using Tencent’s mirror site)
```
pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
```

### 4. 安装sdk (Installing SDK)

> 从其他开发仓库导入sdk包，需要安装sdk, 默认安装到本地python版本的site-packages (To import SDK from other repo, SDK needs to be installed. By default it installs onto local python’s site-packages.)

```shell
 python setup.py install
```

<s>

### 5.使用GRPC (Using GRPC)

```python
from fx_py_sdk.grpc_client import GRPCClient
client = GRPCClient('127.0.0.1:9090')

balances = client.query_all_balances(address="dex1zgpzdf2uqla7hkx85wnn4p2r3duwqzd8cfus97")
print(balances)

balances = client.query_all_balances(address="dex1v0zwwfe3gw2fqdhdnx0hcurh2gzz98z8dagewy")
print(balances)
```

### 6.使用RPC (Using RPC)

```python
from fx_py_sdk.fx_rpc.rpc import HttpRpcClient

rpc_client = HttpRpcClient('http://127.0.0.1:26657')

abci_info = rpc_client.get_abci_info()
print("abci_info:", abci_info)

block_res = rpc_client.get_block_results(100)
print(block_res)
```

### 7.使用Websocket (Using Websocket)

```python
import asyncio
import json
from fx_py_sdk.fx_rpc.ws import FxWebsocket

async def main():
    ws_url = "ws://127.0.0.1:26657/"
    data = {
        "jsonrpc": "2.0",
        "method": "subscribe",
        "params": ["tm.event='NewBlock'"],
        "id": 1
    }

    event = json.dumps(data).encode()
    wss = FxWebsocket(ws_url, event)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### 8.扫描fxdex区块数据，并记录到postgresql (Scan fxdex blockchain data, and record it to postgresql)

**postgres docker execution**

```shell
Docker安装PostgreSQL (Installing PostgreSQL on Docker)

1.拉取镜像 (Pull image)

docker pull postgres

2.启动镜像 (Activate image)

docker run --name postgres -d -p 5432:5432 -e POSTGRES_PASSWORD=123456 postgres

3.进入容器 (Enter container)

docker exec -it postgres psql -U postgres -d postgres

4.创建database (Create database)

create database fxdex;
```

**Create table**

```python
from fx_py_sdk.model.model import Sql
sql = Sql(database="fxdex")
sql.drop_table()
sql.create_table()
```

**启动websocket和rpc同时同步区块 (Websocket and RPC to update simultaneously)** 
>websocket从连接到区块链时的区块开始同步，rpc从数据库断点开始同步直到连接时的区块 (Websocket syncs from the latest block, RPC syncs from database last block to current block)

默认连接本地sql host和port，可以通过环境变量设置 (default environment settings)
```shell
export NETWORK=devnet
export database=postgres
export user=postgres
export password=123456
export host=localhost
export port=5432
```

```python
import asyncio
from fx_py_sdk import scan

async def main():
    """rpc and websocket should run on the same time"""

    ws_scan = scan.WebsocketScan()
    scan.RpcScan(ws_scan)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

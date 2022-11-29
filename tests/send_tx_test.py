from eth_account import Account

from fx_py_sdk.builder import TxBuilder
from fx_py_sdk.grpc_client import GRPCClient
from fx_py_sdk.codec.cosmos.bank.v1beta1.tx_pb2 import MsgSend
from fx_py_sdk.codec.cosmos.base.v1beta1.coin_pb2 import Coin
from google.protobuf.any_pb2 import Any

"""转账交易测试"""


def test_send_tx():
    """导入种子账户"""
    Account.enable_unaudited_hdwallet_features()
    account = Account.from_mnemonic("")

    """获取账户地址"""
    print('address:', account.address)

    """创建GRPC连接"""
    cli = GRPCClient('127.0.0.1:9090')

    """查询chainId"""
    chain_id = cli.query_chain_id()
    print('chain_id:', chain_id)

    """查询账户信息"""
    account_info = cli.query_account_info(account.address)
    print('account, number:', account_info.account_number,
          'sequence:', account_info.sequence)

    """构造 tx_builder 对象"""
    tx_builder = TxBuilder(account, chain_id, account_info.account_number, Coin(
        amount='60', denom='USDT'))

    """构造转账交易msg"""
    send_msg = MsgSend(from_address=account.address, to_address=account.address,
                       amount=[Coin(amount='100', denom='USDT')])
    send_msg_any = Any(type_url='/cosmos.bank.v1beta1.MsgSend',
                       value=send_msg.SerializeToString())

    """构造并签名交易"""
    tx = cli.build_tx(tx_builder, account_info.sequence, [send_msg_any], 5000000)
    print(tx)

    """广播交易"""
    tx_response = cli.broadcast_tx(tx)
    print(tx_response)


if __name__ == '__main__':
    test_send_tx()

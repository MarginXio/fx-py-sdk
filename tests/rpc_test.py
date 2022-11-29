import unittest
from fx_py_sdk.fx_rpc.rpc import *
import os
from fx_py_sdk import constants

network = os.environ[constants.EnvVar.NETWORK]
rpc_url = ""
if network == constants.NetworkENV.LOCAL:
    rpc_url = constants.Network.LOCAL_RPC
elif network == constants.NetworkENV.DEVNET:
    rpc_url = constants.Network.DEVNET_RPC
elif network == constants.NetworkENV.TESTNET:
    rpc_url = constants.Network.TESTNET_RPC
elif network == constants.NetworkENV.MAINNET:
    rpc_url = constants.Network.MAINNET_RPC

rpc_client = HttpRpcClient(rpc_url)


class MyTestCase(unittest.TestCase):

    def test_rpc(self):

        abci_info = rpc_client.get_abci_info()
        print("abci_info:", abci_info)
        assert rpc_client.get_abci_info()

        consensus_state = rpc_client.dump_consensus_state()
        print("consensus_state: ", consensus_state)
        assert rpc_client.dump_consensus_state()

        net_info = rpc_client.get_net_info()
        print("net_info: ", net_info)
        assert rpc_client.get_net_info()

        num_unconfirmed_txs = rpc_client.get_num_unconfirmed_txs()
        print("num_unconfirmed_txs: ", num_unconfirmed_txs)
        assert rpc_client.get_num_unconfirmed_txs()

        status = rpc_client.get_status()
        print("status: ", status)
        assert rpc_client.get_status()

        validators = rpc_client.get_validators(10)
        print("validators: ", validators)
        assert rpc_client.get_validators(10)

        unconfirmed_txs = rpc_client.get_unconfirmed_txs()
        print("unconfirmed_txs: ", unconfirmed_txs)
        assert rpc_client.get_unconfirmed_txs()

        genesis = rpc_client.get_genesis()
        print(genesis)
        assert rpc_client.get_genesis()

    def test_get_block_result(self):
        block_res = rpc_client.get_block_results(100)
        print(block_res)
        assert block_res



if __name__ == '__main__':
    unittest.main()

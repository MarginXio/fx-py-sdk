import unittest
import decimal
from fx_py_sdk.model.model import *
from fx_py_sdk.model.crud import *


class MyTestCase(unittest.TestCase):
    def test_create_database(self):
        sql = Sql()
        sql.create_db("fxdex")

    # def test_create_table(self):
    #     sql = Sql()
    #     sql.create_table("fxdex")

    def test_create_table(self):
        sql = Sql(database="fxdex")
        sql.create_table()

    def test_drop_table(self):
        sql = Sql(database="fxdex")
        sql.drop_table()

    def test_crud(self):
        sql = Crud()
        order_id = "ID-1892-7"
        order = Order(
            block_number=100,
            tx_hash="84E6164550DF980D4FD7AEA68E3B2E3C608B7ADFB730A69C75EEC372CC706D59",
            owner="dex1n58mly6f7er0zs6swtetqgfqs36jaarqlhs528",
            order_id=order_id,
            pair_id="tsla:usdt",
            price=decimal.Decimal(100)
        )
        sql.insert(order)
        order_sql = sql.filterone(Order, Order.order_id == order_id)
        assert order.block_number == order_sql.block_number
        print(order_sql.to_dict())

    def test_orderbook_from_sql(self):
        sql = Crud()
        orderbook = sql.get_orderbook_from_orderbook("tsla:usdt")
        print(orderbook)

    def test_get_orderbook_from_order(self):
        sql = Crud()
        orderbook = sql.get_orderbook_from_order("tsla:usdt")
        print(orderbook)


if __name__ == '__main__':
    unittest.main()

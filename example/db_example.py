from fx_py_sdk.model.crud import Crud
from fx_py_sdk.model.model import *

crud = Crud()

# count orders by address
count = crud.filter_many(Order, Order.owner ==
                         "dex1hajqu45kq3d0ewt7wtevhzlxgjfweja5k2ftgt").count()
print("count: ", count)

# filter with limit and offset
orders = crud.filter_many(
    Order, Order.owner == "dex1hajqu45kq3d0ewt7wtevhzlxgjfweja5k2ftgt").limit(10).offset(2).all()
print([v.to_dict() for v in orders])

# query orderbook
orderbook = crud.get_orderbook_from_order("tsla:usdt")
print(orderbook)

from contextlib import contextmanager
import datetime
from decimal import Decimal
from typing import Dict, Iterable, List, Optional, Union, TypeVar
from sqlalchemy.orm import sessionmaker
from sqlalchemy import case, text
from sqlalchemy.orm.session import Session

from fx_py_sdk.codec.fx.dex.v1.match_pb2 import OrderBook
from sqlalchemy.orm import Query

from fx_py_sdk.model.model import *
from sqlalchemy import or_, and_, func

T = TypeVar("T")

class Crud:
    def __init__(self):
        self.init_session()

    def init_session(self):
        sql = Sql("fxdex")
        self.DBSession = sessionmaker(bind=sql.engine, autocommit=False)
        self.session: Session = self.DBSession()

    @contextmanager
    def auto_session(self):
        session = self.DBSession()
        try:
            yield session
        except Exception as ex:
            logging.error(f"DB Exception: {ex}. Rolling back...", exc_info=True)
            session.rollback()
        finally:
            session.close()

    def insert(self, object):
        with self.auto_session() as session:
            session.add(object)
            session.commit()

    def insert_many(self, objectlist):
        with self.auto_session() as session:
            session.add_all(objectlist)
            session.commit()

    def filterone(self, object: T, *filter) -> T:
        with self.auto_session() as session:
            return session.query(object).filter(*filter).first()

    def filter_many(self, object, *filter) -> Query:
        with self.auto_session() as session:
            return session.query(object).filter(*filter)

    def update(self, object, filter, updic):
        with self.auto_session() as session:
            if not isinstance(filter, Iterable):
                filter = [filter]
            session.query(object).filter(*filter).update(updic)
            session.commit()

    def delete(self, object):
        with self.auto_session() as session:
            session.delete(object)
            session.commit()

    def get_funding_transfer(self, address: str):
        return self.session.query(FundingTransfer).filter(FundingTransfer.owner == address)

    def get_positions(self, address: str):
        return self.session.query(Position).filter(Position.owner == address)

    def get_orders_by_owner(self, owner: str, pair_id: str = None) -> List[Order]:
        filter_conditions = [Order.owner == owner]
        if pair_id:
            filter_conditions.append(Order.pair_id == pair_id)
        return self.session.query(Order).filter(*filter_conditions)

    def get_orders_by_txhash(self, tx_hashes: List[str], pair_id: str = None) -> List[Order]:
        filter_conditions = [Order.pair_id == pair_id]
        if pair_id:
            filter_conditions.append(Order.tx_hash.in_(tx_hashes))
        return self.session.query(Order).filter(*filter_conditions)

    def get_latest_orderbook_record(self, price, pair_id, direction):
        return (self.session.query(Orderbook)
                            .filter(and_(Orderbook.price==price, Orderbook.pair_id==pair_id, Orderbook.direction==direction))
                            .order_by(Orderbook.block_height.desc(), Orderbook.id.desc())
                            .first())

    def get_latest_trade(self, order_id):
        return (self.session.query(Trade)
                            .filter(Trade.order_id==order_id)
                            .order_by(Trade.block_height.desc(), Trade.id.desc())
                            .first())

    def get_orderbook_from_orderbook(self, pair_id: str):
        """get orderbook from sql orderbook table"""
        orderbook_ask = (self.session.query(Orderbook.price, Orderbook.quantity)
                                     .filter(Orderbook.pair_id == pair_id, Orderbook.direction == 'ASK')
                                     .order_by(Orderbook.price)
                                     .limit(100))

        orderbook_bid = (self.session.query(Orderbook.price, Orderbook.quantity)
                                     .filter(Orderbook.pair_id == pair_id, Orderbook.direction == 'BID')
                                     .order_by(Orderbook.price.desc())
                                     .limit(100))
        orderbook = dict()
        asks = []
        bids = []
        for v in orderbook_ask:
            asks.append(dict(zip(v.keys(), v)))
        for v in orderbook_bid:
            bids.append(dict(zip(v.keys(), v)))
        orderbook['asks'] = asks
        orderbook['bids'] = bids
        return orderbook

    def get_orderbook_from_order(self, pair_id: str):
        """get orderbook from sql order table"""
        orderbook = dict()
        asks = []
        bids = []
        ask_items = dict()
        bid_items = dict()
        # ob = dict(ask=[dict(price=0, quantity=0)], bid=[dict(price=0, quantity=0)])
        order_ask = (self.session.query(Order.price, Order.base_quantity)
                                 .filter(Order.pair_id == pair_id,
                                         Order.direction == 'ASK',
                                         or_(Order.status == 'ORDER_PENDING',
                                             Order.status == 'ORDER_PARTIAL_FILLED'))
                                 .order_by(Order.price))

        for order in order_ask:
            order_dict = dict(zip(order.keys(), order))
            if order_dict['price'] in ask_items:
                ask_items[order_dict['price']] = ask_items[order_dict['price']] + order_dict['base_quantity']
            else:
                ask_items[order_dict['price']] = order_dict['base_quantity']

        for key in ask_items.keys():
            item = {'price':key, 'quantity':ask_items[key]}
            asks.append(item)

        order_bid = (self.session.query(Order.price, Order.base_quantity)
                                 .filter(Order.pair_id == pair_id,
                                         Order.direction == 'BID',
                                         or_(Order.status == 'ORDER_PENDING',
                                             Order.status == 'ORDER_PARTIAL_FILLED'))
                                 .order_by(Order.price.desc()))
        for order in order_bid:
            order_dict = dict(zip(order.keys(), order))
            if order_dict['price'] in bid_items:
                bid_items[order_dict['price']] = bid_items[order_dict['price']] + order_dict['base_quantity']
            else:
                bid_items[order_dict['price']] = order_dict['base_quantity']

        for key in bid_items.keys():
            item = {'price':key, 'quantity':bid_items[key]}
            bids.append(item)

        orderbook['asks'] = asks
        orderbook['bids'] = bids
        return orderbook

    def __get_open_order_conditions(self, client_address=None, pair_id=None):
        conditions = [Order.status.in_(('ORDER_PENDING', 'ORDER_PARTIAL_FILLED'))]
        if client_address:
            conditions.append(Order.owner==client_address)
        if pair_id:
            conditions.append(Order.pair_id==pair_id)
        return conditions        

    def query_open_order_count(self, client_address=None, pair_id=None) -> int:
        conditions = self.__get_open_order_conditions(client_address, pair_id)
        return self.session.query(Order).filter(and_(*conditions)).count()

    def query_open_order_count_by_pairid_and_address(self, client_address=None, pair_id=None, limit_records=5) -> int:
        conditions = self.__get_open_order_conditions(client_address, pair_id)
        return (self.session.query(Order.pair_id, Order.owner, func.count(Order.id).label('order_count'))
                            .filter(and_(*conditions))
                            .group_by(Order.pair_id, Order.owner)
                            .order_by(text('order_count DESC'))
                            .limit(limit_records)
                            .all())

    def query_all_locked_fees(self) -> Iterable:
        order_conditions = self.__get_open_order_conditions()
        order_conditions.append(Order.order_type=='ORDER_TYPE_OPEN_POSITION')
        locked_fees = (self.session.query(Order.pair_id, Order.owner, Order.direction, func.sum(Order.locked_fee))
                          .filter(and_(*order_conditions))
                          .group_by(Order.pair_id, Order.owner, Order.direction)
                          .all())
        return locked_fees

    def query_open_order_lock_deposit(self, client_address=None, pair_id=None) -> Decimal:
        # Locked fee
        order_conditions = self.__get_open_order_conditions(client_address, pair_id)
        order_conditions.append(Order.order_type=='ORDER_TYPE_OPEN_POSITION')
        locked_fee = (self.session.query(func.sum(Order.locked_fee))
                                  .filter(and_(*order_conditions))
                                  .first())[0]

        # Margin = SUM(Order.base_quantity * Order.price / Order.leverage) + Added Margin
        position_conditions = self.__get_open_position_conditions(client_address, pair_id)
        margin = (self.session.query(func.sum(Position.margin))
                              .filter(and_(*position_conditions))
                              .first())[0]

        return locked_fee + margin

    def __get_position_conditions(self, client_address=None, pair_id=None):
        conditions = [Position.status=='open']
        if client_address:
            conditions.append(Position.owner==client_address)
        if pair_id:
            conditions.append(Position.pair_id==pair_id)
        return conditions        

    def __query_best_price(self, block_height, direction):
        conditions = [Order.block_height<=block_height,
                      Order.direction==direction,
                      Order.status.in_(('ORDER_PENDING', 'ORDER_PARTIAL_FILLED'))]

        if direction=='BID':
            price_order = Order.price.desc()
        else:
            price_order = Order.price.asc()

        query = (self.session.query(Order.pair_id, Order.price, Order.block_height)
                             .order_by(Order.pair_id, price_order)
                             .distinct(Order.pair_id)
                             .filter(*conditions))
        return query

    def query_mark_prices(self, session=None):
        with (session or self.auto_session()) as session:
            query = (self.session.query(Position.pair_id, Position.mark_price)
                                .filter(and_(Position.mark_price!=0, Position.mark_price!=None))
                                .order_by(Position.pair_id, Position.block_height.desc())
                                .distinct(Position.pair_id))
            return query.all()

    def query_best_bid_ask(self, block_height):
        bid_query = self.__query_best_price(block_height, 'BUY').subquery()
        ask_query = self.__query_best_price(block_height, 'SELL').subquery()

        query = self.session.query(
            func.coalesce(bid_query.c.pair_id, ask_query.c.pair_id),
            bid_query.c.price,
            ask_query.c.price,
            case(
                [(bid_query.c.block_height > ask_query.c.block_height, bid_query.c.block_height)],
                else_ = ask_query.c.block_height
            )
        ).join(
            ask_query,
            bid_query.c.pair_id==ask_query.c.pair_id,
            full=True
        )

        return query.all()

    def query_open_order_margin(self, pair_id: str):
        # Order Margin = Entry Price * Base Quantity / Leverage
        query = """
        SELECT owner, SUM(price * base_quantity / leverage) FROM orders
        WHERE status IN ('ORDER_PENDING', 'ORDER_PARTIAL_FILLED')
        AND order_type = 'ORDER_TYPE_OPEN_POSITION'
        AND pair_id = :pair_id
        GROUP BY 1
        """

        result = self.session.execute(query, params={"pair_id": pair_id}).fetchall()
        return result

    def count(self, object):
        with self.auto_session() as session:
            return session.query(object).count()

    # Exposure
    def __get_exposure(self,
                       addresses: Optional[Union[List[str], str]] = None,
                       pair_ids: Optional[Union[List[str], str]] = None,
                       is_bot: bool = True,
                       as_dollar_value: bool = False) -> Union[Decimal, Dict[str, Decimal]]:
        """
        Gets contract/dollar exposure from database.

        :param addresses:
        :param pair_ids:
        :param is_bot:
        :param as_dollar_value:

        :return: Dictionary of pair_id -> exposure
        """

        # Apply SQL conditions based on parameters
        conditions = [Position.status=='open']

        if addresses:
            if isinstance(addresses, str):
                conditions.append(Position.owner==addresses)
            else:
                conditions.append(Position.owner.in_(addresses))
        elif is_bot:
            bot_addresses = self.session.query(Wallet.address)
            conditions.append(Position.owner.in_(bot_addresses))

        if pair_ids:
            if isinstance(pair_ids, str):
                conditions.append(Position.pair_id==pair_ids)
            else:
                conditions.append(Position.pair_id.in_(pair_ids))

        # Retrieve from DB
        with self.auto_session() as session:
            result = (session.query(Position.pair_id, func.sum(Position.base_quantity * case([(Position.direction=='LONG', 1)], else_=-1)))
                             .filter(*conditions)
                             .group_by(Position.pair_id)
                             .all())
            result_dict = { trade_pair: exposure for trade_pair, exposure in result }

            # Mark quantities to latest mark prices
            if as_dollar_value and result_dict:
                mark_prices = self.query_mark_prices()  # latest mark prices
                for trade_pair, exposure in result_dict.items():
                    for mark_pair, mark_price in mark_prices:
                        if trade_pair==mark_pair:
                            result_dict[trade_pair] = exposure * mark_price
                            break

        if isinstance(pair_ids, str):
            return result_dict.get(pair_ids, Decimal('0'))
        else:
            return result_dict

    def get_contract_exposure(self,
                              addresses: Optional[Union[List[str], str]] = None,
                              pair_ids: Optional[Union[List[str], str]] = None,
                              is_bot: bool = True):
        """Returns a single net contract quantity exposure if pair_id is provided. Otherwise, returns dictionary."""
        return self.__get_exposure(addresses, pair_ids, is_bot)
    
    def get_dollar_exposure(self,
                            addresses: Optional[Union[List[str], str]] = None,
                            pair_ids: Optional[Union[List[str], str]] = None,
                            is_bot: bool = True):
        """Returns a single exposure marked to mark price if pair_id is provided. Otherwise, returns dictionary."""
        return self.__get_exposure(addresses, pair_ids, is_bot, as_dollar_value=True)

    def get_funding_transfers(self, address: str=None, pair_id: str=None, from_datetime: datetime.datetime=None):
        limit_records = 100

        conditions = []
        if address:
            conditions.append(FundingTransfer.owner==address)
        if pair_id:
            conditions.append(FundingTransfer.pair_id==pair_id)
        if from_datetime:
            conditions.append(Block.time>=from_datetime)

        query = (self.session.query(FundingTransfer, Block.time)
                             .join(Block, FundingTransfer.block_height==Block.height)
                             .filter(*conditions)
                             .order_by(Block.height.asc())
                             .limit(limit_records))
        return query.all()

    def update_realized_pnl_logs(self, start_block_height: int, end_block_height: int, pair_id: str = None):
        pair_id_condition = "CASE WHEN :pair_id IS NULL THEN TRUE ELSE {}.pair_id = :pair_id END"
        update_query = f"""
        INSERT INTO realized_pnl_log
            SELECT owner, pair_id, SUM(realized_pnl) AS realized_pnl, SUM(funding_gain) AS funding_gain, SUM(liquidated_margin) AS liquidated_margin, :end_block_height AS block_height FROM (
                SELECT
                    COALESCE(q1.owner, q2.owner, q3.owner, q4.owner) AS owner,
                    COALESCE(q1.pair_id, q2.pair_id, q3.pair_id, q4.pair_id) AS pair_id,
                    COALESCE(q1.realized_pnl, 0) + COALESCE(q4.realized_pnl, 0) AS realized_pnl,
                    COALESCE(q2.funding_fee, 0) + COALESCE(q4.funding_gain, 0) AS funding_gain,
                    COALESCE(q3.margin, 0) + COALESCE(q4.liquidated_margin, 0) AS liquidated_margin,
                    :end_block_height AS block_height
                FROM
                    (SELECT
                        p.owner,
                        p.pair_id,
                        SUM(p.realized_pnl) AS realized_pnl
                    FROM positioning p
                    LEFT JOIN block b on p.block_height=b.height
                    WHERE
                        p.block_height BETWEEN :start_block_height AND :end_block_height
                        AND COALESCE(p.is_batch_update, FALSE) = FALSE
                        AND {pair_id_condition.format('p')}
                    GROUP BY 1,2) q1
                FULL OUTER JOIN
                    (SELECT
                        f.owner,
                        f.pair_id,
                        SUM(funding_fee) AS funding_fee
                    FROM funding_transfer f
                    WHERE
                        f.block_height BETWEEN :start_block_height AND :end_block_height
                        AND {pair_id_condition.format('f')}
                    GROUP BY 1,2) q2 ON q1.owner = q2.owner AND q1.pair_id = q2.pair_id
                FULL OUTER JOIN
                    (SELECT
                        p.owner,
                        p.pair_id,
                        SUM(margin) AS margin
                    FROM position p
                    WHERE
                        p.block_height BETWEEN :start_block_height AND :end_block_height
                        AND p.status='liquidated'
                        AND {pair_id_condition.format('p')}
                    GROUP BY 1,2) q3 ON q1.owner = q3.owner AND q1.pair_id = q3.pair_id
                FULL OUTER JOIN
                    (SELECT DISTINCT ON (owner, pair_id) owner, pair_id, realized_pnl, funding_gain, liquidated_margin, block_height
                     FROM realized_pnl_log log
                     WHERE {pair_id_condition.format('log')}
                     ORDER BY owner ASC, pair_id ASC, block_height DESC) q4 ON q1.owner = q4.owner AND q1.pair_id = q4.pair_id
                ) q
            GROUP BY 1,2
        """

        self.session.execute(update_query, params=
        {
            'start_block_height': start_block_height,
            'end_block_height': end_block_height,
            'pair_id': pair_id
        })
        self.session.commit()

    def delete_data(self,
                    from_block_height: int,
                    verbose=True,
                    pair_id=None):
        """
        Deletes all data starting from block height
        :param from_block_height: Block height to start deleting data from (inclusive)
        :param verbose: If True, logs error/success messages
        :param pair_id: Deletes only data relating to `pair_id`
        """
        if not from_block_height:
            if verbose:
                logging.warning('No initial block height specified, delete_data() did not remove any data')
            return

        block_height_condition = "block_height >= bh"
        pair_id_condition = "CASE WHEN pid IS NULL THEN TRUE ELSE pair_id=pid END"

        delete_query = f"""
        DO $$
        DECLARE bh integer;
        DECLARE pid varchar;
        BEGIN
            SELECT :from_block_height INTO bh;
            SELECT :pair_id INTO pid;

            DELETE FROM block WHERE height >= bh AND {pair_id_condition};
            DELETE FROM funding_transfer WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM orderbook WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM orders WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM position WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM trade WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM positioning WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM error WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM transfer WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM margin WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM oracle_price WHERE {block_height_condition} AND {pair_id_condition};
            DELETE FROM realized_pnl_log wHERE {block_height_condition} AND {pair_id_condition};

            UPDATE error_log SET height=el.height
            FROM (SELECT CASE WHEN bh<height THEN bh-1 ELSE height END as height FROM error_log WHERE {pair_id_condition}) el
            WHERE {pair_id_condition};
        END $$;"""

        try:
            self.session.execute(
                statement = delete_query,
                params={
                    'from_block_height': from_block_height,
                    'pair_id': pair_id
                }
            )
            self.session.commit()
            if verbose:
                logging.info(f'All data from {from_block_height} onward (inclusive) removed from database')
        except Exception as ex:
            if verbose:
                logging.error(f'Could not delete data from {from_block_height}: {ex}')

    def query_latest_block_height(self):
        """Query latest valid block height from database (where both `block_processed` and `tx_events_processed` are true)"""
        return (self.session.query(func.max(Block.height))
                    .filter(and_(Block.tx_events_processed==True, Block.block_processed==True))
                    .scalar())

    def query_lowest_incomplete_height(self, pair_id: str=None):
        """Query lowest block height where either `block_processed` or `tx_events_processed` is false (i.e. block processing is incomplete)"""
        if pair_id:
            return (self.session.query(func.min(Block.height))
                                .filter(
                                    and_(
                                        Block.pair_id==pair_id,
                                        or_(Block.block_processed==False, Block.tx_events_processed==False)
                                    )                                
                                ).scalar())
        else:
            return (self.session.query(func.min(Block.height))
                                .filter(or_(Block.block_processed==False, Block.tx_events_processed==False))
                                .scalar())


    def delete_data_from_lowest_incomplete_height(self,
                                                  pair_id: str = None,
                                                  default_block_height: int = None):
        """
        Deletes data from max block height (i.e. removes topmost block data)
        :param pair_id: `pair_id` of data to delete
        :param default_block_height: In case data is complete, deletes from this height instead
        """
        block_height = self.query_lowest_incomplete_height() or default_block_height
        self.delete_data(block_height, pair_id=pair_id)
            
# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import (
    Index, Column, Integer, String, Boolean,
    Numeric, DateTime, UniqueConstraint
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fx_py_sdk import constants
import os
import logging
import pandas as pd

Base = declarative_base()

def to_dict(self):
    dict_attrs = dict()
    for col in self.__table__.columns:
        attr = getattr(self, col.name, None)
        if attr is not None:
            dict_attrs[col.name] = attr
    return dict_attrs

Base.to_dict = to_dict

class Order(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        UniqueConstraint('order_id', 'pair_id'),
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    block_height = Column(Integer, index=True)
    order_id = Column(String(100), nullable=False)
    tx_hash = Column(String(64))
    owner = Column(String(42))
    liquidation_owner = Column(String(42))
    pair_id = Column(String(20), index=True)
    direction = Column(String(10), index=True)
    price = Column(Numeric, index=True)
    base_quantity = Column(Numeric, index=True)
    quote_quantity = Column(Numeric)
    filled_quantity = Column(Numeric)
    last_filled_quantity = Column(Numeric)
    filled_avg_price = Column(Numeric)
    leverage = Column(Integer)
    status = Column(String(50), index=True)
    order_type = Column(String(50), index=True)
    cost_fee = Column(Numeric)
    locked_fee = Column(Numeric)
    fee_denom = Column(String(10))
    open_block_height = Column(Integer, index=True)
    cancel_block_height = Column(Integer)
    filled_block_height = Column(Integer)
    cancel_time = Column(DateTime)
    position_id = Column(Integer)
    deal_fee = Column(Numeric)
    maker = Column(Boolean)
    block_height = Column(Integer, index=True)
    initial_base_quantity = Column(Numeric)

class Position(Base):
    __tablename__ = 'position'

    position_id = Column(Integer, primary_key=True, nullable=False)
    owner = Column(String(42), index=True)
    pair_id = Column(String(20), primary_key=True)
    direction = Column(String(10), index=True)
    entry_price = Column(Numeric)
    mark_price = Column(Numeric)
    liquidation_price = Column(Numeric)
    base_quantity = Column(Numeric)
    margin = Column(Numeric)
    leverage = Column(Integer)
    realized_pnl = Column(Numeric)
    unrealized_pnl = Column(Numeric)
    margin_rate = Column(Numeric)
    initial_margin = Column(Numeric)
    pending_order_quantity = Column(Numeric)
    status = Column(String(20))  # open, close
    open_height = Column(Integer, index=True)
    close_height = Column(Integer, index=True)
    block_height = Column(Integer, index=True)
    last_order_fill_height = Column(Integer)

class Orderbook(Base):
    __tablename__ = 'orderbook'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    price = Column(Numeric)
    quantity = Column(Numeric)
    direction = Column(String(20))
    pair_id = Column(String(20))
    block_height = Column(Integer)

class Trade(Base):
    __tablename__ = 'trade'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    block_height = Column(Integer, index=True)
    deal_price = Column(Numeric, index=True)
    matched_quantity = Column(Numeric, index=True)
    order_id = Column(String(100), nullable=False, unique=False)
    owner = Column(String(42), index=True)
    liquidation_owner = Column(String(42))
    pair_id = Column(String(20), index=True)
    direction = Column(String(10), index=True)
    price = Column(Numeric)  #entry price
    base_quantity = Column(Numeric)
    quote_quantity = Column(Numeric)
    filled_quantity = Column(Numeric)
    filled_avg_price = Column(Numeric)
    order_type = Column(String(50))
    cost_fee = Column(Numeric)
    locked_fee = Column(Numeric)
    fee_denom = Column(String(10))
    deal_fee = Column(Numeric)
    maker = Column(Boolean)
    position_id = Column(Integer)
    block_height = Column(Integer, index=True)

class FundingTransfer(Base):
    __tablename__ = 'funding_transfer'
    __table_args__ = (
        Index('ix_funding_transfer_owner_pairid_height', 'owner', 'pair_id', 'block_height'),
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    position_id = Column(Integer)
    pair_id = Column(String(20), index=True)
    owner = Column(String(42), index=True)
    funding_fee = Column(Numeric)
    block_height = Column(Integer, index=True)

class Block(Base):
    __tablename__ = 'block'
    __table_args__ = (
        Index('ix_block_height_pair_id', 'height', 'pair_id'),
    )

    height = Column('height', Integer, primary_key=True, autoincrement=False)
    pair_id = Column(String(20), primary_key=True)
    time = Column(DateTime, index=True)
    block_processed = Column(Boolean, default=False, index=True)
    tx_events_processed = Column(Boolean, default=False, index=True)

class Tx(Base):
    __tablename__ = 'tx'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    sender = Column(String(50))
    send_time = Column(String(50))
    type = Column(String(50))  # send_coin, create_order, close_position_order, cancel_order
    tx_hash = Column(String(66), index=True)
    result = Column(String(66))  # error, success

""" auxillary helper classes """
class Positioning(Base):
    __tablename__ = 'positioning'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    owner = Column(String(42), index=True)
    pair_id = Column(String(20), index=True)
    entry_price = Column(Numeric)
    mark_price = Column(Numeric)
    base_quantity = Column(Numeric)
    realized_pnl = Column(Numeric)
    unrealized_pnl = Column(Numeric)
    margin = Column(Numeric)
    order_margin = Column(Numeric)
    direction = Column(String(10))
    position_id = Column(Integer, index=True)
    locked_fees = Column(Numeric)
    block_height = Column(Integer, index=True)
    is_batch_update = Column(Boolean, default=False, index=True)

# Logs realized P&Ls for efficient cumulative calculation
class Realized_Pnl_Log(Base):
    __tablename__ = 'realized_pnl_log'

    owner = Column(String(42), index=True, primary_key=True)
    pair_id = Column(String(42), index=True, primary_key=True)
    realized_pnl = Column(Numeric)
    funding_gain = Column(Numeric)
    liquidated_margin = Column(Numeric)
    block_height = Column(Integer, index=True, primary_key=True)

class Balance(Base):
    __tablename__ = 'balance'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    owner = Column(String(42), index=True)
    token = Column(String(70), index=True)
    amount = Column(Numeric)
    batch_time = Column(DateTime, index=True)
    time = Column(DateTime)
    pair_id = Column(String(20), index=True)

class Pricing(Base):
    __tablename__ = 'pricing'
    __table_args__ = (
        UniqueConstraint('pair_id', 'block_height'),
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pair_id = Column(String(20), index=True)
    best_bid = Column(Numeric)
    best_ask = Column(Numeric)
    oracle_price = Column(Numeric)
    mark_price = Column(Numeric)
    block_height = Column(Integer, index=True)

    def __repr__(self) -> str:
        return (
            f"[{self.pair_id}] Bid: {self.best_bid}, Ask: {self.best_ask}, " +
            f"Oracle px: {self.oracle_price}, Mark px: {self.mark_price} " +
            f"(blk ht: {self.block_height})"
        )

class FundingRate(Base):
    __tablename__ = 'funding_rate'
    __table_args__ = (
        UniqueConstraint('pair_id', 'block_height'),
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pair_id = Column(String(20), index=True)
    rate = Column(Numeric)
    # funding_times = Column(Integer)
    block_height = Column(Integer, index=True)

class Wallet(Base):
    __tablename__ = 'wallet'
    __table_args__ = (
        UniqueConstraint('address', 'pair_id'),
    )

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    address = Column(String(42))
    owner = Column(String(100), index=True)
    pair_id = Column(String(20))
    comment = Column(String(256))
    leverage = Column(Integer)

class Margin(Base):
    __tablename__ = 'margin'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    add_amount = Column(Numeric)
    position_id = Column(Integer, index=True)
    pair_id = Column(String(20), index=True)
    mark_price = Column(Numeric)
    base_quantity = Column(Numeric)
    direction = Column(String(10))
    owner = Column(String(100), index=True)
    leverage = Column(Integer)
    entry_price = Column(Numeric)
    liquidation_price = Column(Numeric)
    margin_rate = Column(Numeric)
    margin = Column(Numeric)
    block_height = Column(Integer, index=True)

class LockedFee(Base):
    __tablename__ = 'locked_fee'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pair_id = Column(String(20), index=True)
    owner = Column(String(100), index=True)
    direction = Column(String(10))
    fees = Column(Numeric)
    block_height = Column(Integer, index=True)

class Error(Base):
    __tablename__ = 'error'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    pair_id = Column(String(20), index=True)
    sender = Column(String(42), index=True)
    log = Column(String(1024))
    block_height = Column(Integer, index=True)

class ErrorLog(Base):
    __tablename__ = 'error_log'
    height = Column(Integer)
    pair_id = Column(String(20), primary_key=True)

class Transfer(Base):
    __tablename__ = 'transfer'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    sender = Column(String(100), index=True)
    recipient = Column(String(100), index=True)
    amount = Column(Numeric)
    token = Column(String(70), index=True)
    block_height = Column(Integer, index=True)
    pair_id = Column(String(20))
class OraclePrice(Base):
    __tablename__ = 'oracle_price'

    market_id = Column('pair_id', String(20), primary_key=True, index=True)
    price = Column(Numeric)
    block_height = Column(Integer, primary_key=True, index=True)

class TradePair(Base):
    __tablename__ = 'trade_pair'
    pair_id = Column(String(20), primary_key=True)

class HedgingOrder(Base):
    __tablename__ = 'hedging_order'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    dex_order_id = Column(String(100))
    dex_trade_id = Column(Integer)
    order_id = Column(String(100))      # Hedging exchange order ID
    order_type = Column(String(50))
    status = Column(String(50), index=True)
    price = Column(Numeric)
    quantity = Column(Numeric)
    direction = Column(String(10))
    symbol = Column(String(20), index=True)
    exchange = Column(String(20), index=True)
    time = Column(DateTime)
    commission = Column(Numeric, default=0)
    gas_fee = Column(Numeric, default=0)

class HedgingTrade(Base):
    __tablename__ = 'hedging_trade'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    order_id = Column(String(100))      # Hedging exchange order ID
    trade_id = Column(String(100))      # Hedging exchange trade ID (if any)
    dex_trade_id = Column(Integer)
    order_type = Column(String(50))
    status = Column(String(50), index=True)
    price = Column(Numeric)
    quantity = Column(Numeric)
    direction = Column(String(10))
    symbol = Column(String(20), index=True)
    exchange = Column(String(20), index=True)
    time = Column(DateTime)

class Sql:
    def __init__(self, database: str = "postgres", user: str = "postgres", password: str = "123456", host: str = "localhost",
                 port: str = "5432"):

        database = os.environ.get(constants.DB.Database, database)
        user = os.environ.get(constants.DB.User, user)
        password = os.environ.get(constants.DB.Password, password)
        host = os.environ.get(constants.DB.Host, host)  # 47.90.177.191
        port = os.environ.get(constants.DB.Port, port)

        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        try:
            self.connect(database)
            logging.info(f'Connected to database {database}')
        except Exception as ex:
            logging.error(f'Failed connecting to database {database}: {ex}')

    def connect(self, db: str):
        """ Connect to the PostgreSQL database server """

        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(self.user, self.password, self.host, self.port, db)
        print(url)
        self.engine = sqlalchemy.create_engine(url, client_encoding='utf8',
                                               pool_pre_ping=True,
                                               pool_recycle=3600)
        self.meta = sqlalchemy.MetaData(bind=self.engine)
        self.session = sessionmaker(bind=self.engine)

    def create_table(self):
        # Creates database schema
        Base.metadata.create_all(self.engine)

    def drop_table(self):
        # Terminates all processes connected to db
        self.engine.execute(f'''
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '{self.database}'
AND pid <> pg_backend_pid();''')

        # Drop all tables
        Base.metadata.drop_all(self.engine)

    def initialize_table(self, csv_filename: str, table_name: str):
        try:
            df = pd.read_csv(csv_filename)
            df.to_sql(table_name, self.engine, if_exists='append', index=False)
        except:
            return

    def initialize_wallets(self):
        self.initialize_table('wallets.csv', 'wallet')

    def initialize_trade_pairs(self):
        self.initialize_table('trade_pairs.csv', 'trade_pair')

    def initialize_error_log_height(self, pair_id, starting_height=None):
        with self.session() as session:
            if not starting_height:
                starting_height = session.execute('SELECT MAX(height) FROM block').first()[0] or 1

            session.execute(f"""
                INSERT INTO error_log (height, pair_id)
                SELECT {starting_height}, '{pair_id}'
                WHERE NOT EXISTS (SELECT * FROM error_log WHERE pair_id = '{pair_id}')
                """)
            session.commit()

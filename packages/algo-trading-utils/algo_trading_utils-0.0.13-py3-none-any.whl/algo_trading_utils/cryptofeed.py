import time
import pandas as pd
from enum import Enum
from datetime import datetime, timezone
from .postgres import get_cursor


class StreamTypes(Enum):
    L2_BOOK = 'l2_book'
    TRADES = 'trades'
    OPEN_INTEREST = 'open_interest'
    LIQUIDATIONS = 'liquidations'
    FUNDING = 'funding'
    CANDLES = 'candles'
    TICKER = 'ticker'


def get_data(
        asset: str,
        stream_type: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        orderbook_type='delta',
        environment='prod'
) -> pd.DataFrame:
    # check params
    assert orderbook_type.lower() in ['delta', 'snapshot']
    assert environment.lower() in ['dev', 'prod']
    assert asset_type.lower() in ['spot', 'futures']

    with get_cursor('postgres', environment) as cursor:
        if not end:
            end = datetime.now(tz=timezone.utc)

        # if the orderbook type is a snapshot
        postfix = ''
        if orderbook_type == 'snapshot':
            postfix = '_snapshot'

        # convert datetime to string
        start_string = start.strftime('%Y-%m-%d %H:%M:%S')
        end_string = end.strftime('%Y-%m-%d %H:%M:%S')

        # run sql query
        print('starting sql query...')
        start = time.time()
        cursor.execute(
            f"SELECT * FROM cryptofeed_{environment.lower()}_{stream_type.lower()}_{asset_type.lower()}_{asset.lower()}_usdt{postfix} WHERE timestamp BETWEEN '{start_string}' AND '{end_string}';"
        )
        end = time.time()
        print(f'sql query finished in {round(end - start, 2)} secs')
        return pd.DataFrame(cursor.fetchall())


def get_all_tables(
        environment='prod'
) -> pd.DataFrame:

    with get_cursor('postgres', environment) as cursor:
        # run sql query
        print('starting sql query...')
        start = time.time()
        cursor.execute(
            """
            SELECT c.relname
            FROM pg_class AS c
            WHERE NOT EXISTS (SELECT 1 FROM pg_inherits AS i
                              WHERE i.inhrelid = c.oid)
              AND c.relkind IN ('r', 'p') AND starts_with(c.relname, 'cryptofeed_');
            """
        )
        end = time.time()
        print(f'sql query finished in {round(end - start, 2)} secs')
        return [i['relname'] for i in cursor.fetchall()]


def get_l2_order_book(
        asset: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        data_type='delta',
        environment='prod'
) -> pd.DataFrame:
    return get_data(
        asset=asset,
        stream_type='l2_book',
        start=start,
        end=end,
        asset_type=asset_type,
        orderbook_type=data_type,
        environment=environment
    )


def get_ticker(
        asset: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        environment='prod'
) -> pd.DataFrame:
    return get_data(
        asset=asset,
        stream_type='ticker',
        start=start,
        end=end,
        asset_type=asset_type,
        environment=environment
    )


def get_trades(
        asset: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        environment='prod'
) -> pd.DataFrame:
    return get_data(
        asset=asset,
        stream_type='trades',
        start=start,
        end=end,
        asset_type=asset_type,
        environment=environment
    )


def get_open_interest(
        asset: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        environment='prod'
) -> pd.DataFrame:
    return get_data(
        asset=asset,
        stream_type='open_interest',
        start=start,
        end=end,
        asset_type=asset_type,
        environment=environment
    )


def get_liquidations(
        asset: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        environment='prod'
) -> pd.DataFrame:
    return get_data(
        asset=asset,
        stream_type='liquidations',
        start=start,
        end=end,
        asset_type=asset_type,
        environment=environment
    )


def get_funding(
        asset: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        environment='prod'
) -> pd.DataFrame:
    return get_data(
        asset=asset,
        stream_type='funding',
        start=start,
        end=end,
        asset_type=asset_type,
        environment=environment
    )


def get_candles(
        asset: str,
        start: datetime,
        end: datetime = None,
        asset_type='spot',
        environment='prod'
) -> pd.DataFrame:
    return get_data(
        asset=asset,
        stream_type='candles',
        start=start,
        end=end,
        asset_type=asset_type,
        environment=environment
    )

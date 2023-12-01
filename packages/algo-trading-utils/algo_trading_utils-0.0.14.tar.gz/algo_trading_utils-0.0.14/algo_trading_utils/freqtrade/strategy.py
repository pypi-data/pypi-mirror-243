import os
import logging
import numpy as np  # noqa
import pandas as pd  # noqa
from datetime import datetime
import sentry_sdk
from tickerdax.client import TickerDax
from freqtrade.strategy.interface import IStrategy


class StrategyBase(IStrategy):
    def __init__(self, *args, **kwargs):
        # if this is a production deployment of freqtrade it should have a sentry io dsn to report error to
        sentry_dsn = os.environ.get('SENTRY_IO_DSN')
        if sentry_dsn:
            sentry_sdk.init(
                dsn=sentry_dsn,
                # Set traces_sample_rate to 1.0 to capture 100%
                # of transactions for performance monitoring.
                environment=os.environ.get('GITHUB_USERNAME'),
                traces_sample_rate=1.0,
            )
            sentry_sdk.set_tag("bot.db_name", os.environ.get('DB_NAME'))

        super().__init__(*args, **kwargs)
        self.tickerdax_client = TickerDax()

        self._leverage_amounts = ['1', '2', '3', '4', '5', '']
        self._ups = ['L', 'UP']
        self._downs = ['S', 'DOWN']
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(level=logging.DEBUG)
        self.external_dataframes = {}

    @staticmethod
    def get_symbol(pair, stake_currency):
        pair = pair.strip()
        for direction in ['S', 'L', 'UP', 'DOWN', '']:
            for number in ['1', '2', '3', '4', '5', '']:
                if ':' in pair:
                    post_fix = f'{number}{direction}/{stake_currency}:{stake_currency}'
                else:
                    post_fix = f'{number}{direction}/{stake_currency}'
                if pair.endswith(post_fix):
                    return pair.replace(post_fix, '')
        return pair

    @staticmethod
    def convert_to_numbers(series):
        converted_values = []
        for value in series.tolist():
            if value in ['up']:
                converted_values.append(1)
            elif value in ['down']:
                converted_values.append(-1)
            else:
                converted_values.append(0)

        return pd.Series(converted_values)

    def get_direction(self, pair):
        for down in self._downs:
            for leverage in self._leverage_amounts:
                if f'{leverage}{down}/' in pair:
                    return -1

        for up in self._ups:
            for leverage in self._leverage_amounts:
                if f'{leverage}{up}/' in pair:
                    return 1
        return 0

    @staticmethod
    def minify_dataframe(dataframe, data_keys):
        for column_name in dataframe.columns:
            if column_name not in data_keys + ['date_external_data']:
                dataframe.drop(column_name, axis=1, inplace=True)
        return dataframe

    def get_external_dataframe(self, route, symbol, since, till, data_keys):
        items = self.tickerdax_client.get_route(
            route=route,
            symbols=[symbol],
            since=since,
            till=till
        )
        # create a dataframe with the external data
        external_dataframe = pd.DataFrame([{
            'timestamp': item['timestamp'],
            **{data_key: item['data'][data_key] for data_key in data_keys if item.get('data')}
        } for item in items])

        # only save the dataframe if there are items
        if items:
            # convert the unix timestamps to panda timestamps
            external_dataframe['date_external_data'] = pd.to_datetime(
                external_dataframe['timestamp'],
                unit='s',
                origin='unix',
                utc=True
            )

            # # only add the specified data keys to save memory
            # external_dataframe = self.minify_dataframe(external_dataframe, data_keys)

            # save the external dataframe in memory
            self.external_dataframes[symbol] = external_dataframe

        return external_dataframe

    def add_external_data(self, dataframe, metadata, route, data_keys):
        symbol = self.get_symbol(metadata['pair'], self.stake_currency)

        # check for existing dataframe in memory
        since = dataframe['date'].iloc[0].to_pydatetime()
        till = dataframe['date'].iloc[-1].to_pydatetime()

        # get all external data for the range of the dataframe dates to populate as many rows as possible
        external_dataframe = self.get_external_dataframe(
            route=route,
            symbol=symbol,
            since=since,
            till=till,
            data_keys=data_keys
        )

        # merge the existing dataframe with the external dataframe using the date columns
        dataframe = dataframe.merge(
            external_dataframe,
            left_on='date',
            right_on='date_external_data',
            how='left'
        )

        return dataframe

    def get_spot_pair(self, pair):
        for direction in self._ups + self._downs:
            for leverage in self._leverage_amounts:
                pair = pair.replace(f'{leverage}{direction}/', '/').split(':')[0]
        return pair

    def get_informative_spot_pairs(self):
        informative_pairs = []
        for pair in self.dp.current_whitelist():
            pair = self.get_spot_pair(pair)
            if (pair, self.timeframe) not in informative_pairs:
                informative_pairs.append((pair, self.timeframe))

        return informative_pairs

    @staticmethod
    def remove_no_volume(dataframe):
        no_volume = []
        for index, value in dataframe['volume'].items():
            if value == 0:
                no_volume.append(index)

        return dataframe.drop(no_volume)

    @staticmethod
    def remove_close_times(dataframe):
        closed = []
        now = datetime.utcnow()
        exchange_open = datetime(year=now.year, month=now.month, day=now.day, hour=13, minute=0)
        exchange_close = datetime(year=now.year, month=now.month, day=now.day, hour=20, minute=0)

        for index, value in dataframe['date'].items():
            # remove weekends
            if value.weekday() in [5, 6]:
                closed.append(index)

            # remove close times during the week
            if exchange_open.time() >= value.time() or value.time() >= exchange_close.time():
                closed.append(index)

        return dataframe.drop(closed)

    @staticmethod
    def print_dataframe_terminal(
            dataframe,
            title,
            table_format='psql',
            show_index=False,
            head=None,
            tail=None,
            logger_name=__name__
    ):
        pd.set_option('display.max_columns', None)
        if head:
            dataframe = dataframe.head(head)
        if tail:
            dataframe = dataframe.tail(tail)
        wrapped_dataframe = pd.DataFrame(
            {title: [dataframe.to_markdown(
                tablefmt=table_format,
                index=show_index
            )]}
        )
        logger = logging.getLogger(logger_name)
        logger.setLevel(level=logging.INFO)
        logger.info(f'\n{wrapped_dataframe.to_markdown(tablefmt=table_format, index=False)}')

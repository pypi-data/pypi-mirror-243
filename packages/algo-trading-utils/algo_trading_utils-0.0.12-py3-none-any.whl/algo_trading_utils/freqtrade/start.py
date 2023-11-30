import os
import re
import sys
import json
import logging
import psycopg2
import subprocess
from datetime import datetime

# TODO add back
# from algo_trading_client import downloader

logging.basicConfig(level=logging.INFO)


class StartBot:
    def __init__(self):
        self._envs = self.get_envs()
        self._name = self._envs.get('NAME')
        self._repo = self._envs.get('REPO')
        self._db_name = self._envs.get('DB_NAME')

        self._db_host = self._envs.get('DB_HOST')
        self._db_user = self._envs.get('DB_USER')
        self._db_password = self._envs.get('DB_PASSWORD')
        self._commit = self._envs.get('COMMIT', 'master')
        self._github_username = self._envs.get('GITHUB_USERNAME')
        self._db_url = f'postgresql+psycopg2://{self._db_user}:{self._db_password}@{self._db_host}:5432/{self._db_name}'
        os.environ.update(self._envs)

    def get_cursor(self, db_name):
        postgres_connection = psycopg2.connect(
            database=db_name,
            user=self._db_user,
            password=self._db_password,
            host=self._db_host,
            port='5432'
        )
        postgres_connection.autocommit = True

        # Creating a cursor object using the cursor() method
        return postgres_connection.cursor()

    def create_database(self):
        # Creating a database
        try:
            with self.get_cursor('postgres') as cursor:
                cursor.execute(f'CREATE DATABASE {self._db_name}')
            print(f'New database "{self._db_name}" created successfully!')
        except psycopg2.errors.DuplicateDatabase:
            print(f'Database "{self._db_name}" already exists!')

    def _create_comment(self, data):
        # Preparing query to create a database
        commit_url = f'https://github.com/{self._github_username}/{self._repo}/commit/{self._commit}'

        # add data as a comment
        sql = f"COMMENT ON DATABASE {self._db_name} IS 'commit_url: {commit_url}\n"
        for key, value in data.items():
            sql += f'{key}: {value}\n'
        sql += "'"

        # Add comment
        with self.get_cursor('postgres') as cursor:
            cursor.execute(sql)
        print(f'Added "{self._db_name}" comment!')

    def _get_database_comment_data(self):
        data = {}
        with self.get_cursor('postgres') as cursor:
            cursor.execute(
                'select description from pg_shdescription '
                'join pg_database on objoid = pg_database.oid '
                f"where datname = '{self._db_name}'"
            )
            for comment in next(cursor)[0].split('\n'):
                if comment:
                    key, value = list(filter(None, comment.strip().split(': ')))
                    data[key.lower().replace(' ', '_')] = value
        return data

    @staticmethod
    def get_envs():
        env_file = os.environ.get('ENV_FILE_NAME')
        if env_file:
            # read the env file
            with open(f'/tmp/compose/{env_file}') as env_file:
                envs = {line.split('=')[0]: line.split('=')[1].strip("'").strip('"') for line in env_file.readlines()
                        if '=' in line}

                # update variables in the env file with the system variables
                envs.update(os.environ)
                return envs
        return {}

    def _get_database_names(self):
        table_names = []
        with self.get_cursor('postgres') as cursor:
            cursor.execute('SELECT datname FROM pg_database WHERE datistemplate = false')

            for row in cursor:
                if row and row[0].startswith(self.type):
                    table_names.append(row[0])
        return table_names

    def get_databases(self):
        database_names = []
        for database_name in self._get_database_names():
            date_object = datetime.strptime(
                re.sub(rf'{self.type}_bot_\d_', '', database_name),
                '%Y_%B_%d_%H_%M'
            )
            data = self._get_database_comment_data()
            database_names.append({
                'database_name': database_name,
                'created_at': date_object,
                **data
            })

        # sort the database names by creation date with the latest as first
        database_names.sort(key=lambda x: x['created_at'], reverse=True)
        return database_names


class StartFreqtrade(StartBot):
    def __init__(self):
        super().__init__()
        self._strategy = self._envs.get('STRATEGY')
        self._config = os.environ.get('CONFIG')
        self._config_file = f'/freqtrade/user_data/configs/{self._config}'
        self._dry_run = os.environ.get('DRY_RUN')
        self._time_frame = os.environ.get('TIMEFRAME', '1m')
        self.type = 'freqtrade'
        self._config_data = self._get_config_data()

    def _get_config_data(self):
        with open(self._config_file, 'r') as config_file:
            return json.load(config_file)

    def get_trading_pairs(self):
        return [pair for pair in self._config_data['exchange']['pair_whitelist'] if ('3S' in pair or '3L' in pair)]

    def create_comment(self):
        self._create_comment(data={
            'strategy': self._strategy,
            'config': self._config,
            'dry_run': self._dry_run
        })

    def start(self):
        envs = self.get_envs()

        # if there is not a specific commit tied to this, launch then use an ephemeral sqlite db
        if self._commit == 'master':
            self._db_url = 'sqlite:///tradesv3.sqlite'
        else:
            self.create_database()
            self.create_comment()

        envs.update({'FREQTRADE__DB_URL': self._db_url})

        from pprint import pprint
        pprint(envs)

        subprocess.run(['freqtrade', *sys.argv[1:]], env=envs)

    def get_database_trades(self, database_name):
        trades = []

        # query trades
        print(f'Getting trades from "{database_name}"...')
        with self.get_cursor(database_name) as cursor:
            # get the column headers for the trades table
            cursor.execute(
                f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'trades' ORDER BY ORDINAL_POSITION")
            keys = [row[0] for row in cursor]

            # get the rows for the trades table
            cursor.execute(f'SELECT * FROM trades')
            for row in cursor:
                trades.append({key: row[index] for index, key in enumerate(keys)})

        # sort trades by open date
        trades.sort(key=lambda x: x['open_date'])
        return trades

    def get_backtest_trades(self):
        backtests_folder = '/freqtrade/user_data/backtest_results/'
        with open(os.path.join(backtests_folder, '.last_result.json'), 'r') as last_result_file:
            data = json.load(last_result_file)

        with open(os.path.join(backtests_folder, data['latest_backtest']), 'r') as latest_backtest:
            data = json.load(latest_backtest)
            trades = data['strategy'][self._strategy]['trades']

        # sort trades by open date
        trades.sort(key=lambda x: x['open_timestamp'])

        return trades

    @staticmethod
    def _filter_dict_against(dict1, dict2):
        filtered_dict = []
        for trade in dict1:
            filtered_item = {}
            for key in dict2[0].keys():
                value = trade.get(key)
                if value:
                    filtered_item[key] = value
            filtered_dict.append(filtered_item)
        return filtered_dict

    @staticmethod
    def _normalize_trade_dates(trades):
        for trade in trades:
            for key, value in trade.items():
                if key in ['close_date', 'open_date'] and type(value) == str:
                    trade[key] = datetime.fromisoformat(value).replace(tzinfo=None)

    def get_filtered_trade_data(self, db_trades, backtest_trades, only_matching_keys=False):
        if only_matching_keys:
            # remove any keys that are not in the backtest
            db_trades = self._filter_dict_against(db_trades, backtest_trades)

            # remove any keys that are not in the database table
            backtest_trades = self._filter_dict_against(backtest_trades, db_trades)

        # normalize date objects
        self._normalize_trade_dates(db_trades)
        self._normalize_trade_dates(backtest_trades)

        # get the first db trade
        first_db_trade_date = db_trades[0]['open_date']

        # don't add backtest trades with open dates before the first database trade
        filtered_backtest_trades = []
        for trade in backtest_trades:
            if first_db_trade_date <= trade.get('open_date'):
                filtered_backtest_trades.append(trade)

        return db_trades, filtered_backtest_trades

    @staticmethod
    def isoformat_trade_dates(trades):
        for index, trade in enumerate(trades):
            # not all trades will have closed yet
            close_date = trade.get('close_date')
            if close_date:
                close_date = close_date.isoformat()

            trades[index].update({
                'close_date': close_date,
                'open_date': trade.get('open_date').isoformat()
            })

    def download(self, since):
        time_string = since.strftime('%Y%m%d')

        # # download from freqtrade
        # subprocess.run(
        #     ['freqtrade',
        #      'download-data',
        #       '--config', f'/freqtrade/user_data/configs/{self._config}',
        #       '--timerange', f'{time_string}-',
        #       '--timeframe', self._time_frame
        #     ],
        #     env=self._envs,
        #     check=True
        # )

        # download from ticker dax
        # os.environ['TIMERANGE'] = f'{time_string}-'
        # downloader.Downloader(
        #     config_file_path=self._config_file
        # )

    def backtest(self, since):
        time_string = since.strftime('%Y%m%d')
        subprocess.run([
            'freqtrade',
            'backtesting',
            '--config', self._config_file,
            '--strategy', self._strategy,
            '--export', 'trades',
            '--timerange', f'{time_string}-',
            '--enable-protections'
        ],
            env=self._envs,
            check=True
        )

    def _get_analysis(self, database_trades, backtest_trades):
        print('Database Trade Number:')
        print(len(database_trades))
        print('Backtest Trade Number:')
        print(len(backtest_trades))

        print('Matching Trade times:')
        matching_trades = []
        for database_trade in database_trades:
            for backtest_trade in backtest_trades:
                time_delta = (database_trade.get('open_date') - backtest_trade.get('open_date'))
                if time_delta.days == 0 and abs(time_delta.seconds) < 60 * 10:
                    if database_trade.get('pair') == backtest_trade.get('pair'):
                        matching_trades.append({
                            'backtest_trade': backtest_trade,
                            'database_trade': database_trade
                        })
                        break
        print(len(matching_trades))
        return matching_trades

    def write_trades_source(self, trades, file_path):
        self.isoformat_trade_dates(trades)
        data = {
            "strategy": {
                "IntoTheBlockStrategy01": {
                    "trades": trades
                }
            }
        }
        with open(file_path, 'w') as file:
            json.dump(data, file)

    def combine_plots(self, pairs):
        header = (
            '<html>'
            '<head><meta charset="utf-8" /></head>'
            '<body>'
        )
        footer = (
            '</body>'
            '</html>'
        )
        # for body

    def compare_plots(self, trades, since):
        time_string = since.strftime('%Y%m%d')
        trade_source = '/freqtrade/user_data/backtest_results/trimmed_backtest.json'
        self.write_trades_source(trades, trade_source)

        for pair in self.get_trading_pairs():
            subprocess.run([
                'freqtrade',
                'plot-dataframe',
                '--config', self._config_file,
                '--strategy', self._strategy,
                '--timeframe', self._time_frame,
                '--timerange', f'{time_string}-',
                '--pairs', pair,
                '--trade-source', 'file',
                '--export-filename', trade_source,
            ],
                env=self._envs,
                check=True
            )

    def compare(self):
        latest_database = self.get_databases()[0]
        database_name = latest_database.get('database_name')
        since = latest_database.get('created_at')

        # run freqtrade download
        self.download(since)

        # run freqtrade backtest
        self.backtest(since)

        database_trades = self.get_database_trades(database_name)
        backtest_trades = self.get_backtest_trades()
        database_trades, backtest_trades = self.get_filtered_trade_data(database_trades, backtest_trades)
        self.compare_plots(backtest_trades, since)

        # matching_trades = self._get_analysis(database_trades, backtest_trades)
        #
        # self.isoformat_trade_dates(database_trades)
        # self.isoformat_trade_dates(backtest_trades)

        # with open('/freqtrade/user_data/backtest_trades.json', 'w') as file:
        #     json.dump(backtest_trades, file, indent=2)
        #
        # with open('/freqtrade/user_data/database_trades.json', 'w') as file:
        #     json.dump(database_trades, file, indent=2)
        #
        # with open('/freqtrade/user_data/matching_trades.json', 'w') as file:
        #     json.dump(matching_trades, file, indent=2)


if __name__ == '__main__':
    arg = sys.argv[1]
    bot = StartFreqtrade()
    if arg == 'trade':
        bot.start()
    if arg == 'compare':
        bot.compare()

        # from pprint import pprint
        # pprint(bot.get_databases())

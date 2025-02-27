import numpy as np
import pandas as pd


def format_large_number_log(num):
    if num < 1000:
        return num
    magnitude = int(np.log10(num))  # 자릿수 계산
    base = num // (10 ** (magnitude - 2))  # 앞의 세 자리 계산
    return base * (10 ** (magnitude - 2))  # 나머지는 0 처리


def format_sj_bs_df(sj_bs_df, stock_code):
    _sj_bs_df = sj_bs_df[sj_bs_df['stock_code'] == stock_code].copy()
    # _sj_bs_df = _sj_bs_df[_sj_bs_df['reprt_code'] == '11011'].copy()

    _sj_bs_df['BPS'] = (_sj_bs_df['price'] / (_sj_bs_df['자본총계'] / _sj_bs_df['share'])).round(3)
    _sj_bs_df['BPS_Change'] = _sj_bs_df['BPS'].pct_change().fillna(0).round(3)
    _sj_bs_df['자본총계_Change'] = _sj_bs_df['자본총계'].pct_change().fillna(0).round(3)
    _sj_bs_df['자본총계'] = _sj_bs_df['자본총계'].apply(format_large_number_log)
    _sj_bs_df['date'] = _sj_bs_df['date'].dt.strftime('%Y-%m-%d')

    _sj_bs_df = _sj_bs_df.loc[:, ['name', 'sector', 'date', 'BPS', 'BPS_Change', '자본총계', '자본총계_Change']]
    return _sj_bs_df


def format_sj_is_df(sj_is_df, stock_code):
    _sj_is_df = sj_is_df[sj_is_df['stock_code'] == stock_code].copy()
    # _sj_is_df = _sj_is_df[_sj_is_df['reprt_code'] == '11011'].copy()

    _sj_is_df['PER'] = (_sj_is_df.loc[:, ['start_price', 'end_price']].mean(
        axis=1) / (_sj_is_df['당기순이익'] / _sj_is_df['share'])).round(3)
    _sj_is_df['PER_Change'] = (_sj_is_df['PER'].pct_change().fillna(0)).round(3)
    _sj_is_df['당기순이익_Change'] = (_sj_is_df['당기순이익'].pct_change().fillna(0)).round(3)
    _sj_is_df['당기순이익'] = _sj_is_df['당기순이익'].apply(format_large_number_log)

    _sj_is_df['매출액'] = _sj_is_df['매출액'].apply(format_large_number_log)
    _sj_is_df['매출액_Change'] = (_sj_is_df['매출액'].pct_change().fillna(0)).round(3)

    _sj_is_df['순이익률'] = (_sj_is_df['당기순이익'] / _sj_is_df['매출액']).round(3)
    _sj_is_df['순이익률_Change'] = (_sj_is_df['순이익률'].pct_change().fillna(0)).round(3)

    _sj_is_df['start_date'] = _sj_is_df['start_date'].dt.strftime('%Y-%m-%d')
    _sj_is_df['end_date'] = _sj_is_df['end_date'].dt.strftime('%Y-%m-%d')

    _sj_is_df = _sj_is_df.loc[:, ['name', 'sector', 'start_date', 'end_date',
                                  'PER', 'PER_Change',
                                  '당기순이익', '당기순이익_Change',
                                  '매출액', '매출액_Change',
                                  '순이익률', '순이익률_Change',
                                  ]]
    return _sj_is_df


class SectorAnalyser:
    def __init__(self, sj_bs_df, sj_is_df):
        self.sj_bs_df = sj_bs_df
        self.sj_is_df = sj_is_df

    def get_stock_dfs(self, stock_code):
        sj_bs_df, sj_is_df = self.sj_bs_df, self.sj_is_df
        
        stock_sj_bs_df = sj_bs_df[(sj_bs_df['stock_code'] == stock_code) & (sj_bs_df['reprt_code'] == '11011')].tail(1)
        stock_sj_is_df = sj_is_df[(sj_is_df['stock_code'] == stock_code) & (sj_is_df['reprt_code'] == '11011')].tail(1)
        return (stock_sj_bs_df, stock_sj_is_df)

    def get_sector_dfs(self, stock_code):
        sj_bs_df, sj_is_df = self.sj_bs_df, self.sj_is_df
        stock_sector = sj_bs_df[(sj_bs_df['stock_code'] == stock_code)]['sector'].unique()[0]

        sector_sj_bs_df = sj_bs_df[(sj_bs_df['sector'] == stock_sector) & (sj_bs_df['reprt_code'] == '11011')].groupby('stock_code').tail(1)
        sector_sj_is_df = sj_is_df[(sj_is_df['sector'] == stock_sector) & (sj_is_df['reprt_code'] == '11011')].groupby('stock_code').tail(1)
        return (sector_sj_bs_df, sector_sj_is_df)

    @staticmethod
    def append_bs_inidicators(bs_df):
        bs_df['BPS'] = bs_df['price'] / (bs_df['자본총계'] / bs_df['share'])
        return bs_df
    
    @staticmethod
    def append_is_inidicators(bs_df):
        price = bs_df.loc[:, ['start_price', 'end_price']].mean(axis=1)
        bs_df['PER'] = price / (bs_df['당기순이익'] / bs_df['share'])
        bs_df['순이익률'] = (bs_df['당기순이익'] / bs_df['매출액'])
        return bs_df
    
    @staticmethod
    def trucated_mean(df, arg, p):
        lower_limit = df[arg].quantile(p)
        upper_limit = df[arg].quantile(1 - p)
        _mean = df[(lower_limit < df[arg]) & (df[arg] < upper_limit)][arg].mean()
        return _mean
    
    def make_stock_sector_df(self, stock_code):
        (stock_sj_bs_df, stock_sj_is_df) = self.get_stock_dfs(stock_code)
        (sector_sj_bs_df, sector_sj_is_df) = self.get_sector_dfs(stock_code)
        
        stock_sj_bs_df = self.append_bs_inidicators(stock_sj_bs_df)
        sector_sj_bs_df = self.append_bs_inidicators(sector_sj_bs_df)
        
        stock_sj_is_df = self.append_is_inidicators(stock_sj_is_df)
        sector_sj_is_df = self.append_is_inidicators(sector_sj_is_df)
        
        sector_bps_mean = self.trucated_mean(sector_sj_bs_df, "BPS", 0.1)
        stock_bps = stock_sj_bs_df.iloc[-1]['BPS']
        
        sector_per_mean = self.trucated_mean(sector_sj_is_df, "PER", 0.1)
        stock_per = stock_sj_is_df.iloc[-1]['PER']
        # npr : net_profit_ratio
        sector_npr_mean = self.trucated_mean(sector_sj_is_df, "순이익률", 0.1)
        stock_npr = stock_sj_is_df.iloc[-1]['순이익률']
        stock_sector_df = pd.DataFrame({
            'stock': {
                'bps': stock_bps,
                'per': stock_per,
                '순이익률': stock_npr
            },
            'sector': {
                'bps': sector_bps_mean,
                'per': sector_per_mean,
                '순이익률': sector_npr_mean
            },

        })
        return stock_sector_df.reset_index()

    def __call__(self, stock_code):
        stock_sector_df = self.make_stock_sector_df(stock_code)
        return stock_sector_df
                        
                        
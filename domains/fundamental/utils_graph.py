from sklearn.preprocessing import MinMaxScaler

class FsStockAnalyser:
    def __init__(self, fs_df):
        self.fs_df = fs_df

    def transform(self, _fs_df):
        scaler = MinMaxScaler()
        feature_cols = ['pbr', 'ppe', 'd_per', 'd_ppp']
        _fs_df.loc[:, feature_cols] = scaler.fit_transform(_fs_df.loc[:, feature_cols])
        _fs_df = _fs_df.rename(columns={
            'pbr': 'equity_market', 'ppe': 'equity_intrinsic',
            'd_per': 'profit_market', 'd_ppp': 'profit_intrinsic',
        })
        _fs_df = _fs_df.loc[:, ['stock_code', 'name', 'sector',
                                'equity_market', 'equity_intrinsic',
                                'profit_market', 'profit_intrinsic']]
        return _fs_df

    def __call__(self, stock_code):
        fs_df = self.fs_df.copy()
        _fs_df = fs_df[fs_df['stock_code'] == stock_code]
        _fs_df = self.transform(_fs_df)
        return _fs_df
import pandas as pd

def get_ROE(df):
    df['ROE'] = df['netIncome'] / df['shareholderEquity']
    return df

def get_currentRatio(df):
    df['currentRatio'] = df['currentAssets'] / df['currentDebt']
    return df

def get_CFORatio(df):
    df['CFORatio'] = df['cashFlow'] / df['currentDebt']
    return df

def get_netProfitMargin(df):
    df['netProfitMargin'] = df['netIncome'] / df['totalRevenue']
    return df

def get_netProfitMargin_sector(df):
    net = df.groupby(['Sector', 'fiscalPeriod'], as_index=False).agg({"netProfitMargin": "mean"}).rename(columns={"netProfitMargin": "NetProfitMargin_sector"})
    temp = pd.merge(df,
                   net,
                   on=['Sector', 'fiscalPeriod'],
                   how='outer')
    return temp


def get_totalAssetTurnover(df):
    df['totalAssetTurnover'] = df['totalRevenue'] / ((df['totalAssets']+df['totalAssets'].shift(1)) / 2 )
    return df

def get_financialLeverage(df):
    df['financialLeverage'] = df['operatingIncome'] / df['netIncome']
    return df

def get_financialLeverage_sector(df):
    fl = df.groupby(['Sector', 'fiscalPeriod'], as_index=False).agg({"financialLeverage": "mean"}).rename(columns={"financialLeverage": "FinancialLeverage_sector"})
    temp = pd.merge(df,
                   fl,
                   on=['Sector', 'fiscalPeriod'],
                   how='outer')
    return temp

def get_financialLeverage_change(df):
    temp = pd.Series((df['financialLeverage'] - df['FinancialLeverage_sector']),name='FinancialLeverage_change')
    df = df.join(temp)
    return df

def get_debtCapital(df):
    df['debtCapital'] = df['totalDebt']/(df['totalDebt']+df['shareholderEquity'])
    return df

def get_PERatio(df):
    df['P/Eratio'] = df['close']/df['actualEPS']
    return df

def get_PERatio_sector(df):
    eps = df.groupby(['Sector', 'fiscalPeriod'], as_index=False).agg({"P/Eratio": "mean"}).rename(columns={"P/Eratio": "P/ERatio_sector"})
    temp = pd.merge(df,
                   eps,
                   on=['Sector', 'fiscalPeriod'],
                   how='outer')
    return temp

def add_variables(df):
    df['NetIncomeChange'] = (df['netIncome'] - df['netIncome'].shift(4)) / df['netIncome'].shift(4)
    df['CashFlowChange'] = df['cashFlow'] - df['cashFlow'].shift(4)
    df['ResearchAndDevelopment_change'] = df['researchAndDevelopment'] - df['researchAndDevelopment'].shift(4)
    return df

def gener_fundamental_variables(df):
    df = get_ROE(df)
    df = get_currentRatio(df)
    df = get_CFORatio(df)
    df = get_netProfitMargin(df)
    df = get_netProfitMargin_sector(df)
    df = get_totalAssetTurnover(df)
    df = get_financialLeverage(df)
    df = get_financialLeverage_sector(df)
    df = get_financialLeverage_change(df)
    df = get_debtCapital(df)
    df = get_PERatio(df)
    df = get_PERatio_sector(df)
    df = add_variables(df)
    return df

#test
# if __name__ == "__main__":
#     df = pd.read_csv('../datasets/data_from_iex.csv')
#     df = gener_fundamental_variables(df)
#     df.to_csv('../datasets/test_variables.csv',index=False)

import numpy as np
def engineer(df):
    x=df.copy()
    x["return_1"]=x.close.pct_change()
    x["return_4"]=x.close.pct_change(4)
    x["sma_12"]=x.close.rolling(12).mean()
    x["sma_gap"]=x.close/x.sma_12-1
    d=x.close.diff(); g=d.clip(lower=0).rolling(14).mean(); l=(-d.clip(upper=0)).rolling(14).mean()
    x["rsi"]=100-(100/(1+g/l.replace(0,np.nan)))
    x["volatility"]=x.return_1.rolling(24).std()
    x["hour"]=x.timestamp.dt.hour
    return x.replace([np.inf,-np.inf],np.nan)
FEATURES=["return_1","return_4","sma_gap","rsi","volatility","hour"]

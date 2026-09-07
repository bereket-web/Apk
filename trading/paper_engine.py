"""Paper-only backtest engine. No live broker execution."""
import pandas as pd
from pathlib import Path
from ml.src.features import engineer,FEATURES
import joblib

STARTING_BALANCE=10_000.0
RISK_PER_TRADE=0.005
MAX_DAILY_LOSS=0.02
SPREAD_COST=0.0001
THRESHOLD=0.60

def run():
    p=Path("data/raw/eurusd_1h.csv")
    df=pd.read_csv(p); df.timestamp=pd.to_datetime(df.timestamp,utc=True)
    df=engineer(df).dropna().reset_index(drop=True)
    bundle=joblib.load("models/baseline.joblib"); model=bundle["model"]
    balance=STARTING_BALANCE; peak=balance; trades=[]
    for i in range(30,len(df)-4):
        row=df.loc[[i],FEATURES]; prob=float(model.predict_proba(row)[0,1])
        if prob<THRESHOLD: continue
        entry=df.close.iloc[i]; exit_=df.close.iloc[i+4]
        # Simple fixed-risk educational simulation, not a brokerage fill model.
        position=balance*RISK_PER_TRADE/max(entry*0.002,1e-9)
        pnl=(exit_-entry-SPREAD_COST)*position
        balance+=pnl; peak=max(peak,balance)
        trades.append({"time":df.timestamp.iloc[i],"prob_up":prob,"pnl":pnl,"balance":balance})
        if balance < STARTING_BALANCE*(1-MAX_DAILY_LOSS): break
    out=pd.DataFrame(trades); Path("reports").mkdir(exist_ok=True)
    out.to_csv("reports/paper_trades.csv",index=False)
    print({"starting":STARTING_BALANCE,"ending":balance,"trades":len(out),"return_pct":(balance/STARTING_BALANCE-1)*100})
if __name__=="__main__": run()

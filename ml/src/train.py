import os,sys,joblib,pandas as pd
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,roc_auc_score
from ml.src.features import engineer,FEATURES

def main():
    p=Path("data/raw/eurusd_1h.csv")
    if not p.exists(): p=Path("ForexSense-AI-v2/data/raw/eurusd_1h.csv")
    df=pd.read_csv(p); df["timestamp"]=pd.to_datetime(df.timestamp,utc=True)
    df=engineer(df); horizon=4
    df["target"]=((df.close.shift(-horizon)/df.close-1)>0.0005).astype(int)
    df=df.dropna().reset_index(drop=True)
    cut=int(len(df)*.8); train,test=df.iloc[:cut],df.iloc[cut:]
    model=Pipeline([("scale",StandardScaler()),("clf",LogisticRegression(max_iter=2000))])
    model.fit(train[FEATURES],train.target)
    prob=model.predict_proba(test[FEATURES])[:,1]
    metrics={"accuracy":float(accuracy_score(test.target,prob>=.5)),"roc_auc":float(roc_auc_score(test.target,prob))}
    os.makedirs("models",exist_ok=True); os.makedirs("reports",exist_ok=True)
    joblib.dump({"model":model,"features":FEATURES},"models/baseline.joblib")
    pd.DataFrame([metrics]).to_csv("reports/metrics.csv",index=False)
    print(metrics)
if __name__=="__main__": main()

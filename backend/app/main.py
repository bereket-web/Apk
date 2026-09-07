from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from pathlib import Path
import pandas as pd, joblib
from ml.src.features import engineer

app=FastAPI(title="ForexSense AI v2",version="2.0.0")
BUNDLE=None
class Candle(BaseModel):
    timestamp:str; open:float; high:float; low:float; close:float
class PredictRequest(BaseModel):
    candles:list[Candle]
@app.on_event("startup")
def startup():
    global BUNDLE
    p=Path("models/baseline.joblib")
    if p.exists(): BUNDLE=joblib.load(p)
@app.get("/health")
def health(): return {"status":"ok","model_loaded":BUNDLE is not None,"mode":"research/paper-only"}
@app.post("/predict")
def predict(req:PredictRequest):
    if BUNDLE is None: raise HTTPException(503,"Model not trained. Run python -m ml.src.train")
    if len(req.candles)<30: raise HTTPException(400,"At least 30 candles required")
    df=pd.DataFrame([x.model_dump() for x in req.candles]); df.timestamp=pd.to_datetime(df.timestamp,utc=True)
    df=engineer(df).dropna(); row=df[BUNDLE["features"]].tail(1)
    p=float(BUNDLE["model"].predict_proba(row)[0,1])
    return {"probability_up":p,"probability_down":1-p,"signal":"UP" if p>=.5 else "DOWN_OR_NEUTRAL","educational_only":True}

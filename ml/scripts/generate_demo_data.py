import numpy as np,pandas as pd
from pathlib import Path
rng=np.random.default_rng(42); n=15000
t=pd.date_range("2022-01-03",periods=n,freq="h",tz="UTC")
r=rng.normal(0,0.0007,n); c=1.1*np.exp(np.cumsum(r)); o=np.r_[c[0],c[:-1]]
s=np.abs(rng.normal(.00025,.00008,n))
df=pd.DataFrame({"timestamp":t,"open":o,"high":np.maximum(o,c)+s,"low":np.minimum(o,c)-s,"close":c})
Path("data/raw").mkdir(parents=True,exist_ok=True); df.to_csv("data/raw/eurusd_1h.csv",index=False)
print("Demo data generated")

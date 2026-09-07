# ForexSense AI v2
End-to-end educational quantitative ML system: historical training pipeline, FastAPI inference API, paper-trading simulator, and Capacitor Android dashboard.

## Safety
Paper trading only. No broker credentials or live-order execution are included. Historical model performance does not guarantee future profitability.

## Architecture
Historical OHLC CSV -> features -> chronological split -> baseline + GRU -> saved artifacts
-> FastAPI prediction service -> paper trading engine -> mobile dashboard.

## Quick start
### 1. Generate demo data and train baseline
```bash
pip install -r ml/requirements.txt
python ml/scripts/generate_demo_data.py
python -m ml.src.train
```
### 2. Run API
```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```
### 3. Run paper simulation
```bash
python -m trading.paper_engine
```
### 4. Build Android app
```bash
cd mobile
npm install
npm run build
npx cap add android
npx cap sync android
```

## Real data format
`timestamp,open,high,low,close` in chronological order.

## Portfolio features
- leakage-aware chronological splitting
- baseline and GRU architecture
- explicit risk limits
- transaction-cost-aware paper simulation
- API layer separated from model training
- mobile client separated from secrets

## Disclaimer
This is a research project, not financial advice.

# ForexSense AI v2 Architecture

## Components
1. ML package: offline feature engineering, chronological training, baseline and GRU model definition.
2. FastAPI: loads approved model artifacts and exposes prediction endpoints.
3. Paper engine: simulates signals with configurable transaction costs and risk limits.
4. Mobile: Capacitor Android client that communicates with the API.

## Security boundary
The mobile app contains no brokerage credentials. Secrets belong in server-side environment variables if a future authorized integration is built.

## Recommended progression
Historical research -> walk-forward validation -> paper trading -> extended monitoring.

Live trading is intentionally out of scope for this repository.

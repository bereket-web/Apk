# ForexSense AI — Android App

A mobile portfolio app for visualizing EUR/USD data and presenting machine-learning market-direction predictions.

## Features
- Mobile-first dashboard
- Price chart
- UP/DOWN probability display
- Forecast horizon selection
- Technical indicator cards
- CSV upload interface
- Educational disclaimer
- Capacitor Android packaging
- GitHub Actions cloud APK build

## Current Model Mode
The included UI uses **demo inference** so the Android app works immediately. The `probability()` function in `src/main.js` is the integration point for a real TensorFlow Lite model or backend API.

## Build APK from GitHub (phone-friendly)
1. Create a new GitHub repository.
2. Upload every file in this project.
3. Commit to the `main` branch.
4. Open **Actions**.
5. Select **Build Android APK**.
6. Run the workflow.
7. Open the completed workflow.
8. Download `ForexSense-AI-debug-apk`.
9. Extract and install the APK on Android.

## Local development
```bash
npm install
npm run dev
```

## Android build
```bash
npm install
npm run build
npx cap add android
npx cap sync android
```

## Portfolio note
For a production-grade version, connect the UI to:
- a FastAPI prediction API, or
- an on-device TensorFlow Lite model.

The app intentionally does not claim trading profitability.

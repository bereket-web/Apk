import Chart from 'chart.js/auto';
import './style.css';

const state = {
  pair: 'EUR/USD',
  horizon: 4,
  prices: [1.0842,1.0848,1.0841,1.0853,1.0860,1.0855,1.0868,1.0874,1.0869,1.0881,1.0876,1.0892],
  prediction: null
};

function probability() {
  // Demo inference. Replace with API/TFLite inference when a trained model is integrated.
  const momentum = state.prices.at(-1) - state.prices.at(-4);
  const volatility = Math.abs(state.prices.at(-1) - state.prices.at(-2));
  let p = 0.5 + momentum * 250 + (Math.random() - .5) * .08 - volatility * 15;
  return Math.max(.05, Math.min(.95, p));
}

function render() {
  const p = state.prediction?.p ?? .5;
  const direction = p >= .5 ? 'UP' : 'DOWN';
  const confidence = Math.round(Math.max(p, 1-p) * 100);

  document.querySelector('#app').innerHTML = `
    <main>
      <header>
        <div>
          <div class="brand">ForexSense <span>AI</span></div>
          <small>Market direction research assistant</small>
        </div>
        <div class="status"><span></span> Demo Mode</div>
      </header>

      <section class="hero">
        <div class="pair-row">
          <div>
            <p class="eyebrow">MARKET</p>
            <h1>${state.pair}</h1>
          </div>
          <select id="horizon">
            <option value="1">Next 1 Hour</option>
            <option value="4" selected>Next 4 Hours</option>
            <option value="24">Next 24 Hours</option>
          </select>
        </div>
        <div class="price">${state.prices.at(-1).toFixed(4)}</div>
        <div class="change">Latest available close</div>
      </section>

      <section class="card chart-card">
        <div class="section-title"><h2>Price Movement</h2><span>12 candles</span></div>
        <canvas id="chart"></canvas>
      </section>

      <section class="prediction card">
        <p class="eyebrow">AI PREDICTION</p>
        <div class="direction ${direction === 'UP' ? 'up' : 'down'}">${direction === 'UP' ? '▲' : '▼'} ${direction}</div>
        <div class="confidence">Confidence: <b>${confidence}%</b></div>
        <div class="bar"><div class="upbar" style="width:${Math.round(p*100)}%"></div></div>
        <div class="probabilities"><span>▲ UP <b>${Math.round(p*100)}%</b></span><span>▼ DOWN <b>${100-Math.round(p*100)}%</b></span></div>
        <button id="predict">Run Prediction</button>
      </section>

      <section class="indicators">
        <div class="metric card"><span>RSI (14)</span><b>${state.prediction?.rsi ?? '—'}</b></div>
        <div class="metric card"><span>MACD</span><b>${state.prediction?.macd ?? '—'}</b></div>
        <div class="metric card"><span>Volatility</span><b>${state.prediction?.vol ?? '—'}</b></div>
      </section>

      <section class="card upload">
        <h2>Analyze Your Data</h2>
        <p>Upload an OHLC CSV to preview data locally. Full model inference can be connected to a FastAPI backend or TensorFlow Lite model.</p>
        <label class="file-btn">Choose CSV<input id="csv" type="file" accept=".csv,text/csv"></label>
        <small id="file-status"></small>
      </section>

      <section class="disclaimer">
        <b>Educational project.</b> Predictions are for machine-learning research and are not financial advice.
      </section>
    </main>
  `;

  new Chart(document.querySelector('#chart'), {
    type: 'line',
    data: {
      labels: state.prices.map((_, i) => `${i+1}`),
      datasets: [{ data: state.prices, borderWidth: 2, tension: .35, pointRadius: 0 }]
    },
    options: { responsive: true, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { ticks: { callback: v => Number(v).toFixed(4) } } } }
  });

  document.querySelector('#horizon').value = String(state.horizon);
  document.querySelector('#horizon').onchange = e => state.horizon = +e.target.value;
  document.querySelector('#predict').onclick = () => {
    const p = probability();
    state.prediction = {
      p,
      rsi: (42 + p*20).toFixed(1),
      macd: p >= .5 ? 'Bullish' : 'Bearish',
      vol: (0.4 + Math.abs(p-.5)*2).toFixed(2) + '%'
    };
    render();
  };
  document.querySelector('#csv').onchange = e => {
    const f = e.target.files[0];
    if (!f) return;
    document.querySelector('#file-status').textContent = `Selected: ${f.name}`;
  };
}
render();
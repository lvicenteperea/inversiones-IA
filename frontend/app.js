const eur = new Intl.NumberFormat('es-ES', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 });

const fields = {
  initialAmount: document.querySelector('#initialAmount'),
  annualReturn: document.querySelector('#annualReturn'),
  monthlyIncome: document.querySelector('#monthlyIncome'),
  years: document.querySelector('#years'),
  inflation: document.querySelector('#inflation'),
};

const statusEl = document.querySelector('#status');
const chart = document.querySelector('#chart');
const ctx = chart.getContext('2d');

function numberValue(input, fallback) {
  const value = Number(input.value);
  return Number.isFinite(value) ? value : fallback;
}

async function runSimulation() {
  statusEl.textContent = 'Calculando...';
  const payload = {
    initial_amount: numberValue(fields.initialAmount, 300000),
    annual_return_pct: numberValue(fields.annualReturn, 3.5),
    monthly_income: numberValue(fields.monthlyIncome, 650),
    years: numberValue(fields.years, 20),
    inflation_pct: numberValue(fields.inflation, 2.5),
  };

  try {
    const response = await fetch('/api/simulation', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error('No se pudo calcular la simulacion');
    const data = await response.json();
    renderSummary(data.rows, payload);
    renderChart(data.rows);
    statusEl.textContent = 'Simulacion actualizada';
  } catch (error) {
    statusEl.textContent = error.message;
  }
}

function renderSummary(rows, payload) {
  const last = rows[rows.length - 1];
  document.querySelector('#finalNominal').textContent = eur.format(Number(last.nominal_value));
  document.querySelector('#finalReal').textContent = eur.format(Number(last.real_value));
  document.querySelector('#totalIncome').textContent = eur.format(payload.monthly_income * payload.years * 12);
}

function renderChart(rows) {
  const width = chart.width;
  const height = chart.height;
  const pad = 42;
  const values = rows.flatMap((row) => [Number(row.nominal_value), Number(row.real_value)]);
  const maxY = Math.max(...values) * 1.08;
  const maxX = Math.max(...rows.map((row) => Number(row.year))) || 1;
  const x = (year) => pad + (width - pad * 2) * (year / maxX);
  const y = (value) => height - pad - (height - pad * 2) * (value / maxY);

  ctx.clearRect(0, 0, width, height);
  ctx.strokeStyle = '#e5e7eb';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i += 1) {
    const yy = pad + (height - pad * 2) * i / 4;
    ctx.beginPath();
    ctx.moveTo(pad, yy);
    ctx.lineTo(width - pad, yy);
    ctx.stroke();
  }

  drawLine(rows, (row) => Number(row.nominal_value), '#344054', false);
  drawLine(rows, (row) => Number(row.real_value), '#667085', true);

  ctx.fillStyle = '#667085';
  ctx.font = '14px system-ui';
  ctx.fillText('Nominal', pad, 22);
  ctx.fillText('Real ajustado por inflacion', 130, 22);
  ctx.fillText('0 anos', pad, height - 10);
  ctx.fillText(`${maxX} anos`, width - pad - 52, height - 10);

  function drawLine(data, accessor, color, dashed) {
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 3;
    ctx.setLineDash(dashed ? [8, 7] : []);
    data.forEach((row, index) => {
      const px = x(Number(row.year));
      const py = y(accessor(row));
      if (index === 0) ctx.moveTo(px, py);
      else ctx.lineTo(px, py);
    });
    ctx.stroke();
    ctx.setLineDash([]);
  }
}

async function loadPortfolios() {
  const container = document.querySelector('#portfolios');
  try {
    const response = await fetch('/api/portfolios');
    if (!response.ok) throw new Error('No se pudieron cargar las carteras');
    const portfolios = await response.json();
    container.innerHTML = portfolios.map((item) => `
      <div class="portfolio-row">
        <div>
          <strong>${item.name}</strong>
          <p>${item.description || ''}</p>
        </div>
        <span>${eur.format(Number(item.initial_amount))}</span>
      </div>
    `).join('');
  } catch (error) {
    container.textContent = error.message;
  }
}

document.querySelector('#runSimulation').addEventListener('click', runSimulation);
Object.values(fields).forEach((input) => input.addEventListener('change', runSimulation));
runSimulation();
loadPortfolios();

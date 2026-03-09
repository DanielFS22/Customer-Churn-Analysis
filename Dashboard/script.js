/* ═══════════════════════════════════════
   CHURN ANALYTICS — script.js
   Consome todas as rotas do app.py
   ═══════════════════════════════════════ */

// BASE vazio = usa o mesmo domínio (funciona local e em produção)
const BASE = '';

Chart.defaults.color         = '#6b7280';
Chart.defaults.borderColor   = '#252a3a';
Chart.defaults.font.family   = "'DM Mono', monospace";
Chart.defaults.font.size     = 11;

const PAL = ['#e8ff47','#ff5f5f','#5faaff','#4ade80','#b8a4ff','#ff9f5f'];

let explorerChartInst = null;
let segData = [];   // cache para o explorador

/* ── helpers ─────────────────────────── */
function fmt(n)  { return Number(n).toLocaleString('pt-BR'); }
function fmtR(n) {
  return 'R$ ' + Number(n).toLocaleString('pt-BR', {
    minimumFractionDigits: 2, maximumFractionDigits: 2
  });
}
function corRisco(taxa) {
  if (taxa >= 70) return '#ff5f5f';
  if (taxa >= 40) return '#e8ff47';
  return '#4ade80';
}
function badgeStatus(taxa) {
  if (taxa >= 70) return '<span class="badge badge-churn">crítico</span>';
  if (taxa >= 40) return '<span class="badge badge-warn">atenção</span>';
  return '<span class="badge badge-ativo">estável</span>';
}
function setStatus(ok, text) {
  const badge = document.getElementById('statusBadge');
  const dot   = document.getElementById('statusDot');
  const span  = document.getElementById('statusText');
  dot.className   = 'status-dot ' + (ok ? 'ok' : 'err');
  badge.className = 'status-badge ' + (ok ? 'ok' : 'err');
  span.textContent = text;
}

/* ── TABS ────────────────────────────── */
document.querySelectorAll('.tab').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
  });
});

/* ── FETCH helpers ───────────────────── */
async function get(path) {
  const res = await fetch(BASE + path);
  if (!res.ok) throw new Error(res.status);
  return res.json();
}

/* ═══════════════════════════════════════
   DASHBOARD — carregar todos os dados
═══════════════════════════════════════ */
async function iniciarDashboard() {
  try {
    // Carrega tudo em paralelo
    const [totalData, rateData, receitaData, ticketData, segmData, diasData, churnData] =
      await Promise.all([
        get('/clientes_total'),
        get('/churn_rate'),
        get('/receita_media'),
        get('/ticket_medio'),
        get('/segmento'),
        get('/distribuicao_dias'),
        get('/churn')
      ]);

    setStatus(true, 'conectado · ' + new Date().toLocaleTimeString('pt-BR'));

    /* ── KPIs ── */
    const total      = totalData[0].total_clientes;
    const totalChurn = rateData[0].total_churn;
    const rate       = rateData[0].churn_rate;
    const receita    = receitaData[0].receita_media;
    const ticket     = ticketData[0].ticket_medio;

    document.getElementById('val-total').textContent  = fmt(total);
    document.getElementById('val-churn').textContent  = fmt(totalChurn);
    document.getElementById('val-rate').textContent   = rate + '%';
    document.getElementById('sub-rate').textContent   =
      rate > 50 ? '⚠ acima do limite crítico' : '✓ dentro do aceitável';
    document.getElementById('val-receita').textContent = fmtR(receita);
    document.getElementById('val-ticket').textContent  = fmtR(ticket);

    /* ── Gráfico Pizza — Ativo vs Churn ── */
    const pieLabels = churnData.map(d => d.churn == 1 ? 'Em Churn' : 'Ativo');
    const pieVals   = churnData.map(d => d.total);
    new Chart(document.getElementById('pieChart'), {
      type: 'doughnut',
      data: {
        labels: pieLabels,
        datasets: [{
          data: pieVals,
          backgroundColor: ['#ff5f5f55','#4ade8055'],
          borderColor:     ['#ff5f5f',  '#4ade80'],
          borderWidth: 2
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: { display: true, labels: { color: '#e8eaf2', padding: 16 } }
        }
      }
    });

    /* ── Gráfico Barras — Churn Rate por Segmento ── */
    segData = segmData;
    new Chart(document.getElementById('segChart'), {
      type: 'bar',
      data: {
        labels: segmData.map(d => d.segmento),
        datasets: [{
          data: segmData.map(d => d.taxa_churn),
          backgroundColor: segmData.map(d => corRisco(d.taxa_churn) + '44'),
          borderColor:     segmData.map(d => corRisco(d.taxa_churn)),
          borderWidth: 2, borderRadius: 6
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { grid: { color: '#1a1e2b' }, ticks: { callback: v => v + '%' } },
          x: { grid: { display: false } }
        }
      }
    });

    /* ── Gráfico Barras — Distribuição por Dias ── */
    new Chart(document.getElementById('diasChart'), {
      type: 'bar',
      data: {
        labels: diasData.map(d => d.faixa),
        datasets: [{
          data: diasData.map(d => d.total),
          backgroundColor: ctx => {
            const l = diasData[ctx.dataIndex]?.faixa || '';
            return (l.includes('91') || l.includes('120+')) ? '#ff5f5f44' : '#5faaff44';
          },
          borderColor: ctx => {
            const l = diasData[ctx.dataIndex]?.faixa || '';
            return (l.includes('91') || l.includes('120+')) ? '#ff5f5f' : '#5faaff';
          },
          borderWidth: 2, borderRadius: 6
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { grid: { color: '#1a1e2b' }, ticks: { callback: v => fmt(v) } },
          x: { grid: { display: false } }
        }
      }
    });

    /* ── Gráfico Barras — Total por Segmento ── */
    new Chart(document.getElementById('segTotalChart'), {
      type: 'bar',
      data: {
        labels: segmData.map(d => d.segmento),
        datasets: [{
          data: segmData.map(d => d.total),
          backgroundColor: PAL.map(c => c + '44'),
          borderColor:     PAL,
          borderWidth: 2, borderRadius: 6
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { grid: { color: '#1a1e2b' }, ticks: { callback: v => fmt(v) } },
          x: { grid: { display: false } }
        }
      }
    });

    /* ── Tabela de segmentos ── */
    document.getElementById('seg-tbody').innerHTML = segmData.map(d => `
      <tr>
        <td style="color:var(--text);font-weight:700">${d.segmento}</td>
        <td>${fmt(d.total)}</td>
        <td>${fmt(d.total_churn)}</td>
        <td style="color:${corRisco(d.taxa_churn)}">${d.taxa_churn}%</td>
        <td>${badgeStatus(d.taxa_churn)}</td>
      </tr>`).join('');

    /* ── Explorador: resumo rápido ── */
    document.getElementById('summaryGrid').innerHTML = `
      <div class="summary-item">
        <div class="s-label">Total</div>
        <div class="s-value" style="color:var(--blue)">${fmt(total)}</div>
      </div>
      <div class="summary-item">
        <div class="s-label">Em Churn</div>
        <div class="s-value" style="color:var(--red)">${fmt(totalChurn)}</div>
      </div>
      <div class="summary-item">
        <div class="s-label">Churn Rate</div>
        <div class="s-value" style="color:var(--yellow)">${rate}%</div>
      </div>
      <div class="summary-item">
        <div class="s-label">Receita Média</div>
        <div class="s-value" style="color:var(--green);font-size:1.1rem">${fmtR(receita)}</div>
      </div>
      <div class="summary-item">
        <div class="s-label">Ticket Médio</div>
        <div class="s-value" style="color:var(--purple);font-size:1.1rem">${fmtR(ticket)}</div>
      </div>
      <div class="summary-item">
        <div class="s-label">Segmentos</div>
        <div class="s-value">${segmData.length}</div>
      </div>
    `;

    /* ── Explorador: tabela comparativa ── */
    document.getElementById('comp-tbody').innerHTML = segmData.map(d => `
      <tr>
        <td style="color:var(--text);font-weight:700">${d.segmento}</td>
        <td>${fmt(d.total)}</td>
        <td>${fmt(d.total_churn)}</td>
        <td style="color:${corRisco(d.taxa_churn)}">${d.taxa_churn}%</td>
        <td>
          <div class="risk-bar-wrap">
            <div class="risk-bar-fill"
                 style="width:${Math.min(d.taxa_churn,100)}%; background:${corRisco(d.taxa_churn)}">
            </div>
          </div>
        </td>
        <td>${badgeStatus(d.taxa_churn)}</td>
      </tr>`).join('');

    gerarGrafico();

  } catch (err) {
    console.error(err);
    setStatus(false, 'erro de conexão');
    document.getElementById('val-total').textContent = 'Erro';
  }
}

/* ═══════════════════════════════════════
   EXPLORADOR — gerador de gráfico
═══════════════════════════════════════ */
async function gerarGrafico() {
  const fonte = document.getElementById('g-fonte').value;
  const tipo  = document.getElementById('g-tipo').value;

  let labels = [], values = [], colors = [];

  try {
    if (fonte === 'segmento') {
      const data = segData.length ? segData : await get('/segmento');
      labels = data.map(d => d.segmento);
      values = data.map(d => d.taxa_churn);
      colors = data.map(d => corRisco(d.taxa_churn));

    } else if (fonte === 'dias') {
      const data = await get('/distribuicao_dias');
      labels = data.map(d => d.faixa);
      values = data.map(d => d.total);
      colors = labels.map((l, i) =>
        (l.includes('91') || l.includes('120+')) ? '#ff5f5f' : PAL[i % PAL.length]
      );

    } else if (fonte === 'churn') {
      const data = await get('/churn');
      labels = data.map(d => d.churn == 1 ? 'Em Churn' : 'Ativo');
      values = data.map(d => d.total);
      colors = ['#ff5f5f', '#4ade80'];
    }

    if (explorerChartInst) explorerChartInst.destroy();

    explorerChartInst = new Chart(document.getElementById('explorerChart'), {
      type: tipo,
      data: {
        labels,
        datasets: [{
          label: document.getElementById('g-fonte').selectedOptions[0].text,
          data: values,
          backgroundColor: colors.map(c => c + '55'),
          borderColor:     colors,
          borderWidth: 2,
          borderRadius: tipo === 'bar' ? 6 : 0,
          fill: tipo === 'line',
          tension: 0.4,
          pointBackgroundColor: '#e8ff47',
          pointRadius: 5
        }]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: {
          legend: {
            display: tipo === 'doughnut' || tipo === 'polarArea',
            labels: { color: '#e8eaf2', padding: 14 }
          }
        },
        scales: (tipo === 'doughnut' || tipo === 'polarArea') ? {} : {
          y: { grid: { color: '#1a1e2b' }, ticks: { callback: v => fmt(v) } },
          x: { grid: { display: false } }
        }
      }
    });

  } catch (err) {
    console.error('Erro ao gerar gráfico:', err);
  }
}

/* ── INIT ──────────────────────────────── */
iniciarDashboard();
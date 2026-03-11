// script.js
// Handles UI interactions and sends form data to the Python server (server.py)
// The eligibility logic runs in loan_logic.py — not here.

// ─── RANGE SLIDER UTILITIES ───────────────────────────────────────────────────

function updateRange(input, displayId, prefix, format) {
  const val = parseInt(input.value);
  const min = parseInt(input.min);
  const max = parseInt(input.max);
  const progress = ((val - min) / (max - min)) * 100;
  input.style.setProperty('--progress', progress + '%');

  if (format) {
    let display;
    if (val >= 100000) display = (val / 100000).toFixed(val % 100000 === 0 ? 0 : 1) + ' L';
    else display = (val / 1000).toFixed(0) + 'K';
    document.getElementById(displayId).innerHTML = prefix + display + ' <small>INR</small>';
  } else {
    document.getElementById(displayId).innerHTML = val + ' <small>/ 900</small>';
  }
}

function updateScoreBars() {
  const score = parseInt(document.getElementById('creditScore').value);
  const bars  = ['bar1','bar2','bar3','bar4'].map(id => document.getElementById(id));
  const label = document.getElementById('scoreLabel');

  bars.forEach(b => b.className = 'score-bar');

  if (score < 500) {
    bars[0].classList.add('poor');
    label.textContent = 'Very Poor'; label.style.color = '#c0392b';
  } else if (score < 600) {
    bars[0].classList.add('poor'); bars[1].classList.add('poor');
    label.textContent = 'Poor'; label.style.color = '#c0392b';
  } else if (score < 700) {
    bars[0].classList.add('fair'); bars[1].classList.add('fair'); bars[2].classList.add('fair');
    label.textContent = 'Fair'; label.style.color = '#e67e22';
  } else if (score < 800) {
    bars.forEach(b => b.classList.add('good'));
    label.textContent = 'Good'; label.style.color = '#f0a500';
  } else {
    bars.forEach(b => b.classList.add('excellent'));
    label.textContent = 'Excellent'; label.style.color = '#27ae60';
  }
}

window.addEventListener('DOMContentLoaded', () => {
  updateRange(document.getElementById('loanAmount'), 'loanDisplay', '₹', true);
  updateRange(document.getElementById('creditScore'), 'scoreDisplay', '', false);
  updateScoreBars();
});

// ─── SUBMIT TO PYTHON SERVER ──────────────────────────────────────────────────

async function checkEligibility() {
  const age         = parseInt(document.getElementById('age').value);
  const income      = parseInt(document.getElementById('income').value);
  const creditScore = parseInt(document.getElementById('creditScore').value);
  const loanAmount  = parseInt(document.getElementById('loanAmount').value);
  const employment  = document.getElementById('employment').value;

  if (!age || !income || !employment) {
    alert('Please fill in all fields.');
    return;
  }

  const btn = document.querySelector('.btn-check');
  btn.textContent = '⏳ Checking...';
  btn.disabled = true;

  try {
    const response = await fetch('/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        age:          age,
        income:       income,
        credit_score: creditScore,
        loan_amount:  loanAmount,
        employment:   employment
      })
    });

    const result = await response.json();
    if (result.error) {
      alert('Error: ' + result.error);
    } else {
      renderResult(result);
    }
  } catch (err) {
    alert('Cannot connect to server.\nRun this in your terminal first:\n\n  python server.py');
  } finally {
    btn.textContent = '✦ Check My Eligibility';
    btn.disabled = false;
  }
}

// ─── RENDER RESULT ────────────────────────────────────────────────────────────

function renderResult(r) {
  const panel = document.getElementById('resultPanel');
  const inner = document.getElementById('resultInner');

  panel.className = 'result-panel';
  inner.className = 'result-inner';

  setTimeout(() => {
    panel.classList.add('visible');
    inner.classList.add('result-' + r.status);

    const icons = { approved: '✓', rejected: '✕', review: '⏳' };

    const detailsHTML = r.details && Object.keys(r.details).length > 0 ? `
      <div class="result-details">
        ${Object.entries(r.details).map(([label, value]) => `
          <div class="result-detail-item">
            <div class="result-detail-label">${label}</div>
            <div class="result-detail-value">${value}</div>
          </div>`).join('')}
      </div>` : '';

    const reasonsHTML = r.reasons && r.reasons.length > 0 ? `
      <div class="result-reasons">
        <div class="result-reasons-title">Key Factors</div>
        ${r.reasons.map(reason => `
          <div class="reason-item">
            <div class="reason-dot"></div>
            <span>${reason}</span>
          </div>`).join('')}
      </div>` : '';

    inner.innerHTML = `
      <div class="result-status">
        <div class="result-icon">${icons[r.status] || '?'}</div>
        <div>
          <div class="result-heading">${r.heading}</div>
          <div class="result-sub">${r.sub || ''}</div>
        </div>
      </div>
      ${detailsHTML}
      ${reasonsHTML}
    `;

    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, 50);
}

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
let currentCase = null;

const money = new Intl.NumberFormat('en-DE', { style: 'currency', currency: 'EUR' });
const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));

function setStep(step) {
  $$('.journey-step').forEach((el) => el.classList.toggle('active', Number(el.dataset.step) === step));
}

function renderEvent(event, index, suspicious) {
  return `<article class="event-card ${suspicious ? 'suspicious' : ''}">
    <div class="event-top"><span class="event-type">transaction.created</span><span class="event-time">+${index === 0 ? 0 : [6, 12, 19, 27][index]}s</span></div>
    <div class="event-amount">${money.format(event.amount_eur)}</div>
    <div class="event-bottom"><span class="event-meta">${escapeHtml(event.city)}, ${escapeHtml(event.country)} · ${escapeHtml(event.device_id)}</span><span class="event-meta">${escapeHtml(event.event_id)}</span></div>
  </article>`;
}

async function startDemo() {
  const button = $('#startDemo');
  button.disabled = true;
  button.textContent = 'Replaying events…';
  setStep(1);
  $('#eventStream').innerHTML = '';
  $('#eventCount').textContent = '0 / 5';
  $('#caseView').innerHTML = '<div class="empty-state"><span>…</span><strong>Watching the stream</strong><small>No threshold crossed yet.</small></div>';
  $('#signalList').innerHTML = '<div class="empty-state compact"><span>…</span><strong>Evaluating evidence</strong><small>Rules inspect the event history as each transaction arrives.</small></div>';
  $('#decisionControls').innerHTML = '';
  $('#auditTrail').innerHTML = '<p>Waiting for case activity…</p>';
  $('#recommendation').className = 'decision-badge waiting';
  $('#recommendation').textContent = 'WATCHING';

  try {
    const response = await fetch('/demo/card-testing', { method: 'POST' });
    if (!response.ok) throw new Error('Scenario failed');
    const payload = await response.json();
    const events = payload.source_events || [];

    for (let index = 0; index < events.length; index += 1) {
      $('#eventStream').insertAdjacentHTML('beforeend', renderEvent(events[index], index, index >= 3));
      $('#eventCount').textContent = `${index + 1} / ${events.length}`;
      await new Promise((resolve) => setTimeout(resolve, 320));
    }

    renderCase(payload.case);
    document.querySelector('.case-panel').scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (error) {
    $('#eventStream').innerHTML = '<div class="empty-state"><span>!</span><strong>Could not run the scenario</strong><small>Check the API/deployment health and retry.</small></div>';
  } finally {
    button.disabled = false;
    button.textContent = 'Replay investigation';
  }
}

function renderCase(caseData) {
  currentCase = caseData;
  setStep(2);
  const recommendation = $('#recommendation');
  recommendation.textContent = caseData.recommended_decision;
  recommendation.className = `decision-badge ${caseData.recommended_decision.toLowerCase()}`;

  $('#caseView').innerHTML = `<div class="case-hero">
    <span class="case-label">${escapeHtml(caseData.case_id)}</span>
    <div class="risk-row"><strong class="risk-score">${caseData.risk_score}</strong><span class="risk-caption">risk points from two inspectable rules</span></div>
    <div class="case-kpis">
      <div><strong>${caseData.signals.length}</strong><small>signals</small></div>
      <div><strong>${caseData.related_event_ids.length}</strong><small>source events</small></div>
      <div><strong>${escapeHtml(caseData.status)}</strong><small>case status</small></div>
    </div>
    <div class="source-chain"><strong>Traceability chain</strong><p>event IDs → rule evidence → risk score → ${escapeHtml(caseData.recommended_decision)} recommendation → human decision → audit entry</p></div>
  </div>`;

  $('#signalList').innerHTML = caseData.signals.map((signal) => {
    const evidence = Object.entries(signal.evidence).map(([key, value]) => `<strong>${escapeHtml(key)}</strong>: ${escapeHtml(value)}`).join(' · ');
    return `<article class="signal-card">
      <div class="signal-top"><span class="signal-name">${escapeHtml(signal.name.replaceAll('_', ' '))}</span><span class="signal-score">+${signal.score}</span></div>
      <div class="signal-evidence">${evidence}</div>
      <span class="signal-confidence">${escapeHtml(signal.confidence)} CONFIDENCE · DETERMINISTIC</span>
    </article>`;
  }).join('');

  $('#decisionControls').innerHTML = `<div class="decision-controls">
    <button class="allow" data-decision="ALLOW">Allow</button>
    <button class="review" data-decision="REVIEW">Keep in review</button>
    <button class="block" data-decision="BLOCK">Block</button>
  </div>`;
  $$('[data-decision]').forEach((button) => button.addEventListener('click', () => decide(button.dataset.decision)));
  loadAudit();
}

async function decide(decision) {
  if (!currentCase) return;
  setStep(3);
  const response = await fetch(`/cases/${currentCase.case_id}/decision`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ decision, analyst: 'demo.analyst', reason: 'Evidence reviewed in FraudFlow investigator cockpit' })
  });
  if (!response.ok) return;
  currentCase = await response.json();
  $('#decisionControls').innerHTML = `<div class="hero-note"><strong>Decision recorded:</strong> ${escapeHtml(decision)}. The audit entry retains the evidence that was visible at decision time.</div>`;
  await loadAudit();
}

async function loadAudit() {
  if (!currentCase) return;
  const response = await fetch(`/cases/${currentCase.case_id}/audit`);
  if (!response.ok) return;
  const audit = await response.json();
  $('#auditTrail').innerHTML = audit.map((entry) => `<div class="audit-entry"><strong>${escapeHtml(entry.action)}</strong> · ${escapeHtml(entry.actor)} · ${new Date(entry.timestamp).toLocaleTimeString()}</div>`).join('');
}

async function loadProof() {
  try {
    const response = await fetch('/proof/summary');
    if (!response.ok) throw new Error('Proof unavailable');
    const proof = await response.json();
    $('#proofScore').textContent = `${proof.passed}/${proof.total}`;
    $('#proofItems').innerHTML = proof.evals.map((item) => `<div class="proof-item"><span class="proof-check">✓</span><div><strong>${escapeHtml(item.label)}</strong><small>${escapeHtml(item.detail)}</small></div><span>PASS</span></div>`).join('');
    $('#roleMap').innerHTML = proof.role_map.map((item) => `<div class="role-map-row"><strong>${escapeHtml(item.requirement)}</strong><p>${escapeHtml(item.proof)}</p><a href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer">inspect proof ↗</a></div>`).join('');
  } catch (error) {
    $('#proofScore').textContent = '—';
    $('#proofItems').innerHTML = '<div class="proof-item"><span>!</span><div><strong>Proof API unavailable</strong><small>The repository evidence links below remain inspectable.</small></div><span>CHECK</span></div>';
  }
}

$('#startDemo').addEventListener('click', startDemo);
$$('.journey-step').forEach((step) => step.addEventListener('click', () => {
  const number = Number(step.dataset.step);
  setStep(number);
  if (number === 1) $('#investigation').scrollIntoView({ behavior: 'smooth' });
  if (number === 4) $('#proof').scrollIntoView({ behavior: 'smooth' });
}));
loadProof();

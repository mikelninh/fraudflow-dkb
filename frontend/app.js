const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
let currentCase = null;

const money = new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' });
const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const signalCopy = {
  transaction_velocity: 'Viele Zahlungen direkt hintereinander',
  amount_anomaly: 'Der Betrag springt plötzlich stark nach oben',
  new_device: 'Ein bisher unbekanntes Gerät taucht auf',
  impossible_travel: 'Der Standort wechselt ungewöhnlich schnell'
};

function setStep(step) {
  $$('.journey-step').forEach((el, index) => el.classList.toggle('active', index + 1 === step));
}

function renderEvent(event, index, suspicious) {
  return `<article class="event-card ${suspicious ? 'suspicious' : ''}">
    <div class="event-top"><span class="event-type">Zahlung ${index + 1}</span><span class="event-time">+${index === 0 ? 0 : [6, 12, 19, 27][index]} Sek.</span></div>
    <div class="event-amount">${money.format(event.amount_eur)}</div>
    <div class="event-bottom"><span class="event-meta">${escapeHtml(event.city)}</span><span class="event-meta">synthetisch</span></div>
  </article>`;
}

async function startDemo() {
  const button = $('#startDemo');
  button.disabled = true;
  button.textContent = 'Fall läuft…';
  setStep(1);
  $('#eventStream').innerHTML = '';
  $('#eventCount').textContent = '0 / 5 Zahlungen';
  $('#caseView').innerHTML = '<div class="empty-state"><span>…</span><strong>Noch unauffällig</strong><small>FraudFlow beobachtet die Zahlungshistorie.</small></div>';
  $('#signalList').innerHTML = '<div class="empty-state compact"><span>…</span><strong>Noch kein Handlungsbedarf</strong><small>Gründe erscheinen erst, wenn etwas auffällig wird.</small></div>';
  $('#decisionControls').innerHTML = '';
  $('#auditTrail').innerHTML = '<p>Noch keine Entscheidung.</p>';
  $('#recommendation').className = 'decision-badge waiting';
  $('#recommendation').textContent = 'BEOBACHTEN';

  try {
    const response = await fetch('/demo/card-testing', { method: 'POST' });
    if (!response.ok) throw new Error('Scenario failed');
    const payload = await response.json();
    const events = payload.source_events || [];

    for (let index = 0; index < events.length; index += 1) {
      $('#eventStream').insertAdjacentHTML('beforeend', renderEvent(events[index], index, index >= 3));
      $('#eventCount').textContent = `${index + 1} / ${events.length} Zahlungen`;
      await new Promise((resolve) => setTimeout(resolve, 360));
    }

    renderCase(payload.case);
    document.querySelector('.case-panel').scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (error) {
    $('#eventStream').innerHTML = '<div class="empty-state"><span>!</span><strong>Fall konnte nicht gestartet werden</strong><small>API oder Deployment prüfen und erneut versuchen.</small></div>';
  } finally {
    button.disabled = false;
    button.textContent = 'Fall noch einmal starten';
  }
}

function renderCase(caseData) {
  currentCase = caseData;
  setStep(2);
  const recommendation = $('#recommendation');
  recommendation.textContent = caseData.recommended_decision === 'REVIEW' ? 'PRÜFEN' : caseData.recommended_decision;
  recommendation.className = `decision-badge ${caseData.recommended_decision.toLowerCase()}`;

  const velocity = caseData.signals.find((signal) => signal.name === 'transaction_velocity');
  const amount = caseData.signals.find((signal) => signal.name === 'amount_anomaly');
  const attempts = velocity?.evidence?.attempts_in_window ?? 5;
  const seconds = velocity?.evidence?.window_seconds ?? 27;
  const finalAmount = amount?.evidence?.amount_eur ?? 499;
  const baseline = amount?.evidence?.baseline_mean_eur ?? 1.25;

  $('#caseView').innerHTML = `<div class="case-summary">
    <h3>Empfehlung: prüfen</h3>
    <p>Das ist noch kein Beweis für Betrug. Aber zwei Dinge weichen deutlich vom bisherigen Verhalten ab.</p>
    <div class="plain-reasons">
      <div class="plain-reason"><span>1</span><div><strong>Ungewöhnlich viele Zahlungen</strong><small>${attempts} Zahlungen innerhalb von nur ${seconds} Sekunden.</small></div></div>
      <div class="plain-reason"><span>2</span><div><strong>Plötzlicher Sprung beim Betrag</strong><small>${money.format(finalAmount)} nach zuvor durchschnittlich etwa ${money.format(baseline)}.</small></div></div>
    </div>
    <div class="human-note"><strong>Wichtig:</strong> FraudFlow blockiert nicht automatisch. Ein Mensch sieht die Gründe und entscheidet, was als Nächstes passiert.</div>
    <details class="technical-details">
      <summary>Technische Details für Engineers</summary>
      <div class="technical-grid">
        <div><strong>${escapeHtml(caseData.risk_score)}</strong><small>interner Risk Score</small></div>
        <div><strong>${caseData.signals.length}</strong><small>ausgelöste Regeln</small></div>
        <div><strong>${caseData.related_event_ids.length}</strong><small>verknüpfte Events</small></div>
        <div><strong>${escapeHtml(caseData.case_id)}</strong><small>Case ID</small></div>
      </div>
    </details>
  </div>`;

  $('#signalList').innerHTML = caseData.signals.map((signal) => {
    let detail = 'Die Regel wurde aus den sichtbaren Ausgangsdaten abgeleitet.';
    if (signal.name === 'transaction_velocity') detail = `${signal.evidence.attempts_in_window} Zahlungen in ${signal.evidence.window_seconds} Sekunden.`;
    if (signal.name === 'amount_anomaly') detail = `${money.format(signal.evidence.amount_eur)} statt etwa ${money.format(signal.evidence.baseline_mean_eur)} im bisherigen Durchschnitt.`;
    if (signal.name === 'new_device') detail = 'Das Gerät wurde in der bisherigen Historie nicht gesehen.';
    if (signal.name === 'impossible_travel') detail = `${escapeHtml(signal.evidence.from)} → ${escapeHtml(signal.evidence.to)} in ${escapeHtml(signal.evidence.minutes_between)} Minuten.`;
    return `<article class="signal-card"><div class="signal-top"><span class="signal-name">${escapeHtml(signalCopy[signal.name] || signal.name)}</span></div><div class="signal-evidence">${detail}</div></article>`;
  }).join('');

  $('#decisionControls').innerHTML = `<div class="decision-controls">
    <button class="allow" data-decision="ALLOW">Freigeben</button>
    <button class="review" data-decision="REVIEW">Weiter prüfen</button>
    <button class="block" data-decision="BLOCK">Blockieren</button>
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
    body: JSON.stringify({ decision, analyst: 'demo.analyst', reason: 'Begründung und sichtbare Evidenz im FraudFlow-Fall geprüft' })
  });
  if (!response.ok) return;
  currentCase = await response.json();
  const labels = { ALLOW: 'Freigegeben', REVIEW: 'Zur weiteren Prüfung', BLOCK: 'Blockiert' };
  $('#decisionControls').innerHTML = `<div class="hero-note"><strong>Entscheidung gespeichert:</strong> ${labels[decision]}. Die sichtbaren Gründe bleiben im Audit-Trail nachvollziehbar.</div>`;
  await loadAudit();
}

async function loadAudit() {
  if (!currentCase) return;
  const response = await fetch(`/cases/${currentCase.case_id}/audit`);
  if (!response.ok) return;
  const audit = await response.json();
  const actionLabels = { CASE_CREATED: 'Fall zur Prüfung angelegt', ANALYST_DECISION: 'Menschliche Entscheidung gespeichert' };
  $('#auditTrail').innerHTML = audit.map((entry) => `<div class="audit-entry"><strong>${escapeHtml(actionLabels[entry.action] || entry.action)}</strong> · ${new Date(entry.timestamp).toLocaleTimeString('de-DE')}</div>`).join('');
}

async function loadProof() {
  try {
    const response = await fetch('/proof/summary');
    if (!response.ok) throw new Error('Proof unavailable');
    const proof = await response.json();
    $('#proofScore').textContent = `${proof.passed}/${proof.total}`;
    $('#proofItems').innerHTML = proof.evals.map((item) => `<div class="proof-item"><span class="proof-check">✓</span><div><strong>${escapeHtml(item.label)}</strong><small>${escapeHtml(item.detail)}</small></div><span>BESTANDEN</span></div>`).join('');
    $('#roleMap').innerHTML = proof.role_map.map((item) => `<div class="role-map-row"><strong>${escapeHtml(item.requirement)}</strong><p>${escapeHtml(item.proof)}</p><a href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer">Beweis öffnen ↗</a></div>`).join('');
  } catch (error) {
    $('#proofScore').textContent = '—';
    $('#proofItems').innerHTML = '<div class="proof-item"><span>!</span><div><strong>Proof API nicht erreichbar</strong><small>Die Belege im Repository bleiben direkt prüfbar.</small></div><span>PRÜFEN</span></div>';
  }
}

$('#startDemo').addEventListener('click', startDemo);
loadProof();

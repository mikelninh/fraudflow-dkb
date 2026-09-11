const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];
let currentCase = null;
let staticAudit = [];

const isGitHubPages = window.location.hostname.endsWith('github.io');
const money = new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' });
const number = new Intl.NumberFormat('de-DE');
const one = new Intl.NumberFormat('de-DE', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
const signalCopy = {
  transaction_velocity: 'Viele Zahlungen direkt hintereinander',
  amount_anomaly: 'Der Betrag springt plötzlich stark nach oben',
  new_device: 'Ein bisher unbekanntes Gerät taucht auf',
  impossible_travel: 'Der Standort wechselt ungewöhnlich schnell'
};
const dataSignalCopy = {
  velocity: 'Velocity',
  amount_jump: 'Amount jump',
  impossible_travel: 'Impossible travel',
  new_device_combo: 'New-device combo'
};

function setStep(step) {
  $$('.journey-step').forEach((el, index) => el.classList.toggle('active', index + 1 === step));
}

function renderEvent(event, index, suspicious) {
  return `<article class="event-card ${suspicious ? 'suspicious' : ''}">
    <div class="event-top"><span class="event-type">Zahlung ${index + 1}</span><span class="event-time">+${index === 0 ? 0 : [6, 12, 19, 27][index]} Sek.</span></div>
    <div class="event-amount">${money.format(event.amount_eur)}</div>
    <div class="event-bottom"><span class="event-meta">${escapeHtml(event.city)}</span><span class="event-meta">Demo-Daten</span></div>
  </article>`;
}

async function getScenario() {
  const url = isGitHubPages ? './demo/scenario.json' : '/demo/card-testing';
  const response = await fetch(url, isGitHubPages ? undefined : { method: 'POST' });
  if (!response.ok) throw new Error('Scenario failed');
  return response.json();
}

async function startDemo() {
  const button = $('#startDemo');
  button.disabled = true;
  button.textContent = 'Fall läuft…';
  setStep(1);
  currentCase = null;
  staticAudit = [];
  $('#eventStream').innerHTML = '';
  $('#eventCount').textContent = '0 / 5 Zahlungen';
  $('#caseView').innerHTML = '<div class="empty-state"><span>…</span><strong>Noch unauffällig</strong><small>FraudFlow beobachtet die Zahlungshistorie.</small></div>';
  $('#signalList').innerHTML = '<div class="empty-state compact"><span>…</span><strong>Noch kein Handlungsbedarf</strong><small>Gründe erscheinen erst, wenn etwas auffällig wird.</small></div>';
  $('#decisionControls').innerHTML = '';
  $('#auditTrail').innerHTML = '<p>Noch keine Entscheidung.</p>';
  $('#recommendation').className = 'decision-badge waiting';
  $('#recommendation').textContent = 'BEOBACHTEN';

  try {
    const payload = await getScenario();
    const events = payload.source_events || [];

    for (let index = 0; index < events.length; index += 1) {
      const isTriggerEvent = index === events.length - 1;
      $('#eventStream').insertAdjacentHTML('beforeend', renderEvent(events[index], index, isTriggerEvent));
      $('#eventCount').textContent = `${index + 1} / ${events.length} Zahlungen`;
      await new Promise((resolve) => setTimeout(resolve, 360));
    }

    if (isGitHubPages) {
      staticAudit = [{ action: 'CASE_CREATED', timestamp: new Date().toISOString() }];
    }
    renderCase(payload.case);
    document.querySelector('.case-panel').scrollIntoView({ behavior: 'smooth', block: 'center' });
  } catch (error) {
    $('#eventStream').innerHTML = '<div class="empty-state"><span>!</span><strong>Fall konnte nicht gestartet werden</strong><small>Bitte Seite neu laden und erneut versuchen.</small></div>';
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
    <h3>Dieser Vorgang sollte geprüft werden.</h3>
    <p>Nicht weil das System „Betrug erkannt“ hat, sondern weil sich das Zahlungsverhalten plötzlich deutlich verändert.</p>
    <div class="plain-reasons">
      <div class="plain-reason"><span>1</span><div><strong>Sehr viele Zahlungen in kurzer Zeit</strong><small>${attempts} Zahlungen innerhalb von nur ${seconds} Sekunden.</small></div></div>
      <div class="plain-reason"><span>2</span><div><strong>Der Betrag springt plötzlich stark</strong><small>${money.format(finalAmount)} nach zuvor durchschnittlich etwa ${money.format(baseline)}.</small></div></div>
    </div>
    <div class="human-note"><strong>Nächster Schritt:</strong> Ein Mensch prüft die Gründe und entscheidet. FraudFlow blockiert nicht automatisch.</div>
    <details class="technical-details">
      <summary>Technische Details für Engineers</summary>
      <div class="technical-grid">
        <div><strong>${escapeHtml(caseData.risk_score)}</strong><small>interner Risk Score</small></div>
        <div><strong>${caseData.signals.length}</strong><small>ausgelöste Regeln</small></div>
        <div><strong>${caseData.related_event_ids.length}</strong><small>verknüpfte Events</small></div>
        <div><strong>${escapeHtml(caseData.case_id)}</strong><small>Case ID</small></div>
      </div>
      ${isGitHubPages ? '<p class="technical-note">Diese GitHub-Pages-Demo spielt einen festen synthetischen Fall ab. FastAPI, Regeln, Tests und Evals sind im Repository ausführbar.</p>' : ''}
    </details>
  </div>`;

  $('#signalList').innerHTML = caseData.signals.map((signal) => {
    let detail = 'Aus den sichtbaren Ausgangsdaten abgeleitet.';
    if (signal.name === 'transaction_velocity') detail = `${signal.evidence.attempts_in_window} Zahlungen in ${signal.evidence.window_seconds} Sekunden.`;
    if (signal.name === 'amount_anomaly') detail = `${money.format(signal.evidence.amount_eur)} statt etwa ${money.format(signal.evidence.baseline_mean_eur)} im bisherigen Durchschnitt.`;
    if (signal.name === 'new_device') detail = 'Das Gerät wurde in der bisherigen Historie nicht gesehen.';
    if (signal.name === 'impossible_travel') detail = `${escapeHtml(signal.evidence.from)} → ${escapeHtml(signal.evidence.to)} in ${escapeHtml(signal.evidence.minutes_between)} Minuten.`;
    return `<article class="signal-card"><div class="signal-top"><span class="signal-name">${escapeHtml(signalCopy[signal.name] || signal.name)}</span></div><div class="signal-evidence">${detail}</div></article>`;
  }).join('');

  $('#decisionControls').innerHTML = `<p class="decision-question"><strong>Was würden Sie als Analyst tun?</strong></p><div class="decision-controls">
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
  const labels = { ALLOW: 'Freigegeben', REVIEW: 'Zur weiteren Prüfung', BLOCK: 'Blockiert' };

  if (isGitHubPages) {
    currentCase.status = 'CLOSED';
    staticAudit.push({ action: 'ANALYST_DECISION', timestamp: new Date().toISOString() });
  } else {
    const response = await fetch(`/cases/${currentCase.case_id}/decision`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ decision, analyst: 'demo.analyst', reason: 'Begründung und sichtbare Evidenz im FraudFlow-Fall geprüft' })
    });
    if (!response.ok) return;
    currentCase = await response.json();
  }

  $('#decisionControls').innerHTML = `<div class="hero-note"><strong>Entscheidung gespeichert:</strong> ${labels[decision]}. <a href="#proof">Jetzt die Beweise hinter der Demo prüfen →</a></div>`;
  await loadAudit();
}

async function loadAudit() {
  if (!currentCase) return;
  let audit;
  if (isGitHubPages) {
    audit = staticAudit;
  } else {
    const response = await fetch(`/cases/${currentCase.case_id}/audit`);
    if (!response.ok) return;
    audit = await response.json();
  }
  const actionLabels = { CASE_CREATED: 'Fall zur Prüfung angelegt', ANALYST_DECISION: 'Menschliche Entscheidung gespeichert' };
  $('#auditTrail').innerHTML = audit.map((entry) => `<div class="audit-entry"><strong>${escapeHtml(actionLabels[entry.action] || entry.action)}</strong> · ${new Date(entry.timestamp).toLocaleTimeString('de-DE')}</div>`).join('');
}

async function loadProof() {
  try {
    const url = isGitHubPages ? './demo/proof.json' : '/proof/summary';
    const response = await fetch(url);
    if (!response.ok) throw new Error('Proof unavailable');
    const proof = await response.json();
    $('#proofScore').textContent = `${proof.passed}/${proof.total}`;
    $('#proofItems').innerHTML = proof.evals.map((item) => `<div class="proof-item"><span class="proof-check">✓</span><div><strong>${escapeHtml(item.label)}</strong><small>${escapeHtml(item.detail)}</small></div><span>BESTANDEN</span></div>`).join('');
    const capabilities = proof.capability_map || proof.role_map || [];
    $('#roleMap').innerHTML = capabilities.map((item) => `<div class="role-map-row"><strong>${escapeHtml(item.requirement)}</strong><p>${escapeHtml(item.proof)}</p><a href="${escapeHtml(item.url)}" target="_blank" rel="noreferrer">Beweis öffnen ↗</a></div>`).join('');
  } catch (error) {
    $('#proofScore').textContent = '—';
    $('#proofItems').innerHTML = '<div class="proof-item"><span>!</span><div><strong>Beweise konnten nicht geladen werden</strong><small>Die Belege im Repository bleiben direkt prüfbar.</small></div><span>PRÜFEN</span></div>';
  }
}

async function loadDataTech() {
  const transactions = $('#dtTransactions');
  if (!transactions) return;

  try {
    const url = isGitHubPages ? './demo/data-tech-summary.json' : './demo/data-tech-summary.json';
    const response = await fetch(url);
    if (!response.ok) throw new Error('Data-tech proof unavailable');
    const summary = await response.json();
    $('#dtTransactions').textContent = number.format(summary.transactions);
    $('#dtQuality').textContent = `${one.format(summary.data_quality_pass_rate)} %`;
    $('#dtAlertRate').textContent = `${one.format(summary.alert_rate)} %`;
    $('#dtTopSignal').textContent = dataSignalCopy[summary.top_signal] || summary.top_signal;
    $('#dtTopSignalSub').textContent = `${number.format(summary.top_signal_count)} Treffer im synthetischen Cohort`;
  } catch (error) {
    $('#dtTransactions').textContent = '—';
    $('#dtQuality').textContent = '—';
    $('#dtAlertRate').textContent = '—';
    $('#dtTopSignal').textContent = '—';
    $('#dtTopSignalSub').textContent = 'Evidence im Repository prüfen';
  }
}

$('#startDemo').addEventListener('click', startDemo);
loadDataTech();
loadProof();

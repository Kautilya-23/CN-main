document.addEventListener('DOMContentLoaded', () => {

  // ── ELEMENTS ──────────────────────────────────────────────────────────
  const heroSection = document.getElementById('hero-section');
  const mainForm = document.getElementById('main-form');
  const resultsSection = document.getElementById('results-section');
  const detailsSection = document.getElementById('details-section');

  const symptomsInput = document.getElementById('symptoms-input');
  const cityInput = document.getElementById('city-input');
  const analyzeBtn = document.getElementById('analyze-btn');
  const btnText = document.getElementById('btn-text');
  const btnLoader = document.getElementById('btn-loader');
  const errorMessage = document.getElementById('error-message');

  const newSearchBtn = document.getElementById('new-search-btn');
  const backToResultsBtn = document.getElementById('back-to-results-btn');
  const hospitalFilter = document.getElementById('hospital-filter');
  const hospitalsList = document.getElementById('hospitals-list');

  const summarySymptoms = document.getElementById('summary-symptoms');
  const summaryLocation = document.getElementById('summary-location');
  const aiAnalysisSummary = document.getElementById('ai-analysis-summary');
  const summarySpeciality = document.getElementById('summary-speciality');
  const summaryUrgency = document.getElementById('summary-urgency');
  const summaryDiseases = document.getElementById('summary-diseases');
  const consultNowWrapper = document.getElementById('consult-now-wrapper');

  // ── STATE ─────────────────────────────────────────────────────────────
  let currentHospitals = [];
  let currentAnalysis = null;
  let currentSymptoms = '';
  let currentCity = '';
  let activeSection = 'hero';   // 'hero' | 'results' | 'details'
  let currentDetailHospital = null;    // the hospital object currently shown in details

  // ── PERSISTENCE HELPERS ───────────────────────────────────────────────
  const STORAGE_KEY = 'careNavigator_results';

  function saveState() {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify({
        hospitals: currentHospitals,
        analysis: currentAnalysis,
        symptoms: currentSymptoms,
        city: currentCity,
        activeSection: activeSection,
        detailHospital: currentDetailHospital
      }));
    } catch (e) { /* storage quota hit - ignore */ }
  }

  function clearState() {
    sessionStorage.removeItem(STORAGE_KEY);
  }

  function restoreState() {
    try {
      const raw = sessionStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const saved = JSON.parse(raw);
      if (!saved || !saved.hospitals || saved.hospitals.length === 0) return null;
      currentHospitals = saved.hospitals;
      currentAnalysis = saved.analysis;
      currentSymptoms = saved.symptoms;
      currentCity = saved.city;
      activeSection = saved.activeSection || 'results';
      currentDetailHospital = saved.detailHospital || null;
      return activeSection;   // returns which section to restore
    } catch (e) {
      return null;
    }
  }

  // ── INIT ──────────────────────────────────────────────────────────────
  if (analyzeBtn) {

    analyzeBtn.disabled = false;
  }

  // Restore the section the user was on when they reloaded
  const restoredSection = restoreState();
  if (restoredSection === 'details' && currentDetailHospital) {
    // Render the hospital list in background (needed for filter / back-to-results)
    renderSummary();
    renderHospitals();
    showHospitalDetails(currentDetailHospital);
  } else if (restoredSection === 'results') {
    renderSummary();
    renderHospitals();
    showSection('results');
  }

  // ── EVENT LISTENERS ───────────────────────────────────────────────────
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', handleAnalyze);
  }
  if (newSearchBtn) {
    newSearchBtn.addEventListener('click', () => { clearState(); showSection('hero'); });
  }
  if (backToResultsBtn) {
    backToResultsBtn.addEventListener('click', () => {
      currentDetailHospital = null;
      activeSection = 'results';
      saveState();
      showSection('results');
    });
  }
  if (hospitalFilter) {
    hospitalFilter.addEventListener('change', renderHospitals);
  }
  if (symptomsInput) {
    symptomsInput.addEventListener('input', () => {
      if (analyzeBtn) analyzeBtn.disabled = !symptomsInput.value.trim();
    });
  }

  // ── VOICE INPUT (Web Speech API) ─────────────────────────────────────
  const micBtn = document.getElementById('mic-btn');
  const micListening = document.getElementById('mic-listening');

  if (micBtn && symptomsInput) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      // Browser doesn't support speech recognition - hide the button
      micBtn.style.display = 'none';
    } else {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;

      // Map page language to BCP-47 tags for the Speech API
      const SPEECH_LANG_MAP = {
        'en': 'en-IN', 'hi': 'hi-IN', 'mr': 'mr-IN',
        'gu': 'gu-IN', 'pa': 'pa-IN', 'bn': 'bn-IN',
        'ta': 'ta-IN', 'te': 'te-IN'
      };
      const pageLang = (typeof LANG_PREFIX !== 'undefined' && LANG_PREFIX)
        ? LANG_PREFIX.replace('/', '')
        : 'en';
      recognition.lang = SPEECH_LANG_MAP[pageLang] || 'en-IN';

      let isRecording = false;
      let finalTranscript = '';  // accumulated finalized text

      micBtn.addEventListener('click', () => {
        if (isRecording) {
          recognition.stop();
        } else {
          // Preserve any existing text in the textarea
          finalTranscript = symptomsInput.value;
          try { recognition.start(); } catch (e) { /* already started */ }
        }
      });

      recognition.onstart = () => {
        isRecording = true;
        micBtn.classList.add('recording');
        micBtn.setAttribute('aria-pressed', 'true');
        if (micListening) micListening.classList.add('visible');
      };

      recognition.onend = () => {
        isRecording = false;
        micBtn.classList.remove('recording');
        micBtn.setAttribute('aria-pressed', 'false');
        if (micListening) micListening.classList.remove('visible');
      };

      recognition.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += (finalTranscript ? ' ' : '') + transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        // Show final + interim in the textarea
        symptomsInput.value = finalTranscript + (interimTranscript ? ' ' + interimTranscript : '');
        // Enable the analyze button
        if (analyzeBtn) analyzeBtn.disabled = !symptomsInput.value.trim();
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        isRecording = false;
        micBtn.classList.remove('recording');
        micBtn.setAttribute('aria-pressed', 'false');
        if (micListening) micListening.classList.remove('visible');

        if (event.error === 'not-allowed' || event.error === 'service-not-allowed') {
          showError(T.errorGeneric || 'Microphone access denied. Please allow microphone access and try again.');
        }
      };
    }
  }

  // ── NAVIGATION ────────────────────────────────────────────────────────
  function showSection(section) {
    if (heroSection) heroSection.style.display = 'none';
    if (mainForm) mainForm.style.display = 'none';
    if (resultsSection) resultsSection.style.display = 'none';
    if (detailsSection) detailsSection.style.display = 'none';

    if (section === 'hero') {
      if (heroSection) heroSection.style.display = 'block';
      if (mainForm) mainForm.style.display = 'block';
    } else if (section === 'results') {
      if (resultsSection) resultsSection.style.display = 'block';
    }
    else if (section === 'details') {
      if (detailsSection) detailsSection.style.display = 'block';
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // ── LOADING STATE ─────────────────────────────────────────────────────
  function setLoading(isLoading) {
    if (!analyzeBtn || !btnText || !btnLoader) return;
    analyzeBtn.disabled = isLoading;
    if (isLoading) {
      btnText.style.display = 'none';
      btnLoader.style.display = 'flex';
    } else {
      btnText.style.display = 'flex';
      btnLoader.style.display = 'none';
    }
  }

  // ── ERROR STATE ───────────────────────────────────────────────────────
  function showError(msg) {
    if (!errorMessage) return;
    const msgEl = errorMessage.querySelector('span') || errorMessage;
    if (errorMessage.querySelector('span')) {
      errorMessage.querySelector('span').textContent = msg;
    } else {
      errorMessage.textContent = msg;
    }
    errorMessage.classList.add('visible');
  }

  function hideError() {
    if (!errorMessage) return;
    errorMessage.classList.remove('visible');
  }


  // ── ANALYZE ───────────────────────────────────────────────────────────
  async function handleAnalyze() {
    const symptoms = symptomsInput.value.trim();
    const city = cityInput.value;
    if (!symptoms) return;

    setLoading(true);
    hideError();

    try {
      // 1. Analyze symptoms
      const analyzeRes = await fetch(LANG_PREFIX + '/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms_text: symptoms, location: city })
      });
      const analyzeData = await analyzeRes.json();
      if (analyzeData.error) throw new Error(analyzeData.error);

      currentAnalysis = analyzeData.analysis;
      currentSymptoms = symptoms;
      currentCity = city;

      // 2. Search hospitals
      const speciality = currentAnalysis?.speciality || 'General Physician';
      const disease = currentAnalysis?.possible_diseases?.[0]?.name || 'General';
      const params = new URLSearchParams({ speciality, city, disease });

      const hospitalsRes = await fetch(`${LANG_PREFIX}/api/hospitals?${params.toString()}`);
      const hospitalsData = await hospitalsRes.json();
      if (hospitalsData.error) throw new Error(hospitalsData.error);

      currentHospitals = hospitalsData.hospitals;
      activeSection = 'results';
      currentDetailHospital = null;

      // 3. Persist & Render
      saveState();
      renderSummary();
      renderHospitals();
      showSection('results');

    } catch (err) {
      console.error(err);
      showError(T.errorGeneric);
    } finally {
      setLoading(false);
    }
  }

  // ── RENDER SUMMARY SIDEBAR ────────────────────────────────────────────
  function renderSummary() {
    if (summarySymptoms) summarySymptoms.textContent = currentSymptoms || '-';
    if (summaryLocation) summaryLocation.textContent = currentCity || '-';

    if (!currentAnalysis) return;

    if (aiAnalysisSummary) aiAnalysisSummary.classList.remove('hidden');
    if (summarySpeciality) summarySpeciality.textContent = currentAnalysis.speciality || '-';

    // Urgency badge - classes defined in results_section CSS
    const urgency = (currentAnalysis.urgency || 'low').toLowerCase();
    if (summaryUrgency) {
      summaryUrgency.textContent = urgency.charAt(0).toUpperCase() + urgency.slice(1);
      summaryUrgency.className = 'urgency-badge ' + (
        urgency === 'high' ? 'urgency-high' :
          urgency === 'medium' ? 'urgency-medium' :
            'urgency-low'
      );
    }

    // Consult Now wrapper visibility based on urgency
    if (consultNowWrapper) {
      if (urgency === 'low') {
        consultNowWrapper.classList.remove('hidden');
      } else {
        consultNowWrapper.classList.add('hidden');
      }
    }

    // Possible diseases
    if (summaryDiseases) {
      summaryDiseases.innerHTML = '';
      (currentAnalysis.possible_diseases || []).forEach(d => {
        const div = document.createElement('div');
        div.className = 'disease-tag';
        div.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="12"/>
            <line x1="12" y1="16" x2="12.01" y2="16"/>
          </svg>
          <span style="flex:1">${d.name}</span>
          <span style="font-family:'DM Mono',monospace;font-size:13px;color:#9ca3af">
            ${(d.probability * 100).toFixed(0)}%
          </span>`;
        summaryDiseases.appendChild(div);
      });
    }
  }

  // ── RENDER HOSPITAL CARDS ─────────────────────────────────────────────
  function renderHospitals() {
    hospitalsList.innerHTML = '';
    const filter = hospitalFilter.value;
    const filtered = currentHospitals.filter(h =>
      filter === 'all' ? true : (h.hospital_type || '').toLowerCase() === filter
    );

    if (filtered.length === 0) {
      hospitalsList.innerHTML = `
        <div style="
          background:#ffffff;border:1px dashed #e5e5e3;border-radius:16px;
          padding:48px 24px;text-align:center;
        ">
          <p style="font-size:14px;color:#9ca3af;font-weight:300;">
            ${T.noHospitals}
          </p>
        </div>`;
      return;
    }

    filtered.forEach(h => {
      const card = document.createElement('div');
      card.className = 'result-card';
      card.setAttribute('role', 'article');
      card.setAttribute('aria-label', h.name);
      const stars = h.rating ? `
        <div class="rc-badge-rating" aria-label="Rating ${h.rating} out of 5">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          <span>${h.rating}</span>
        </div>` : '';

      const beds = h.total_beds ? `
        <div class="rc-stat beds">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
            <path d="M2 4v16M2 8h18a2 2 0 0 1 2 2v10M2 16h20M6 8v8"/>
          </svg>
          <span>${h.total_beds}</span> ${T.beds}
        </div>` : '';

      const docs = h.doctor_count ? `
        <div class="rc-stat docs">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          <span>${h.doctor_count}</span> ${T.doctors}
        </div>` : '';

      const cost = h.cost_text ? `
        <div class="rc-stat cost">
          
          <span>${h.cost_text}</span>
        </div>` : '';

      const specs = (h.specialities || []).slice(0, 4)
        .map(s => `<span class="rc-spec">${s}</span>`).join('');

      const hasStats = h.total_beds || h.doctor_count || h.cost_text;
      card.innerHTML = `
        <div class="rc-arrow view-details-btn" aria-hidden="true">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            aria-hidden="true" focusable="false">
            <line x1="5" y1="12" x2="19" y2="12"/>
            <polyline points="12 5 19 12 12 19"/>
          </svg>
        </div>

        <div class="rc-badges">
          <span class="rc-badge-type">${h.hospital_type || T.hospital}</span>
          ${stars}
        </div>

        <h4 class="rc-name">${h.name}</h4>

        <p class="rc-address">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
            aria-hidden="true" focusable="false">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
            <circle cx="12" cy="10" r="3"/>
          </svg>
          ${h.address}${h.city ? ', ' + h.city : ''}
        </p>

        ${hasStats ? `
        <div class="rc-divider"></div>
        <div class="rc-stats">${beds}${docs}${cost}</div>` : ''}

        ${specs ? `<div class="rc-specs">${specs}</div>` : ''}

        <div class="rc-divider"></div>

        <div style="display:flex;gap:10px;">
          <button class="view-details-btn btn-directions" aria-label="${T.details} - ${h.name}">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              style="width:13px;height:13px;" aria-hidden="true" focusable="false">
              <circle cx="11" cy="11" r="8"/>
              <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            ${T.details}
          </button>

          ${h.map_url ? `
          <a href="${h.map_url}" target="_blank" aria-label="${T.directions} - ${h.name}" style="
            flex:1;display:flex;align-items:center;justify-content:center;gap:6px;
            padding:10px 14px;background:#0f0f0f;border:1px solid #0f0f0f;
            border-radius:10px;font-family:'DM Sans',sans-serif;font-size:13px;
            font-weight:600;color:#ffffff;text-decoration:none;
            transition:background 0.15s;
          ">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              style="width:13px;height:13px;" aria-hidden="true" focusable="false">
              <polygon points="3 11 22 2 13 21 11 13 3 11"/>
            </svg>
            ${T.directions}
          </a>` : `
          <button disabled aria-disabled="true" style="
            flex:1;padding:10px 14px;background:#fafaf9;border:1px solid #e5e5e3;
            border-radius:10px;font-size:13px;font-weight:600;color:#d1d5db;
            cursor:not-allowed;font-family:'DM Sans',sans-serif;
          ">${T.noMap}</button>`}
        </div>`;

      card.querySelectorAll('.view-details-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          showHospitalDetails(h);
        });
      });

      // Hover styles for the details button via JS (no Tailwind needed)
      const detailsBtn = card.querySelector('.view-details-btn');
      detailsBtn.addEventListener('mouseenter', () => {
        detailsBtn.style.background = '#f0f9ff';
        detailsBtn.style.borderColor = '#bae6fd';
        detailsBtn.style.color = '#0ea5e9';
      });
      detailsBtn.addEventListener('mouseleave', () => {
        detailsBtn.style.background = '#fafaf9';
        detailsBtn.style.borderColor = '#e5e5e3';
        detailsBtn.style.color = '#4b5563';
      });

      hospitalsList.appendChild(card);
    });
  }

  // ── HOSPITAL DETAIL VIEW ──────────────────────────────────────────────
  async function showHospitalDetails(hospital) {
    const content = document.getElementById('hospital-detail-content');

    // Persist which hospital is open BEFORE the async fetch so a
    // reload mid-load will still restore the right details page.
    currentDetailHospital = hospital;
    activeSection = 'details';
    saveState();

    // Show a loading state
    content.innerHTML = `
    <div style="padding:60px;text-align:center;" role="status" aria-live="polite">
      <div class="btn-spinner" style="margin:0 auto 12px;width:24px;height:24px;" aria-hidden="true"></div>
      <p style="font-size:13px;color:#9ca3af;">${T.loadingDetails}</p>
    </div>`;

    showSection('details');

    try {
      // Fetch the detail page - Django already renders everything
      const res = await fetch(`${LANG_PREFIX}/hospitals/${hospital.id}/`);
      const html = await res.text();

      // Parse and extract just the content block
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const pageBody = doc.querySelector('.detail-page');

      // Inject into the detail section
      content.innerHTML = '';
      content.appendChild(pageBody);

      // Prepend the cost card
      const costCard = buildCostCard(hospital);
      pageBody.querySelector('.dpage-body').insertAdjacentHTML('afterbegin', costCard);

    } catch (err) {
      console.error(err);
      content.innerHTML = `<p style="padding:40px;text-align:center;color:#9ca3af;" role="alert">${T.failedDetails}</p>`;
    }
  }

  function buildCostCard(hospital) {
    if (!hospital.cost_text) return '';
    return `
    <div class="cost-summary-card" style="
      background:#fff;border:1px solid #e9e9e7;border-radius:16px;
      padding:20px 24px;margin-bottom:20px;
      display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:16px;
    ">
      <div style="flex:1; min-width:200px;">
        <span style="font-family:'DM Mono',monospace;font-size:12px;text-transform:uppercase;
          letter-spacing:0.1em;color:#a6a695;display:block;margin-bottom:4px;">
          ${T.summaryOfSymptoms}
        </span>
        <span style="font-family:'DM Sans',sans-serif;font-size:15px;font-weight:500;
          color:#0f0f0f;letter-spacing:-0.01em;display:block;margin-bottom:12px;line-height:1.5;">
          ${currentSymptoms}
        </span>
      
        <span style="font-family:'DM Mono',monospace;font-size:12px;text-transform:uppercase;
          letter-spacing:0.1em;color:#a6a695;display:block;margin-bottom:4px;">
          ${T.estimatedCost}
        </span>
        <span style="font-family:'DM Mono',monospace;font-size:22px;font-weight:500;
          color:#0f0f0f;letter-spacing:-0.03em;display:block;">
          ${hospital.cost_text}
        </span>
      </div>
      <div class="cost-summary-actions" style="display:flex;flex-direction:column;gap:8px;align-items:stretch;min-width:180px;width:100%;max-width:240px;">
        <button class="btn-primary" style="white-space:nowrap; position:relative; display:flex; align-items:center; justify-content:center; gap:6px; width:100%; margin:0;">
          ${T.bookAppointment}
          <span style="font-family:'DM Sans',sans-serif; font-size:9px; font-weight:700; text-transform:uppercase; background:#38bdf8; color:#0f0f0f; padding:2px 6px; border-radius:4px; line-height:1; letter-spacing:0.04em;">Soon</span>
        </button>
        <button class="btn-secondary" style="white-space:nowrap; width:100%; display:flex; align-items:center; justify-content:center;">${T.callHospital}</button>
      </div>
    </div>`;
  }

}); // end DOMContentLoaded
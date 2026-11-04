/**
 * LankaMedi AI — Client Application Controller (v2.0 Redesign)
 */

let currentLang = 'en';
let selectedFile = null;
let currentAnalysisData = null;

// Preset Scenarios for Sri Lankan Clinical Education
const PRESET_SCENARIOS = {
    dengue: {
        en: `PATIENT DIAGNOSTIC REPORT — HEMATOLOGY
Hospital: Colombo National Hospital (NHSL)
Patient Name: Mr. K. Silva
NIC: 921456789V | Phone: 0772345678
Clinical Notes: Day 4 high continuous fever, retro-orbital pain, bleeding gums, severe lethargy. Suspected Dengue Hemorrhagic Fever.

INVESTIGATION RESULTS:
- Full Blood Count (FBC):
  * Hemoglobin (Hb): 15.2 g/dL (Rising hematocrit)
  * Platelet Count: 32,000 /uL (Critically Low, Ref: 150,000 - 450,000 /uL)
  * White Blood Cells (WBC): 2,400 /uL (Leukopenia)

URGENT MEDICAL ACTION: Immediate inpatient fluid management & admission protocol indicated.`,
        si: `රෝග විනිශ්චය රසායනාගාර වාර්තාව — රක්තවේදය
රෝහල: කොළඹ ජාතික රෝහල (NHSL)
රෝගියා: කේ. සිල්වා මහතා
ජා.හැ.අංකය: 921456789V | දුරකථනය: 0772345678
සායනික සටහන: දින 4ක් තිස්සේ පවතින තද උණ, ඇස් යට වේදනාව, විදුරුමහෙන් ලේ ගැලීම. ඩෙංගු රක්තපාත උණ සැකය.

පරීක්ෂණ වාර්තාව:
- පට්ටිකා ගණන (Platelet Count): 32,000 /uL (අතිශය අඩු මට්ටමක පවතී, සාමාන්‍ය: 150,000 - 450,000 /uL)
- හිමොග්ලොබින් (Hemoglobin): 15.2 g/dL
- සුදු රුධිරාණු (WBC): 2,400 /uL`,
        ta: `மருத்துவ ஆய்வக அறிக்கை — இரத்தவியல்
மருத்துவமனை: கொழும்பு தேசிய மருத்துவமனை
நோயாளி பெயர்: திரு. கே. சில்வா
அடையாள அட்டை: 921456789V | தொலைபேசி: 0772345678
மருத்துவக் குறிப்பு: 4 நாட்களாக நீடிக்கும் காய்ச்சல், ஈறுகளில் இரத்தப்போக்கு. டெங்கு காய்ச்சல் சந்தேகம்.

பரிசோதனை முடிவுகள்:
- இரத்த தட்டணுக்கள் (Platelet Count): 32,000 /uL (மிகவும் ஆபத்தான குறைவு)
- ஹீமோகுளோபின் (Hemoglobin): 15.2 g/dL
- வெள்ளையணுக்கள் (WBC): 2,400 /uL`
    },

    diabetes: {
        en: `PATIENT DIAGNOSTIC REPORT — BIOCHEMISTRY
Laboratory: Asiri Surgical Hospital Diagnostics, Colombo
Patient Name: Mrs. Priyanthi Wickramasinghe
NIC: 197482301928 | Phone: 0718765432
Age: 51 Years | Gender: Female
Clinical Notes: Review for routine diabetes management and mixed dyslipidemia.

LABORATORY INVESTIGATION:
1. Glycemic Parameters:
   - Fasting Blood Sugar (FBS): 154 mg/dL (High, Ref: 70 - 100 mg/dL)
   - Glycated Hemoglobin (HbA1c): 7.8 % (High, Ref: < 5.7 %)

2. Lipid Profile:
   - Total Cholesterol: 242 mg/dL (High, Ref: < 200 mg/dL)
   - LDL Cholesterol: 158 mg/dL (Elevated, Ref: < 100 mg/dL)
   - HDL Cholesterol: 41 mg/dL (Borderline)
   - Serum Triglycerides: 215 mg/dL (High, Ref: < 150 mg/dL)

3. Renal Screening:
   - Serum Creatinine: 0.9 mg/dL (Normal, Ref: 0.6 - 1.2 mg/dL)`,
        si: `රසායනාගාර පරීක්ෂණ වාර්තාව — ජෛව රසායනය
රසායනාගාරය: ආසිරි රෝහල, කොළඹ
රෝගියා: ප්‍රියන්ති වික්‍රමසිංහ මහත්මිය
ජා.හැ.අංකය: 197482301928 | දුරකථනය: 0718765432
වයස: අවුරුදු 51 | ගැහැණු

පරීක්ෂණ වාර්තාව:
- නිරාහාර රුධිර සීනි (FBS): 154 mg/dL (ඉහළ අගයක්, සාමාන්‍ය: 70 - 100 mg/dL)
- Glycated Hemoglobin (HbA1c): 7.8 % (ඉහළ අගයක්)
- සම්පූර්ණ කොලෙස්ටරෝල්: 242 mg/dL (ඉහළ අගයක්, සාමාන්‍ය: < 200 mg/dL)
- LDL කොලෙස්ටරෝල්: 158 mg/dL (ඉහළ අගයක්)
- සෙරම් ක්‍රියැටිනින්: 0.9 mg/dL (සාමාන්‍ය මට්ටම)`,
        ta: `மருத்துவ ஆய்வக அறிக்கை
ஆய்வகம்: ஆசிரி மருத்துவமனை, கொழும்பு
நோயாளி: திருமதி பிரியந்தி விக்கிரமசிங்க
அடையாள அட்டை: 197482301928 | தொலைபேசி: 0718765432

பரிசோதனை முடிவுகள்:
- இரத்த சர்க்கரை அளவு (FBS): 154 mg/dL (அதிகம்)
- HbA1c: 7.8 % (அதிகம்)
- மொத்த கொலஸ்ட்ரால்: 242 mg/dL (அதிகம்)
- எல்.டி.எல் (LDL): 158 mg/dL (அதிகம்)
- சீரம் கிரியேட்டினின்: 0.9 mg/dL (சாதாரண நிலை)`
    },

    kidney: {
        en: `LABORATORY INVESTIGATION REPORT — NEPHROLOGY
Laboratory: Nawaloka Hospitals PLC, Colombo
Patient Name: Mr. D. Gunasekara
Age: 64 Years | Gender: Male
Clinical Notes: Longstanding hypertension, generalized ankle edema, decreased urine output.

RENAL FUNCTION PANEL:
- Serum Creatinine: 2.8 mg/dL (Significantly Elevated, Ref: 0.6 - 1.2 mg/dL)
- Blood Urea: 72 mg/dL (High, Ref: 15 - 45 mg/dL)
- Hemoglobin (Hb): 9.8 g/dL (Moderate normocytic anemia of chronic disease)
- Serum Potassium: 5.4 mmol/L (Borderline high)

CLINICAL RECOMMENDATION: Urgent nephrology consultation & renal ultrasound recommended.`,
        si: `රසායනාගාර වාර්තාව — වකුගඩු ක්‍රියාකාරීත්වය
රෝහල: නවලෝක රෝහල, කොළඹ
රෝගියා: ඩී. ගුණසේකර මහතා | වයස: 64
සායනික සටහන: වළලුකර ඉදිමීම සහ මුත්‍රා පිටවීම අඩුවීම.

වකුගඩු පරීක්ෂණ වාර්තාව:
- සෙරම් ක්‍රියැටිනින් (Serum Creatinine): 2.8 mg/dL (ඉතා ඉහළ අගයක්, සාමාන්‍ය: 0.6 - 1.2 mg/dL)
- හිමොග්ලොබින් (Hemoglobin): 9.8 g/dL (අඩු මට්ටමක පවතී)
- Blood Urea: 72 mg/dL (ඉහළ අගයක්)

වහාම වකුගඩු විශේෂඥ වෛද්‍යවරයකු (Nephrologist) හමුවිය යුතුය.`,
        ta: `மருத்துவ ஆய்வக அறிக்கை — சிறுநீரக செயல்பாடு
மருத்துவமனை: நவலொக மருத்துவமனை
நோயாளி: திரு. டி. குணசேகர | வயது: 64

சிறுநீரக பரிசோதனை முடிவுகள்:
- சீரம் கிரியேட்டினின் (Serum Creatinine): 2.8 mg/dL (மிக அதிகம்)
- ஹீமோகுளோபின் (Hemoglobin): 9.8 g/dL (குறைவு)
- இரத்த யூரியா: 72 mg/dL (அதிகம்)

உடனடியாக சிறுநீரக மருத்துவ நிபுணரை அணுகவும்.`
    },

    normal: {
        en: `ROUTINE ANNUAL HEALTH CHECKUP REPORT
Laboratory: Durdans Hospital Diagnostics, Colombo
Patient Name: Ms. Nilmini Jayawardena
Age: 29 Years | Gender: Female
Clinical Indications: Pre-employment executive annual medical wellness screening.

INVESTIGATION RESULTS:
- Fasting Blood Sugar (FBS): 86 mg/dL (Normal, Ref: 70 - 100 mg/dL)
- Hemoglobin (Hb): 13.4 g/dL (Normal, Ref: 11.5 - 16.5 g/dL)
- Platelet Count: 245,000 /uL (Normal, Ref: 150,000 - 450,000 /uL)
- Total Cholesterol: 172 mg/dL (Desirable, Ref: < 200 mg/dL)
- Serum Creatinine: 0.8 mg/dL (Normal, Ref: 0.6 - 1.2 mg/dL)
- Alanine Aminotransferase (ALT/SGPT): 22 U/L (Normal, Ref: 7 - 55 U/L)

SUMMARY: All biochemical and hematological indicators are within healthy physiological limits.`,
        si: `වාර්ෂික සාමාන්‍ය සෞඛ්‍ය පරීක්ෂණ වාර්තාව
රසායනාගාරය: ඩර්ඩන්ස් රෝහල, කොළඹ
රෝගියා: නිල්මිණි ජයවර්ධන මෙනෙවිය | වයස: 29

පරීක්ෂණ වාර්තාව:
- නිරාහාර රුධිර සීනි (FBS): 86 mg/dL (සාමාන්‍ය යහපත් මට්ටම)
- හිමොග්ලොබින් (Hb): 13.4 g/dL (සාමාන්‍ය මට්ටම)
- පට්ටිකා ගණන (Platelets): 245,000 /uL (සාමාන්‍ය මට්ටම)
- සම්පූර්ණ කොලෙස්ටරෝල්: 172 mg/dL (සාමාන්‍ය යහපත් මට්ටම)
- සෙරම් ක්‍රියැටිනින්: 0.8 mg/dL (සාමාන්‍ය මට්ටම)

සාරාංශය: සියලුම රසායනාගාර අගයන් නිරෝගී සාමාන්‍ය මට්ටමේ පවතී.`,
        ta: `வழக்கமான வருடாந்திர மருத்துவ பரிசோதனை
ஆய்வகம்: டர்டன்ஸ் மருத்துவமனை, கொழும்பு
நோயாளி: செல்வி நில்மினி ஜயவர்தன | வயது: 29

பரிசோதனை முடிவுகள்:
- இரத்த சர்க்கரை (FBS): 86 mg/dL (சாதாரண நிலை)
- ஹீமோகுளோபின் (Hb): 13.4 g/dL (சாதாரண நிலை)
- இரத்த தட்டணுக்கள் (Platelets): 245,000 /uL (சாதாரண நிலை)
- மொத்த கொலஸ்ட்ரால்: 172 mg/dL (சாதாரண நிலை)
- சீரம் கிரியேட்டினின்: 0.8 mg/dL (சாதாரண நிலை)

அனைத்து ஆய்வக முடிவுகளும் ஆரோக்கியமான இயல்பான வரம்பிற்குள் உள்ளன.`
    }
};

document.addEventListener('DOMContentLoaded', () => {
    initLanguage();
    initNavbar();
    initDropzone();
    initTabs();
    initPresetScenarios();
    initPrivacyAudit();
    initEventListeners();
    loadReferenceRanges();
    initFaqAccordion();
    registerServiceWorker();
    setupNetworkStatusListeners();
    setupPwaInstall();
});

function initLanguage() {
    const savedLang = localStorage.getItem('lankamedi_lang') || 'en';
    setLanguage(savedLang);
}

function setLanguage(lang) {
    if (!I18N_TRANSLATIONS[lang]) return;
    currentLang = lang;
    localStorage.setItem('lankamedi_lang', lang);

    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    const dict = I18N_TRANSLATIONS[lang];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = dict[key];
            } else {
                el.textContent = dict[key];
            }
        }
    });
}

function initTabs() {
    const triggers = document.querySelectorAll('.tab-trigger');
    triggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            triggers.forEach(t => t.classList.remove('active'));
            trigger.classList.add('active');

            const tab = trigger.dataset.tab;
            if (tab === 'file') {
                document.getElementById('fileTabPanel').style.display = 'block';
                document.getElementById('textTabPanel').style.display = 'none';
            } else {
                document.getElementById('fileTabPanel').style.display = 'none';
                document.getElementById('textTabPanel').style.display = 'block';
            }
        });
    });
}

function initPresetScenarios() {
    document.querySelectorAll('.preset-pill').forEach(pill => {
        pill.addEventListener('click', () => {
            const presetKey = pill.dataset.preset;
            const scenario = PRESET_SCENARIOS[presetKey];
            if (!scenario) return;

            // Switch to text tab
            document.querySelectorAll('.tab-trigger')[1].click();
            const text = scenario[currentLang] || scenario.en;
            const textarea = document.getElementById('reportTextArea');
            textarea.value = text;
            textarea.classList.add('flash-highlight');
            setTimeout(() => textarea.classList.remove('flash-highlight'), 600);

            // Scroll workspace into view
            const workspace = document.getElementById('workspaceCard');
            if (workspace) {
                workspace.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}

function initPrivacyAudit() {
    const auditBtn = document.getElementById('btnAuditPrivacy');
    if (!auditBtn) return;

    auditBtn.addEventListener('click', async () => {
        const textarea = document.getElementById('reportTextArea');
        const text = textarea.value.trim();
        if (!text) {
            alert('Please paste some medical report text first to test privacy redaction.');
            return;
        }

        auditBtn.disabled = true;
        auditBtn.textContent = 'Auditing PII...';

        try {
            const resp = await fetch('/api/v1/deidentify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text }),
            });
            const data = await resp.json();
            if (resp.ok && data.sanitized_text) {
                textarea.value = data.sanitized_text;
                textarea.classList.add('flash-highlight');
                setTimeout(() => textarea.classList.remove('flash-highlight'), 600);
                showToast('🛡️ All NIC numbers, phone numbers & patient identifiers have been masked!');
            }
        } catch (err) {
            alert('Privacy audit failed: ' + err.message);
        } finally {
            auditBtn.disabled = false;
            auditBtn.textContent = I18N_TRANSLATIONS[currentLang]?.btnAuditPrivacy || '🛡️ Audit Privacy (Mask NIC & Phone)';
        }
    });
}

function initDropzone() {
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');

    if (!dropzone || !fileInput) return;

    ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropzone.classList.remove('dragover');
        }, false);
    });

    dropzone.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        if (dt.files.length > 0) {
            handleFileSelection(dt.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    const removeBtn = document.getElementById('removeFileBtn');
    if (removeBtn) {
        removeBtn.addEventListener('click', clearSelectedFile);
    }
}

function handleFileSelection(file) {
    selectedFile = file;
    const preview = document.getElementById('filePreview');
    const nameEl = document.getElementById('previewFileName');
    const sizeEl = document.getElementById('previewFileSize');
    const thumbEl = document.getElementById('previewThumb');

    nameEl.textContent = file.name;
    sizeEl.textContent = `${(file.size / 1024).toFixed(1)} KB`;

    if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (e) => {
            thumbEl.innerHTML = `<img src="${e.target.result}" style="width:100%; height:100%; border-radius:8px; object-fit:cover;">`;
        };
        reader.readAsDataURL(file);
    } else {
        thumbEl.innerHTML = `📄`;
    }

    preview.classList.add('active');
}

function clearSelectedFile() {
    selectedFile = null;
    document.getElementById('fileInput').value = '';
    document.getElementById('filePreview').classList.remove('active');
}

function initEventListeners() {
    const startBtn = document.getElementById('startConversationBtn');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            const workspace = document.getElementById('workspaceCard');
            if (workspace) {
                workspace.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    }

    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', runAnalysis);
    }

    const exportBtn = document.getElementById('exportBtn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => window.print());
    }

    const shareBtn = document.getElementById('shareWhatsAppBtn');
    if (shareBtn) {
        shareBtn.addEventListener('click', shareOnWhatsApp);
    }

    const resetBtn = document.getElementById('resetAnalysisBtn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            document.getElementById('resultsContainer').style.display = 'none';
            document.getElementById('emergencyBanner').classList.remove('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

async function runAnalysis() {
    const activeTab = document.querySelector('.tab-trigger.active').dataset.tab;
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-label');
    const spinner = analyzeBtn.querySelector('.spinner');

    let fetchOptions = {};

    if (activeTab === 'file') {
        if (!selectedFile) {
            alert('Please select or drag & drop a medical report file (PDF or Image).');
            return;
        }
        const formData = new FormData();
        formData.append('report_file', selectedFile);
        formData.append('language', currentLang);
        fetchOptions = {
            method: 'POST',
            body: formData,
        };
    } else {
        const text = document.getElementById('reportTextArea').value.trim();
        if (!text) {
            alert('Please enter or paste medical report contents.');
            return;
        }
        fetchOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                report_text: text,
                language: currentLang,
            }),
        };
    }

    // UI Loading state
    analyzeBtn.disabled = true;
    spinner.style.display = 'inline-block';
    btnText.textContent = I18N_TRANSLATIONS[currentLang]?.btnAnalyzing || 'Analyzing Report...';
    document.getElementById('resultsContainer').style.display = 'none';
    document.getElementById('emergencyBanner').classList.remove('active');

    try {
        const response = await fetch('/api/v1/analyze', fetchOptions);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Medical analysis request failed.');
        }

        currentAnalysisData = data;
        renderAnalysisResults(data);
    } catch (err) {
        alert(`Analysis Error: ${err.message}`);
    } finally {
        analyzeBtn.disabled = false;
        spinner.style.display = 'none';
        btnText.textContent = I18N_TRANSLATIONS[currentLang]?.btnAnalyze || 'Analyze Report';
    }
}

function renderAnalysisResults(data) {
    const resultsContainer = document.getElementById('resultsContainer');
    const statusBadge = document.getElementById('statusBadge');
    const statusDesc = document.getElementById('statusDescription');

    // Status Indicator
    statusBadge.textContent = data.status;
    statusBadge.style.backgroundColor = data.color || '#0f766e';

    if (data.status === 'Critical') {
        statusDesc.textContent = 'Severe or life-threatening indicators identified. Seek hospital evaluation immediately.';
    } else if (data.status === 'Needs Attention') {
        statusDesc.textContent = 'Out-of-range clinical parameters found. Review recommendations with your physician.';
    } else {
        statusDesc.textContent = 'Key diagnostic indicators are within standard physiological reference ranges.';
    }

    // Emergency Alert Handling (1990 Suwa Seriya)
    const emergencyBanner = document.getElementById('emergencyBanner');
    if (data.emergency_alert && data.emergency_alert.is_emergency) {
        document.getElementById('emergencyReason').textContent = data.emergency_alert.trigger_reason;
        document.getElementById('emergencyActionPlan').textContent = data.emergency_alert.action_plan;
        emergencyBanner.classList.add('active');
    } else {
        emergencyBanner.classList.remove('active');
    }

    // Metrics Counters
    animateValue('criticalIssuesCount', data.critical_issues || 0);
    animateValue('warningIssuesCount', data.warning_issues || 0);
    animateValue('positiveIndicatorsCount', data.positive_indicators || 0);

    // Biomarkers Grid with Visual Range Sliders
    renderBiomarkers(data.biomarkers || []);

    // Treatment Plan Columns
    renderPlanSection('conditionsList', data.treatment_plan?.conditions || []);
    renderPlanSection('medicationsList', data.treatment_plan?.medications || []);
    renderPlanSection('lifestyleList', data.treatment_plan?.lifestyle || []);
    renderPlanSection('notesList', data.treatment_plan?.notes || []);

    // Display container and scroll
    resultsContainer.style.display = 'block';
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function renderBiomarkers(biomarkers) {
    const container = document.getElementById('biomarkersContainer');
    const section = document.getElementById('biomarkersSection');

    if (!biomarkers || biomarkers.length === 0) {
        section.style.display = 'none';
        return;
    }

    section.style.display = 'block';
    container.innerHTML = '';

    biomarkers.forEach(b => {
        const card = document.createElement('div');
        card.className = `biomarker-card status-${b.status}`;

        // Calculate slider gauge percentage
        const gaugePercentage = calculateBiomarkerPosition(b.observed_value, b.reference_interval, b.status);

        card.innerHTML = `
            <div class="biomarker-header">
                <div>
                    <span class="biomarker-category">${b.category}</span>
                    <h4 class="biomarker-name">${b.display_name}</h4>
                </div>
                <span class="biomarker-badge status-${b.status}">${b.status}</span>
            </div>

            <div class="biomarker-reading">
                ${b.observed_value.toLocaleString()} <span class="biomarker-unit">${b.unit}</span>
            </div>

            <!-- Visual Range Gauge Bar -->
            <div class="gauge-container">
                <div class="gauge-bar">
                    <span class="gauge-zone zone-low">Low</span>
                    <span class="gauge-zone zone-normal">Normal</span>
                    <span class="gauge-zone zone-high">High</span>
                </div>
                <div class="gauge-pin" style="left: ${gaugePercentage}%;"></div>
            </div>

            <div class="biomarker-ref">Standard Range: <strong>${b.reference_interval}</strong></div>
            <div class="biomarker-interpretation">${b.interpretation}</div>
        `;
        container.appendChild(card);
    });
}

function calculateBiomarkerPosition(val, refInterval, status) {
    // Relative visual position for slider pin between 8% and 92%
    if (status === 'Normal') return 50;
    if (status === 'Low') return 18;
    if (status === 'High') return 82;
    if (status === 'Critical') return val < 100000 ? 10 : 92;
    return 50;
}

function renderPlanSection(listId, items) {
    const listEl = document.getElementById(listId);
    listEl.innerHTML = '';

    if (!items || items.length === 0) {
        const empty = document.createElement('li');
        empty.className = 'plan-pill';
        empty.textContent = 'None identified in report.';
        listEl.appendChild(empty);
        return;
    }

    items.forEach(item => {
        const li = document.createElement('li');
        li.className = 'plan-pill';
        li.textContent = item;
        listEl.appendChild(li);
    });
}

function shareOnWhatsApp() {
    if (!currentAnalysisData) {
        alert('Please run an analysis first.');
        return;
    }

    const status = currentAnalysisData.status;
    const conditions = (currentAnalysisData.treatment_plan?.conditions || []).join(', ');
    const textToShare = `🏥 *LankaMedi AI — Medical Report Summary*\n\n*Status:* ${status}\n*Conditions Noted:* ${conditions || 'None'}\n\n*Important:* Educational summary for clinical consultation only. Review with a doctor.\nAnalyzed via LankaMedi AI (Sri Lanka)`;

    const whatsappUrl = `https://api.whatsapp.com/send?text=${encodeURIComponent(textToShare)}`;
    window.open(whatsappUrl, '_blank');
}

async function loadReferenceRanges() {
    const grid = document.getElementById('referenceRangesGrid');
    if (!grid) return;

    try {
        const resp = await fetch('/api/v1/reference-ranges');
        const data = await resp.json();
        const ranges = data.reference_ranges || {};

        grid.innerHTML = '';
        Object.entries(ranges).forEach(([key, info]) => {
            const card = document.createElement('div');
            card.className = 'ref-range-card';
            const lowStr = info.low !== null ? info.low : '0';
            const highStr = info.high !== null ? info.high : 'N/A';
            card.innerHTML = `
                <div class="ref-range-badge">${info.category}</div>
                <h4 class="ref-range-name">${info.display_name}</h4>
                <div class="ref-range-interval">${lowStr} – ${highStr} ${info.unit}</div>
                <p class="ref-range-guidance">${info.guidance}</p>
            `;
            grid.appendChild(card);
        });
    } catch (e) {
        console.warn('Could not load reference ranges:', e);
    }
}

function initFaqAccordion() {
    document.querySelectorAll('.faq-item').forEach(item => {
        const question = item.querySelector('.faq-question');
        question.addEventListener('click', () => {
            const isOpen = item.classList.contains('active');
            document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('active'));
            if (!isOpen) {
                item.classList.add('active');
            }
        });
    });
}

function animateValue(elementId, target) {
    const el = document.getElementById(elementId);
    let start = 0;
    const duration = 600;
    const stepTime = 25;
    const steps = duration / stepTime;
    const increment = target / steps;

    if (target === 0) {
        el.textContent = '0';
        return;
    }

    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            el.textContent = target;
            clearInterval(timer);
        } else {
            el.textContent = Math.floor(start);
        }
    }, stepTime);
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast-alert';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.classList.add('visible'), 50);
    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

function initNavbar() {
    const nav = document.getElementById('mainNav');
    const mobileToggle = document.getElementById('mobileToggle');
    const mobileOverlay = document.getElementById('mobileOverlay');
    const mobileClose = document.getElementById('mobileDrawerClose');

    // 1. Scroll effect (scrolled class, inspired by Delta Gemunupura College)
    let navScrollTick = false;
    window.addEventListener('scroll', () => {
        if (!navScrollTick) {
            window.requestAnimationFrame(() => {
                if (window.scrollY > 40) {
                    nav?.classList.add('scrolled');
                } else {
                    nav?.classList.remove('scrolled');
                }
                updateActiveNavLink();
                navScrollTick = false;
            });
            navScrollTick = true;
        }
    }, { passive: true });

    if (window.scrollY > 40) {
        nav?.classList.add('scrolled');
    }

    // 2. Mobile toggle & drawer
    function openMobileMenu() {
        mobileToggle?.classList.add('active');
        mobileOverlay?.classList.add('active');
        if (mobileOverlay) mobileOverlay.hidden = false;
        document.body.style.overflow = 'hidden';
    }

    function closeMobileMenu() {
        mobileToggle?.classList.remove('active');
        mobileOverlay?.classList.remove('active');
        if (mobileOverlay) mobileOverlay.hidden = true;
        document.body.style.overflow = '';
    }

    mobileToggle?.addEventListener('click', () => {
        if (mobileOverlay?.classList.contains('active')) {
            closeMobileMenu();
        } else {
            openMobileMenu();
        }
    });

    mobileClose?.addEventListener('click', closeMobileMenu);

    mobileOverlay?.addEventListener('click', (e) => {
        if (e.target === mobileOverlay) {
            closeMobileMenu();
        }
    });

    // Close mobile drawer on link clicks
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            closeMobileMenu();
        });
    });

    // 3. Scrollspy active link highlighter
    function updateActiveNavLink() {
        const sections = [
            { id: 'workspaceCard', href: '#workspaceCard' },
            { id: 'howItWorks', href: '#howItWorks' },
            { id: 'supportedLabs', href: '#supportedLabs' },
            { id: 'referenceRangesSection', href: '#referenceRangesSection' },
            { id: 'emergencySection', href: '#emergencySection' },
            { id: 'faqSection', href: '#faqSection' }
        ];

        let currentSectionId = '';
        const scrollPosition = window.scrollY + 200;

        for (const sec of sections) {
            const el = document.getElementById(sec.id);
            if (el) {
                const top = el.offsetTop;
                const height = el.offsetHeight;
                if (scrollPosition >= top && scrollPosition < top + height) {
                    currentSectionId = sec.href;
                    break;
                }
            }
        }

        if (currentSectionId) {
            document.querySelectorAll('.nav-menu .nav-item').forEach(item => {
                const link = item.querySelector('.nav-link');
                const href = link?.getAttribute('href');
                if (href === currentSectionId) {
                    item.classList.add('active');
                } else if (!item.classList.contains('has-dropdown') || !item.querySelector(`.nav-dropdown a[href="${currentSectionId}"]`)) {
                    item.classList.remove('active');
                }
            });

            document.querySelectorAll('.mobile-nav-item').forEach(item => {
                const link = item.querySelector('.mobile-nav-link');
                if (link?.getAttribute('href') === currentSectionId) {
                    item.classList.add('active');
                } else {
                    item.classList.remove('active');
                }
            });
        }
    }
}

/* ==========================================================================
   Progressive Web App (PWA) Controller
   ========================================================================== */

/**
 * Registers the Service Worker with root scope
 */
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js', { scope: '/' })
                .then((registration) => {
                    console.log('[PWA] Service Worker registered successfully with scope:', registration.scope);

                    // Check for active worker update
                    registration.addEventListener('updatefound', () => {
                        const newWorker = registration.installing;
                        if (!newWorker) return;

                        newWorker.addEventListener('statechange', () => {
                            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                                console.log('[PWA] New version detected; ready to activate.');
                                showToast('LankaMedi AI update available. Refreshing...', 'info');
                                setTimeout(() => {
                                    newWorker.postMessage({ action: 'skipWaiting' });
                                    window.location.reload();
                                }, 1200);
                            }
                        });
                    });
                })
                .catch((err) => {
                    console.warn('[PWA] Service Worker registration failed:', err);
                });
        });
    }
}

/**
 * Monitors online and offline connectivity and presents reactive banners
 */
function setupNetworkStatusListeners() {
    const offlineBanner = document.getElementById('offlineBanner');

    function handleOnline() {
        if (offlineBanner) offlineBanner.setAttribute('hidden', '');
        showToast('Online mode restored. AI clinical synthesis active.');
    }

    function handleOffline() {
        if (offlineBanner) offlineBanner.removeAttribute('hidden');
        showToast('You are offline. Reference ranges & 1990 contacts remain accessible.');
    }

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Initial check
    if (!navigator.onLine && offlineBanner) {
        offlineBanner.removeAttribute('hidden');
    }
}

/**
 * Handles beforeinstallprompt and triggers native PWA installation dialog
 */
let deferredInstallPrompt = null;

function setupPwaInstall() {
    const pwaInstallBtn = document.getElementById('pwaInstallBtn');
    const mobilePwaBox = document.getElementById('mobilePwaBox');
    const mobilePwaBtn = document.getElementById('mobilePwaBtn');

    // Browser fires beforeinstallprompt when PWA criteria are met
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent default mini-infobar on mobile Chrome
        e.preventDefault();
        deferredInstallPrompt = e;

        // Unhide install buttons in desktop navbar & mobile drawer
        if (pwaInstallBtn) pwaInstallBtn.removeAttribute('hidden');
        if (mobilePwaBox) mobilePwaBox.removeAttribute('hidden');
        console.log('[PWA] Install prompt captured and buttons revealed.');
    });

    async function triggerInstall() {
        if (!deferredInstallPrompt) {
            // If already installed or browser doesn't support beforeinstallprompt
            showToast('To install, tap your browser menu and choose "Add to Home Screen" or "Install App"');
            return;
        }

        deferredInstallPrompt.prompt();
        const choiceResult = await deferredInstallPrompt.userChoice;
        console.log('[PWA] User installation decision:', choiceResult.outcome);

        deferredInstallPrompt = null;
        if (pwaInstallBtn) pwaInstallBtn.setAttribute('hidden', '');
        if (mobilePwaBox) mobilePwaBox.setAttribute('hidden', '');
    }

    if (pwaInstallBtn) {
        pwaInstallBtn.addEventListener('click', triggerInstall);
    }
    if (mobilePwaBtn) {
        mobilePwaBtn.addEventListener('click', triggerInstall);
    }

    window.addEventListener('appinstalled', () => {
        console.log('[PWA] LankaMedi AI was installed successfully!');
        if (pwaInstallBtn) pwaInstallBtn.setAttribute('hidden', '');
        if (mobilePwaBox) mobilePwaBox.setAttribute('hidden', '');
        showToast('LankaMedi AI app installed successfully!');
    });

    // Check if running in standalone display mode (already installed)
    if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
        console.log('[PWA] Running in standalone PWA window');
        if (pwaInstallBtn) pwaInstallBtn.setAttribute('hidden', '');
        if (mobilePwaBox) mobilePwaBox.setAttribute('hidden', '');
    }
}


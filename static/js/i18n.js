/**
 * Trilingual localization dictionary for LankaMedi AI
 * Supports: English (en), Sinhala (si), Tamil (ta)
 */

const I18N_TRANSLATIONS = {
    en: {
        // Navigation
        navAnalyze: "Analyze",
        navGuide: "Clinical Guide",
        navGuideHint: "Learn the workflow before you upload",
        navHow: "How It Works",
        navHowHint: "Privacy-first 4-step analysis flow",
        navLabs: "Supported Labs",
        navLabsHint: "Asiri, Nawaloka, Durdans & more",
        navRanges: "Reference Ranges",
        navRangesHint: "SLMA-aligned biomarker intervals",
        navEmergency: "1990 Emergency",
        navFaq: "FAQ",
        mobileMenuTag: "Menu",
        brandSubtitle: "LankaMedi AI",

        // Hero
        heroEyebrow: "Clinical report analysis in seconds",
        heroLine1: "Understand your",
        heroPill1: "lab results",
        heroLine2: "with",
        heroPill2: "clear AI insights",
        heroLine3: "built for patients and clinics",
        heroSubtitle: "Upload a PDF or photo, or paste report text. Get biomarker readings, risk flags, and doctor-ready discussion points.",
        btnStart: "Analyze My Report",
        btnSample: "Try Sample Report",
        chipOcr: "PDF & photo ready",
        chipLabs: "Biomarker ranges",
        chipLang: "EN · SI · TA",
        chipPrivacy: "NIC masked first",
        statOcrValue: "OCR",
        statLangValue: "3",
        statPrivacyValue: "PII",

        // Workspace
        workspaceTitle: "Analyze Medical Report",
        workspaceHint: "Your sensitive information (NIC, phone numbers, names) is masked automatically before processing.",
        tabFile: "📄 Document / Photo Upload",
        tabText: "📝 Paste Report Text",
        dropzoneTitle: "Drag & drop your lab report here",
        dropzoneSubtitle: "or click to browse from device (PDF, PNG, JPG, JPEG, WEBP)",
        dropzoneFormats: "Supports all Sri Lankan lab formats: Asiri, Nawaloka, Durdans, Hemas, General Hospital",
        samplePresetLabel: "Quick Sample Scenarios:",
        presetDengue: "🩸 Dengue Warning (Low Platelets)",
        presetDiabetes: "🍬 Diabetes & Cholesterol",
        presetKidney: "🫘 Kidney Screening",
        presetNormal: "🩺 Normal Routine Checkup",
        textareaLabel: "Enter or paste lab test results / clinical notes:",
        textareaPlaceholder: "Paste Fasting Blood Sugar (FBS), Platelet count (FBC), Serum Creatinine, Lipid profile, or doctor notes...",
        btnAuditPrivacy: "🛡️ Audit Privacy (Mask NIC & Phone)",
        btnAnalyze: "Analyze Report",
        btnAnalyzing: "Analyzing Report...",

        // Emergency
        emergencyTitle: "CRITICAL MEDICAL ALERT: IMMEDIATE ACTION REQUIRED",
        emergencyCallBtn: "Call 1990 Suwa Seriya Ambulance",

        // Results
        resultsTitle: "Clinical Analysis Summary",
        statusGood: "Good (Normal Findings)",
        statusNeedsAttention: "Needs Clinical Attention",
        statusCritical: "Critical Alert",
        btnExport: "🖨️ Print / Save PDF",
        btnShareWhatsApp: "📱 Share on WhatsApp",
        btnReset: "🔄 Analyze Another Report",
        metricCritical: "Critical Issues",
        metricWarning: "Warning Signs",
        metricPositive: "Positive Indicators",
        sectionBiomarkers: "🔬 Evaluated Biomarkers & Standard Reference Intervals",
        sectionConditions: "🩺 Observed Conditions & Differential Findings",
        sectionMedications: "💊 Medication Topics for Doctor Discussion",
        sectionLifestyle: "🥗 Sri Lankan Dietary & Lifestyle Guidance",
        sectionNotes: "📝 Clinical Notes & Monitoring Protocols",

        // How it works
        howTitle: "How LankaMedi AI Works",
        howSubtitle: "A 4-step clinical pipeline built for patient safety, privacy, and clinical accuracy.",
        howStep1Title: "1. Multi-Format Upload",
        howStep1Desc: "Upload photographed lab slips, scanned PDFs, or paste medical text directly. Automatic image enhancement ensures high OCR legibility.",
        howStep2Title: "2. PII / NIC Redaction",
        howStep2Desc: "Before sending data anywhere, Sri Lankan National Identity Card (NIC) numbers, telephone numbers, emails, and patient names are stripped.",
        howStep3Title: "3. Biomarker Range Match",
        howStep3Desc: "Values (Platelets, FBS, HbA1c, Creatinine, Cholesterol) are evaluated against established Sri Lanka Medical Association (SLMA) intervals.",
        howStep4Title: "4. Trilingual AI Synthesis",
        howStep4Desc: "Advanced AI models (NVIDIA NIM & Google Gemini) synthesize personalized summaries in English, Sinhala, or Tamil with 1990 triage.",

        // Supported Labs
        labsTitle: "Supported Diagnostic Formats",
        labsSubtitle: "Pre-calibrated to recognize laboratory reports from leading private diagnostic chains and government healthcare facilities in Sri Lanka.",

        // Range Explorer
        rangesTitle: "Interactive Lab Reference Range Explorer",
        rangesSubtitle: "Learn what common blood and diagnostic test values mean in Sri Lanka.",

        // Helplines
        emergencySectionTitle: "Sri Lanka Emergency & Health Helplines",
        emergencySectionSubtitle: "Keep these official Sri Lankan toll-free emergency and health information hotlines handy.",

        // FAQ
        faqTitle: "Frequently Asked Questions",
        faqSubtitle: "Everything you need to know about safety, privacy, and report analysis.",

        // Disclaimer
        disclaimerTitle: "Medical AI Notice & Compliance:",
        disclaimerBody: "LankaMedi AI provides educational summaries only and does NOT replace licensed physician judgment or diagnosis. Always consult a qualified clinician.",

        // PWA Keys
        pwaOfflineAlert: "📡 Offline Mode: Internet disconnected. Saved lab reference ranges and 1990 emergency contacts remain active.",
        pwaInstall: "Install App",
        pwaInstallMobile: "Install LankaMedi AI App",
    },

    si: {
        // Navigation
        navAnalyze: "විශ්ලේෂණය",
        navGuide: "සායනික මාර්ගෝපදේශය",
        navGuideHint: "උඩුගත කිරීමට පෙර ක්‍රියාපටිපාටිය දැනගන්න",
        navHow: "ක්‍රියාකාරිත්වය",
        navHowHint: "පෞද්ගලිකත්වයට ප්‍රමුඛත්වය දෙන පියවර 4ක්",
        navLabs: "රසායනාගාර",
        navLabsHint: "ආසිරි, නවලෝක, ඩර්ඩන්ස් සහ තවත්",
        navRanges: "දර්ශක සීමාවන්",
        navRangesHint: "SLMA දර්ශක පරාස",
        navEmergency: "1990 හදිසි ඇමතුම්",
        navFaq: "ප්‍රශ්න සහ පිළිතුරු",
        mobileMenuTag: "මෙනුව",
        brandSubtitle: "LankaMedi AI",

        // Hero
        heroEyebrow: "තත්පර කිහිපයකින් වාර්තා විශ්ලේෂණය",
        heroLine1: "ඔබේ",
        heroPill1: "ලැබ් ප්‍රතිඵල",
        heroLine2: "තේරුම් ගන්න",
        heroPill2: "පැහැදිලි AI තීක්ෂණ",
        heroLine3: "රෝගීන්ට සහ සායන සඳහා",
        heroSubtitle: "PDF හෝ ඡායාරූපයක් උඩුගත කරන්න, නැතහොත් පෙළ paste කරන්න. දර්ශක, අවදානම් සහ වෛද්‍ය සාකච්ඡා කරුණු ලබා ගන්න.",
        btnStart: "මගේ වාර්තාව විශ්ලේෂණය කරන්න",
        btnSample: "ආදර්ශ වාර්තාවක් බලන්න",
        chipOcr: "PDF සහ ඡායාරූප",
        chipLabs: "දර්ශක පරාස",
        chipLang: "EN · SI · TA",
        chipPrivacy: "ජා.හැ.අ. සඟවයි",
        statOcrValue: "OCR",
        statLangValue: "3",
        statPrivacyValue: "PII",

        // Workspace
        workspaceTitle: "වෛද්‍ය වාර්තාව විශ්ලේෂණය කරන්න",
        workspaceHint: "ඔබගේ සංවේදී තොරතුරු (ජා.හැ.අංකය, දුරකථන අංක, නම) පද්ධතිය මගින් ස්වයංක්‍රීයව සඟවනු ලැබේ.",
        tabFile: "📄 ලේඛන / ඡායාරූප උඩුගත කරන්න",
        tabText: "📝 වාර්තා පෙළ ඇතුළත් කරන්න",
        dropzoneTitle: "ඔබගේ රසායනාගාර වාර්තාව මෙතැනට Drag & drop කරන්න",
        dropzoneSubtitle: "හෝ උපාංගයෙන් තෝරා ගැනීමට click කරන්න (PDF, PNG, JPG, JPEG, WEBP)",
        dropzoneFormats: "සියලුම ශ්‍රී ලාංකික රසායනාගාර වාර්තා: ආසිරි, නවලෝක, ඩර්ඩන්ස්, හේමාස්, රජයේ රෝහල්",
        samplePresetLabel: "ක්ෂණික ආදර්ශ වාර්තා:",
        presetDengue: "🩸 ඩෙංගු අවදානම (අඩු පට්ටිකා)",
        presetDiabetes: "🍬 දියවැඩියාව සහ කොලෙස්ටරෝල්",
        presetKidney: "🫘 වකුගඩු පරීක්ෂාව",
        presetNormal: "🩺 සාමාන්‍ය වාර්ෂික පරීක්ෂාව",
        textareaLabel: "පරීක්ෂණ වාර්තාවේ අන්තර්ගතය මෙහි ඇතුළත් කරන්න:",
        textareaPlaceholder: "නිරාහාර රුධිර සීනි (FBS), සම්පූර්ණ රුධිර පරීක්ෂාව (FBC පට්ටිකා), සෙරම් ක්‍රියැටිනින්, කොලෙස්ටරෝල් මෙහි paste කරන්න...",
        btnAuditPrivacy: "🛡️ පුද්ගලිකත්වය පරීක්ෂා කරන්න (ජා.හැ.අංක සඟවන්න)",
        btnAnalyze: "වාර්තාව විශ්ලේෂණය කරන්න",
        btnAnalyzing: "විශ්ලේෂණය වෙමින් පවතී...",

        // Emergency
        emergencyTitle: "අතිශය හදිසි වෛද්‍ය අනතුරු ඇඟවීමයි",
        emergencyCallBtn: "1990 සුවසැරිය ගිලන්රථය අමතන්න",

        // Results
        resultsTitle: "සායනික විශ්ලේෂණ සාරාංශය",
        statusGood: "යහපත් (සාමාන්‍ය මට්ටම)",
        statusNeedsAttention: "වෛද්‍ය අවධානය අවශ්‍යයි",
        statusCritical: "අත්‍යවශ්‍ය හදිසි අවස්ථාවක්",
        btnExport: "🖨️ මුද්‍රණය / PDF සුරකින්න",
        btnShareWhatsApp: "📱 WhatsApp මගින් යවන්න",
        btnReset: "🔄 වෙනත් වාර්තාවක් පරීක්ෂා කරන්න",
        metricCritical: "අවදානම් ගැටළු",
        metricWarning: "අවවාදාත්මක සලකුණු",
        metricPositive: "යහපත් දර්ශක",
        sectionBiomarkers: "🔬 පරීක්ෂා කරන ලද රසායනාගාර දර්ශක සහ සාමාන්‍ය සීමාවන්",
        sectionConditions: "🩺 නිරීක්ෂණය වූ සෞඛ්‍ය තත්ත්වයන්",
        sectionMedications: "💊 වෛද්‍යවරයා සමඟ සාකච්ඡා කළ යුතු ඖෂධ කරුණු",
        sectionLifestyle: "🥗 ශ්‍රී ලාංකික ආහාර සහ ජීවන රටා උපදෙස්",
        sectionNotes: "📝 සායනික සටහන් සහ පසු විපරම් උපදෙස්",

        // How it works
        howTitle: "LankaMedi AI ක්‍රියාත්මක වන ආකාරය",
        howSubtitle: "රෝගී ආරක්ෂාව, පුද්ගලිකත්වය සහ වෛද්‍ය නිරවද්‍යතාවය මුල් කරගත් 4-පියවර සායනික ක්‍රමවේදය.",
        howStep1Title: "1. වාර්තාව ලබාදීම",
        howStep1Desc: "ඡායාරූප ගත් වාර්තා, ස්කෑන් කළ PDF හෝ සටහන් ඇතුළත් කරන්න. දියුණු OCR මගින් අකුරු පහසුවෙන් කියවයි.",
        howStep2Title: "2. ජාතික හැඳුනුම්පත් අංක සැඟවීම",
        howStep2Desc: "කිසිදු දත්තයක් බාහිරට යැවීමට පෙර ශ්‍රී ලාංකික ජා.හැ. අංක, දුරකථන අංක සහ නම් ඉවත් කර ආරක්ෂා කරයි.",
        howStep3Title: "3. දර්ශක සංසන්දනය",
        howStep3Desc: "පට්ටිකා, රුධිර සීනි, ක්‍රියැටිනින්, කොලෙස්ටරෝල් ශ්‍රී ලංකා වෛද්‍ය සංගමයේ (SLMA) සම්මත සීමාවන් සමඟ සංසන්දනය කෙරේ.",
        howStep4Title: "4. ත්‍රිභාෂා AI සාරාංශය",
        howStep4Desc: "NVIDIA සහ Google Gemini තාක්ෂණයෙන් සිංහල, දෙමළ හෝ ඉංග්‍රීසි බසින් සරල පැහැදිලි කිරීමක් සහ 1990 හදිසි මඟපෙන්වීමක් ලබාදෙයි.",

        // Supported Labs
        labsTitle: "සහාය දක්වන රසායනාගාර ආකෘති",
        labsSubtitle: "ශ්‍රී ලංකාවේ ප්‍රමුඛ පෙළේ පෞද්ගලික රසායනාගාර ජාල සහ රජයේ රෝහල් වාර්තා පහසුවෙන් හඳුනාගනී.",

        // Range Explorer
        rangesTitle: "රසායනාගාර දර්ශක සීමාවන් ගවේෂකය",
        rangesSubtitle: "ශ්‍රී ලංකාවේ සම්මත රුධිර සහ වෛද්‍ය පරීක්ෂණ අගයන්හි තේරුම වටහා ගන්න.",

        // Helplines
        emergencySectionTitle: "ශ්‍රී ලංකාවේ හදිසි සහ සෞඛ්‍ය උපකාරක අංක",
        emergencySectionSubtitle: "අවශ්‍ය ඕනෑම මොහොතක පහත නිල හදිසි ඇමතුම් සේවාවන් සම්බන්ධ කරගන්න.",

        // FAQ
        faqTitle: "නිතර අසන ප්‍රශ්න",
        faqSubtitle: "ආරක්ෂාව, පුද්ගලිකත්වය සහ වාර්තා විශ්ලේෂණය පිළිබඳ සියලු විස්තර.",

        // Disclaimer
        disclaimerTitle: "වෛද්‍යමය නිවේදනය:",
        disclaimerBody: "මෙම තොරතුරු අධ්‍යාපනික සහ මඟපෙන්වීම් සඳහා පමණි. නිසි රෝග විනිශ්චය සඳහා ලියාපදිංචි වෛද්‍යවරයකු හමුවන්න.",

        // PWA Keys
        pwaOfflineAlert: "📡 නොබැඳි මාදිලිය: අන්තර්ජාල සම්බන්ධතාවය බිඳවැටී ඇත. සුරකින ලද දර්ශක සීමාවන් සහ 1990 හදිසි ඇමතුම් සක්‍රීයව පවතී.",
        pwaInstall: "ඇප් එක ස්ථාපනය කරන්න",
        pwaInstallMobile: "LankaMedi AI ඇප් එක ස්ථාපනය කරන්න",
    },

    ta: {
        // Navigation
        navAnalyze: "பகுப்பாய்வு",
        navGuide: "மருத்துவ வழிகாட்டி",
        navGuideHint: "பதிவேற்றத்திற்கு முன் செயல்முறையை அறியுங்கள்",
        navHow: "செயல்படும் முறை",
        navHowHint: "தனியுரிமை முன்னுரிமை 4 படிகள்",
        navLabs: "ஆய்வகங்கள்",
        navLabsHint: "ஆசிரி, நவலொக, டர்டன்ஸ் மற்றும் மேலும்",
        navRanges: "குறிகாட்டிகள்",
        navRangesHint: "SLMA குறிகாட்டி வரம்புகள்",
        navEmergency: "1990 அவசரம்",
        navFaq: "அடிக்கடி கேட்கப்படும் கேள்விகள்",
        mobileMenuTag: "மெனு",
        brandSubtitle: "LankaMedi AI",

        // Hero
        heroEyebrow: "விநாடிகளில் மருத்துவ அறிக்கை பகுப்பாய்வு",
        heroLine1: "உங்கள்",
        heroPill1: "ஆய்வக முடிவுகளை",
        heroLine2: "புரிந்துகொள்ளுங்கள்",
        heroPill2: "தெளிவான AI நுண்ணறிவுடன்",
        heroLine3: "நோயாளிகள் மற்றும் மருத்துவமனைகளுக்காக",
        heroSubtitle: "PDF அல்லது புகைப்படத்தைப் பதிவேற்றவும், அல்லது உரையை ஒட்டவும். குறிகாட்டிகள், அபாயங்கள் மற்றும் மருத்துவர் விவாதப் புள்ளிகளைப் பெறுங்கள்.",
        btnStart: "எனது அறிக்கையை பகுப்பாய்வு செய்",
        btnSample: "மாதிரி அறிக்கையைப் பார்க்கவும்",
        chipOcr: "PDF & புகைப்படம்",
        chipLabs: "குறிகாட்டி வரம்புகள்",
        chipLang: "EN · SI · TA",
        chipPrivacy: "அடையாள எண் மறைப்பு",
        statOcrValue: "OCR",
        statLangValue: "3",
        statPrivacyValue: "PII",

        // Workspace
        workspaceTitle: "மருத்துவ அறிக்கையை பகுப்பாய்வு செய்யுங்கள்",
        workspaceHint: "உங்கள் தேசிய அடையாள அட்டை எண், தொலைபேசி எண்கள் தானாகவே மறைக்கப்படும்.",
        tabFile: "📄 ஆவணம் / புகைப்படம்",
        tabText: "📝 உரையை ஒட்டவும்",
        dropzoneTitle: "உங்கள் மருத்துவ அறிக்கையை இங்கே இழுத்து விடவும்",
        dropzoneSubtitle: "அல்லது சாதனத்திலிருந்து தேர்ந்தெடுக்கவும் (PDF, PNG, JPG, JPEG, WEBP)",
        dropzoneFormats: "அனைத்து இலங்கை ஆய்வக அறிக்கைகள்: ஆசிரி, நவலொக, டர்டன்ஸ், ஹேமாஸ், அரசு மருத்துவமனை",
        samplePresetLabel: "மாதிரி அறிக்கைகள்:",
        presetDengue: "🩸 டெங்கு எச்சரிக்கை (குறைந்த தட்டணுக்கள்)",
        presetDiabetes: "🍬 நீரிழிவு & கொலஸ்ட்ரால்",
        presetKidney: "🫘 சிறுநீரக பரிசோதனை",
        presetNormal: "🩺 வழக்கமான மருத்துவ பரிசோதனை",
        textareaLabel: "மருத்துவ அறிக்கை உரையை உள்ளிடவும்:",
        textareaPlaceholder: "இரத்த சர்க்கரை (FBS), இரத்த தட்டணுக்கள் (Platelets), சீரம் கிரியேட்டினின், கொலஸ்ட்ரால் போன்றவற்றை ஒட்டவும்...",
        btnAuditPrivacy: "🛡️ தனியுரிமை தணிக்கை (NIC மறை)",
        btnAnalyze: "அறிக்கையை பகுப்பாய்வு செய்",
        btnAnalyzing: "பகுப்பாய்வு செய்யப்படுகிறது...",

        // Emergency
        emergencyTitle: "அவசர மருத்துவ எச்சரிக்கை - உடனடி நடவடிக்கை தேவை",
        emergencyCallBtn: "1990 சுவசரிய ஆம்புலன்ஸை அழைக்கவும்",

        // Results
        resultsTitle: "மருத்துவ பகுப்பாய்வு சுருக்கம்",
        statusGood: "நன்று (சாதாரண நிலை)",
        statusNeedsAttention: "மருத்துவ கவனிப்பு தேவை",
        statusCritical: "அவசர எச்சரிக்கை",
        btnExport: "🖨️ அச்சிட / PDF சேமிக்க",
        btnShareWhatsApp: "📱 WhatsApp இல் பகிரவும்",
        btnReset: "🔄 புதிய பகுப்பாய்வு",
        metricCritical: "சிக்கலான பிரச்சினைகள்",
        metricWarning: "எச்சரிக்கை அறிகுறிகள்",
        metricPositive: "நேர்மறை குறிகாட்டிகள்",
        sectionBiomarkers: "🔬 மதிப்பிடப்பட்ட ஆய்வக குறிகாட்டிகள் மற்றும் சாதாரண வரம்புகள்",
        sectionConditions: "🩺 கண்டறியப்பட்ட நிலைமைகள்",
        sectionMedications: "💊 மருத்துவரிடம் ஆலோசிக்க வேண்டிய மருந்துகள்",
        sectionLifestyle: "🥗 இலங்கை உணவு மற்றும் வாழ்க்கை முறை ஆலோசனைகள்",
        sectionNotes: "📝 மருத்துவ குறிப்புகள் மற்றும் கண்காணிப்பு",

        // How it works
        howTitle: "LankaMedi AI எவ்வாறு செயல்படுகிறது",
        howSubtitle: "பாதுகாப்பு, தனியுரிமை மற்றும் மருத்துவ துல்லியத்தை மையமாகக் கொண்ட 4-படி முறை.",
        howStep1Title: "1. பதிவேற்றம்",
        howStep1Desc: "புகைப்படங்கள், PDF அல்லது அறிக்கையை உள்ளிடுங்கள். மேம்பட்ட OCR தெளிவான வாசிப்பை உறுதி செய்கிறது.",
        howStep2Title: "2. தனிநபர் தகவல் பாதுகாப்பு",
        howStep2Desc: "இலங்கை தேசிய அடையாள அட்டை (NIC), தொலைபேசி எண்கள் அகற்றப்பட்டு மறைக்கப்படுகின்றன.",
        howStep3Title: "3. குறிகாட்டிகள் ஒப்பீடு",
        howStep3Desc: "இரத்த தட்டணுக்கள், சர்க்கரை, கொலஸ்ட்ரால் ஆகியவை இலங்கை மருத்துவ சங்கத்தின் (SLMA) வரம்புகளுடன் ஒப்பிடப்படுகின்றன.",
        howStep4Title: "4. முமொழி AI சுருக்கம்",
        howStep4Desc: "NVIDIA மற்றும் Google Gemini மூலம் தமிழ், சிங்களம் அல்லது ஆங்கிலத்தில் தெளிவான விளக்கம் மற்றும் 1990 வழிகாட்டுதல்.",

        // Supported Labs
        labsTitle: "ஆதரிக்கப்படும் ஆய்வக வடிவங்கள்",
        labsSubtitle: "இலங்கையின் முன்னணி தனியார் ஆய்வகங்கள் மற்றும் அரசு மருத்துவமனை அறிக்கைகளை எளிதில் அடையாளம் காணும்.",

        // Range Explorer
        rangesTitle: "ஆய்வக குறிகாட்டிகள் வழிகாட்டி",
        rangesSubtitle: "இலங்கையின் வழக்கமான இரத்த மற்றும் நோயறிதல் பரிசோதனை வரம்புகளைப் புரிந்து கொள்ளுங்கள்.",

        // Helplines
        emergencySectionTitle: "இலங்கை அவசர மற்றும் சுகாதார உதவி எண்கள்",
        emergencySectionSubtitle: "அவசர காலத்தில் தொடர்பு கொள்ள வேண்டிய இலவச உதவி எண்கள்.",

        // FAQ
        faqTitle: "அடிக்கடி கேட்கப்படும் கேள்விகள்",
        faqSubtitle: "பாதுகாப்பு மற்றும் அறிக்கைப் பகுப்பாய்வு பற்றிய தகவல்கள்.",

        // Disclaimer
        disclaimerTitle: "மருத்துவ அறிவிப்பு:",
        disclaimerBody: "இது கல்வி நோக்கங்களுக்கானது மட்டுமே. முறையான சிகிச்சைக்கு பதிவுசெய்யப்பட்ட மருத்துவரை அணுகவும்.",

        // PWA Keys
        pwaOfflineAlert: "📡 ஆஃப்லைன் முறை: இணைய இணைப்பு துண்டிக்கப்பட்டுள்ளது. ஆய்வக வரம்புகள் மற்றும் 1990 அவசர எண்கள் தொடர்ந்து செயல்படுகின்றன.",
        pwaInstall: "செயலியை நிறுவவும்",
        pwaInstallMobile: "LankaMedi AI செயலியை நிறுவவும்",
    }
};

window.I18N_TRANSLATIONS = I18N_TRANSLATIONS;

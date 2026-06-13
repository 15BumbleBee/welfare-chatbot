SCHEMES = [
    {
        "id": "pm_kisan",
        "name": "PM-KISAN",
        "name_hi": "पीएम किसान",
        "name_ta": "பிஎம் கிசான்",
        "description": "Direct income support of ₹6,000/year to small and marginal farmers in 3 installments.",
        "eligibility": {
            "occupation": ["farmer"],
            "land_ownership": True,
            "land_max_hectares": 2.0,
            "income_max": None,
            "excluded": ["government employees", "taxpayers earning >1.5L"]
        },
        "documents": ["Aadhaar card", "Land ownership records (Khatoni/Jamabandi)", "Bank account passbook", "Mobile number linked to Aadhaar"],
        "documents_hi": ["आधार कार्ड", "भूमि स्वामित्व रिकॉर्ड (खतौनी)", "बैंक पासबुक", "आधार से जुड़ा मोबाइल नंबर"],
        "documents_ta": ["ஆதார் அட்டை", "நில உரிமை ஆவணங்கள்", "வங்கி பாஸ்புக்", "ஆதாருடன் இணைக்கப்பட்ட மொபைல் எண்"],
        "apply_url": "https://pmkisan.gov.in",
        "apply_steps": "1. Visit pmkisan.gov.in\n2. Click 'Farmer Corner' → 'New Farmer Registration'\n3. Enter Aadhaar number\n4. Fill in land and bank details\n5. Submit and note registration number",
        "tags": ["farmer", "income", "agriculture"]
    },
    {
        "id": "ayushman_bharat",
        "name": "Ayushman Bharat PM-JAY",
        "name_hi": "आयुष्मान भारत पीएम-जेएवाई",
        "name_ta": "ஆயுஷ்மான் பாரத்",
        "description": "Health insurance cover of ₹5 lakh/year per family for secondary and tertiary hospitalization.",
        "eligibility": {
            "occupation": ["any"],
            "secc_listed": True,
            "income_max": 300000,
            "excluded": ["families with government job", "families owning 4-wheeler"]
        },
        "documents": ["Aadhaar card", "Ration card", "SECC family ID (if available)", "Income certificate"],
        "documents_hi": ["आधार कार्ड", "राशन कार्ड", "SECC पारिवारिक आईडी", "आय प्रमाण पत्र"],
        "documents_ta": ["ஆதார் அட்டை", "ரேஷன் கார்டு", "SECC குடும்ப அடையாளம்", "வருமான சான்றிதழ்"],
        "apply_url": "https://pmjay.gov.in",
        "apply_steps": "1. Call 14555 or visit nearest empanelled hospital\n2. Show Aadhaar + ration card\n3. Hospital verifies eligibility on portal\n4. Get Ayushman card issued",
        "tags": ["health", "insurance", "family"]
    },
    {
        "id": "pmay_gramin",
        "name": "PMAY-Gramin",
        "name_hi": "प्रधानमंत्री आवास योजना ग्रामीण",
        "name_ta": "பிரதம மந்திரி ஆவாஸ் யோஜனா கிராமீண",
        "description": "Financial assistance of ₹1.2–1.4 lakh to houseless or kutcha house owners in rural areas.",
        "eligibility": {
            "occupation": ["any"],
            "residence": "rural",
            "house_type": ["houseless", "kutcha"],
            "secc_listed": True,
            "excluded": ["pucca house owners", "urban residents"]
        },
        "documents": ["Aadhaar card", "BPL/SECC certificate", "Bank account details", "Photo of current house/land", "Job card (MGNREGA) if available"],
        "documents_hi": ["आधार कार्ड", "बीपीएल/SECC प्रमाण पत्र", "बैंक खाता विवरण", "वर्तमान घर/जमीन की फोटो"],
        "documents_ta": ["ஆதார் அட்டை", "BPL/SECC சான்றிதழ்", "வங்கி கணக்கு விவரங்கள்", "தற்போதைய வீட்டின் புகைப்படம்"],
        "apply_url": "https://pmayg.nic.in",
        "apply_steps": "1. Contact your Gram Panchayat office\n2. Verify name in SECC/Awaas+ list\n3. Gram Sabha approval\n4. Online registration by Panchayat official\n5. Construction in 3 installments via DBT",
        "tags": ["housing", "rural", "construction"]
    },
    {
        "id": "ujjwala",
        "name": "PM Ujjwala Yojana",
        "name_hi": "प्रधानमंत्री उज्ज्वला योजना",
        "name_ta": "பிரதம மந்திரி உஜ்வலா யோஜனா",
        "description": "Free LPG connection to women from BPL/SECC households. First cylinder and stove subsidized.",
        "eligibility": {
            "gender": "female",
            "age_min": 18,
            "occupation": ["any"],
            "income": "BPL",
            "excluded": ["existing LPG connection holder in household"]
        },
        "documents": ["Aadhaar card", "BPL ration card", "Bank account passbook", "Passport-size photo", "Self-declaration of no existing LPG connection"],
        "documents_hi": ["आधार कार्ड", "बीपीएल राशन कार्ड", "बैंक पासबुक", "पासपोर्ट साइज फोटो"],
        "documents_ta": ["ஆதார் அட்டை", "BPL ரேஷன் கார்டு", "வங்கி பாஸ்புக்", "கடவுச்சீட்டு அளவு புகைப்படம்"],
        "apply_url": "https://pmuy.gov.in",
        "apply_steps": "1. Visit nearest LPG distributor (HP/Bharat/Indane Gas)\n2. Submit KYC form (Form 1 and 2)\n3. Attach Aadhaar + BPL card\n4. Connection issued within 7-10 days",
        "tags": ["women", "cooking", "energy", "BPL"]
    },
    {
        "id": "nrega",
        "name": "MGNREGA",
        "name_hi": "मनरेगा",
        "name_ta": "மகாத்மா காந்தி தேசிய ஊரக வேலை உத்தரவாதத் திட்டம்",
        "description": "Guarantees 100 days of wage employment per year to every rural household. Wage: ₹200-350/day.",
        "eligibility": {
            "occupation": ["any"],
            "residence": "rural",
            "age_min": 18,
            "excluded": ["urban residents"]
        },
        "documents": ["Aadhaar card", "Bank/Post Office account", "Ration card or proof of residence"],
        "documents_hi": ["आधार कार्ड", "बैंक/डाकघर खाता", "राशन कार्ड या निवास प्रमाण"],
        "documents_ta": ["ஆதார் அட்டை", "வங்கி/தபால் நிலைய கணக்கு", "ரேஷன் கார்டு"],
        "apply_url": "https://nrega.nic.in",
        "apply_steps": "1. Visit Gram Panchayat and fill registration form\n2. Get Job Card issued (free, within 15 days)\n3. Request work at Panchayat\n4. Work allocated within 15 days or get unemployment allowance",
        "tags": ["employment", "rural", "wages", "work"]
    },
    {
        "id": "sukanya_samriddhi",
        "name": "Sukanya Samriddhi Yojana",
        "name_hi": "सुकन्या समृद्धि योजना",
        "name_ta": "சுகன்யா சம்ரித்தி யோஜனா",
        "description": "Small savings scheme for girl children. 8.2% interest rate, tax-free maturity at 21 years.",
        "eligibility": {
            "gender": "female",
            "age_max": 10,  # girl child age
            "excluded": ["girl child above 10 years", "NRI families"]
        },
        "documents": ["Girl child's birth certificate", "Parent/guardian Aadhaar", "Parent/guardian photo ID", "Address proof"],
        "documents_hi": ["बालिका का जन्म प्रमाण पत्र", "माता-पिता/अभिभावक का आधार", "पते का प्रमाण"],
        "documents_ta": ["பெண் குழந்தையின் பிறப்பு சான்றிதழ்", "பெற்றோர் ஆதார்", "முகவரி சான்று"],
        "apply_url": "https://www.indiapost.gov.in",
        "apply_steps": "1. Visit any post office or authorized bank\n2. Fill SSY account opening form\n3. Submit documents + initial deposit (min ₹250)\n4. Get passbook",
        "tags": ["girl child", "savings", "education", "women"]
    },
    {
        "id": "pm_vishwakarma",
        "name": "PM Vishwakarma Yojana",
        "name_hi": "पीएम विश्वकर्मा योजना",
        "name_ta": "பிரதம மந்திரி விஸ்வகர்மா யோஜனா",
        "description": "Support for traditional artisans and craftspeople. Includes ₹15,000 toolkit grant, skill training, and collateral-free loans up to ₹3 lakh at 5% interest.",
        "eligibility": {
            "occupation": ["carpenter", "blacksmith", "potter", "weaver", "goldsmith", "cobbler", "tailor", "barber", "mason", "washerman", "artisan"],
            "age_min": 18,
            "excluded": ["salaried employees", "income taxpayers"]
        },
        "documents": ["Aadhaar card", "Bank account", "Mobile number", "Proof of traditional occupation (self-declaration)"],
        "documents_hi": ["आधार कार्ड", "बैंक खाता", "मोबाइल नंबर", "पारंपरिक व्यवसाय का प्रमाण"],
        "documents_ta": ["ஆதார் அட்டை", "வங்கி கணக்கு", "மொபைல் எண்", "பாரம்பரிய தொழில் சான்று"],
        "apply_url": "https://pmvishwakarma.gov.in",
        "apply_steps": "1. Visit CSC (Common Service Center) near you\n2. Register on pmvishwakarma.gov.in with Aadhaar\n3. Verify via Gram Panchayat/ULB\n4. Complete skill training\n5. Apply for toolkit grant and loan",
        "tags": ["artisan", "craftsman", "skill", "loan", "self-employed"]
    },
    {
        "id": "e_shram",
        "name": "e-Shram Card",
        "name_hi": "ई-श्रम कार्ड",
        "name_ta": "இ-ஷ்ரம் அட்டை",
        "description": "National database registration for unorganized workers. Provides ₹2 lakh accident insurance and priority access to welfare schemes.",
        "eligibility": {
            "occupation": ["gig worker", "daily wage", "construction worker", "domestic worker", "street vendor", "agricultural labor"],
            "age_min": 16,
            "age_max": 59,
            "excluded": ["EPFO/ESIC members", "income taxpayers"]
        },
        "documents": ["Aadhaar card", "Mobile number linked to Aadhaar", "Bank account"],
        "documents_hi": ["आधार कार्ड", "आधार से जुड़ा मोबाइल नंबर", "बैंक खाता"],
        "documents_ta": ["ஆதார் அட்டை", "ஆதாருடன் இணைக்கப்பட்ட மொபைல் எண்", "வங்கி கணக்கு"],
        "apply_url": "https://eshram.gov.in",
        "apply_steps": "1. Visit eshram.gov.in or nearest CSC\n2. Enter Aadhaar and OTP\n3. Fill occupation and bank details\n4. Download e-Shram card",
        "tags": ["gig worker", "unorganized", "insurance", "registration"]
    },
    {
        "id": "pm_svamitva",
        "name": "PM SVAMITVA",
        "name_hi": "पीएम स्वामित्व",
        "name_ta": "பிரதம மந்திரி ஸ்வாமித்வா",
        "description": "Provides property rights/title deeds (Property Cards) to rural household owners, enabling them to use property as financial asset.",
        "eligibility": {
            "occupation": ["any"],
            "residence": "rural",
            "property": "abadi land (village inhabited area)",
            "excluded": ["urban residents", "forest land occupants"]
        },
        "documents": ["Aadhaar card", "Existing house proof", "Mobile number"],
        "documents_hi": ["आधार कार्ड", "मौजूदा घर का प्रमाण", "मोबाइल नंबर"],
        "documents_ta": ["ஆதார் அட்டை", "இப்போதுள்ள வீட்டின் சான்று", "மொபைல் எண்"],
        "apply_url": "https://svamitva.nic.in",
        "apply_steps": "1. Drone survey conducted by Survey of India in your village\n2. Property boundaries verified by local Panchayat\n3. Property Card distributed via state revenue department\n4. Download digital card from svamitva.nic.in",
        "tags": ["property", "rural", "land rights", "title deed"]
    }
]
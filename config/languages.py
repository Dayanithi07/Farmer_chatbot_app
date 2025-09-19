"""Language configuration for the farming assistant."""

SUPPORTED_LANGUAGES = {
    'en': {
        'name': 'English',
        'code': 'en',
        'tts_code': 'en',
        'flag': '🇺🇸'
    },
    'hi': {
        'name': 'हिंदी (Hindi)',
        'code': 'hi',
        'tts_code': 'hi',
        'flag': '🇮🇳'
    },
    'ta': {
        'name': 'தமிழ் (Tamil)',
        'code': 'ta',
        'tts_code': 'ta',
        'flag': '🇮🇳'
    },
    'te': {
        'name': 'తెలుగు (Telugu)',
        'code': 'te',
        'tts_code': 'te',
        'flag': '🇮🇳'
    },
    'kn': {
        'name': 'ಕನ್ನಡ (Kannada)',
        'code': 'kn',
        'tts_code': 'kn',
        'flag': '🇮🇳'
    },
    'ml': {
        'name': 'മലയാളം (Malayalam)',
        'code': 'ml',
        'tts_code': 'ml',
        'flag': '🇮🇳'
    },
    'bn': {
        'name': 'বাংলা (Bengali)',
        'code': 'bn',
        'tts_code': 'bn',
        'flag': '🇧🇩'
    }
}

# UI Text translations
UI_TRANSLATIONS = {
    'en': {
        'app_title': '🌾 AI Farming Assistant',
        'welcome': 'Welcome to your AI Farming Assistant',
        'select_language': 'Select your preferred language:',
        'location_prompt': 'Please share your location for weather and soil data',
        'speak_request': '🎤 Speak your farming question',
        'upload_image': '📸 Upload crop image for disease detection',
        'weather_title': '🌦️ Weather Information',
        'soil_title': '🌱 Soil Analysis',
        'disease_title': '🔍 Disease Detection',
        'advisory_title': '🧑‍🌾 Farming Advisory',
        'processing': 'Processing your request...',
        'error': 'Sorry, there was an error processing your request.',
        'no_location': 'Location access is required for weather and soil data.',
        'speak_button': 'Click to speak',
        'stop_button': 'Stop recording'
    },
    'hi': {
        'app_title': '🌾 एआई कृषि सहायक',
        'welcome': 'आपके एआई कृषि सहायक में आपका स्वागत है',
        'select_language': 'अपनी पसंदीदा भाषा चुनें:',
        'location_prompt': 'मौसम और मिट्टी के डेटा के लिए कृपया अपना स्थान साझा करें',
        'speak_request': '🎤 अपना कृषि प्रश्न बोलें',
        'upload_image': '📸 रोग की पहचान के लिए फसल की तस्वीर अपलोड करें',
        'weather_title': '🌦️ मौसम की जानकारी',
        'soil_title': '🌱 मिट्टी विश्लेषण',
        'disease_title': '🔍 रोग की पहचान',
        'advisory_title': '🧑‍🌾 कृषि सलाह',
        'processing': 'आपके अनुरोध को संसाधित कर रहे हैं...',
        'error': 'खुशी है, आपके अनुरोध को संसाधित करने में त्रुटि हुई।',
        'no_location': 'मौसम और मिट्टी के डेटा के लिए स्थान पहुंच आवश्यक है।',
        'speak_button': 'बोलने के लिए क्लिक करें',
        'stop_button': 'रिकॉर्डिंग बंद करें'
    },
    'ta': {
        'app_title': '🌾 AI விவசாய உதவியாளர்',
        'welcome': 'உங்கள் AI விவசாய உதவியாளருக்கு வரவேற்கிறோம்',
        'select_language': 'உங்கள் விருப்பமான மொழியைத் தேர்ந்தெடுக்கவும்:',
        'location_prompt': 'வானிலை மற்றும் மண் தரவுகளுக்கு உங்கள் இருப்பிடத்தைப் பகிரவும்',
        'speak_request': '🎤 உங்கள் விவசாய கேள்வியைப் பேசுங்கள்',
        'upload_image': '📸 நோய் கண்டறிதலுக்கு பயிர் படத்தை பதிவேற்றவும்',
        'weather_title': '🌦️ வானிலை தகவல்',
        'soil_title': '🌱 மண் பகுப்பாய்வு',
        'disease_title': '🔍 நோய் கண்டறிதல்',
        'advisory_title': '🧑‍🌾 விவசாய ஆலோசனை',
        'processing': 'உங்கள் கோரிக்கையை செயலாக்குகிறது...',
        'error': 'மன்னிக்கவும், உங்கள் கோரிக்கையை செயலாக்குவதில் பிழை ஏற்பட்டது.',
        'no_location': 'வானிலை மற்றும் மண் தரவுகளுக்கு இருப்பிட அணுகல் தேவை.',
        'speak_button': 'பேச கிளிக் செய்யவும்',
        'stop_button': 'பதிவை நிறுத்து'
    },
    'te': {
        'app_title': '🌾 AI వ్యవసాయ సహాయకుడు',
        'welcome': 'మీ AI వ్యవసాయ సహాయకుడికి స్వాగతం',
        'select_language': 'మీ ఇష్టమైన భాషను ఎంచుకోండి:',
        'location_prompt': 'వాతావరణం మరియు మట్టి డేటా కోసం దయచేసి మీ స్థానాన్ని పంచుకోండి',
        'speak_request': '🎤 మీ వ్యవసాయ ప్రశ్నను మాట్లాడండి',
        'upload_image': '📸 వ్యాధి గుర్తింపు కోసం పంట చిత్రాన్ని అప్‌లోడ్ చేయండి',
        'weather_title': '🌦️ వాతావరణ సమాచారం',
        'soil_title': '🌱 మట్టి విశ్లేషణ',
        'disease_title': '🔍 వ్యాధి గుర్తింపు',
        'advisory_title': '🧑‍🌾 వ్యవసాయ సలహా',
        'processing': 'మీ అభ్యర్థనను ప్రాసెస్ చేస్తున్నాము...',
        'error': 'క్షమించండి, మీ అభ్యర్థనను ప్రాసెస్ చేయడంలో లోపం ఉంది.',
        'no_location': 'వాతావరణం మరియు మట్టి డేటా కోసం స్థాన యాక్సెస్ అవసరం.',
        'speak_button': 'మాట్లాడటానికి క్లిక్ చేయండి',
        'stop_button': 'రికార్డింగ్ ఆపండి'
    }
}
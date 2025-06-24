import streamlit as st
import requests
import time
import urllib3
import base64
from PIL import Image
import io
import json

# Disable SSL warnings for internal testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(
    page_title="AI Dermatologist - Skincare Recommendations", 
    page_icon="🧴",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        font-size: 2.5rem;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #A23B72;
        font-size: 1.5rem;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #F18F01;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #2E86AB;
        margin: 1rem 0;
    }
    .stButton > button {
        background-color: #2E86AB;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #A23B72;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'image_analysis' not in st.session_state:
    st.session_state.image_analysis = None

# API Configuration
SKINCARE_API_URL = "https://skincare_products_prod.tanjirouji.workers.dev/test-vertex-catalog"
ORBO_AI_URL = "https://api.orbo.ai/analyze"  # Replace with actual Orbo AI endpoint

def analyze_image_with_orbo(image_data):
    """Analyze image using Orbo AI for facial features"""
    try:
        # Convert image to base64
        buffered = io.BytesIO()
        image_data.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # Mock Orbo AI response (replace with actual API call)
        mock_response = {
            "skin_type": "combination",
            "visible_concerns": ["fine_lines", "dark_spots"],
            "skin_tone": "medium",
            "age_estimate": "25-35",
            "confidence": 0.87
        }
        
        # Actual API call would be:
        # headers = {"Authorization": "Bearer YOUR_ORBO_API_KEY"}
        # payload = {"image": img_str, "analysis_type": "facial_skin"}
        # response = requests.post(ORBO_AI_URL, json=payload, headers=headers)
        # return response.json()
        
        return mock_response
    except Exception as e:
        st.error(f"Image analysis failed: {e}")
        return None

def main():
    st.markdown('<h1 class="main-header">🧴 AI Dermatologist - Personalized Skincare</h1>', unsafe_allow_html=True)
    
    # Progress bar
    progress = st.session_state.step / 6
    st.progress(progress)
    st.write(f"Step {st.session_state.step} of 6")
    
    if st.session_state.step == 1:
        complexion_assessment()
    elif st.session_state.step == 2:
        age_assessment()
    elif st.session_state.step == 3:
        medical_history()
    elif st.session_state.step == 4:
        environment_assessment()
    elif st.session_state.step == 5:
        lifestyle_assessment()
    elif st.session_state.step == 6:
        final_recommendations()

def complexion_assessment():
    st.markdown('<h2 class="section-header">🔍 C - Complexion Assessment</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📸 Upload Your Photo (Optional)")
        uploaded_file = st.file_uploader(
            "Upload a clear photo of your face for AI analysis",
            type=['jpg', 'jpeg', 'png'],
            help="This helps our AI analyze your skin type and concerns more accurately"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            if st.button("🔬 Analyze Image with AI"):
                with st.spinner("Analyzing your skin with AI..."):
                    analysis = analyze_image_with_orbo(image)
                    if analysis:
                        st.session_state.image_analysis = analysis
                        st.success("✅ Image analysis complete!")
                        
                        # Display analysis results
                        st.markdown('<div class="info-box">', unsafe_allow_html=True)
                        st.write("**AI Analysis Results:**")
                        st.write(f"- Detected Skin Type: {analysis.get('skin_type', 'Unknown')}")
                        st.write(f"- Visible Concerns: {', '.join(analysis.get('visible_concerns', []))}")
                        st.write(f"- Confidence: {analysis.get('confidence', 0)*100:.1f}%")
                        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("📝 Manual Assessment")
        
        # Pre-fill with AI analysis if available
        default_skin_type = st.session_state.image_analysis.get('skin_type', 'normal') if st.session_state.image_analysis else 'normal'
        default_concerns = st.session_state.image_analysis.get('visible_concerns', []) if st.session_state.image_analysis else []
        
        skin_type = st.selectbox(
            "What's your skin type?",
            ["oily", "dry", "normal", "combination", "sensitive"],
            index=["oily", "dry", "normal", "combination", "sensitive"].index(default_skin_type)
        )
        
        concerns = st.multiselect(
            "What are your main skin concerns?",
            ["acne", "dark spots", "wrinkles", "fine lines", "redness", "blackheads", "dullness", "enlarged pores", "uneven texture"],
            default=default_concerns
        )
        
        skin_tone = st.selectbox(
            "Your skin tone:",
            ["very fair", "fair", "medium", "olive", "dark", "very dark"]
        )
        
        sensitivity_level = st.slider(
            "How sensitive is your skin? (1=Not sensitive, 5=Very sensitive)",
            1, 5, 3
        )
        
        st.session_state.user_data.update({
            'skin_type': skin_type,
            'concerns': concerns,
            'skin_tone': skin_tone,
            'sensitivity_level': sensitivity_level
        })
    
    if st.button("Next: Age Assessment →"):
        st.session_state.step = 2
        st.rerun()

def age_assessment():
    st.markdown('<h2 class="section-header">🎂 A - Age Assessment</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        age_group = st.selectbox(
            "Your age group:",
            ["under 18", "18-24", "25-35", "36-50", "50+"]
        )
        
        hormonal_changes = st.multiselect(
            "Any hormonal changes? (Select all that apply)",
            ["puberty", "menstruation", "pregnancy", "menopause", "none"]
        )
    
    with col2:
        skin_aging_concerns = st.multiselect(
            "Age-related skin concerns:",
            ["fine lines", "wrinkles", "age spots", "loss of elasticity", "sagging", "none"]
        )
        
        previous_treatments = st.text_area(
            "Any previous anti-aging treatments?",
            placeholder="e.g., retinoids, chemical peels, botox, etc."
        )
    
    st.session_state.user_data.update({
        'age_group': age_group,
        'hormonal_changes': hormonal_changes,
        'skin_aging_concerns': skin_aging_concerns,
        'previous_treatments': previous_treatments
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Next: Medical History →"):
            st.session_state.step = 3
            st.rerun()

def medical_history():
    st.markdown('<h2 class="section-header">🏥 M - Medical History</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        allergies = st.text_area(
            "Known allergies (skincare ingredients or general):",
            placeholder="e.g., fragrance, salicylic acid, nuts, etc."
        )
        
        skin_conditions = st.multiselect(
            "Current or past skin conditions:",
            ["eczema", "psoriasis", "rosacea", "dermatitis", "acne", "none"]
        )
        
        medications = st.text_area(
            "Current medications that might affect skin:",
            placeholder="e.g., birth control, antibiotics, retinoids, etc."
        )
    
    with col2:
        recent_procedures = st.multiselect(
            "Recent cosmetic procedures (last 6 months):",
            ["chemical peel", "microdermabrasion", "laser treatment", "botox", "fillers", "none"]
        )
        
        doctor_recommendations = st.text_area(
            "Any dermatologist recommendations:",
            placeholder="Specific ingredients to use or avoid"
        )
        
        pregnancy_nursing = st.radio(
            "Are you pregnant or nursing?",
            ["no", "pregnant", "nursing"]
        )
    
    st.session_state.user_data.update({
        'allergies': allergies,
        'skin_conditions': skin_conditions,
        'medications': medications,
        'recent_procedures': recent_procedures,
        'doctor_recommendations': doctor_recommendations,
        'pregnancy_nursing': pregnancy_nursing
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Next: Environment →"):
            st.session_state.step = 4
            st.rerun()

def environment_assessment():
    st.markdown('<h2 class="section-header">🌍 E - Environment Assessment</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌦️ Climate Conditions")
        humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=60)
        temperature = st.slider("Temperature (°C)", min_value=-10, max_value=50, value=25)
        
        climate_type = st.selectbox(
            "Your climate type:",
            ["tropical", "dry", "temperate", "cold", "humid", "arid"]
        )
        
        seasonal_changes = st.multiselect(
            "How does your skin change with seasons?",
            ["drier in winter", "oilier in summer", "more sensitive in spring", "breakouts in humid weather", "no change"]
        )
    
    with col2:
        st.subheader("🏢 Environment Factors")
        work_environment = st.selectbox(
            "Work environment:",
            ["office (AC)", "outdoors", "hospital/clinical", "home", "industrial", "other"]
        )
        
        pollution_exposure = st.slider(
            "Pollution exposure level (1=Low, 5=High)",
            1, 5, 3
        )
        
        sun_exposure = st.selectbox(
            "Daily sun exposure:",
            ["minimal (indoor)", "moderate (some outdoor)", "high (mostly outdoor)", "extreme (beach/snow)"]
        )
        
        water_quality = st.selectbox(
            "Water quality for washing:",
            ["soft water", "hard water", "filtered water", "well water", "unknown"]
        )
    
    st.session_state.user_data.update({
        'humidity': humidity,
        'temperature': temperature,
        'climate_type': climate_type,
        'seasonal_changes': seasonal_changes,
        'work_environment': work_environment,
        'pollution_exposure': pollution_exposure,
        'sun_exposure': sun_exposure,
        'water_quality': water_quality
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Next: Lifestyle →"):
            st.session_state.step = 5
            st.rerun()

def lifestyle_assessment():
    st.markdown('<h2 class="section-header">🏃‍♀️ L - Lifestyle Assessment</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Budget & Preferences")
        budget = st.selectbox(
            "Budget range:",
            ["budget (under $50)", "mid-range ($50-150)", "premium ($150-300)", "luxury (over $300)"]
        )
        
        routine_preference = ""
        
        ingredient_preference = st.multiselect(
            "Ingredient preferences:",
            ["natural/organic", "fragrance-free", "vegan", "cruelty-free", "Korean skincare", "clinical/medical grade"]
        )
    
    with col2:
        st.subheader("🌟 Lifestyle Factors")
        exercise_frequency = st.selectbox(
            "Exercise frequency:",
            ["daily", "3-4 times/week", "1-2 times/week", "rarely", "never"]
        )
        
        sleep_quality = st.slider(
            "Sleep quality (1=Poor, 5=Excellent)",
            1, 5, 3
        )
        
        stress_level = st.slider(
            "Stress level (1=Low, 5=High)",
            1, 5, 3
        )
        
        diet_type = st.multiselect(
            "Diet characteristics:",
            ["high sugar", "dairy-heavy", "vegetarian", "vegan", "low-carb", "balanced", "processed foods"]
        )
        
        smoking_alcohol = st.multiselect(
            "Lifestyle factors:",
            ["smoking", "regular alcohol", "frequent travel", "shift work", "none"]
        )
    
    st.session_state.user_data.update({
        'budget': budget,
        'routine_preference': routine_preference,
        'ingredient_preference': ingredient_preference,
        'exercise_frequency': exercise_frequency,
        'sleep_quality': sleep_quality,
        'stress_level': stress_level,
        'diet_type': diet_type,
        'smoking_alcohol': smoking_alcohol
    })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Get My Recommendations! 🎉"):
            st.session_state.step = 6
            st.rerun()

def final_recommendations():
    st.markdown('<h2 class="section-header">✨ Your Personalized Skincare Recommendations</h2>', unsafe_allow_html=True)
    
    # Prepare data for API call
    api_payload = {
        "profile": {
            "skin_type": st.session_state.user_data.get('skin_type', 'normal'),
            "concerns": st.session_state.user_data.get('concerns', []),
            "age_group": st.session_state.user_data.get('age_group', '25-35'),
            "budget": map_budget(st.session_state.user_data.get('budget', 'mid-range')),
            "routine_preference": map_routine_preference(st.session_state.user_data.get('routine_preference', 'standard')),
            "location": {
                "climate": {
                    "humidity": st.session_state.user_data.get('humidity', 60),
                    "temperature": st.session_state.user_data.get('temperature', 25)
                }
            }
        },
        "advanced_profile": st.session_state.user_data,
        "image_analysis": st.session_state.image_analysis
    }
    
    if st.button("🔄 Regenerate Recommendations"):
        get_recommendations(api_payload)
    
    # Auto-generate recommendations on first visit to this step
    if 'recommendations' not in st.session_state:
        get_recommendations(api_payload)
    
    # Display recommendations if available
    if 'recommendations' in st.session_state:
        display_recommendations(st.session_state.recommendations)
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous"):
            st.session_state.step = 5
            st.rerun()
    with col2:
        if st.button("🔄 Start Over"):
            # Reset all session state
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def get_recommendations(payload):
    with st.spinner("🧪 Analyzing your profile..."):
        time.sleep(1.5)
    
    with st.spinner("✨ Creating your personalized skincare routine..."):
        try:
            response = requests.post(SKINCARE_API_URL, json=payload, verify=False, timeout=30)
            response.raise_for_status()
            data = response.json()
            st.session_state.recommendations = data
            st.success("🎉 Your personalized recommendations are ready!")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API call failed: {e}")
            # Fallback to mock data
            st.session_state.recommendations = get_mock_recommendations()

def display_recommendations(data):
    # Display routine summary
    if 'recommendations' in data and 'routine_summary' in data['recommendations']:
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.write("**Your Skincare Analysis:**")
        st.write(data['recommendations']['routine_summary'])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display products
    if 'recommendations' in data and 'selected_products' in data['recommendations']:
        st.subheader("🛍️ Recommended Products")
        
        for i, product in enumerate(data['recommendations']['selected_products']):
            with st.expander(f"{i+1}. {product['name']} - {product['brand']} (Match: {product['match_score']}%)"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Category:** {product['category']}")
                    st.write(f"**Usage:** {product['usage_instructions']}")
                    st.write(f"**Why recommended:** {product['reason']}")
                    st.write(f"**Key ingredients:** {', '.join(product['key_matching_ingredients'])}")
                
                with col2:
                    st.write(f"**Price:** ₹{product['price']}")
                    if 'reviews' in product and product['reviews'].get('rating'):
                        st.write(f"**Rating:** {product['reviews']['rating']}⭐")
    
    # Display routines
    if 'recommendations' in data and 'routine' in data['recommendations']:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🌅 Morning Routine")
            for step in data['recommendations']['routine'].get('morning_routine', []):
                st.write(f"• {step}")
        
        with col2:
            st.subheader("🌙 Evening Routine")
            for step in data['recommendations']['routine'].get('evening_routine', []):
                st.write(f"• {step}")
        
        # Tips and timeline
        st.subheader("💡 Expert Tips")
        for tip in data['recommendations']['routine'].get('tips', []):
            st.write(f"• {tip}")
        
        st.subheader("📅 Expected Results Timeline")
        st.write(data['recommendations']['routine'].get('timeline', 'Results typically visible in 4-6 weeks with consistent use.'))

def map_budget(budget_str):
    mapping = {
        "budget (under $50)": "low",
        "mid-range ($50-150)": "mid-range", 
        "premium ($150-300)": "premium",
        "luxury (over $300)": "premium"
    }
    return mapping.get(budget_str, "mid-range")

def map_routine_preference(routine_str):
    mapping = {
        "minimal (3-4 products)": "minimal",
        "standard (5-7 products)": "standard",
        "detailed (8+ products)": "detailed"
    }
    return mapping.get(routine_str, "standard")

def get_mock_recommendations():
    # Return the data from your document as fallback
    return json.loads('''
    {
        "success": true,
        "recommendations": {
            "routine_summary": "This routine focuses on hydrating, soothing, and strengthening dry, sensitive skin while addressing fine lines.",
            "selected_products": [
                {
                    "name": "Gentle Hydrating Cleanser",
                    "brand": "CeraVe",
                    "category": "Cleanser",
                    "match_score": 92,
                    "key_matching_ingredients": ["Ceramides", "Hyaluronic Acid"],
                    "usage_instructions": "Use morning and evening",
                    "reason": "Perfect for sensitive skin with barrier-repairing ingredients",
                    "price": 1200
                }
            ],
            "routine": {
                "morning_routine": [
                    "Gentle cleanser",
                    "Hydrating serum", 
                    "Moisturizer with SPF"
                ],
                "evening_routine": [
                    "Gentle cleanser",
                    "Treatment serum",
                    "Night moisturizer"
                ],
                "tips": [
                    "Always patch test new products",
                    "Use sunscreen daily",
                    "Be consistent with your routine"
                ],
                "timeline": "Visible improvements in 4-6 weeks"
            }
        }
    }
    ''')

if __name__ == "__main__":
    main()

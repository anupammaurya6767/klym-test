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
    page_title="AI Dermatologist - Quick Skincare Demo", 
    page_icon="🧴",
    layout="wide"
)

# Enhanced Custom CSS for beautiful UI
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header {
        color: #4a5568;
        font-size: 1.8rem;
        margin: 2rem 0 1rem 0;
        padding: 1rem;
        background: linear-gradient(90deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .info-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        margin: 1.5rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50px;
        border: none;
        padding: 0.8rem 2.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .result-container {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    .product-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .product-card:hover {
        transform: translateX(10px);
    }
    
    .routine-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .emoji-header {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# API Configuration
SKINCARE_API_URL = "https://skincare_products_prod.tanjirouji.workers.dev/test-vertex-catalog"

def analyze_image_mock(image_data):
    """Mock image analysis"""
    return {
        "skin_type": "combination",
        "visible_concerns": ["fine_lines", "dark_spots"],
        "confidence": 0.87
    }

def main():
    st.markdown('<h1 class="main-header">🧴 AI Dermatologist - Quick Demo</h1>', unsafe_allow_html=True)
    
    # Progress bar
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    progress = st.session_state.step / 3
    st.progress(progress)
    st.write(f"**Step {st.session_state.step} of 3** ✨")
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.step == 1:
        basic_info()
    elif st.session_state.step == 2:
        skin_assessment()
    elif st.session_state.step == 3:
        show_recommendations()

def basic_info():
    st.markdown('<div class="section-header">👋 Tell Us About Yourself</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        
        name = st.text_input("💫 What's your name?", placeholder="Enter your name")
        
        age_group = st.selectbox(
            "🎂 Your age group:",
            ["18-24", "25-35", "36-50", "50+"]
        )
        
        skin_goal = st.selectbox(
            "🎯 What's your main skincare goal?",
            ["Anti-aging", "Acne treatment", "Hydration", "Brightening", "General maintenance"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.session_state.user_data.update({
            'name': name,
            'age_group': age_group,
            'skin_goal': skin_goal
        })
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Optional: Upload Photo")
        uploaded_file = st.file_uploader(
            "For better AI analysis",
            type=['jpg', 'jpeg', 'png'],
            help="Optional: Helps AI analyze your skin better"
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
            st.session_state.user_data['has_image'] = True
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Next: Skin Assessment →", key="next1"):
        if name:
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Please enter your name to continue!")

def skin_assessment():
    st.markdown('<div class="section-header">🔍 Quick Skin Assessment</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 🧴 Skin Type")
        skin_type = st.radio(
            "What's your skin type?",
            ["Oily", "Dry", "Normal", "Combination", "Sensitive"],
            horizontal=True
        )
        
        st.markdown("### 🎯 Main Concerns")
        concerns = st.multiselect(
            "Select your top concerns:",
            ["Acne", "Dark spots", "Wrinkles", "Dryness", "Oiliness", "Sensitivity", "Dullness"]
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### 💰 Budget Range")
        budget = st.selectbox(
            "Your budget for skincare:",
            ["Budget (Under ₹2000)", "Mid-range (₹2000-5000)", "Premium (₹5000+)"]
        )
        
        st.markdown("### 🌍 Environment")
        climate = st.selectbox(
            "Your climate:",
            ["Hot & Humid", "Hot & Dry", "Moderate", "Cold & Dry"]
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.session_state.user_data.update({
        'skin_type': skin_type.lower(),
        'concerns': [c.lower() for c in concerns],
        'budget': budget,
        'climate': climate
    })
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Previous", key="prev1"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Get My Recommendations! 🎉", key="final"):
            st.session_state.step = 3
            st.rerun()

def show_recommendations():
    st.markdown('<div class="section-header">✨ Your Personalized Skincare Plan</div>', unsafe_allow_html=True)
    
    # Welcome message
    name = st.session_state.user_data.get('name', 'there')
    st.markdown(f'<div class="result-container">', unsafe_allow_html=True)
    st.markdown(f"## Hello {name}! 👋")
    st.markdown("Here's your personalized skincare routine based on our analysis:")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate recommendations
    if 'recommendations' not in st.session_state:
        get_recommendations()
    
    if 'recommendations' in st.session_state:
        display_beautiful_recommendations()
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Previous", key="prev2"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("🔄 New Recommendations", key="regen"):
            if 'recommendations' in st.session_state:
                del st.session_state.recommendations
            get_recommendations()
            st.rerun()
    with col3:
        if st.button("🔄 Start Over", key="restart"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

def get_recommendations():
    with st.spinner("🧪 Analyzing your skin profile..."):
        time.sleep(2)
    
    with st.spinner("✨ Creating your personalized routine..."):
        # Prepare API payload
        api_payload = {
            "profile": {
                "skin_type": st.session_state.user_data.get('skin_type', 'normal'),
                "concerns": st.session_state.user_data.get('concerns', []),
                "age_group": st.session_state.user_data.get('age_group', '25-35'),
                "budget": map_budget(st.session_state.user_data.get('budget', 'Mid-range')),
                "climate": st.session_state.user_data.get('climate', 'moderate')
            },
            "user_data": st.session_state.user_data
        }
        
        try:
            response = requests.post(SKINCARE_API_URL, json=api_payload, verify=False, timeout=15)
            response.raise_for_status()
            st.session_state.recommendations = response.json()
            st.success("🎉 Your personalized recommendations are ready!")
        except:
            # Fallback to mock data for demo
            st.session_state.recommendations = get_mock_recommendations()
            st.success("🎉 Demo recommendations generated!")

def display_beautiful_recommendations():
    data = st.session_state.recommendations
    
    # Skin Analysis Summary
    if 'recommendations' in data:
        recs = data['recommendations']
        
        st.markdown('<div class="result-container">', unsafe_allow_html=True)
        st.markdown("### 🔬 Your Skin Analysis")
        st.markdown(recs.get('routine_summary', 'Custom routine designed for your skin type and concerns.'))
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recommended Products
        if 'selected_products' in recs:
            st.markdown("## 🛍️ Recommended Products")
            
            for i, product in enumerate(recs['selected_products'][:4]):  # Show top 4 products
                st.markdown(f'<div class="product-card">', unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### {i+1}. {product['name']}")
                    st.markdown(f"**Brand:** {product['brand']} | **Category:** {product['category']}")
                    st.markdown(f"**Why recommended:** {product['reason']}")
                    st.markdown(f"**Key ingredients:** {', '.join(product.get('key_matching_ingredients', ['N/A']))}")
                
                with col2:
                    st.markdown(f"### ₹{product.get('price', 'N/A')}")
                    st.markdown(f"**Match: {product.get('match_score', 85)}%** ⭐")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Skincare Routines
        if 'routine' in recs:
            st.markdown("## 📅 Your Daily Routine")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="routine-card">', unsafe_allow_html=True)
                st.markdown('<div class="emoji-header">🌅</div>', unsafe_allow_html=True)
                st.markdown("### Morning Routine")
                for step in recs['routine'].get('morning_routine', []):
                    st.markdown(f"• {step}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="routine-card">', unsafe_allow_html=True)
                st.markdown('<div class="emoji-header">🌙</div>', unsafe_allow_html=True)
                st.markdown("### Evening Routine")
                for step in recs['routine'].get('evening_routine', []):
                    st.markdown(f"• {step}")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Expert Tips
            st.markdown('<div class="result-container">', unsafe_allow_html=True)
            st.markdown("### 💡 Expert Tips")
            for tip in recs['routine'].get('tips', ['Use sunscreen daily', 'Be consistent with your routine']):
                st.markdown(f"✨ {tip}")
            
            st.markdown("### 📈 Expected Results")
            st.markdown(recs['routine'].get('timeline', 'Visible improvements in 4-6 weeks with consistent use.'))
            st.markdown('</div>', unsafe_allow_html=True)

def map_budget(budget_str):
    mapping = {
        "Budget (Under ₹2000)": "low",
        "Mid-range (₹2000-5000)": "mid-range", 
        "Premium (₹5000+)": "premium"
    }
    return mapping.get(budget_str, "mid-range")

def get_mock_recommendations():
    skin_type = st.session_state.user_data.get('skin_type', 'normal')
    concerns = st.session_state.user_data.get('concerns', [])
    
    return {
        "success": True,
        "recommendations": {
            "routine_summary": f"This routine is designed for {skin_type} skin, focusing on {', '.join(concerns[:2]) if concerns else 'general care'} with gentle yet effective ingredients.",
            "selected_products": [
                {
                    "name": "Gentle Hydrating Cleanser",
                    "brand": "CeraVe",
                    "category": "Cleanser",
                    "match_score": 92,
                    "key_matching_ingredients": ["Ceramides", "Hyaluronic Acid"],
                    "reason": "Perfect for your skin type with barrier-repairing ingredients",
                    "price": 1200
                },
                {
                    "name": "Niacinamide Serum",
                    "brand": "The Ordinary",
                    "category": "Treatment",
                    "match_score": 88,
                    "key_matching_ingredients": ["Niacinamide", "Zinc"],
                    "reason": "Addresses your main concerns while being gentle",
                    "price": 800
                },
                {
                    "name": "Daily Moisturizer SPF 30",
                    "brand": "Neutrogena",
                    "category": "Moisturizer + Sunscreen",
                    "match_score": 90,
                    "key_matching_ingredients": ["SPF 30", "Hyaluronic Acid"],
                    "reason": "Perfect for daily protection and hydration",
                    "price": 950
                },
                {
                    "name": "Night Repair Cream",
                    "brand": "Olay",
                    "category": "Night Moisturizer",
                    "match_score": 87,
                    "key_matching_ingredients": ["Peptides", "Vitamins"],
                    "reason": "Helps repair and rejuvenate skin overnight",
                    "price": 1500
                }
            ],
            "routine": {
                "morning_routine": [
                    "Gentle Hydrating Cleanser",
                    "Niacinamide Serum (if using)",
                    "Daily Moisturizer with SPF 30"
                ],
                "evening_routine": [
                    "Gentle Hydrating Cleanser",
                    "Treatment serum (alternate days)",
                    "Night Repair Cream"
                ],
                "tips": [
                    "Always patch test new products before full use",
                    "Introduce new products one at a time",
                    "Consistency is key - stick to the routine for best results",
                    "Never skip sunscreen during the day"
                ],
                "timeline": "You should start seeing improvements in 4-6 weeks with consistent use. Full results typically visible in 8-12 weeks."
            }
        }
    }

if __name__ == "__main__":
    main()

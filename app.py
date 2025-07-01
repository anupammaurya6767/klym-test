import streamlit as st
import requests
import time
import urllib3

# Disable SSL warnings for internal testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="Skincare Recommendation Tester", page_icon="🧴")

st.title("🧴 Skincare Product Recommendation Tester")

API_URL = "https://klym-products.klym-life.workers.dev/test-vertex-catalog"

# --- User Profile Form ---
st.header("🧍‍♀️ User Profile")

# Add name field
name = st.text_input("Your Name", placeholder="Enter your name")

skin_type = st.selectbox("Skin Type", ["oily", "dry", "normal", "combination", "sensitive"])
concerns = st.multiselect("Skin Concerns", ["acne", "dark spots", "wrinkles", "redness", "blackheads", "dullness"])
age_group = st.selectbox("Age Group", ["under 18", "18-24", "25-35", "36-50", "50+"])
budget = st.selectbox("Budget Range", ["low", "mid-range", "premium"])
routine_preference = ""

st.header("🌦️ Climate Conditions")
humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=60)
temperature = st.slider("Temperature (°C)", min_value=-10, max_value=50, value=25)

# --- Get Recommendations ---
if st.button("💡 Get Recommendations"):
    if not name.strip():
        st.error("Please enter your name to continue!")
    else:
        with st.spinner("🧪 Getting things ready…"):
            time.sleep(1.5)

        with st.spinner("✨ Creating your personalized skincare routine…"):
            payload = {
                "profile": {
                    "name": name,
                    "skin_type": skin_type,
                    "concerns": concerns,
                    "age_group": age_group,
                    "budget": budget,
                    "routine_preference": routine_preference,
                    "location": {
                        "climate": {
                            "humidity": humidity,
                            "temperature": temperature
                        }
                    }
                }
            }

            try:
                response = requests.post(API_URL, json=payload, verify=False)
                response.raise_for_status()
                data = response.json()

                st.success(f"🎉 Recommendations ready for {name}!")

                # Display personalized greeting
                st.markdown(f"## Hello {name}! 👋")
                st.markdown("Here are your personalized skincare recommendations:")

                # Display routine summary if available
                if 'recommendations' in data and 'routine_summary' in data['recommendations']:
                    st.subheader("📋 Your Skin Analysis")
                    st.info(data['recommendations']['routine_summary'])

                # Display recommended products
                if 'recommendations' in data and 'selected_products' in data['recommendations']:
                    st.subheader("🛍️ Recommended Products")
                    
                    products = data['recommendations']['selected_products']
                    for i, product in enumerate(products, 1):
                        with st.expander(f"{i}. {product.get('name', 'Product')} - {product.get('brand', 'Brand')} (Match: {product.get('match_score', 'N/A')}%)"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write(f"**Category:** {product.get('category', 'N/A')}")
                                st.write(f"**Usage:** {product.get('usage_instructions', 'Follow product instructions')}")
                                st.write(f"**Why recommended:** {product.get('reason', 'Good for your skin type')}")
                                
                                # Display key ingredients
                                ingredients = product.get('key_matching_ingredients', [])
                                if ingredients:
                                    st.write(f"**Key ingredients:** {', '.join(ingredients)}")
                            
                            with col2:
                                price = product.get('price', 'N/A')
                                if price != 'N/A':
                                    st.write(f"**Price:** ₹{price}")
                                else:
                                    st.write(f"**Price:** {price}")
                                
                                # Display rating if available
                                if 'reviews' in product and product['reviews'].get('rating'):
                                    rating = product['reviews']['rating']
                                    st.write(f"**Rating:** {rating}⭐")

                # Display routines
                if 'recommendations' in data and 'routine' in data['recommendations']:
                    routine = data['recommendations']['routine']
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🌞 Morning Routine")
                        morning_routine = routine.get('morning_routine', [])
                        if morning_routine:
                            for item in morning_routine:
                                st.markdown(f"• {item}")
                        else:
                            st.write("No morning routine provided")
                    
                    with col2:
                        st.subheader("🌙 Evening Routine")
                        evening_routine = routine.get('evening_routine', [])
                        if evening_routine:
                            for item in evening_routine:
                                st.markdown(f"• {item}")
                        else:
                            st.write("No evening routine provided")

                    # Display tips
                    if 'tips' in routine:
                        st.subheader("💡 Expert Tips")
                        for tip in routine['tips']:
                            st.markdown(f"✨ {tip}")

                    # Display timeline
                    if 'timeline' in routine:
                        st.subheader("📆 Expected Results Timeline")
                        st.markdown(f"⏰ {routine['timeline']}")

                # Expandable full response for debugging
                with st.expander("🧾 Full API Response (Debug)"):
                    st.json(data)

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 API call failed: {e}")
                st.info("Make sure the API endpoint is accessible and try again.")

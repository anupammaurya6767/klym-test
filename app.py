import streamlit as st
import requests
import time
import urllib3

# Disable SSL warnings for internal testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

st.set_page_config(page_title="Skincare Recommendation Tester", page_icon="🧴")

st.title("🧴 Skincare Product Recommendation Tester")

API_URL = "https://skincare_products_prod.tanjirouji.workers.dev/test-vertex-catalog"

# --- User Profile Form ---
st.header("🧍‍♀️ User Profile")

skin_type = st.selectbox("Skin Type", ["oily", "dry", "normal", "combination", "sensitive"])
concerns = st.multiselect("Skin Concerns", ["acne", "dark spots", "wrinkles", "redness", "blackheads", "dullness"])
age_group = st.selectbox("Age Group", ["under 18", "18-24", "25-35", "36-50", "50+"])
budget = st.selectbox("Budget Range", ["low", "mid-range", "premium"])
routine_preference = st.radio("Routine Preference", ["minimal", "standard", "detailed"])

st.header("🌦️ Climate Conditions")
humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=60)
temperature = st.slider("Temperature (°C)", min_value=-10, max_value=50, value=25)

# --- Get Recommendations ---
if st.button("💡 Get Recommendations"):
    with st.spinner("🧪 Getting things ready…"):
        time.sleep(1.5)

    with st.spinner("✨ Creating your personalized skincare routine…"):
        payload = {
            "profile": {
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

            st.success("🎉 Recommendations ready!")

            # st.subheader("📋 Routine Summary")
            # st.write(data.get("routine_summary", "No summary provided."))

            # st.subheader("🌞 Morning Routine")
            # for item in data.get("routine", {}).get("morning_routine", []):
            #     st.markdown(f"- {item}")

            # st.subheader("🌙 Evening Routine")
            # for item in data.get("routine", {}).get("evening_routine", []):
            #     st.markdown(f"- {item}")

            # st.subheader("💡 Tips")
            # for tip in data.get("routine", {}).get("tips", []):
            #     st.markdown(f"- {tip}")

            # st.subheader("📆 Expected Timeline")
            # st.markdown(data.get("routine", {}).get("timeline", "4–6 weeks"))

            st.subheader("🧾 Full Response (Debug)")
            st.json(data)

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API call failed: {e}")

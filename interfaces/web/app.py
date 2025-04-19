import streamlit as st
import requests

# Configuration
API_URL = "http://localhost:8000/analyze"

st.title("ShieldNet AI Defender")
st.subheader("Phishing Detection Interface")

# Input form
text_input = st.text_area("Enter text to analyze:")
if st.button("Analyze"):
    if text_input:
        response = requests.post(
            API_URL,
            json={"text": text_input}
        )
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"Analysis Result: {result['threat_type']}")
            st.metric("Confidence", f"{result['confidence']:.2%}")
        elif response.status_code == 429:
            st.error("Rate limit exceeded - try again in 60 seconds")
        else:
            st.error(f"API Error: {response.text}")
    else:
        st.warning("Please enter text to analyze")

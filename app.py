import streamlit as st

# Import config first to ensure environment variables are set
from src import config
from src.services.lekhak_service import generate_content

st.set_page_config(page_title="Lekhak AI")
st.title("Lekhak AI — Content Generator")

prompt = st.text_area("Enter your request:", height=140)

# Track session per user
if "user_id" not in st.session_state:
    st.session_state["user_id"] = "streamlit_user"

if st.button("Generate"):
    if not prompt.strip():
        st.warning("Please enter something.")
        st.stop()

    with st.spinner("Generating..."):
        result = generate_content(prompt, st.session_state["user_id"])
        st.success(result)

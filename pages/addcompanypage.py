import streamlit as st
from src.database import SessionLocal, create_company

st.set_page_config(page_title="Add Company - Lekhak AI", layout="wide")

st.title("Add New Company")
st.markdown("*Register a new company to start generating content*")

st.markdown("---")

with st.form("add_company_form"):
    st.subheader("Register New Company")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Company Name *", placeholder="e.g., TechCorp Inc.")

    with col2:
        industry = st.text_input(
            "Industry *", placeholder="e.g., Software, Healthcare, Finance"
        )

    description = st.text_area(
        "Company Description *",
        height=150,
        placeholder="Describe what your company does, its mission, and key offerings...",
    )

    submitted = st.form_submit_button(
        "Add Company", type="primary", use_container_width=True
    )

    if submitted:
        if not all([name.strip(), industry.strip(), description.strip()]):
            st.error("Please fill in all required fields (marked with *).")
        else:
            try:
                db = SessionLocal()
                create_company(
                    db,
                    name=name.strip(),
                    industry=industry.strip(),
                    description=description.strip(),
                )
                db.close()
                st.success(f"Company '{name}' added successfully!")
            except Exception as e:
                st.error(f" Error adding company: {e}")

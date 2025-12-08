import streamlit as st
from src.database import (
    SessionLocal,
    get_all_companies,
    create_product,
)

st.set_page_config(page_title="Add Product - Lekhak AI", layout="wide")

st.title("Add New Product/Service")
st.markdown("*Add products or services to your companies*")

db = SessionLocal()
companies = get_all_companies(db)
db.close()

if not companies:
    st.warning("No companies found. Please add a company first.")
    st.info("Use the 'Add Company' page from the sidebar to create your first company.")
    st.stop()

st.markdown("---")

company_options = {f"{c.name} ({c.industry})": c.id for c in companies}

with st.form("add_product_form"):
    st.subheader("Add New Product/Service")

    selected_company = st.selectbox("Select Company *", list(company_options.keys()))

    name = st.text_input(
        "Product/Service Name *", placeholder="e.g., Cloud Storage Pro, Marketing Suite"
    )

    description = st.text_area(
        "Description *",
        height=100,
        placeholder="Describe the product/service, its purpose, and target audience...",
    )

    key_features = st.text_area(
        "Key Features *",
        height=100,
        placeholder="List the main features and benefits (one per line or comma-separated)...",
    )

    submitted = st.form_submit_button(
        "Add Product/Service", type="primary", use_container_width=True
    )

    if submitted:
        if not all([name.strip(), description.strip(), key_features.strip()]):
            st.error("Please fill in all required fields (marked with *).")
        else:
            try:
                company_id = company_options[selected_company]
                db = SessionLocal()
                create_product(
                    db,
                    company_id=company_id,
                    name=name.strip(),
                    description=description.strip(),
                    key_features=key_features.strip(),
                )
                db.close()
                st.success(
                    f"Product '{name}' added successfully to {selected_company}!"
                )
            except Exception as e:
                st.error(f"❌ Error adding product: {e}")

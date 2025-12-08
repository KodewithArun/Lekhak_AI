import streamlit as st
import asyncio

from src.services.lekhak_service import async_generate_content
from src.database import (
    SessionLocal,
    init_db,
    get_all_companies,
    get_company_by_id,
    get_products_by_company,
    save_conversation,
)

try:
    init_db()
except Exception as e:
    st.error(f"Database initialization error: {e}")

st.set_page_config(page_title="Lekhak AI - Content Generator", layout="wide")

if "user_id" not in st.session_state:
    st.session_state["user_id"] = "streamlit_user"

db = SessionLocal()
try:
    companies = get_all_companies(db)
    tables_exist = True
except Exception:
    tables_exist = False
finally:
    db.close()

if not tables_exist:
    st.title("Welcome to Lekhak AI")
    st.markdown("### First Time Setup Required")
    st.info(
        "The database tables need to be created. Click the button below to initialize."
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Initialize Database", type="primary", use_container_width=True):
            with st.spinner("Creating database tables..."):
                try:
                    from src.database import Base, engine

                    Base.metadata.create_all(bind=engine)
                    st.success("Database initialized successfully!")
                    st.info("Please refresh the page to continue.")
                    st.stop()
                except Exception as e:
                    st.error(f"Error initializing database: {e}")
                    st.stop()
    st.stop()


async def main():
    st.title("Lekhak AI — Content Generator")
    st.markdown("*Generate professional content for your company's marketing needs*")

    db = SessionLocal()
    companies = get_all_companies(db)
    db.close()

    if not companies:
        st.warning(
            "No companies found. Please add a company first using the 'Add Company' page from the sidebar."
        )
        st.stop()

    company_options = {f"{c.name} ({c.industry})": c.id for c in companies}
    selected_company_name = st.selectbox("Select Company", list(company_options.keys()))
    selected_company_id = company_options[selected_company_name]

    db = SessionLocal()
    company = get_company_by_id(db, selected_company_id)
    products = get_products_by_company(db, selected_company_id)
    db.close()

    product_options = {"-- Select Product/Service --": None}
    for p in products:
        product_options[f"{p.name}"] = p.id

    selected_product_name = st.selectbox(
        "Select Product/Service (Optional)", list(product_options.keys())
    )
    selected_product_id = product_options[selected_product_name]

    st.markdown("---")

    prompt = st.text_area(
        "What content would you like to create?",
        height=150,
        placeholder="Example: Create a LinkedIn post about our new product launch...",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        generate_btn = st.button(
            "Generate Content", type="primary", use_container_width=True
        )

    if generate_btn:
        if not prompt.strip():
            st.warning("Please enter a content request.")
            st.stop()

        with st.spinner("AI agents are creating your content..."):
            try:
                result = await async_generate_content(
                    prompt,
                    st.session_state["user_id"],
                    company_id=selected_company_id,
                    product_id=selected_product_id,
                )

                save_conversation(
                    company_id=selected_company_id,
                    user_query=prompt,
                    generated_content=result,
                    product_id=selected_product_id,
                )

                st.success("Content generated successfully!")
                st.markdown("---")
                st.markdown(result)
            except Exception as e:
                st.error(f"Error generating content: {e}")


if __name__ == "__main__":
    asyncio.run(main())

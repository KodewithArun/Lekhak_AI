import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")


# Helper functions
def get_companies():
    try:
        response = requests.get(f"{API_BASE_URL}/companies/")
        if response.status_code == 200:
            return response.json().get("companies", [])
        return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


def create_company(name, industry, description):
    try:
        response = requests.post(
            f"{API_BASE_URL}/companies/",
            json={"name": name, "industry": industry, "description": description},
        )
        if response.status_code == 200:
            return response.json()
        st.error(f"Error: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def get_products_by_company(company_id):
    try:
        response = requests.get(f"{API_BASE_URL}/products/company/{company_id}")
        if response.status_code == 200:
            return response.json().get("products", [])
        return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


def create_product(name, description, company_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/products/",
            json={"name": name, "description": description, "company_id": company_id},
        )
        if response.status_code == 200:
            return response.json()
        st.error(f"Error: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def get_conversations():
    try:
        response = requests.get(f"{API_BASE_URL}/conversations/")
        if response.status_code == 200:
            return response.json().get("conversations", [])
        return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


def generate_content(prompt, company_id=None, product_id=None):
    try:
        payload = {"prompt": prompt, "user_id": "streamlit_user"}
        if company_id:
            payload["company_id"] = company_id
        if product_id:
            payload["product_id"] = product_id

        response = requests.post(f"{API_BASE_URL}/content/generated/", json=payload)
        if response.status_code == 200:
            return response.json()
        st.error(f"Error: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# Page config
st.set_page_config(page_title="Lekhak AI", layout="centered")

# Title
st.title("Lekhak AI")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Generate Content", "Create Company", "Create Product", "Chat History"],
)

#  GENERATE CONTENT PAGE
if page == "Generate Content":

    companies = get_companies()

    if not companies:
        st.warning("No companies available. Please create a company first.")
    else:
        # Company selection
        company_options = {c["name"]: c["id"] for c in companies}
        selected_company_name = st.selectbox(
            "Select Company", list(company_options.keys())
        )
        selected_company_id = company_options[selected_company_name]

        # Product selection (auto-filtered by company)
        products = get_products_by_company(selected_company_id)

        if products:
            product_options = {p["name"]: p["id"] for p in products}
            selected_product_name = st.selectbox(
                "Select Product", list(product_options.keys())
            )
            selected_product_id = product_options[selected_product_name]
        else:
            st.info("No products available for this company")
            selected_product_id = None

        # Content request
        user_prompt = st.text_area("Enter your content request", height=150)

        # Generate button
        if st.button("Generate Content", type="primary"):
            if user_prompt:
                with st.spinner("Generating..."):
                    result = generate_content(
                        user_prompt, selected_company_id, selected_product_id
                    )

                    if result:
                        st.success("Content generated!")
                        st.subheader("Generated Content")
                        st.write(result.get("content", "No content returned"))
            else:
                st.error("Please enter a content request")

#  CREATE COMPANY PAGE
elif page == "Create Company":
    st.header("Create Company")

    company_name = st.text_input("Company Name")
    industry = st.text_input("Industry")
    description = st.text_area("Description")

    if st.button("Create Company", type="primary"):
        if company_name:
            result = create_company(company_name, industry, description)
            if result:
                st.success(f"Company '{company_name}' created successfully!")
        else:
            st.error("Please enter a company name")

#  CREATE PRODUCT PAGE
elif page == "Create Product":
    st.header("Create Product")

    companies = get_companies()

    if not companies:
        st.warning("No companies available. Please create a company first.")
    else:
        product_name = st.text_input("Product Name")
        description = st.text_area("Description")

        # Company selection
        company_options = {c["name"]: c["id"] for c in companies}
        selected_company_name = st.selectbox(
            "Select Company", list(company_options.keys())
        )
        selected_company_id = company_options[selected_company_name]

        if st.button("Create Product", type="primary"):
            if product_name:
                result = create_product(product_name, description, selected_company_id)
                if result:
                    st.success(f"Product '{product_name}' created successfully!")
            else:
                st.error("Please enter a product name")

#  CHAT HISTORY PAGE
elif page == "Chat History":
    st.header("Chat History")

    conversations = get_conversations()

    if conversations:
        for conv in conversations:
            with st.expander(
                f"Conversation {conv['id']} - {conv.get('created_at', 'N/A')}"
            ):
                st.write(f"**User Query:** {conv.get('user_query', 'N/A')}")
                st.write(
                    f"**Generated Content:** {conv.get('generated_content', 'N/A')}"
                )
                st.write(f"**Company ID:** {conv.get('company_id', 'N/A')}")
                st.write(f"**Product ID:** {conv.get('product_id', 'N/A')}")
    else:
        st.info("No chat history available")

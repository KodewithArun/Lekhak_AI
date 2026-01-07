import streamlit as st
import requests
import os
import uuid
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

st.set_page_config(layout="wide", page_title="Lekhak AI")


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


def get_frameworks():
    try:
        response = requests.get(f"{API_BASE_URL}/frameworks/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


def create_company(name, industry, description, url):
    try:
        response = requests.post(
            f"{API_BASE_URL}/companies/",
            json={
                "name": name,
                "industry": industry,
                "description": description,
                "url": url,
            },
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


def create_product(name, description, url, company_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/products/",
            json={
                "name": name,
                "description": description,
                "url": url,
                "company_id": company_id,
            },
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
        user_id = st.session_state.get("user_id")
        params = {"user_id": user_id} if user_id else {}
        response = requests.get(f"{API_BASE_URL}/conversations/", params=params)
        if response.status_code == 200:
            return response.json().get("conversations", [])
        return []
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []


def generate_content(
    prompt, company_id=None, product_id=None, framework_id=None, tone=None
):
    try:
        # Use unique user_id from session state
        user_id = st.session_state.get("user_id", "streamlit_user")

        # Generate a unique session_id for every single task to ensure isolation.
        task_session_id = f"task_{uuid.uuid4().hex[:8]}"

        payload = {"prompt": prompt, "user_id": user_id, "session_id": task_session_id}
        if company_id:
            payload["company_id"] = company_id
        if product_id:
            payload["product_id"] = product_id
        if framework_id:
            payload["framework_id"] = framework_id
        if tone:
            payload["tone"] = tone
        response = requests.post(f"{API_BASE_URL}/content/generated/", json=payload)
        if response.status_code == 200:
            return response.json()
        st.error(f"Error: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# Page config is handled at the top


# Initialize User Session
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())


# Title
st.title("Lekhak AI")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Generate Content",
        "Create Company",
        "Create Product",
        "Framework Library",
        "Chat History",
    ],
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

        # Framework selection
        frameworks = get_frameworks()
        selected_framework_id = None
        if frameworks:
            framework_options = {f["name"]: f["id"] for f in frameworks}
            framework_names = list(framework_options.keys())

            # Find index of "General" to set as default
            try:
                default_index = framework_names.index("General")
            except ValueError:
                default_index = 0

            selected_framework_name = st.selectbox(
                "Select Framework", framework_names, index=default_index
            )

            # Find the full object just to get ID
            selected_fw = next(
                (f for f in frameworks if f["name"] == selected_framework_name), None
            )
            if selected_fw:
                selected_framework_id = selected_fw["id"]
                # Minimal info (optional, or remove entirely if "separate navigation" means strictly separate)
                # st.caption(selected_fw.get('description', ''))

        # select the tone of voice
        tone = st.selectbox(
            "Select Tone of Voice",
            [
                "Professional",
                "Casual",
                "Conversational",
                "Friendly",
                "Formal",
                "Authoritative",
                "Inspirational",
                "Educational",
                "Emotional",
                "Storytelling",
            ],
        )

        # Content request
        user_prompt = st.text_area("Enter your content request", height=150)

        # Generate button
        if st.button("Generate Content", type="primary"):
            if user_prompt:
                with st.spinner("Generating..."):
                    result = generate_content(
                        prompt=user_prompt,
                        company_id=selected_company_id,
                        product_id=selected_product_id,
                        framework_id=selected_framework_id,
                        tone=tone,
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
    url = st.text_input("Website URL")

    if st.button("Create Company", type="primary"):
        if company_name:
            result = create_company(company_name, industry, description, url)
            if result:
                st.success(f"Company '{company_name}' created successfully!")
        else:
            st.error("Please enter a company name")

#  CREATE PRODUCT PAGE
elif page == "Create Product":
    st.header("Create Product")
    # ... (rest of Product Logic) ...

    companies = get_companies()

    if not companies:
        st.warning("No companies available. Please create a company first.")
    else:
        product_name = st.text_input("Product Name")
        description = st.text_area("Description")
        url = st.text_input("Product URL")

        # Company selection
        company_options = {c["name"]: c["id"] for c in companies}
        selected_company_name = st.selectbox(
            "Select Company", list(company_options.keys())
        )
        selected_company_id = company_options[selected_company_name]

        if st.button("Create Product", type="primary"):
            if product_name:
                result = create_product(
                    product_name, description, url, selected_company_id
                )
                if result:
                    st.success(f"Product '{product_name}' created successfully!")
            else:
                st.error("Please enter a product name")

#  FRAMEWORK LIBRARY PAGE
elif page == "Framework Library":
    st.header("Framework Reference Library")
    st.markdown("Explore our professional writing methodologies.")

    frameworks = get_frameworks()
    if frameworks:
        # 1. Framework Selection
        fw_options = {f["name"]: f for f in frameworks}
        selected_fw_name = st.selectbox(
            "Select Framework to View:", list(fw_options.keys())
        )

        fw = fw_options[selected_fw_name]

        # 2. Framework Instructions (Unified)
        st.markdown("##### Framework Guidelines")
        with st.container(border=True):
            st.markdown(
                fw.get("instruction", "No instructions available.").replace("\\n", "\n")
            )

    else:
        st.warning("Library is empty.")

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

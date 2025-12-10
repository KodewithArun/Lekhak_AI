import streamlit as st
import requests

# Configuration
API_BASE_URL = "http://localhost:8000/api"


# Helper functions for API calls
def get_companies():
    try:
        response = requests.get(f"{API_BASE_URL}/companies/")
        if response.status_code == 200:
            return response.json().get("companies", [])
        return []
    except Exception as e:
        st.error(f"Error fetching companies: {str(e)}")
        return []


def create_company(name, industry, description):
    try:
        response = requests.post(
            f"{API_BASE_URL}/companies/",
            json={"name": name, "industry": industry, "description": description},
        )
        if response.status_code == 200:
            return response.json()
        st.error(f"Error creating company: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error creating company: {str(e)}")
        return None


def get_products():
    try:
        response = requests.get(f"{API_BASE_URL}/products/")
        if response.status_code == 200:
            return response.json().get("products", [])
        return []
    except Exception as e:
        st.error(f"Error fetching products: {str(e)}")
        return []


def create_product(name, description, company_id):
    try:
        response = requests.post(
            f"{API_BASE_URL}/products/",
            json={"name": name, "description": description, "company_id": company_id},
        )
        if response.status_code == 200:
            return response.json()
        st.error(f"Error creating product: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error creating product: {str(e)}")
        return None


def get_products_by_company(company_id):
    try:
        response = requests.get(f"{API_BASE_URL}/products/company/{company_id}")
        if response.status_code == 200:
            return response.json().get("products", [])
        return []
    except Exception as e:
        st.error(f"Error fetching products for company: {str(e)}")
        return []


def get_conversations():
    try:
        response = requests.get(f"{API_BASE_URL}/conversations/")
        if response.status_code == 200:
            return response.json().get("conversations", [])
        return []
    except Exception as e:
        st.error(f"Error fetching conversations: {str(e)}")
        return []


def generate_content(prompt, company_id=None, product_id=None):
    try:
        payload = {"prompt": prompt, "user_id": "streamlit_user"}
        if company_id:
            payload["company_id"] = company_id
        if product_id:
            payload["product_id"] = product_id

        response = requests.post(
            f"{API_BASE_URL}/content/generated/",
            json=payload,
        )
        if response.status_code == 200:
            return response.json()
        st.error(f"Error generating content: {response.text}")
        return None
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None


# Initialize session state
if "companies" not in st.session_state:
    st.session_state.companies = get_companies()
if "products" not in st.session_state:
    st.session_state.products = get_products()
if "conversations" not in st.session_state:
    st.session_state.conversations = get_conversations()

# Main app
st.set_page_config(page_title="Lekhak AI", layout="wide")
st.title("Lekhak AI Content Generation Platform")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to", ["Content Generation", "Companies", "Products", "Conversations"]
)

# Content Generation Page
if page == "Content Generation":
    st.header("Generate Content with Lekhak AI")

    # Form for content generation
    with st.form("content_generation_form"):
        st.subheader("Generate New Content")

        # Company selection
        companies = st.session_state.companies
        selected_company_id = None
        selected_product_id = None

        if companies:
            company_options = {c["name"]: c["id"] for c in companies}
            selected_company_name = st.selectbox(
                "Select Company (optional)", ["None"] + list(company_options.keys())
            )
            selected_company_id = (
                company_options.get(selected_company_name)
                if selected_company_name != "None"
                else None
            )
        else:
            st.warning("No companies available. Please create a company first.")

        # Product selection - show all products or filter by company
        products = st.session_state.products
        if products:
            # Filter products by selected company if a company is selected
            if selected_company_id:
                filtered_products = [
                    p for p in products if p.get("company_id") == selected_company_id
                ]
                if filtered_products:
                    product_options = {p["name"]: p["id"] for p in filtered_products}
                    selected_product_name = st.selectbox(
                        "Select Product (optional)",
                        ["None"] + list(product_options.keys()),
                    )
                    selected_product_id = (
                        product_options.get(selected_product_name)
                        if selected_product_name != "None"
                        else None
                    )
                else:
                    st.info("No products found for this company")
            else:
                # Show all products if no company is selected
                product_options = {p["name"]: p["id"] for p in products}
                selected_product_name = st.selectbox(
                    "Select Product (optional)",
                    ["None"] + list(product_options.keys()),
                )
                selected_product_id = (
                    product_options.get(selected_product_name)
                    if selected_product_name != "None"
                    else None
                )
        else:
            st.warning("No products available. Please create a product first.")

        # User prompt
        user_prompt = st.text_area("Enter your prompt", height=150)

        # Submit button
        submit_button = st.form_submit_button("Generate Content")

        if submit_button and user_prompt:
            with st.spinner("Generating content..."):
                result = generate_content(
                    prompt=user_prompt,
                    company_id=selected_company_id,
                    product_id=selected_product_id,
                )

                if result:
                    st.success("Content generated successfully!")
                    st.subheader("Generated Content")
                    st.write(result["content"])

                    # Show metadata
                    with st.expander("Content Details"):
                        st.json(
                            {
                                "Company ID": result.get("company_id"),
                                "Product ID": result.get("product_id"),
                                "Generated At": result.get("generated_at"),
                                "Conversation ID": result.get("conversation_id"),
                            }
                        )

                    # Refresh conversations
                    st.session_state.conversations = get_conversations()

# Companies Page
elif page == "Companies":
    st.header("Company Management")

    # Tabs for company operations
    tab1, tab2 = st.tabs(["View Companies", "Create Company"])

    with tab1:
        st.subheader("All Companies")
        companies = st.session_state.companies

        if companies:
            for company in companies:
                with st.expander(
                    f"{company['name']} ({company.get('industry', 'N/A')})"
                ):
                    st.write(f"**ID:** {company['id']}")
                    st.write(f"**Description:** {company.get('description', 'N/A')}")
                    st.write(f"**Created At:** {company.get('created_at', 'N/A')}")

                    # Show products for this company
                    company_products = get_products_by_company(company["id"])
                    if company_products:
                        st.write("**Products:**")
                        for product in company_products:
                            st.write(f"- {product['name']}")
        else:
            st.info("No companies found.")

    with tab2:
        st.subheader("Create New Company")
        with st.form("create_company_form"):
            name = st.text_input("Company Name")
            industry = st.text_input("Industry")
            description = st.text_area("Description")

            submit_button = st.form_submit_button("Create Company")

            if submit_button and name:
                new_company = create_company(name, industry, description)
                if new_company:
                    st.success(f"Company '{name}' created successfully!")
                    st.session_state.companies = get_companies()  # Refresh companies

# Products Page
elif page == "Products":
    st.header("Product Management")

    # Tabs for product operations
    tab1, tab2 = st.tabs(["View Products", "Create Product"])

    with tab1:
        st.subheader("All Products")
        products = st.session_state.products

        if products:
            for product in products:
                with st.expander(f"{product['name']}"):
                    st.write(f"**ID:** {product['id']}")
                    st.write(f"**Company ID:** {product.get('company_id', 'N/A')}")
                    st.write(f"**Description:** {product.get('description', 'N/A')}")
                    st.write(f"**Created At:** {product.get('created_at', 'N/A')}")
        else:
            st.info("No products found.")

    with tab2:
        st.subheader("Create New Product")
        with st.form("create_product_form"):
            name = st.text_input("Product Name")
            description = st.text_area("Description")

            # Company selection
            companies = st.session_state.companies
            if companies:
                company_options = {c["name"]: c["id"] for c in companies}
                selected_company_name = st.selectbox(
                    "Select Company", list(company_options.keys())
                )
                company_id = company_options[selected_company_name]
            else:
                st.error("No companies available. Please create a company first.")
                company_id = None

            submit_button = st.form_submit_button("Create Product")

            if submit_button and name and company_id:
                new_product = create_product(name, description, company_id)
                if new_product:
                    st.success(f"Product '{name}' created successfully!")
                    st.session_state.products = get_products()  # Refresh products

# Conversations Page
elif page == "Conversations":
    st.header("Conversation History")

    conversations = st.session_state.conversations

    if conversations:
        for conversation in conversations:
            with st.expander(f"Conversation {conversation['id']}"):
                st.write(f"**ID:** {conversation['id']}")
                st.write(f"**Company ID:** {conversation.get('company_id', 'N/A')}")
                st.write(f"**Product ID:** {conversation.get('product_id', 'N/A')}")
                st.write(f"**User Query:** {conversation.get('user_query', 'N/A')}")
                st.write(
                    f"**Generated Content:** {conversation.get('generated_content', 'N/A')}"
                )
                st.write(f"**Created At:** {conversation.get('created_at', 'N/A')}")
    else:
        st.info("No conversations found.")

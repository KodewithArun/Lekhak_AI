"""Database package."""

# 1. Engine & Session
from src.database.session import (
    engine,
    SessionLocal,
    Base,
    init_db,
    drop_db,
    get_db,
)

# 2. Models
from src.database.models import Company, Product, Conversation

# 3. CRUD Functions
from src.database.crud import (
    # Company CRUD
    create_company,
    get_company_by_id,
    get_all_companies,
    update_company,
    delete_company,
    # Product CRUD
    create_product,
    get_product_by_id,
    get_products_by_company,
    update_product,
    delete_product,
    # Conversation CRUD
    create_conversation,
    save_conversation,
)

__all__ = [
    # Engine & Session
    "engine",
    "SessionLocal",
    "Base",
    "init_db",
    "drop_db",
    "get_db",
    # Models
    "Company",
    "Product",
    "Conversation",
    # Company CRUD
    "create_company",
    "get_company_by_id",
    "get_all_companies",
    "update_company",
    "delete_company",
    # Product CRUD
    "create_product",
    "get_product_by_id",
    "get_products_by_company",
    "update_product",
    "delete_product",
    # Conversation CRUD
    "create_conversation",
    "save_conversation",
]

from enum import StrEnum


class Role(StrEnum):
    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    CUSTOMER = "customer"
    SUPPORT = "support"
    OPERATIONS = "operations"
    FINANCE = "finance"
    HOTEL_MANAGER = "hotel_manager"

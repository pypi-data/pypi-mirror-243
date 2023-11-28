from enum import Enum
from typing import Dict, Tuple


class WarehouseAsset(Enum):
    """Assets that can be extracted from warehouses"""

    COLUMN = "column"
    COLUMN_LINEAGE = "column_lineage"  # specific to snowflake
    DATABASE = "database"
    EXTERNAL_COLUMN_LINEAGE = "external_column_lineage"
    EXTERNAL_TABLE_LINEAGE = "external_table_lineage"
    GRANT_TO_ROLE = "grant_to_role"
    GRANT_TO_USER = "grant_to_user"
    GROUP = "group"
    QUERY = "query"
    ROLE = "role"
    SCHEMA = "schema"
    TABLE = "table"
    USER = "user"
    VIEW_DDL = "view_ddl"


class WarehouseAssetGroup(Enum):
    """Groups of assets that can be extracted together"""

    CATALOG = "catalog"
    EXTERNAL_LINEAGE = "external_lineage"
    QUERY = "query"
    ROLE = "role"
    SNOWFLAKE_LINEAGE = "snowflake_lineage"
    VIEW_DDL = "view_ddl"


# tuple of supported assets for each group (depends on the technology)
SupportedAssets = Dict[WarehouseAssetGroup, Tuple[WarehouseAsset, ...]]


# shared by all technologies
CATALOG_ASSETS = (
    WarehouseAsset.DATABASE,
    WarehouseAsset.SCHEMA,
    WarehouseAsset.TABLE,
    WarehouseAsset.COLUMN,
)

# shared by technologies supporting queries
QUERIES_ASSETS = (WarehouseAsset.QUERY,)
VIEWS_ASSETS = (WarehouseAsset.VIEW_DDL,)

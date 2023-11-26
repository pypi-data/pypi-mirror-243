from typing import List

from pydantic import Field

from .base_model import BaseModel


class ListDatabricksWarehouses(BaseModel):
    databricks_list_warehouses: List[
        "ListDatabricksWarehousesDatabricksListWarehouses"
    ] = Field(alias="databricksListWarehouses")


class ListDatabricksWarehousesDatabricksListWarehouses(BaseModel):
    name: str
    http_path: str = Field(alias="httpPath")


ListDatabricksWarehouses.model_rebuild()
ListDatabricksWarehousesDatabricksListWarehouses.model_rebuild()

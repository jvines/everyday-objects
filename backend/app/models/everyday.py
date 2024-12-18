from pydantic import BaseModel


class Item(BaseModel):
    
    item: str
    
    class Config:
        from_attributes = True


class ItemAddress(Item):
    
    address: str
    
    class Config:
        from_attributes = True


class Material(BaseModel):
    
    material: str
    type: str
    exporter: str
    co2_kg: float
    diesel_kg: float
    carbon_footprint: float
    hydric_footprint: float
    diesel_consumption: float
    
    class Config:
        from_attributes = True
        

class ItemMaterial(BaseModel):
    
    body_materials: list[str]
    detail_materials: list[str]
    material_ids: list[int]


class MaterialIdList(BaseModel):
    """Class that adds a new item"""
    material_ids: list[int]


class EnvironmentalImpact(BaseModel):
    
    total_co2: float
    total_diesel: float
    total_carbon_footprint: float
    total_hydric_footprint: float
    total_diesel_consumption: float

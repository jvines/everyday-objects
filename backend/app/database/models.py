from . import Base
from sqlalchemy import Column, Integer, String, Boolean, Float


class Item(Base):
    __tablename__ = "item"
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    item = Column(String, nullable=False)


class Material(Base):
    __tablename__ = 'material'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    type = Column(String, nullable=False)
    material = Column(String, nullable=False)
    exporter = Column(String, nullable=False)
    co2_kg = Column(Float, nullable=False, default=0)
    diesel_kg = Column(Float, nullable=False, default=0)
    carbon_footprint = Column(Float, nullable=False, default=0)
    hydric_footprint = Column(Float, nullable=False, default=0)
    diesel_consumption = Column(Float, nullable=False, default=0)


class ItemMaterial(Base):
    __tablename__ = 'item_material'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    object_id = Column(Integer, nullable=False)
    material_id = Column(Integer, nullable=False)
    is_fixed = Column(Boolean, nullable=False, default=False)
    
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException
from .models import Item, Material, ItemMaterial
from . import engine, wait_for_db_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not wait_for_db_connection():
        raise HTTPException(status_code=503, detail="Database not available")
    with Session(engine) as session:
        items = session.scalars(select(Item)).all()
        materials = session.scalars(select(Material)).all()
        if not len(items) and not len(materials):
            from .constants import ITEMS, MATERIALS, ITEM_MATERIALS
            items = [Item(**item) for item in ITEMS]
            materials = [Material(**material) for material in MATERIALS]
            session.add_all(items)
            session.add_all(materials)
            session.commit()
            add_item_materials = []
            for item in ITEM_MATERIALS:
                statement = select(Item).filter_by(item=item)
                item_object = session.scalars(statement).first()
                item_id = item_object.id
                fixed_materials = ITEM_MATERIALS[item]['fixed']
                variable_materials = ITEM_MATERIALS[item]['variable']
                for material in fixed_materials:
                    statement = select(Material).filter_by(material=material)
                    material_object = session.scalars(statement).first()
                    material_id = material_object.id
                    add_item_materials.append(
                        ItemMaterial(**{
                            'object_id': item_id,
                            'material_id': material_id,
                            'is_fixed': True
                        })
                    )
                for material in variable_materials:
                    statement = select(Material).filter_by(material=material)
                    material_object = session.scalars(statement).first()
                    material_id = material_object.id
                    add_item_materials.append(
                        ItemMaterial(**{
                            'object_id': item_id,
                            'material_id': material_id,
                            'is_fixed': False
                        })
                    )
                session.add_all(add_item_materials)
                session.commit()
            
    yield
    
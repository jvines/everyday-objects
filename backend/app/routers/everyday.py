from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from ..database import get_db, models
from ..models.everyday import *


router = APIRouter(
    prefix='/everyday'
)


@router.post('/impact')
def calculate_environmental_impact(material_list: MaterialIdList,
                      db: Session = Depends(get_db)) -> EnvironmentalImpact:
    total_co2, total_diesel = 0, 0
    total_carbon_footprint, total_hydric_footprint = 0, 0
    total_diesel_consumption = 0
    for material_id in material_list.material_ids:
        material = (
            db
            .query(models.Material)
            .filter(models.Material.id == material_id)
        ).first()
        total_co2 += material.co2_kg
        total_diesel += material.diesel_kg
        total_carbon_footprint += material.carbon_footprint
        total_hydric_footprint += material.hydric_footprint
        total_diesel_consumption += material.diesel_consumption
    return EnvironmentalImpact(
        total_co2=total_co2,
        total_diesel=total_diesel,
        total_carbon_footprint=total_carbon_footprint,
        total_hydric_footprint=total_hydric_footprint,
        total_diesel_consumption=total_diesel_consumption
    )
        

@router.get('/object/{object_id}')
def get_object_materials(object_id: int, db: Session = Depends(get_db)) \
        -> ItemMaterial:
    item_materials = (
        db
        .query(models.ItemMaterial)
        .filter(models.ItemMaterial.object_id == object_id)
    ).all()
    body_materials = []
    detail_materials = []
    material_ids = []
    for item_material in item_materials:
        material = (
            db
            .query(models.Material)
            .filter(models.Material.id == item_material.material_id)
            .first()
            .material
        )
        if item_material.is_fixed:
            body_materials.append(material)
            
        else:
            detail_materials.append(material)
            
        material_ids.append(item_material.material_id)
    
    return ItemMaterial(
        body_materials=body_materials,
        detail_materials=detail_materials,
        material_ids=material_ids,
    )


@router.get('/object')
async def get_objects(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return items


@router.get('/material')
async def get_materials(db: Session = Depends(get_db)):
    materials = db.query(models.Material).all()
    return materials


@router.post(
    '/object',
    status_code=status.HTTP_201_CREATED,
    response_model=Item | ItemAddress
)
async def add_object(item: ItemAddress | Item, db: Session = Depends(get_db)):
    
    new_item = models.Item(**item.dict())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return new_item


@router.post(
    '/material',
    status_code=status.HTTP_201_CREATED,
    response_model=Material
)
async def add_material(material: Material, db: Session = Depends(get_db)):
    
    new_material = models.Material(**material.dict())
    db.add(new_material)
    db.commit()
    db.refresh(new_material)
    
    return new_material


@router.post(
    '/material/bulk',
    status_code=status.HTTP_201_CREATED,
    response_model=list[Material]
)
async def bulk_add_material(materials: list[Material],
                            db: Session = Depends(get_db)):
    response = []
    for material in materials:
        new_material = models.Material(**material.dict())
        response.append(new_material)
    db.add_all(response)
    db.commit()
    
    return response


@router.post(
    '/object/bulk',
    status_code=status.HTTP_201_CREATED,
    response_model=list[Item]
)
async def bulk_add_item(items: list[Item],
                        db: Session = Depends(get_db)):
    response = []
    for item in items:
        new_item = models.Item(**item.dict())
        response.append(new_item)
    db.add_all(response)
    db.commit()
    
    return response


@router.post(
    '/object_material',
    status_code=status.HTTP_201_CREATED,
    response_model=ItemMaterial
)
async def add_item_material(item_material: ItemMaterial,
                            db: Session = Depends(get_db)):
    
    new_item_material = models.ItemMaterial(**item_material.dict())
    db.add(new_item_material)
    db.commit()
    db.refresh(new_item_material)
    
    return new_item_material
    
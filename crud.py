from sqlalchemy.orm import Session
from typing import List, Optional
import database
import schemas

# Category CRUD operations
def get_categories(db: Session, token: str, skip: int = 0, limit: int = 100):
    return db.query(database.Category).filter(database.Category.token == token).offset(skip).limit(limit).all()

def get_category(db: Session, category_id: int, token: str):
    return db.query(database.Category).filter(database.Category.id == category_id, database.Category.token == token).first()

def create_category(db: Session, category: schemas.CategoryCreate, token: str):
    db_category = database.Category(**category.dict(), token=token)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate, token: str):
    db_category = get_category(db, category_id, token)
    if db_category:
        update_data = category.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_category, field, value)
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, token: str):
    db_category = get_category(db, category_id, token)
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category

# Tag CRUD operations
def get_tags(db: Session, token: str, skip: int = 0, limit: int = 100):
    return db.query(database.Tag).filter(database.Tag.token == token).offset(skip).limit(limit).all()

def get_tag(db: Session, tag_id: int, token: str):
    return db.query(database.Tag).filter(database.Tag.id == tag_id, database.Tag.token == token).first()

def create_tag(db: Session, tag: schemas.TagCreate, token: str):
    db_tag = database.Tag(**tag.dict(), token=token)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

def update_tag(db: Session, tag_id: int, tag: schemas.TagUpdate, token: str):
    db_tag = get_tag(db, tag_id, token)
    if db_tag:
        update_data = tag.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_tag, field, value)
        db.commit()
        db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int, token: str):
    db_tag = get_tag(db, tag_id, token)
    if db_tag:
        db.delete(db_tag)
        db.commit()
    return db_tag

# Product CRUD operations
def get_products(db: Session, token: str, skip: int = 0, limit: int = 100):
    return db.query(database.Product).filter(database.Product.token == token).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: int, token: str):
    return db.query(database.Product).filter(database.Product.id == product_id, database.Product.token == token).first()

def create_product(db: Session, product: schemas.ProductCreate, token: str):
    product_data = product.dict()
    tag_ids = product_data.pop('tag_ids', [])
    
    db_product = database.Product(**product_data, token=token)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Add tags
    if tag_ids:
        tags = db.query(database.Tag).filter(database.Tag.id.in_(tag_ids), database.Tag.token == token).all()
        db_product.tags = tags
        db.commit()
        db.refresh(db_product)
    
    return db_product

def update_product(db: Session, product_id: int, product: schemas.ProductUpdate, token: str):
    db_product = get_product(db, product_id, token)
    if db_product:
        update_data = product.dict(exclude_unset=True)
        tag_ids = update_data.pop('tag_ids', None)
        
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        # Update tags if provided
        if tag_ids is not None:
            tags = db.query(database.Tag).filter(database.Tag.id.in_(tag_ids), database.Tag.token == token).all()
            db_product.tags = tags
        
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int, token: str):
    db_product = get_product(db, product_id, token)
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

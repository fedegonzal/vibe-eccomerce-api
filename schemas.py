from pydantic import BaseModel
from typing import List, Optional

# Category schemas
class CategoryBase(BaseModel):
    title: str
    description: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    title: Optional[str] = None
    description: Optional[str] = None

class Category(CategoryBase):
    id: int
    picture: Optional[str] = None
    
    class Config:
        from_attributes = True

# Tag schemas
class TagBase(BaseModel):
    title: str

class TagCreate(TagBase):
    pass

class TagUpdate(TagBase):
    title: Optional[str] = None

class Tag(TagBase):
    id: int
    
    class Config:
        from_attributes = True

# Product schemas
class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    category_id: int

class ProductCreate(ProductBase):
    tag_ids: Optional[List[int]] = []

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None

class Product(ProductBase):
    id: int
    pictures: Optional[List[str]] = []
    category: Optional[Category] = None
    tags: Optional[List[Tag]] = []
    
    class Config:
        from_attributes = True

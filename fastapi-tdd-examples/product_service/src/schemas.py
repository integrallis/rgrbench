"""Pydantic schemas for Product Service"""

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    quantity: int


class ProductUpdate(BaseModel):
    name: str
    quantity: int


class ProductResponse(BaseModel):
    id: int
    name: str
    quantity: int
    version: int

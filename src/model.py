from typing import Optional
from sqlmodel import SQLModel, Field
from src.config import ENGINE


class Good(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # clé primaire
    title: Optional[str] = None
    price: Optional[str] = None
    market_price: Optional[str] = None
    image: Optional[str] = None
    product_link: Optional[str] = None
    total_sold: Optional[str] = None


class Processes(SQLModel, table=True):
    process_id: Optional[str] = Field(default=None, primary_key=True, max_length=64)
    status: str


# Create all tables of the database
def create_db_and_tables():
    SQLModel.metadata.create_all(ENGINE)

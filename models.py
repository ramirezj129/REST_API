from sqlalchemy.orm import declarative_base
from database import engine
from sqlalchemy import String,Boolean,Integer,Column,Text

Base = declarative_base()

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False,unique=True)
    description = Column(Text)
    price = Column(Integer,nullable=False)
    sold = Column(Boolean,default=False)

Base.metadata.create_all(engine)

from fastapi import FastAPI,status,HTTPException
from models import Item
from database import session
from pydantic import BaseModel
from typing import Optional,List
import models

app = FastAPI()

class Item(BaseModel):
    id:int
    name:str
    description:str
    price:int
    sold:bool

    class Config:
        orm_mode=True

@app.post("/new_item/",response_model=Item, status_code=status.HTTP_201_CREATED)
def create_game(item:Item):
    session_item= session.query(models.Item).filter(models.Item.name==item.name).first()
    
    if session_item is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE)

    
    new_game = models.Item(name=item.name,description=item.description,price=item.price, sold = item.sold)
    session.add(new_game)
    session.commit()
    return new_game

@app.get("/",response_model=List[Item], status_code=status.HTTP_200_OK)
def get_all_games():
    game_items = session.query(models.Item).all()
    return game_items

@app.get("/item/{items_id}",response_model=Item, status_code=status.HTTP_200_OK)
def get_game(item_id:int):
    game_query = session.query(models.Item).filter(models.Item.id==item_id).first()
    return game_query

@app.put("/update/{items_id}", response_model=Item,status_code=status.HTTP_202_ACCEPTED)
def update_game(items_id:int, item:Item):
    game_update = session.query(models.Item).filter(models.Item.id==items_id).first()
    game_update.id = item.id
    game_update.name = item.name
    game_update.description = item.description
    game_update.price = item.price
    game_update.sold = item.sold

    session.commit()
    return game_update

@app.delete("/delete/{items_id}", response_model=Item,status_code=status.HTTP_202_ACCEPTED)
def delete_game(items_id: int):
    delete_game = session.query(models.Item).filter(models.Item.id==items_id).first()
    
    if delete_game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    session.delete(delete_game)
    session.commit()

    return delete_game
   

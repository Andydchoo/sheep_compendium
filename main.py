from fastapi import FastAPI, HTTPException, status
from models.db import db
from models.models import Sheep
from typing import List

app = FastAPI()

@app.get("/sheep/{id}", response_model=Sheep)
def read_sheep(id: int):
    sheep = db.get_sheep(id)
    if sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return sheep

@app.post("/sheep", response_model=Sheep, status_code=status.HTTP_201_CREATED)
def add_sheep(sheep: Sheep):
    if sheep.id in db.data:
        raise HTTPException(status_code=400, detail="Sheep with this ID already exists")
    db.data[sheep.id] = sheep
    return sheep

@app.get("/sheep", response_model=List[Sheep])
def read_all_sheep():
    return db.get_all_sheep()

@app.put("/sheep/{id}", response_model=Sheep)
def update_sheep(id: int, sheep: Sheep):
    updated_sheep = db.update_sheep(id, sheep)
    if updated_sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return updated_sheep

@app.delete("/sheep/{id}")
def delete_sheep(id: int):
    deleted_sheep = db.delete_sheep(id)
    if deleted_sheep is None:
        raise HTTPException(status_code=404, detail="Sheep not found")
    return {"message": "Sheep deleted successfully"}
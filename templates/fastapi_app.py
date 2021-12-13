import os
import fastapi_models as models
from fastapi_models import Cities
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi_database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy import and_
import requests
from pydantic import BaseModel
from starlette.responses import RedirectResponse
from typing import Generator, Optional, Iterable, Dict
import json

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="")

#base model data structure
class CityRequest(BaseModel):
    name: str
    timezone: str

#base model data structure
class CityUpdate(BaseModel):
    name: str
    timezone: str
    newname: str
    newtimezone: str

#connect to database
def get_db() -> Generator:
    try:
        db=SessionLocal()
        yield db
    finally:
        db.close()

@app.get('/')
def home(request: Request, timezone: Optional[str]=None, db: Session = Depends(get_db)) -> object:
    '''
    show all cities on home route
    '''
    
    city = db.query(Cities)

    if timezone:
        city = city.filter(Cities.timezone == timezone)

    city = city.all()

    return templates.TemplateResponse(
        "fastapi_home.html", {
        "request": request,
        "city": city,
        "timezone": timezone
    })

def fetch_time(id: int) -> None:
    '''
    fetch time in that city
    '''
    db = SessionLocal()
    
    #query database on city ID
    city = db.query(Cities).filter(Cities.id == id).first()

    r = requests.get(f'http://worldtimeapi.org/api/timezone/{city.timezone}')    
    current_time = r.json()['datetime']

    city.time = current_time

    #add in time
    db.add(city)
    db.commit()

@app.post('/cities')
async def create_city(city_request: CityRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Dict[str,str]:
    '''
    creates city and stores in database
    dependency: database connection
    runs background task asynchronously
    '''
    city = Cities()
    city.name = city_request.name
    city.timezone = city_request.timezone
    db.add(city)
    db.commit()

    #fetch time in background
    background_tasks.add_task(fetch_time, city.id)

    return {
        "code": "success",
        "message": "city added to database"
    }

@app.get('/cities')
def get_cities(db: Session = Depends(get_db)) -> Iterable[str]:

    cities = db.query(Cities).all()

    json_cities = jsonable_encoder(cities)

    return {
        json.dumps(json_cities)
    }

@app.delete('/cities')
def delete_city(city_request: CityRequest, db: Session = Depends(get_db)) -> Dict[str,str]:
    '''
    deletes city by finding first city and timezone with that name
    '''
    
    name = city_request.name
    timezone = city_request.timezone

    city = db.query(Cities).filter(and_(Cities.name == name, Cities.timezone == timezone)).first()
    db.delete(city)
    db.commit()

    return {
        "code":"success",
        "message":"city deleted from database"
        }

@app.post('/update')
def update_city(city_update: CityUpdate, db: Session = Depends(get_db)) -> Dict[str,str]:
    '''
    updates timezone by finding first city with that name
    '''

    name = city_update.name
    timezone = city_update.timezone

    newname = city_update.newname
    newzone = city_update.newtimezone

    city = db.query(Cities).filter(and_(Cities.name == name, Cities.timezone == timezone)).first()

    city.name = newname

    city.timezone = newzone

    db.commit()

    return {
        "code":"success",
        "message":"city updated in database"
        }

if __name__ == "__main__":
    print("Check http://127.0.0.1:8000/redoc OR \n http://127.0.0.1:8000/docs to play around!")
    os.system("uvicorn fastapi_app:app --reload")
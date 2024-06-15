from datetime import datetime
import re
from fastapi import Body, FastAPI, Depends, File, Request, Response
from typing import Union, Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from db import service
from db.models import Meet, Model, Person
from db.base import init_models, get_session
from uuid import uuid4
import typer
import base64
import asyncio
app = FastAPI()

# db resetting
cli = typer.Typer()
@cli.command()
def db_init_models():
    asyncio.run(init_models())
    print("Done")
if __name__ == "__main__":
    cli()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/meet/new")
async def post_meet(names:Annotated[dict[str, int], Body(embed=True)], photo:Annotated[Union[str, None], Body(embed=True)], sess: Union[AsyncSession, None] = Depends(get_session)):
    time = datetime.now()
    with open(f"images/{'_'.join(names.keys())}_{time.strftime('%Y-%m-%d-%H-%M-%S')}.jpg", 'wb') as file:
        file.write(base64.decodebytes(bytes(photo, 'utf-8')))
    await service.add_meet(sess, names, f"{'_'.join(names)}_{time.strftime('%Y-%m-%d-%H-%M-%S')}.jpg")

@app.get("/meet/all")
async def get_meet_all(limit: int = 10, offset: int = 0, sess: Union[AsyncSession, None] = Depends(get_session)):
    if limit == -1:
        limit = None
    meets = await service.get_all_meets(limit, offset, sess)
    for meet in meets:
        meet.photo = base64.b64encode(open("images/"+meet.photo, "rb").read()).decode() 
    return meets

@app.get("/meet/unwatched")
async def get_meet_unwatched(sess: Union[AsyncSession, None] = Depends(get_session)):
    meets = await service.get_unwatched_meets(sess)
    for meet in meets:
        meet.photo = base64.b64encode(open("images/"+meet.photo, "rb").read()).decode() 
    return meets

@app.get("/meet/{id}")
async def get_meet_by_id(id: int,response_class:Response, sess: Union[AsyncSession, None] = Depends(get_session)):
    meet = await service.get_meet_by_id(id, sess)
    print(meet)
    if meet is not None:
        meet.photo = base64.b64encode(open("images/"+meet.photo, "rb").read()).decode() 
        return meet
    else:
        response_class.status_code = 404
        return "Not found"

@app.get("/meet/person/{id}")
async def get_meet_by_person_id(id: int, sess: Union[AsyncSession, None] = Depends(get_session)):
    meets = await service.get_meets_by_person_id(id, sess)
    meet = meets[0]
    meet.photo = base64.b64encode(open("images/"+meet.photo, "rb").read()).decode() 
    return meet

@app.get("/person/all")
async def get_all_persons(response_class:Response,limit: int = 10, offset: int = 0,  sess: Union[AsyncSession, None] = Depends(get_session)):
    if limit == -1:
        limit = None
    persons = await service.get_all_persons(limit, offset, sess)
    # print(persons)
    if len(persons) == 0:
        response_class.status_code = 404
        return "Not found"
    return persons

# @app.get("/person/{name}")
# async def get_person_by_name(name: str, sess: Union[AsyncSession, None] = Depends(get_session)):
#     person = await service.get_person_by_name(name, sess)
#     return person


@app.get("/person/{id}")
async def get_person_by_id(id: int,response_class:Response, sess: Union[AsyncSession, None] = Depends(get_session)):
    person = await service.get_person_by_id(id, sess)
    if person is None:
        response_class.status_code = 404
        return "Not found"
    return person

@app.get("/model")
async def get_model(sess: Union[AsyncSession, None] = Depends(get_session)):
    models: list[Model] = await service.get_models(sess)
    for model in models:
        model.image_path = base64.b64encode(open(model.image_path, "rb").read()).decode()
    return models

@app.post("/model")
async def post_model(name: str, photo :Annotated[str, Body(embed=True)], sess: Union[AsyncSession, None] = Depends(get_session)):
    salt = uuid4()
    with open(f"models/{name}_{salt}.jpg", 'wb') as file:
        file.write(base64.decodebytes(bytes(photo, 'utf-8')))

    await service.add_model(sess,name, f"models/{name}_{salt}.jpg")
    
    return {"message": "Done"}
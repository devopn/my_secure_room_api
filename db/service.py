from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from .models import *
from typing import Union

# async def get_questions(session: AsyncSession, count: int, mode: int, type: Union[int, None]) -> list[Question]:

# 	result = await session.execute(select(Question).where(Question.type == type).order_by(func.random()).limit(count))
	
# 	return result.scalars().all()

async def get_unwatched_meets(session: AsyncSession) -> list[Meet]:
	result = await session.execute(select(Meet).where(Meet.watched == False).order_by(Meet.datetime))
	u = update(Meet).where(Meet.watched == False).values(watched = True)
	await session.execute(u)
	await session.commit()
	return result.scalars().all()

async def get_all_meets(limit, offset, session: AsyncSession) -> list[Meet]:
	result = await session.execute(select(Meet).order_by(Meet.datetime.desc()).offset(offset).limit(limit))
	return result.scalars().all()

async def add_meet(session: AsyncSession, names: dict[str, int], image:str):
	meet = Meet()
	meet.names = names
	meet.persons_ids = []
	for i in names.keys():
		person = await session.execute(select(Person).where(Person.name == i))
		person = person.scalars().first()
		if person is None:
			person = Person()
			person.name = i
			person.display_name = i
			session.add(person)
			await session.commit()
		meet.persons_ids.append(person.id)
	meet.photo = image

	session.add(meet)
	await session.commit()

async def get_meet_by_id(id: int, session: AsyncSession) -> Meet:
	res = await session.execute(select(Meet).where(Meet.id == id))
	return res.scalars().first()

async def get_person_by_name(name: str, session: AsyncSession) -> Person:
	res = await session.execute(select(Person).where(Person.name == name))
	return res.scalars().first()

async def get_person_by_id(id: int, session: AsyncSession) -> Person:
	res = await session.execute(select(Person).where(Person.id == id))
	return res.scalars().first()

async def get_all_persons(limit, offset, session: AsyncSession) -> list[Person]:
	result = await session.execute(select(Person).order_by(Person.id.desc()).offset(offset).limit(limit))
	return result.scalars().all()

async def get_meets_by_person_id(id: int, session: AsyncSession) -> list[Meet]:	
	result = await session.execute(select(Meet))
	result = result.scalars().all()
	result = [i for i in result if id in i.persons_ids]
	return result
	
async def change_person_name(session: AsyncSession, old_name: str, new_name: str):
	person = await session.execute(select(Person).where(Person.name == old_name))
	person = person.scalars().first()
	person.name = new_name
	await session.commit()

async def add_model(session: AsyncSession, name: str, image_path: str):
	model = Model()
	model.name = name
	model.image_path = image_path
	session.add(model)
	person = Person()
	person.name = name
	session.add(person)
	await session.commit()

async def get_models(session: AsyncSession):
	result = await session.execute(select(Model).where(Model.used == False))
	await session.execute(update(Model).where(Model.used == False).values(used = True))
	await session.commit()
	return result.scalars().all()
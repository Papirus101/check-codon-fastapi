import uvicorn

from fastapi import FastAPI

from db.base import database
from endpoints import users, codon

app = FastAPI(title='Проверка наличия кодонов в ДНК')
app.include_router(users.router, prefix='/user', tags=['users'])
app.include_router(codon.router, prefix='/codon', tags=['codon'])


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, host='0.0.0.0', reload=True)
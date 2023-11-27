import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from axdocsystem.src.db import setup_db, get_uowf
from axdocsystem.src.settings import Settings
from axdocsystem.src.api.registrator import register_all
from axdocsystem.utils.mock_data import create_mock_data
from axdocsystem.utils.utils.one_time_token_manager import OneTimeTokenManager


app = FastAPI()
settings = Settings()  # type: ignore
uowf = get_uowf(settings)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    # await create_mock_data(uowf)
    register_all(
        app=app, 
        uowf=uowf, 
        token_manager=OneTimeTokenManager(token_size=32),
        settings=settings,
    )

    await setup_db(uowf)


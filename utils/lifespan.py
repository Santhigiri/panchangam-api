
from contextlib import asynccontextmanager
import pickle

from fastapi import FastAPI

PANCHANGAM_CACHE = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    global PANCHANGAM_CACHE
    for year in range(2020, 2031):
        file_name = f"data/panchangam_{year}.pkl"
        with open(file_name, "rb") as f:
            PANCHANGAM_CACHE.update(pickle.load(f))

    print("Cache loaded", len(PANCHANGAM_CACHE))
    
    yield

    print("Shutdown")

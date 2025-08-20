from typing import List
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from src import bot
import time
from src.config import API_KEY
from src.database_manager import (
    get_all_goods,
    get_process_status,
)
from src.model import Good, create_db_and_tables

# Dépendance pour vérifier l'API Key
def verify_api_key(api_key: str = Header(...)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

app = FastAPI(title="Temu Scraper", on_startup=[create_db_and_tables])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get-data", dependencies=[Depends(verify_api_key)])
def get_data(background_tasks: BackgroundTasks, url: str, click_number: int):
    # "https://www.temu.com/search_result.html?search_key=birthday%20gift" -- 3
    # Start The Process
    process_time = int(time.time())
    process_id = f"id_{process_time}"

    background_tasks.add_task(bot.main, url, click_number, process_id)
    return {
        "message": "Job started",
        "process": process_id,
    }


@app.get("/get-status", dependencies=[Depends(verify_api_key)])
def check_status(process_id: str) -> dict:
    # Get the process status
    status = get_process_status(process_id)
    if status:
        return {"process_id": process_id, "status": status}
    raise HTTPException(status_code=404, detail="Process not found")


@app.get("/get-goods", response_model=List[Good], dependencies=[Depends(verify_api_key)])
def get_goods():
    return get_all_goods()

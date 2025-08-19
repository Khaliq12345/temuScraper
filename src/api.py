from typing import List
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src import bot
import time
from src.database_manager import (
    get_all_goods,
    get_process_status,
)
from src.model import Good, create_db_and_tables

app = FastAPI(title="Temu Scraper", on_startup=[create_db_and_tables])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/get-data")
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


@app.get("/get-status")
def check_status(process_id: str) -> dict:
    # Get the process status
    status = get_process_status(process_id)
    if status:
        return {"process_id": process_id, "status": status}
    raise HTTPException(status_code=404, detail="Process not found")


@app.get("/get-goods", response_model=List[Good])
def get_goods():
    return get_all_goods()

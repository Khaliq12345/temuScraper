from typing import List
from sqlmodel import Session, select
from src.model import Good, Processes
from contextlib import contextmanager
from src.config import ENGINE


# Get the Database Session
@contextmanager
def get_session():
    session = Session(ENGINE)
    try:
        yield session
    except Exception as e:
        raise ValueError(f"DB error - {e}")
    finally:
        session.close()


# Sauvegarde d'une liste de Good
def save_data(goods: list[Good]):
    with get_session() as session:
        session.add_all(goods)
        session.commit()


# Fonction pour récupérer tous les goods
def get_all_goods() -> List[Good]:
    with get_session() as session:
        stmt = select(Good)
        return list(session.exec(stmt).all())


# To Update the process Status
def update_process_status(
    process_id: str,
    status: str,
):
    with get_session() as session:
        stmt = select(Processes).where(Processes.process_id == process_id)
        process = session.exec(stmt).one_or_none()
        if process:
            # Mise à jour d'un process existant
            process.status = status
        else:
            # Création d'un nouveau process
            process = Processes(
                process_id=process_id,
                status=status,
            )
            session.add(process)
        session.commit()
        session.refresh(process)
        return process


# Retrieve a process status
def get_process_status(process_id: str):
    with get_session() as session:
        stmt = select(Processes).where(Processes.process_id == process_id)
        response = session.exec(stmt).one()
        if response:
            return response.status
    return None

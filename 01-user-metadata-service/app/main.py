import time
import uuid
from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from tenacity import retry, stop_after_attempt, wait_exponential, wait_random
from datetime import datetime

from .db import Base, engine, SessionLocal
from .models import User
from .metrics import TOTAL_REQUESTS, SUCCESS_COUNT, FAILURE_COUNT, REQUEST_LATENCY
from .circuit_breaker import db_circuit_breaker

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Metadata Service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware("http")
async def add_logging_and_metrics(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()

    TOTAL_REQUESTS.inc()
    try:
        response = await call_next(request)
        SUCCESS_COUNT.inc()
        return response
    except Exception as e:
        FAILURE_COUNT.inc()
        raise e
    finally:
        latency = (time.time() - start) * 1000
        REQUEST_LATENCY.observe(latency)
        print(f"request_id={request_id} path={request.url.path} latency_ms={latency:.2f}")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5) + wait_random(0, 1)
)
@db_circuit_breaker
def save_user(db: Session, user: User):
    db.add(user)
    db.commit()

@app.post("/user")
def create_user(payload: dict, db: Session = Depends(get_db)):
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    # Idempotency: if user exists, return it (do not create duplicate)
    existing = db.query(User).filter(User.user_id == user_id).first()
    if existing:
        return existing

    user = User(
        user_id=user_id,
        name=payload.get("name"),
        email=payload.get("email"),
        phone=payload.get("phone"),
        created_at=datetime.utcnow()
    )

    try:
        save_user(db, user)
    except Exception as e:
        FAILURE_COUNT.inc()
        raise HTTPException(status_code=500, detail="Database write failed")


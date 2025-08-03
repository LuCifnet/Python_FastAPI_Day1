from fastapi import FastAPI
from app.database import Base, engine
from app.routers import users
from app.middlewares import log_requests, error_handler

Base.metadata.create_all(bind=engine)

app = FastAPI()

#middleware
app.middleware("http")(log_requests)
app.middleware("http")(error_handler)

app.include_router(users.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello!. Go to /docs"}

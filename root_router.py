from fastapi import APIRouter

root_router = APIRouter()


@root_router.get("/")
def read_root():
    return {"message": "Hello World"}

from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()

@router.get("/{name}")
def get_topic(name: str):
    return {"name": name}
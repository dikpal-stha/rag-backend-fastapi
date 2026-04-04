from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def test_chat():
    return {"message": "This route works perfectly!"}

    
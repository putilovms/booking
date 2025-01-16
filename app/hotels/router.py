from fastapi import APIRouter


router = APIRouter(
    prefix="/hotels",
    tags=['Hotels and Rooms']
)


@router.get("")
def get_hotels():
    pass

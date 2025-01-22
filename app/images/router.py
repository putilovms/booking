import shutil

from fastapi import APIRouter, UploadFile

from app.tasks.tasks import process_pic

router = APIRouter(
    prefix="/images",
    tags=["Загрузка изображений"]
)


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    im_path = f"app/static/images/{name}.webp"
    with open(im_path, "wb+") as f:
        shutil.copyfileobj(file.file, f)
    process_pic.delay(im_path)
